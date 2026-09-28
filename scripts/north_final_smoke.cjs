// Desktop-only presentation regression against the existing local API.
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const fs=require('node:fs'),path=require('node:path');
const out=path.resolve(__dirname,'../docs/verification/north-final-030');
fs.mkdirSync(out,{recursive:true});
const check=(condition,message)=>{if(!condition)throw Error(message)};
const close=(a,b)=>Math.abs(a-b)<=Math.max(1e-5,Math.abs(b)*1e-6);
(async()=>{
  const browser=await chromium.launch({headless:true,channel:'chrome',args:['--enable-unsafe-swiftshader']});
  const checks=[],errors=[];
  for(const [width,height] of [[1280,720],[1440,900]]){
    const context=await browser.newContext({viewport:{width,height}});
    const page=await context.newPage();
    page.on('pageerror',e=>errors.push(e.message));
    const response=page.waitForResponse(r=>r.url().endsWith('/api/north/plan')&&r.ok());
    await page.goto('http://127.0.0.1:8011/#north',{waitUntil:'domcontentloaded'});
    const plan=await (await response).json();
    await page.locator('.ns-decision-grid').waitFor({timeout:60000});
    const water=plan.decision_story.water_security,totals=plan.plan.totals,allocations=plan.plan.allocations;
    check(close(water.annual_demand_m3,totals.water_m3),'Displayed demand basis differs from model total');
    check(water.source_balance_status==='CLOSED','Source allocation does not close');
    check(close(water.sources.reduce((s,r)=>s+r.m3,0),totals.water_m3),'Sources do not sum to new water');
    check(close(allocations.reduce((s,r)=>s+r.water_m3,0),totals.water_m3),'Crop-level water does not sum to new water');
    check(plan.plan.monthly.every(r=>close(r.stored_water_used_m3+r.freshwater_m3+r.desalinated_m3,r.demand_m3)),'Monthly source use does not close');
    check(await page.locator('.ns-crop-list').getByText('m³/yıl yeni su',{exact:false}).count()>0,'Crop-water link missing');
    check(await page.locator('.nw-critical-definition').innerText().then(t=>t.includes('yedek su gereği')),'Critical-period definition missing');
    check(await page.locator('.ns-decision-grid').isVisible(),'Water and production are not together');
    check(!(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth)),'Horizontal viewport overflow');
    await page.screenshot({path:path.join(out,`north-main-${width}x${height}.png`)});
    if(width===1440){
      await page.getByRole('button',{name:/Su ayrıntısı/}).click();
      await page.locator('.north-detail-content').waitFor();
      await page.locator('.north-detail-content').screenshot({path:path.join(out,'north-water-detail-1440x900.png')});
      await page.locator('.north-detail-content').evaluate(element=>{element.scrollTop=element.scrollHeight});
      await page.locator('.north-detail-content').screenshot({path:path.join(out,'north-water-monthly-1440x900.png')});
      await page.getByRole('button',{name:'SAHA GÜNCELLEMESİ'}).click();
      await page.getByRole('dialog',{name:'Kuzey saha doğrulaması'}).waitFor();
      const dialog=page.getByRole('dialog',{name:'Kuzey saha doğrulaması'});
      await dialog.getByText('MEVCUT PROTOTİP · v0.1').waitFor();
      check((await dialog.innerText()).includes('fiziksel cihazın ve kontrollü su deneyi sonucunun doğrulandığına dair kayıt yok'),'Prototype status overstated');
      await page.screenshot({path:path.join(out,'north-field-1440x900.png')});
      await dialog.getByRole('button',{name:'Üretim pilotu'}).click();
      await dialog.getByText('Kontrollü üretim deneyi').waitFor();
      check(await dialog.getByText('Henüz ölçülmedi').count()===4,'Missing pilot measurements became zero or invented');
      await page.screenshot({path:path.join(out,'north-pilot-1440x900.png')});
      const pdf=await page.request.post('http://127.0.0.1:8011/api/north/report',{data:plan.request});
      check(pdf.ok(),'North PDF request failed');
      fs.writeFileSync(path.join(out,'north-decision.pdf'),await pdf.body());
      await dialog.getByRole('button',{name:'Kuzey saha panelini kapat'}).click();
      check(await page.locator('.ns-decision-grid').isVisible(),'Closing field dialog lost the result');
      await page.getByRole('spinbutton',{name:'Simülasyon yılı'}).fill('2051');
      const futureResponse=page.waitForResponse(r=>r.url().endsWith('/api/north/plan')&&r.ok()&&r.request().postData()?.includes('"target_year":2051'));
      await page.getByRole('button',{name:'Simülasyonu çalıştır'}).click();
      const future=await (await futureResponse).json();
      check(future.plan.totals.desalinated_m3===0,'Expected no-desalination comparison scenario changed');
      await page.locator('.nw-advice').getByText('Bu planda deniz suyundan arıtılmış su tahsis edilmiyor.').waitFor();
      check(!(await page.locator('.nw-source-summary').innerText()).includes('Arıtılmış deniz'),'Unused source shown as allocated');
      await page.locator('.north-canvas').evaluate(element=>{element.scrollTop=0});
      await page.screenshot({path:path.join(out,'north-no-desal-2051.png')});
    }
    checks.push({viewport:`${width}x${height}`,new_water_m3:totals.water_m3,source_sum_m3:water.sources.reduce((s,r)=>s+r.m3,0),crop_water_sum_m3:allocations.reduce((s,r)=>s+r.water_m3,0),critical_month:water.critical_month?.label||null,critical_basis:water.critical_month?.basis||null,desalination_m3:totals.desalinated_m3,overflow:false});
    await context.close();
  }
  check(errors.length===0,'Browser errors: '+errors.join('; '));
  fs.writeFileSync(path.join(out,'browser-qa.json'),JSON.stringify({checks,errors},null,2));
  await browser.close();
  console.log('NORTH FINAL OK',checks.map(c=>c.viewport).join(', '));
})().catch(error=>{console.error(error);process.exit(1)});

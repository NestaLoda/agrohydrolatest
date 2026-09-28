// Optional browser verification: npm install --no-save playwright in a separate test environment.
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const fs = require('node:fs');
const path = require('node:path');
(async () => {
  const browser = await chromium.launch({headless:true, channel:'chrome', args:['--enable-unsafe-swiftshader']});
  const context = await browser.newContext({viewport:{width:1440,height:1000}});
  const external=[]; const errors=[]; const failed=[];
  await context.route('**/*', route => {
    const u = new URL(route.request().url());
    if (!['127.0.0.1','localhost'].includes(u.hostname) && ['http:','https:'].includes(u.protocol)) {external.push(u.href);return route.abort();}
    return route.continue();
  });
  const page=await context.newPage();
  page.on('pageerror',e=>errors.push(e.message));
  page.on('response',r=>{if(r.status()>=400)failed.push({url:r.url(),status:r.status()});});
  const out=path.resolve('docs/verification');fs.mkdirSync(out,{recursive:true});
  await page.goto('http://127.0.0.1:8000/',{waitUntil:'networkidle'});
  await page.getByRole('heading',{level:1}).waitFor();
  const screens=[];
  for(let i=1;i<=8;i++) {
    await page.evaluate(i=>{location.hash=`adim-${i}`;},i);
    await page.waitForTimeout(250);
    screens.push({step:i,title:await page.getByRole('heading',{level:1}).innerText(),overflow:await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth)});
    if(i===1 || i===3)await page.screenshot({path:path.join(out,`screen-${i}.png`),fullPage:true});
  }
  await page.evaluate(()=>location.hash='adim-5');
  const interactions=[];
  let responsePromise=page.waitForResponse(r=>r.url().endsWith('/api/decision') && r.request().method()==='POST');
  await page.getByRole('button',{name:'Üretim desenini hesapla',exact:true}).click();
  let decision=await (await responsePromise).json();
  if(decision.status!=='conditional' || Math.abs(decision.totals.production_kg-1000)>1e-6)throw Error('Default decision failed');
  interactions.push({test:'production decision',status:decision.status,run_id:decision.run_id});
  await page.screenshot({path:path.join(out,'screen-5.png'),fullPage:true});
  await page.evaluate(()=>location.hash='adim-6');
  responsePromise=page.waitForResponse(r=>r.url().endsWith('/api/pwn/example'));
  await page.getByRole('button',{name:/Açıklayıcı simülasyonu aç/}).click();
  const profile=await (await responsePromise).json();
  if(profile.source_kind!=='SIMULATION_EXPLANATORY' || profile.sample_count!==61)throw Error('PWN fixture failed');
  await page.getByRole('img',{name:/Simülasyon: ham/}).waitFor();
  interactions.push({test:'PWN example',source:profile.source_kind,samples:profile.sample_count});
  const fixture=await (await context.request.get('http://127.0.0.1:8000/api/pwn/example.csv')).body();
  await page.getByLabel('PWN CSV dosyası').setInputFiles({name:'simulation.csv',mimeType:'text/csv',buffer:fixture});
  await page.getByLabel('Bu veri nereden geliyor?').selectOption('SIMULATION_EXPLANATORY');
  await page.getByLabel('Derinlik nasıl belirlendi?').selectOption('encoder_vertical_tank');
  responsePromise=page.waitForResponse(r=>r.url().endsWith('/api/pwn/analyze'));
  await page.getByRole('button',{name:/Dosyayı analiz et/}).click();
  const imported=await (await responsePromise).json();
  if(!imported.raw_saved || imported.source_kind!=='SIMULATION_EXPLANATORY')throw Error('CSV import failed');
  interactions.push({test:'CSV import with provenance',sha256:imported.sha256});
  await page.screenshot({path:path.join(out,'screen-6.png'),fullPage:true});
  await page.evaluate(()=>location.hash='adim-7');
  await page.getByLabel('Kaynak suyu sıcaklığı').fill('18');
  responsePromise=page.waitForResponse(r=>r.url().endsWith('/api/sensitivity'));
  await page.getByRole('button',{name:/Kaynak suyu etkisini hesapla/}).click();
  const sensitivity=await (await responsePromise).json();
  if(Math.abs(sensitivity.after.specific_energy_kwh_m3-6.7)>1e-6)throw Error('Sensitivity failed');
  interactions.push({test:'source water sensitivity',specific_energy_kwh_m3:sensitivity.after.specific_energy_kwh_m3});
  await page.evaluate(()=>location.hash='adim-5');
  responsePromise=page.waitForResponse(r=>r.url().endsWith('/api/decision'));
  await page.getByRole('button',{name:'Üretim desenini hesapla',exact:true}).click();
  const after=await (await responsePromise).json();
  if(after.totals.energy_kwh>=decision.totals.energy_kwh)throw Error('Changed source input did not reach decision');
  interactions.push({test:'source condition reaches optimizer',before_kwh:decision.totals.energy_kwh,after_kwh:after.totals.energy_kwh});
  await page.getByLabel('Enerji bütçesi').fill('0');
  responsePromise=page.waitForResponse(r=>r.url().endsWith('/api/decision'));
  await page.getByRole('button',{name:'Üretim desenini hesapla',exact:true}).click();
  const infeasible=await (await responsePromise).json();
  if(infeasible.totals!==null || infeasible.allocations.length)throw Error('Impossible resource budget generated a plan');
  interactions.push({test:'impossible resources',status:infeasible.status});
  await page.getByRole('button',{name:'Kanıt kaydı'}).click();
  await page.getByRole('dialog').waitFor();
  await page.keyboard.press('Escape');
  await page.getByRole('dialog').waitFor({state:'hidden'});
  interactions.push({test:'source dialog keyboard close',status:'passed'});
  await page.setViewportSize({width:390,height:844});
  const mobile=[];
  for(let i=1;i<=8;i++){
    await page.evaluate(i=>location.hash=`adim-${i}`,i);await page.waitForTimeout(150);
    mobile.push({step:i,overflow:await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth)});
  }
  await page.screenshot({path:path.join(out,'mobile.png'),fullPage:true});
  console.log('SCREENS',JSON.stringify(screens));
  console.log('ERRORS',JSON.stringify({errors,failed,external}));
  fs.writeFileSync(path.join(out,'browser-smoke.json'),JSON.stringify({screens,mobile,interactions,errors,failed,blocked_external_requests:external},null,2));
  await browser.close();
  if(errors.length || failed.length || external.length || [...screens,...mobile].some(s=>s.overflow))throw Error('Browser verification contains failures');
})().catch(e=>{console.error(e);process.exit(1)});

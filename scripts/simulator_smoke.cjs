const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
(async()=>{
 const browser=await chromium.launch({channel:'chrome',headless:true,args:['--enable-unsafe-swiftshader']});
 const report={verified_at:new Date().toISOString(),version:'0.3.0',checks:[],screens:[],errors:[],failed:[],blocked_external_requests:[]};
 const out=path.resolve('docs/verification');
 try {
 const context=await browser.newContext({viewport:{width:1440,height:1000}});
 await context.route('**/*',r=>{const u=new URL(r.request().url());if(['http:','https:'].includes(u.protocol)&&!['127.0.0.1','localhost'].includes(u.hostname)){report.blocked_external_requests.push(u.href);return r.abort()}return r.continue()});
 const page=await context.newPage();page.setDefaultTimeout(12000);
 page.on('pageerror',e=>report.errors.push(e.message));page.on('response',r=>{if(r.status()>=400)report.failed.push({url:r.url(),status:r.status()})});
 const record=(test,data={})=>report.checks.push({test,passed:true,...data});
 const call=async(endpoint,button)=>{const waiting=page.waitForResponse(r=>r.url().endsWith(endpoint)&&r.request().method()==='POST');await button.click();const r=await waiting;assert.equal(r.status(),200);return r.json()};
 const run=()=>call('/api/simulate',page.getByRole('button',{name:'Hesapla / simüle et',exact:true}));
 const go=async hash=>{await page.evaluate(h=>location.hash=h,hash);await page.waitForTimeout(150)};
 await page.goto('http://127.0.0.1:8000/#simulation',{waitUntil:'networkidle'});
 await page.getByRole('button',{name:'Hesapla / simüle et',exact:true}).waitFor();
 const first=await run();assert.equal(first.status,'conditional');assert.equal(first.optimized.crops.length,5);
 record('Official Konya baseline loads and fractional default budget submits',{run_id:first.run_id});
 await page.getByRole('button',{name:'Suyu %20 azalt',exact:true}).click();await page.getByText(/Görünen sonuç önceki çalıştırmaya ait/).waitFor();
 const cut=await run();assert.equal(cut.status,'conditional');assert.ok(cut.optimized.totals.water_m3<first.optimized.totals.water_m3*.801);assert.ok(cut.optimized.crops.some(c=>Math.abs(c.delta_area_ha)>1));
 record('Twenty-percent water scenario changes crop hectares and preserves minimum production',{water_m3:cut.optimized.totals.water_m3,crops:cut.optimized.crops.map(c=>({id:c.crop_id,ha:c.area_ha}))});
 await page.evaluate(()=>scrollTo(0,0));await page.waitForTimeout(120);await page.screenshot({path:path.join(out,'simulator-turkiye.png'),fullPage:true});
 await page.getByRole('button',{name:'Yüklü başlangıca dön',exact:true}).click();await page.getByLabel('ET₀ çarpanı',{exact:true}).fill('1.2');const dry=await run();assert.ok(dry.current.totals.water_m3>first.current.totals.water_m3);record('ET0 changes water demand through the shared crop-water calculation');
 await page.getByRole('button',{name:'Yüklü başlangıca dön',exact:true}).click();await page.getByLabel('Yeni aday ürün',{exact:true}).selectOption('sunflower');await page.getByRole('button',{name:'Ürün ekle',exact:true}).click();
 await page.locator('.crop-editor-details > summary').click();await page.getByLabel('Ayçiçeği mevcut alan',{exact:true}).fill('0');await page.getByLabel('Ayçiçeği tarla verimi',{exact:true}).fill('2000');
 const added=await run();assert.equal(added.request.crops.length,6);assert.ok(added.excluded_options.some(o=>o.crop_id==='sunflower'));assert.equal(added.baseline.crops.find(c=>c.crop_id==='sunflower').area_ha,0);
 record('User can add a crop and edit yield; unknown suitability stays excluded and official baseline stays unchanged');
 await page.getByText('Ürünlerin ayrıntılı parametreleri',{exact:true}).click();await page.locator('.scenario-editor summary').filter({hasText:/^Ayçiçeği$/}).click();await page.getByLabel('Ayçiçeği iklim uygunluğu',{exact:true}).selectOption('true');await page.getByLabel('Ayçiçeği zemin uygunluğu',{exact:true}).selectOption('true');const manual=await run();assert.equal(manual.status,'conditional');assert.ok(manual.optimized.crops.find(c=>c.crop_id==='sunflower').production_kg>0);record('Explicit user suitability and yield activate added crop in optimized pattern');
 await page.getByRole('button',{name:'Yüklü başlangıca dön',exact:true}).click();
 await page.getByLabel('Çalışma bölgesi',{exact:true}).selectOption('gap_sanliurfa');await page.waitForFunction(()=>document.querySelector('.workspace-heading p')?.textContent.includes('Şanlıurfa'));await run();await page.getByRole('button',{name:'Suyu %20 azalt',exact:true}).click();const urfa=await run();assert.equal(urfa.status,'conditional');assert.equal(urfa.optimized.crops.length,4);assert.ok(urfa.optimized.crops.some(c=>Math.abs(c.delta_area_ha)>1));record('Second official region produces a different constrained crop pattern');
 await page.getByLabel('Planlama modu',{exact:true}).selectOption('north');await page.getByRole('button',{name:'Uygun saha varsayımıyla portföy dene',exact:true}).waitFor();const unknown=await run();assert.equal(unknown.optimized,null);record('Unknown northern climate and soil do not become a feasible field plan');
 await page.getByRole('button',{name:'Uygun saha varsayımıyla portföy dene',exact:true}).click();const north=await run();assert.equal(north.status,'conditional');assert.equal(north.optimized.crops.length,3);assert.ok(north.optimized.allocations.some(a=>a.capacity_unit==='m2'));assert.ok(north.optimized.allocations.some(a=>a.capacity_unit==='ha'));
 record('Explicit northern scenario solves barley, potato and hydroponic lettuce in native ha and m2 units',{water_m3:north.optimized.totals.water_m3,energy_kwh:north.optimized.totals.energy_kwh});
 await page.evaluate(()=>scrollTo(0,0));await page.waitForTimeout(120);await page.screenshot({path:path.join(out,'simulator-north.png'),fullPage:true});
 await go('pattern');await page.getByRole('heading',{name:'Ürün deseni / karar',exact:true}).waitFor();assert.equal(await page.getByLabel('Planlama modu').inputValue(),'north');record('Shared scenario and result persist in decision workspace');
 await go('pwn');await page.getByRole('button',{name:'Saha öncesi / sonrası desen',exact:true}).click();const field=await call('/api/pattern-field-update',page.getByRole('button',{name:'Eşleştir ve deseni yeniden hesapla',exact:true}));assert.equal(field.before.status,'conditional');assert.equal(field.after.status,'infeasible');assert.equal(field.comparison.calibration_applied,false);
 record('Matched simulated water observation reruns the same portfolio engine; 10 to 5 C crosses fixed energy constraint',{before:field.before.status,after:field.after.status});await page.evaluate(()=>scrollTo(0,0));await page.waitForTimeout(120);await page.screenshot({path:path.join(out,'simulator-field.png'),fullPage:true});
 await page.getByLabel(/Zamanı 24 saat kaydır/).check();const bad=await call('/api/pattern-field-update',page.getByRole('button',{name:'Eşleştir ve deseni yeniden hesapla',exact:true}));assert.equal(bad.after,null);record('Time mismatch prevents field-derived pattern update');
 await page.getByRole('button',{name:'Profil / CSV kaydı',exact:true}).click();const waiting=page.waitForResponse(r=>r.url().endsWith('/api/pwn/example'));await page.getByRole('button',{name:'Açıklayıcı simülasyonu yükle',exact:true}).click();assert.equal((await(await waiting).json()).sample_count,61);
 const csv=await(await context.request.get('http://127.0.0.1:8000/api/pwn/example.csv')).body();await page.getByLabel('PWN CSV dosyası',{exact:true}).setInputFiles({name:'simulator-smoke.csv',mimeType:'text/csv',buffer:csv});await page.getByLabel(/^Verinin kaynağı/).selectOption('SIMULATION_EXPLANATORY');await page.getByLabel(/^Derinlik yöntemi/).selectOption('encoder_vertical_tank');const imported=await call('/api/pwn/analyze',page.getByRole('button',{name:'Dosyayı analiz et',exact:true}));assert.ok(imported.raw_saved);await go('evidence');await go('pwn');await page.getByRole('img',{name:'Ham sinyal derinlik profili'}).waitFor();record('Existing PWN example, import, raw preservation and navigation persistence work',{sha256:imported.sha256});
 await page.getByRole('button',{name:'Kanıt çekmecesi',exact:true}).click();await page.getByRole('dialog').waitFor();await page.keyboard.press('Escape');await page.getByRole('dialog').waitFor({state:'hidden'});record('Evidence drawer remains keyboard accessible');
 for(const width of [1440,390]){await page.setViewportSize({width,height:width===390?844:1000});for(const hash of ['simulation','pattern','pwn','evidence']){await go(hash);report.screens.push({workspace:hash,width,overflow:await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth)})}}
 await go('simulation');await page.evaluate(()=>scrollTo(0,0));await page.waitForTimeout(120);await page.screenshot({path:path.join(out,'simulator-mobile.png'),fullPage:true});
 assert.equal(report.errors.length,0);assert.equal(report.failed.length,0);assert.equal(report.blocked_external_requests.length,0);assert.ok(report.screens.every(s=>!s.overflow));
 report.passed=true;
 }catch(e){report.passed=false;report.failure=String(e);throw e}finally{fs.writeFileSync(path.join(out,'simulator-smoke.json'),JSON.stringify(report,null,2));await browser.close();console.log(JSON.stringify(report,null,2))}
})().catch(e=>{console.error(e);process.exit(1)});


const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1300,height:900}});
const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
await p.goto('file://'+process.argv[2]);await p.waitForTimeout(1500);
const ids=['measure','furniture','walls','ceiling','elevations','bath'];
for(const id of ids){const el=await p.$('#'+id);await el.screenshot({path:'s_'+id+'.png'});}
await p.click('#v-wood');await p.waitForTimeout(300);
for(const id of ['furniture','elevations']){const el=await p.$('#'+id);await el.screenshot({path:'w_'+id+'.png'});}
console.log('errors:',JSON.stringify(errs));await b.close();})();

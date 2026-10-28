const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();
for(const f of ['proekt-belyi-mramor.html','renders-belyi-mramor.html']){const p=await b.newPage({viewport:{width:1300,height:900}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.route('**/fonts.googleapis.com/**',r=>r.abort());
const s=require('fs').readFileSync(f,'utf8');await p.setContent('<!doctype html><html><head><meta charset="utf-8"></head><body>'+s+'</body></html>');await p.waitForTimeout(800);
console.log(f,JSON.stringify(errs),await p.evaluate(()=>document.querySelectorAll('figure').length+' fig, seg:'+document.querySelectorAll('.seg').length));}
await b.close();})();

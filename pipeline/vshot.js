const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});const p=await b.newPage({viewport:{width:1280,height:900}});
const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error'||m.type()==='warning')errs.push(m.text())});
await p.route('**/three.min.js',r=>r.fulfill({path:'npmthree/package/build/three.min.js',contentType:'application/javascript'}));
await p.route('**/OrbitControls.js',r=>r.fulfill({path:'npmthree/package/examples/js/controls/OrbitControls.js',contentType:'application/javascript'}));
await p.route('**/fonts.googleapis.com/**',r=>r.abort());
await p.goto('file://'+process.argv[2]);await p.waitForTimeout(4000);
const shots=process.argv.slice(3);
for(const s of shots){const [room,v,mode]=s.split(':');await p.evaluate(([r,v,m])=>{__bm.set('v',v);__bm.set('mode',m);__bm.setView(r);},[room,v,mode]);await p.waitForTimeout(1500);await (await p.$('#stage')).screenshot({path:'v_'+s.replace(/:/g,'_')+'.png'});}
console.log(JSON.stringify(errs.slice(0,8)));await b.close();})();

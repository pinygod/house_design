const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1300,height:900}});
const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.route('**/fonts.googleapis.com/**',r=>r.abort());
await p.goto('file://'+process.argv[2]);await p.addStyleTag({content:'.top{position:static!important}'});await p.waitForTimeout(1000);
await (await p.$('#bath')).screenshot({path:'z_bath.png'});
await (await p.$('#furniture .fig')).screenshot({path:'z_furn.png'});
console.log(JSON.stringify(errs));await b.close();})();

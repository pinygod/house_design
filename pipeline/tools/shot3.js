const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1300,height:900}});
const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+process.argv[2]);await p.addStyleTag({content:'.top{position:static!important}'});await p.waitForTimeout(1500);
for(const id of ['furniture','floors','ceiling']){await (await p.$('#'+id+' .fig')).screenshot({path:'y_'+id+'.png'});}
await (await p.$('#eKit')).screenshot({path:'y_kit.png'});
console.log(JSON.stringify(errs));await b.close();})();

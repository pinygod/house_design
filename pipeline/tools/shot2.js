const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1300,height:900}});
await p.goto('file://'+process.argv[2]);await p.addStyleTag({content:'.top{position:static!important}'});await p.waitForTimeout(1200);
await p.click('#v-wood');await p.waitForTimeout(300);
for(const id of ['walls','elevations']){await (await p.$('#'+id)).screenshot({path:'x_'+id+'.png'});}
await p.click('#v-green');await p.waitForTimeout(300);
await (await p.$('#bath')).screenshot({path:'x_bath.png'});
await b.close();})();

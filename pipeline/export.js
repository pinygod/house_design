const {chromium}=require('playwright'); const fs=require('fs');
(async()=>{const b=await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});const p=await b.newPage({viewport:{width:800,height:500}});
await p.route('**/three.min.js',r=>r.fulfill({path:'npmthree/package/build/three.min.js',contentType:'application/javascript'}));
await p.route('**/OrbitControls.js',r=>r.fulfill({path:'npmthree/package/examples/js/controls/OrbitControls.js',contentType:'application/javascript'}));
await p.route('**/fonts.googleapis.com/**',r=>r.abort());
p.on('pageerror',e=>console.log('ERR',e.message));
await p.goto('file://'+process.cwd()+'/vprev.html');await p.waitForTimeout(3000);
await p.addScriptTag({path:'npmthree/package/examples/js/exporters/GLTFExporter.js'});
for(const v of ['green','wood']){
  const b64=await p.evaluate(async(v)=>{__bm.set('v',v);__bm.setView('zal');
    const roots=[__bm.groups.stat,__bm.groups.ceil,__bm.groups.vari];
    const jobs=[];
    roots.forEach(r=>r.traverse(o=>{if(!o.isMesh)return; const mats=Array.isArray(o.material)?o.material:[o.material]; const m=mats.find(x=>x.map&&(x.map.repeat.x!==1||x.map.repeat.y!==1||x.map.offset.x||x.map.offset.y)); if(m) jobs.push([o,m.map.repeat.clone(),m.map.offset.clone()]);}));
    jobs.forEach(([o,rp,of])=>{o.geometry=o.geometry.clone(); const uv=o.geometry.attributes.uv; if(!uv)return; for(let i=0;i<uv.count;i++){uv.setXY(i,uv.getX(i)*rp.x+of.x,uv.getY(i)*rp.y+of.y);} uv.needsUpdate=true;});
    jobs.forEach(([o])=>{(Array.isArray(o.material)?o.material:[o.material]).forEach(m=>{if(m.map){m.map.repeat.set(1,1);m.map.offset.set(0,0);}});});
    const ex=new THREE.GLTFExporter();
    const buf=await new Promise(res=>ex.parse(roots,res,{binary:true,maxTextureSize:2048}));
    let s='';const u=new Uint8Array(buf);for(let i=0;i<u.length;i+=32768)s+=String.fromCharCode.apply(null,u.subarray(i,i+32768));return btoa(s);},v);
  fs.writeFileSync('scene_'+v+'.glb',Buffer.from(b64,'base64')); console.log(v,b64.length);
  await p.reload();await p.waitForTimeout(3000);await p.addScriptTag({path:'npmthree/package/examples/js/exporters/GLTFExporter.js'});
}
await b.close();})();

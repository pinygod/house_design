import base64, re
S = open('viz-src.html').read()
fails = []
S = S[:S.index('  /* radiator niches')] + S[S.index('  /* end radiator niches */\n')+len('  /* end radiator niches */\n'):]  # floor 3 has no radiator niches

def cut(start, end, new):
    global S
    i = S.find(start)
    j = S.find(end, i + 1)
    if i < 0 or j < 0:
        fails.append(('cut', start[:50]))
        return
    S = S[:i] + new + S[j:]

def rp(a, b, cnt=1):
    global S
    c = S.count(a)
    if c != cnt:
        fails.append((c, a[:70]))
        return
    S = S.replace(a, b)

# ---------- header ----------
rp('<title>Белый мрамор в 3D</title>', '<title>Третий этаж в 3D</title>')
rp('<div class="eyebrow">Проект «Белый мрамор» · 3D-визуализация</div><h1>Помещения в объёме</h1>',
   '<div class="eyebrow">Проект «Белый мрамор» · третий этаж · 3D-визуализация</div><h1>Третий этаж в объёме</h1>')

# ---------- constants ----------
cut("const MARBLE='__MARBLE__';", "let state=", r"""const MARBLE='__MARBLE__', RUT='__RUT__';
const FW=9490, FD=10800;
const ROOMS=[
  {id:'bed',n:'Спальня',x:4650,y:0,w:4840,h:4100},
  {id:'cab1',n:'Кабинет 1',x:0,y:0,w:4150,h:3700},
  {id:'cab2',n:'Кабинет 2',x:0,y:4030,w:4150,h:3820},
  {id:'cor',n:'Коридор',x:3130,y:8300,w:4250,h:2500,area:'≈21,0',meta:'≈21 м² · Г-образный, 4250 × 2500 + 2730 × 3800 мм'},
  {id:'cor2',n:'Коридор',x:4650,y:4500,w:2730,h:3800,sub:1},
  {id:'gard',n:'Гардероб',x:7540,y:4500,w:1950,h:6300},
  {id:'bath',n:'Ванная',x:0,y:8300,w:2750,h:2500}
];
const OPEN=[{x:4950,y:4100,w:800,h:400},{x:4150,y:2600,w:500,h:800},{x:4150,y:4650,w:500,h:800},{x:7380,y:5150,w:160,h:800},{x:2750,y:8500,w:380,h:700},{x:4650,y:8300,w:2730,h:0,v:1}];
const WIN=[['l',740,2040],['t',1880,3370],['l',5400,6800],['t',5435,7500,0],['r',1200,4000],['r',5150,7950],['b',1450,2750],['b',5720,7100]];
const SPOT=[[5200,700],[5200,1900],[5200,3200],[6500,900],[8700,900],[7600,1500],
  [1000,1000],[3100,1000],[1000,2700],[3100,2700],[1000,5000],[3100,5000],[1000,6900],[3100,6900],
  [8500,5200],[8500,6500],[8500,7400],[8500,9000],[8500,10100],[2000,8900],[500,9300],[1500,10400],[2400,10400]];
const LINES=[[[4650,5200],[7380,6900]],[[5600,4500],[6900,8300]],[[7380,5600],[4650,7900]],[[6200,4500],[7380,5300]],[[3130,8900],[7380,10100]],[[3800,10800],[5600,8300]],[[5200,10800],[7380,9000]]];
const STAIR={x:3200,y:9850,w:3220,h:950};
const WH=2750, CH=2550, M=v=>v/1000;

const VIEWS={
  bed:{pos:[5300,1500,450],look:[7600,900,3800]},
  cab1:{pos:[3500,1500,3300],look:[900,1000,1600]},
  cab2:{pos:[3600,1500,4400],look:[1200,950,7300]},
  cor:{pos:[6900,1600,4800],look:[4300,1100,10000]},
  gard:{pos:[8300,1500,4700],look:[8300,1000,9500]},
  bath:{pos:[2600,1500,9900],look:[600,1150,8500]},
  plan:{}
};
const INFO={
  bed:{green:['Стена за изголовьем мягкий синий вместе со скрытой дверью','Кровать 1800 с мягким изголовьем в букле, плед и подушки в синем бархате, шерстяной ковёр','ТВ справа от балконной двери на дубовой консоли','6 встраиваемых спотов в обход кровати, дверь в одной плоскости со стеной коридора']},
  cab1:{green:['Вход из спальни, окна в двух стенах','Стол из светлого дуба 1600, рабочее кресло, стеллаж','Молочные стены, 4 спота']},
  cab2:{green:['Стена за рабочим местом мягкий синий','Стол из светлого дуба 1600, стеллаж вдоль стены, растение','4 спота']},
  cor:{green:['Общая комната без мебели, пол Alpine Floor «Ратленд» 608 × 303','Хаотичные световые линии в потолке','Проём лестницы с чёрным ограждением и чёрной окантовкой торца перекрытия']},
  gard:{green:['Шкафы до потолка с молочными фасадами','Колонна у левой стены целиком облицована зеркалом','Шкаф у стены с окном укорочен: за колонной свободная зона 1350 мм','Банкетка под окном']},
  bath:{green:['Короб инсталляции до потолка и стена за ним в чёрном фактурном керамограните','Стена с тумбой до короба и стена с дверью в белом мраморе, стена с ванной в белом рельефном керамограните','Ванна под окном слева от входа, тумба из дуба, круглое зеркало с подсветкой','Вертикальная световая линия у унитаза, полотенцесушитель справа от унитаза, мрамор в дверном проёме']},
  plan:{green:['Весь этаж сверху, без потолков','Пол Alpine Floor «Ратленд» без порогов','Потяните для вращения, колесо приближает']}
};

""")
rp("[...ROOMS.map(r=>[r.id,r.n,(r.w*r.h/1e6).toFixed(1).replace('.',',')+' м²']),['plan','Весь этаж','3D-план']]",
   "[...ROOMS.filter(r=>!r.sub).map(r=>[r.id,r.n,(r.area||(r.w*r.h/1e6).toFixed(1).replace('.',','))+' м²']),['plan','Весь этаж','3D-план']]")
rp("let state={alt:false,room:'zal',v:'green',mode:'day'};", "let state={room:'bed',v:'green',mode:'day'};")
rp("const img=new Image(); img.onload=init; img.src=MARBLE;",
   "const img=new Image(), rimg=new Image(); let nl=0; const done=()=>{if(++nl===2)init();}; img.onload=done; rimg.onload=done; img.src=MARBLE; rimg.src=RUT;")
rp("  const marbleT=prep(new THREE.Texture(img));", "  const marbleT=prep(new THREE.Texture(img)); const rutT=prep(new THREE.Texture(rimg));")
rp("rugShag:std('#D8D0C2',1),", "rugShag:std('#D8D0C2',1), blue:std('#7389A0',.92), blueVel:std('#7D90A6',.85),")

# ---------- floor ----------
cut("  /* floor */", "  /* walls by grid */", r"""  /* floor: Alpine Floor Rutland 608x303, half-offset; texture sheet = 1212 x 1216 mm */
  const flMat=tex(rutT,1,1,{roughness:.5},'rutland');
  function floorRect(x0,z0,x1,z1){const P=[[x0,z0],[x1,z0],[x1,z1],[x0,z1]].map(([x,z])=>[M(x),M(z)]); const g=new THREE.BufferGeometry();
    g.setAttribute('position',new THREE.Float32BufferAttribute(P.flatMap(([x,z])=>[x,0,z]),3)); g.setAttribute('uv',new THREE.Float32BufferAttribute(P.flatMap(([x,z])=>[x/1.212,-z/1.216]),2));
    g.setIndex([0,3,2,0,2,1]); g.computeVertexNormals(); const m=new THREE.Mesh(g,flMat); m.receiveShadow=true; G.add(m);}
  floorRect(0,0,FW,STAIR.y); floorRect(0,STAIR.y,STAIR.x,FD); floorRect(STAIR.x+STAIR.w,STAIR.y,FW,FD);
  const ground=new THREE.Mesh(new THREE.PlaneGeometry(90,90),std('#9AA39A',1)); ground.rotation.x=-Math.PI/2; ground.position.set(4.75,-6.1,5.4); ground.receiveShadow=true; G.add(ground);

""")

# ---------- walls grid generalisation ----------
rp("const wr=WIN.map(([s,a,b,sill,nr])=>({s,sill:sill||850,nr,...(s==='t'?{x:a,y:-500,w:b-a,h:500}:s==='b'?{x:a,y:11327,w:b-a,h:500}:s==='l'?{x:-500,y:a,w:500,h:b-a}:{x:8712,y:a,w:500,h:b-a})}));",
   "const wr=WIN.map(([s,a,b,sill])=>({s,sill:sill===0?0:(sill||850),...(s==='t'?{x:a,y:-500,w:b-a,h:500}:s==='b'?{x:a,y:FD,w:b-a,h:500}:s==='l'?{x:-500,y:a,w:500,h:b-a}:{x:FW,y:a,w:500,h:b-a})}));")
rp("const xs=uniq([-500,9212,", "const xs=uniq([-500,FW+500,")
rp("const zs=uniq([-500,11827,", "const zs=uniq([-500,FD+500,")
rp("    B(r.x,r.y,r.w,r.h,0,r.sill,MAT.wall); B(r.x,r.y,r.w,r.h,2350,WH,MAT.wall);",
   "    if(r.sill>0) B(r.x,r.y,r.w,r.h,0,r.sill,MAT.wall); B(r.x,r.y,r.w,r.h,2350,WH,MAT.wall);")
rp("const z=r.s==='t'?-270:11577;", "const z=r.s==='t'?-270:FD+250;")
rp("const x=r.s==='l'?-270:8942;", "const x=r.s==='l'?-270:FW+230;")
rp("  OPEN.forEach(o=>B(o.x,o.y,o.w,o.h,o.ext?2050:2000,WH,MAT.wall));",
   "  OPEN.filter(o=>!o.v).forEach(o=>B(o.x,o.y,o.w,o.h,2000,WH,MAT.wall));\n  B(7540,7890,1190,400,0,WH,MAT.wall); // partition inside the walk-in wardrobe")

# ---------- stairs (void with the flight from floor 2) ----------
cut("  /* stairs */", "  /* shadow skirting", r"""  /* stair void: flight from the floor below, black slab edge, black railing */
  { const bm=blackM(.3,1), BK=MAT.black, DW=STAIR.w/14, X0=STAIR.x, X1=STAIR.x+STAIR.w, Y0=STAIR.y;
    for(let k=0;k<14;k++){const x=X1-(k+1)*DW, top=-(k+1)*218; B(x,Y0,DW,STAIR.h,top-380,top,[bm,MAT.wall,bm,MAT.wall,MAT.wall,MAT.wall]); B(x+DW,Y0+12,8,STAIR.h-24,top+192,top+206,MAT.emis,false);}
    B(X0,Y0-20,STAIR.w,20,-300,0,BK); B(X0-20,Y0-20,20,STAIR.h+20,-300,0,BK); B(X1,Y0-20,20,STAIR.h+20,-300,0,BK);
    B(X0,Y0-20,STAIR.w,20,-3100,-300,MAT.wall); B(X0-20,Y0,20,STAIR.h,-3100,-300,MAT.wall); B(X0,FD,STAIR.w,20,-3100,0,MAT.wall);
    B(X0-500,Y0,STAIR.w+1000,STAIR.h,-3120,-3100,std('#CFCBC4',.8));
    const RY=Y0-60; B(X0,RY,STAIR.w,40,960,1000,BK);
    for(let x=X0+30;x<=X1-30;x+=120) B(x-6,RY+14,12,12,0,960,BK); }
""")

# ---------- shadow skirting: virtual openings cut the ceiling line too ----------
rp("""      const cuts=OPEN.map(o=>{
        if(sd==='t'&&Math.abs(o.y+o.h-r.y)<2) return [o.x,o.x+o.w];
        if(sd==='b'&&Math.abs(o.y-(r.y+r.h))<2) return [o.x,o.x+o.w];
        if(sd==='l'&&Math.abs(o.x+o.w-r.x)<2) return [o.y,o.y+o.h];
        if(sd==='r'&&Math.abs(o.x-(r.x+r.w))<2) return [o.y,o.y+o.h];
        return null;}).filter(Boolean);
      if(r.id==='cor'&&sd==='b') cuts.push([STAIR.x,STAIR.x+STAIR.w]);
      const segs=[]; let s0=a; cuts.sort((p,q)=>p[0]-q[0]).forEach(([c0,c1])=>{if(c1<=a||c0>=b)return; if(c0>s0)segs.push([s0,c0]); s0=Math.max(s0,c1);}); if(s0<b)segs.push([s0,b]);""",
   """      const hit=o=>{
        if(sd==='t'&&Math.abs(o.y+o.h-r.y)<2) return [o.x,o.x+o.w];
        if(sd==='b'&&Math.abs(o.y-(r.y+r.h))<2) return [o.x,o.x+o.w];
        if(sd==='l'&&Math.abs(o.x+o.w-r.x)<2) return [o.y,o.y+o.h];
        if(sd==='r'&&Math.abs(o.x-(r.x+r.w))<2) return [o.y,o.y+o.h];
        return null;};
      const cuts=OPEN.map(hit).filter(Boolean), vcuts=OPEN.filter(o=>o.v).map(hit).filter(Boolean);
      if(r.id==='cor'&&sd==='b') cuts.push([STAIR.x,STAIR.x+STAIR.w]);
      const split=cs=>{const out=[]; let s0=a; cs.slice().sort((p,q)=>p[0]-q[0]).forEach(([c0,c1])=>{if(c1<=a||c0>=b)return; if(c0>s0)out.push([s0,c0]); s0=Math.max(s0,c1);}); if(s0<b)out.push([s0,b]); return out;};
      const segs=split(cuts), csegs=split(vcuts);""")
rp("      ((r.id==='cor'&&sd==='b')?segs:[[a,b]]).forEach(([p0,p1])=>put(p0,p1,2688,2700));",
   "      csegs.forEach(([p0,p1])=>put(p0,p1,CH-12,CH));")

# ---------- ceilings ----------
cut("  /* ceilings + spots + lines */", "  /* variant-dependent */", r"""  /* ceilings + spots + lines */
  G=groups.ceil;
  ROOMS.forEach(r=>B(r.x,r.y,r.w,r.h,CH,WH,MAT.ceil));
  SPOT.forEach(([x,z])=>{Cy(x,z,50,CH-8,CH,MAT.black); Cy(x,z,32,CH-12,CH-6,MAT.emis).castShadow=false;});
  LINES.forEach(([[x1,z1],[x2,z2]])=>{const L=Math.hypot(x2-x1,z2-z1); const m=new THREE.Mesh(new THREE.BoxGeometry(M(L),.012,.035),MAT.emis); m.position.set(M((x1+x2)/2),M(CH)-.005,M((z1+z2)/2)); m.rotation.y=-Math.atan2(z2-z1,x2-x1); G.add(m);});

""")

# ---------- furniture & finishes ----------
cut("  function buildVariant(v){", "  function pendant(", r"""  function buildVariant(v){
    groups.vari.traverse(o=>{if(o.geometry)o.geometry.dispose();}); groups.vari.clear(); G=groups.vari;
    const T=3, BL=MAT.blue, BV=MAT.blueVel, hm=MAT.metalB;
    const plant=(px,pz,s=1)=>{Cy(px,pz,170*s,0,380*s,MAT.graph); Cy(px,pz,10,380*s,1250*s,MAT.leather);
      for(let i=0;i<12;i++){const a=i*2.4, y=(780+(i%5)*150)*s, m=new THREE.Mesh(new THREE.SphereGeometry(1,20,10),MAT.leaf); m.scale.set(.11*s,.012,.29*s); m.rotation.order='YXZ'; m.rotation.y=a; m.rotation.x=-.55-(i%3)*.15; m.position.set(M(px)+Math.sin(a)*.18*s,M(y),M(pz)+Math.cos(a)*.18*s); m.castShadow=true; G.add(m);}};
    const chair=(cx,cz,back)=>{Cy(cx,cz,300,0,30,hm); Cy(cx,cz,25,30,430,hm); Cy(cx,cz,250,430,500,MAT.graph); if(back<0) B(cx-200,cz-290,400,60,500,950,MAT.graph); else B(cx-200,cz+230,400,60,500,950,MAT.graph);};
    /* accent walls and bath finishes */
    B(4650,4100-T,300,T,0,CH,BL); B(5750,4100-T,3740,T,0,CH,BL); B(4950,4100-T,800,T,2000,CH,BL);
    B(0,7850-T,4150,T,0,CH,BL);
    B(1000,8300,1750,T,0,CH,marble(1.75,2.55)); B(0,8300,1000,200,0,CH,porcB(1,2.55)); B(0,8500,T,2300,0,CH,porcB(2.3,2.55));
    B(0,FD-T,1450,T,0,CH,porcW(1.45,2.55)); B(1450,FD-T,1300,T,0,850,porcW(1.3,.85)); B(1450,FD-T,1300,T,2350,CH,porcW(1.3,.2)); B(2750-T,8300,T,200,0,CH,marble(.2,2.55)); B(2750-T,9200,T,1600,0,CH,marble(1.6,2.55)); B(2750-T,8500,T,700,2000,CH,marble(.7,.55));
    B(2750,8500,340,T,0,2000,marble(.34,2)); B(2750,9200-T,340,T,0,2000,marble(.34,2)); B(2750,8500,340,700,2000-T,2000,marble(.34,.7)); // marble wraps the door reveal up to the leaf
    B(4950,4100,T,360,0,2000,BL); B(5750-T,4100,T,360,0,2000,BL); B(4950,4100,800,360,2000-T,2000,BL); // blue reveal: bedroom door sits flush with the corridor
    /* hidden doors */
    B(4950,4460,800,40,0,2000,[MAT.wall,MAT.wall,MAT.wall,MAT.wall,MAT.wall,BL]); loop([[4.95,0.002,4.503],[5.75,0.002,4.503],[5.75,2,4.503],[4.95,2,4.503]],seamMat);
    B(4610,2600,40,800,0,2000,MAT.wall); loop([[4.653,0.002,2.6],[4.653,0.002,3.4],[4.653,2,3.4],[4.653,2,2.6]],seamMat);
    B(4610,4650,40,800,0,2000,MAT.wall); loop([[4.653,0.002,4.65],[4.653,0.002,5.45],[4.653,2,5.45],[4.653,2,4.65]],seamMat);
    B(7380,5150,40,800,0,2000,MAT.wall); loop([[7.377,0.002,5.15],[7.377,0.002,5.95],[7.377,2,5.95],[7.377,2,5.15]],seamMat);
    B(3090,8500,40,700,0,2000,MAT.wall); loop([[3.133,0.002,8.5],[3.133,0.002,9.2],[3.133,2,9.2],[3.133,2,8.5]],seamMat);
    /* handles */
    const hz=(xc,zf,n,hd)=>{const z0=n>0?zf:zf-8; B(xc-25,z0,50,8,975,1025,hm); B(xc-7,n>0?zf:zf-45,14,45,993,1007,hm); const zl=n>0?zf+30:zf-48; B(hd<0?xc-130:xc,zl,130,18,991,1009,hm);};
    const hx=(xf,zc,n,hd)=>{const x0=n>0?xf:xf-8; B(x0,zc-25,8,50,975,1025,hm); B(n>0?xf:xf-45,zc-7,45,14,993,1007,hm); const xl=n>0?xf+30:xf-48; B(xl,hd<0?zc-130:zc,18,130,991,1009,hm);};
    hz(5680,4500,1,-1); hz(5680,4460,-1,-1); hx(4650,3330,1,-1); hx(4610,3330,-1,-1); hx(4650,5380,1,-1); hx(4610,5380,-1,-1);
    hx(7380,5880,-1,-1); hx(7420,5880,1,-1); hx(3130,8570,1,1); hx(3090,8570,-1,1);
    /* switches */
    const swW=MAT.white, swB=MAT.metalB;
    const sx=(xf,zc,n,y,m)=>{B(n>0?xf:xf-10,zc-43,10,86,y-43,y+43,m); B(n>0?xf+10:xf-14,zc-30,4,60,y-30,y+30,m);};
    const sz=(xc,zf,n,y,m)=>{B(xc-43,n>0?zf:zf-10,86,10,y-43,y+43,m); B(xc-30,n>0?zf+10:zf-14,60,4,y-30,y+30,m);};
    sz(5850,4097,-1,900,swB); sz(6050,4097,-1,750,swB); sz(9150,4097,-1,750,swB); sx(4150,2450,-1,900,swW); sx(4150,5600,-1,900,swW);
    sz(5850,4500,1,900,swW); sx(4650,5600,1,900,swW); sx(3130,9350,1,900,swW); sx(7380,6050,-1,900,swW); sx(7540,6050,1,900,swW);
    /* bedroom */
    B(6200,1500,2800,2100,0,22,MAT.rugShag,false);
    B(6700,1900,1800,2200,100,350,MAT.fabric); B(6650,4000,1900,97,100,1250,MAT.boucle);
    B(6760,2000,1680,2000,350,560,MAT.linen); B(6720,1950,1760,1350,520,600,std('#C9CCD0',1)); B(6720,2050,1760,420,600,630,BV);
    B(6860,3480,680,420,560,720,MAT.linen); B(7660,3480,680,420,560,720,MAT.linen); B(7350,3330,400,150,600,900,BV);
    B(6150,3600,450,400,150,550,oak(.45,.4)); B(8600,3600,450,400,150,550,oak(.45,.4));
    B(7700,0,1500,380,300,560,oak(1.5,.26)); B(7800,0,1230,35,1050,1760,MAT.gloss);
    /* cabinet 1 */
    B(600,3000,1600,700,720,750,oak(1.6,.7)); B(620,3020,40,640,0,720,MAT.graph); B(2140,3020,40,640,0,720,MAT.graph);
    B(1150,3560,700,25,950,1350,MAT.gloss); B(1460,3480,80,120,750,950,MAT.graph); chair(1400,2550,-1);
    B(3800,300,350,2100,0,2200,MAT.white); for(const y of [600,1000,1400,1800]) B(3795,320,6,2060,y,y+8,MAT.graph);
    B(500,600,2600,1900,0,15,MAT.rugShag,false);
    /* cabinet 2 */
    B(700,7150,1600,700,720,750,oak(1.6,.7)); B(720,7170,40,640,0,720,MAT.graph); B(2240,7170,40,640,0,720,MAT.graph);
    B(1150,7800,700,25,950,1350,MAT.gloss); B(1460,7700,80,120,750,950,MAT.graph); chair(1400,6700,-1);
    B(300,4030,2600,350,0,2200,MAT.white); for(const y of [600,1000,1400,1800]) B(320,4377,2560,6,y,y+8,MAT.graph);
    plant(3700,7500,.9);
    /* walk-in wardrobe */
    B(7540,4500,600,600,0,CH,MAT.white); B(7540,6000,600,1890,0,CH,MAT.white); B(7540,8290,600,2510,0,CH,MAT.white);
    B(8890,4500,600,650,0,CH,MAT.white); B(8990,9000,500,1800,0,CH,MAT.white); B(8140,10200,850,600,0,CH,MAT.white);
    for(const z of [6600,7250,8900,9550,10200]) B(8138,z-2,4,4,0,CH,MAT.graph);
    for(const z of [9600,10200]) B(8988,z-2,4,4,0,CH,MAT.graph);
    B(9040,5300,450,2400,0,450,MAT.white); B(9060,5350,410,2300,450,520,MAT.boucle);
    B(8140,7882,598,8,0,CH,MAT.mirror); B(8730,7882,8,416,0,CH,MAT.mirror); B(8140,8290,598,8,0,CH,MAT.mirror); // column clad in mirror on all open faces
    /* bath */
    const tb=new THREE.Mesh(new THREE.CylinderGeometry(.18,.15,.28,40),MAT.gloss); tb.scale.set(1,1,1.45); tb.position.set(.5,.34,8.77); tb.castShadow=true; G.add(tb);
    const ts=new THREE.Mesh(new THREE.CylinderGeometry(.185,.185,.02,40),MAT.gloss); ts.scale.set(1,1,1.45); ts.position.set(.5,.49,8.77); G.add(ts);
    B(350,8500,300,110,260,480,MAT.gloss); B(375,8500,250,8,1000,1150,hm);
    B(1600,8303,800,460,400,850,oak(.8,.45)); B(1590,8303,820,470,850,880,MAT.ceramic); B(1800,8380,400,300,877,883,std('#DCE1E4',.2));
    Cy(2000,8380,12,880,1080,hm); B(1988,8380,24,110,1050,1070,hm); Cy(1800,8400,30,880,1060,MAT.black); Cy(2250,8400,28,880,1000,MAT.ceramic);
    const mir=new THREE.Mesh(new THREE.CylinderGeometry(.3,.3,.015,48),MAT.mirror); mir.rotation.x=Math.PI/2; mir.position.set(2,1.55,8.31); G.add(mir);
    const ring=new THREE.Mesh(new THREE.TorusGeometry(.305,.01,8,64),MAT.emis); ring.position.set(2,1.55,8.308); G.add(ring);
    B(1050,10050,1700,750,0,550,marble(1.7,.55)); B(1050,10050,1700,750,550,580,MAT.ceramic); B(1150,10150,1500,550,578,584,MAT.water);
    B(1850,10044,900,10,580,2000,MAT.glass,false); B(1850,10042,900,14,1986,2000,hm); B(1850,10042,14,14,580,2000,hm); B(2736,10042,14,14,580,2000,hm);
    Cy(2730,10425,12,1100,2150,hm); B(2510,10413,220,24,2140,2160,hm); Cy(2510,10425,125,2118,2132,hm); B(2717,10355,30,140,1080,1150,hm);
    Cy(45,8620,10,600,1400,hm); Cy(45,9020,10,600,1400,hm); for(let k=0;k<6;k++) B(35,8620,20,400,620+k*150,632+k*150,hm); B(60,8660,20,320,820,1380,BV); // towel rail on the black wall to the toilet's right
    B(150,8500,12,6,0,CH,MAT.emis,false); // vertical light line on the box, right of the toilet
    applyMode();
  }
""")

# ---------- lights, camera, ui ----------
rp("if(room==='plan'){pts=[[5720,6777],[1173,6500],[7000,2000],[4100,2200],[3300,10000]];}",
   "if(room==='plan'){pts=[[7000,2000],[2000,1800],[2000,6000],[5500,9300],[8500,7000]];}")
rp("sun.target.position.set(4.4,0,5.6);", "sun.target.position.set(4.75,0,5.4);")
rp("if(plan){camera.fov=45; camera.position.set(4.4,16.5,13.5); controls.target.set(4.4,0,5.4); controls.update();}",
   "if(plan){camera.fov=45; camera.position.set(4.75,16.5,13.5); controls.target.set(4.75,0,5.4); controls.update();}")
rp("controls.target.set(4.4,0,5.6);", "controls.target.set(4.75,0,5.4);")
rp("$('iEy').textContent='Акцент · эвкалипт'", "$('iEy').textContent='Акцент · мягкий синий'")
rp("$('iMeta').textContent=r?`${(r.w*r.h/1e6).toFixed(1).replace('.',',')} м² · ${r.w} × ${r.h} мм · потолок 2,7 м`:'≈89 м² · 7 помещений';",
   "$('iMeta').textContent=r?(r.meta||`${(r.w*r.h/1e6).toFixed(1).replace('.',',')} м² · ${r.w} × ${r.h} мм`)+' · потолок 2,6 м':'≈92 м² · 6 помещений';")
rp("try{localStorage.setItem('bm3d',", "try{localStorage.setItem('bm3d3',")
rp("try{const s=JSON.parse(localStorage.getItem('bm3d')||'{}');", "try{const s=JSON.parse(localStorage.getItem('bm3d3')||'{}');")

rp('текстиль и декор упрощены. <a href="https://claude.ai/artifact/NdNLScfeLo88R2JBLUzSV9" target="_blank" rel="noopener" style="color:var(--ink)">Рендеры ↗</a> · <a href="https://claude.ai/artifact/9MB8Cj6L6JAypYiB44Hc24" target="_blank" rel="noopener" style="color:var(--ink)">Альбом 2-го этажа ↗</a> · <a href="https://claude.ai/artifact/TtxLQreexDNjqHi2Xh63z7" target="_blank" rel="noopener" style="color:var(--ink)">3D 3-го этажа ↗</a></p>', 'текстиль и декор упрощены. <a href="https://claude.ai/artifact/NdNLScfeLo88R2JBLUzSV9" target="_blank" rel="noopener" style="color:var(--ink)">Рендеры ↗</a> · <a href="https://claude.ai/artifact/McGG55hERMoPMfJy1exJJC" target="_blank" rel="noopener" style="color:var(--ink)">Альбом 3-го этажа ↗</a> · <a href="https://claude.ai/artifact/28H1v2KMhfgMxbCvUBXe2U" target="_blank" rel="noopener" style="color:var(--ink)">3D 2-го этажа ↗</a></p>')  # n3note
print('FAILS', fails)
open('viz3-src.html', 'w').write(S)
b = lambda f: 'data:image/jpeg;base64,' + base64.b64encode(open(f, 'rb').read()).decode()
out = S.replace('__MARBLE__', b('marble.jpg')).replace('__RUT__', b('rutland.jpg'))
open('viz3-belyi-mramor.html', 'w').write(out)
open('v3prev.html', 'w').write('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body>' + out + '</body></html>')

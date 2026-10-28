p='viz-src.html'; s=open(p).read()
def rp(a,b):
    global s
    assert s.count(a)==1,a[:60]; s=s.replace(a,b)
rp("B(2448,10327,20,1000,WH,WH+600,MAT.wall);","B(2448,10327,20,1000,WH,WH+600,MAT.wall); B(2448,11327,3140,20,WH,WH+600,MAT.wall);")
rp("    art(g);\n","""    art(g);
    B(5300,6930,320,230,370,400,MAT.ceramic); B(5320,6945,280,200,400,425,MAT.black); Cy(5950,7150,110,370,430,g?MAT.black:MAT.brass);
    Cy(5000,4950,70,600,930,MAT.ceramic); Cy(5200,4960,55,600,780,MAT.black); Cy(6300,4980,90,600,690,MAT.ceramic);
    B(5200,7930,500,420,500,520,g?MAT.velvet:std('#CFC6B8',1));
""")
rp("    B(1796,0,550,400,0,1900,MAT.black);","    Cy(1173,1825,60,750,1010,MAT.ceramic); Cy(1173,1825,65,1005,1012,MAT.black);\n    B(1796,0,550,400,0,1900,MAT.black);")
rp("B(5760,1200,420,760,560,720,MAT.linen); B(5760,2040,420,760,560,720,MAT.linen);","B(5760,1200,420,760,560,720,MAT.linen); B(5760,2040,420,760,560,720,MAT.linen); B(7150,1110,420,1780,600,630,g?MAT.velvet:std('#B9A88F',1)); B(5900,1500,180,520,720,800,g?MAT.velvet:std('#CFC6B8',1)); B(5900,2080,180,520,720,800,MAT.fabricL);")
rp("Cy(8690,10120,10,600,1400,V.metal);","B(8655,10140,20,340,820,1380,g?MAT.velvet:std('#D8CDBE',1)); Cy(7130,9420,30,880,1060,MAT.black); Cy(7480,9420,28,880,1000,MAT.ceramic);\n    Cy(8690,10120,10,600,1400,V.metal);")
rp("B(1500,9347,600,8,900,1950,MAT.mirror);","B(1500,9347,600,8,900,1950,MAT.mirror); B(1500,9360,200,300,450,520,MAT.black);")
open(p,'w').write(s)
import base64
s=s.replace('__MARBLE__','data:image/jpeg;base64,'+base64.b64encode(open('marble.jpg','rb').read()).decode())
open('viz-belyi-mramor.html','w').write(s)
open('vprev.html','w').write('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body>'+s+'</body></html>')
p='render.py'; r=open(p).read()
def rr(a,b):
    global r
    assert r.count(a)==1,a[:60]; r=r.replace(a,b)
rr("""# smooth shading for curved objects
for ob in sc.objects:
    if ob.type == 'MESH' and len(ob.data.polygons) > 30:
        for poly in ob.data.polygons: poly.use_smooth = True""","""# smooth shading for curved objects, bevels for boxes
SOFT = ('fabric', 'fabricL', 'linen', 'velvet', 'rug', 'leather')
SKIP = ('wall', 'ceil', 'glass', 'curtain', 'emis')
for ob in list(sc.objects):
    if ob.type != 'MESH': continue
    names = [m.name.split('.')[0] for m in ob.data.materials if m]
    if len(ob.data.polygons) > 30:
        for poly in ob.data.polygons: poly.use_smooth = True
        continue
    if not names or any(n in SKIP for n in names): continue
    dims = sorted(ob.dimensions)
    soft = any(n in SOFT for n in names)
    w = min(0.035 if soft else 0.004, dims[0] * 0.45)
    if w < 0.0008: continue
    bv = ob.modifiers.new('bv', 'BEVEL'); bv.width = w; bv.segments = 4 if soft else 2; bv.limit_method = 'ANGLE'
    for poly in ob.data.polygons: poly.use_smooth = True
    try: ob.data.set_sharp_from_angle(angle=math.radians(40))
    except Exception: pass""")
rr("""    'zal': ([8350, 1450, 7500], [4300, 1100, 5600]),""","""    'zal': ([8350, 1450, 7500], [4300, 1100, 5600]),
    'zal2': ([8350, 1450, 5000], [4400, 950, 8300]),""")
rr("try: sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'None'\nexcept Exception: pass","""try: sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'None'
except Exception: pass
try:
    sc.view_settings.use_white_balance = True; sc.view_settings.white_balance_temperature = 6500 if eve else 7300
except Exception as e: print('wb', e)""")
open(p,'w').write(r)
print('ok')

import glob, base64, io, json, os
from PIL import Image, ImageEnhance
imgs={}
os.makedirs('rend_out',exist_ok=True)
for f in sorted(glob.glob('rend/*.jpg'))+sorted(glob.glob('rend3/*.jpg')):
    if 'cor2' in f: continue
    k=os.path.basename(f)[:-4]  # green_day_zal
    im=Image.open(f).convert('RGB')
    r,g,b=im.split()
    eve='_eve_' in k
    r=r.point(lambda v:min(255,int(v*(1.03 if eve else 1.05))))
    b=b.point(lambda v:int(v*(0.97 if eve else 0.92)))
    im=Image.merge('RGB',(r,g,b))
    im=ImageEnhance.Contrast(im).enhance(1.06)
    from PIL import ImageStat
    L=ImageStat.Stat(im.convert('L')).mean[0]/255
    tgt=0.40 if eve else 0.58
    if abs(L-tgt)>0.04:
        import math
        gm=max(0.75,min(1.3,math.log(tgt)/math.log(max(L,0.05))))
        im=im.point(lambda v:int(255*((v/255)**gm)))
    im.save('rend_out/'+k+'.jpg',quality=84)
    buf=io.BytesIO(); im.save(buf,'JPEG',quality=80,optimize=True)
    imgs[k]='data:image/jpeg;base64,'+base64.b64encode(buf.getvalue()).decode()
s=open('gal-src.html').read().replace('__IMAGES__',json.dumps(imgs))
open('renders-belyi-mramor.html','w').write(s)
print(len(imgs), round(len(s)/1e6,2),'MB')

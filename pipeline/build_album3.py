import base64
lines=open('proekt-belyi-mramor.html').read().split('\n')
head='\n'.join(lines[:186]).replace('<title>Проект «Белый мрамор»</title>','<title>Третий этаж «Белого мрамора»</title>',1)
b=lambda f:'data:image/jpeg;base64,'+base64.b64encode(open(f,'rb').read()).decode()
head=head.replace('</defs>','  <pattern id="rut" patternUnits="userSpaceOnUse" width="1212" height="1216"><image href="'+b('rutland.jpg')+'" width="1212" height="1216" preserveAspectRatio="none"/></pattern>\n</defs>',1)
body=open('album3-body.html').read().replace('__VIZ3__','https://claude.ai/artifact/TtxLQreexDNjqHi2Xh63z7').replace('__GAL__','https://claude.ai/artifact/NdNLScfeLo88R2JBLUzSV9').replace('__PLAN3__',b('plan3.jpg'))
open('proekt3-belyi-mramor.html','w').write(head+'\n\n'+body)

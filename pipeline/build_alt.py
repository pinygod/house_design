# Собирает страницу «Спальня 1 (Альтернатива)»: встраивает кадры варианта А из rend_out (после buildgal.py)
import base64, json, os
keys = ['green_day_topalt', 'green_day_alt1', 'green_day_alt2', 'green_day_alt3', 'green_day_alt4', 'green_eve_alt1']
img = {k: 'data:image/jpeg;base64,' + base64.b64encode(open(f'rend_out/{k}.jpg', 'rb').read()).decode() for k in keys if os.path.exists(f'rend_out/{k}.jpg')}
s = open('alt-src.html', encoding='utf-8').read().replace('__ALTIMG__', json.dumps(img))
open('alt-belyi-mramor.html', 'w', encoding='utf-8').write(s)
print(len(img), 'images', round(len(s) / 1e6, 2), 'MB')

# Собирает общую страницу проекта: каждый документ кладётся внутрь в base64 и открывается в своём iframe (srcdoc).
import base64, json

DOCS = {
    'plan': 'plans.html',
    'album-f2': 'proekt-belyi-mramor.html',
    'album-f3': 'proekt3-belyi-mramor.html',
    '3d-f2': 'viz-belyi-mramor.html',
    '3d-f3': 'viz3-belyi-mramor.html',
    'renders': 'renders-belyi-mramor.html',
    'alt': 'alt-belyi-mramor.html',
}
URLS = {
    'album-f2': 'https://claude.ai/artifact/9MB8Cj6L6JAypYiB44Hc24',
    'album-f3': 'https://claude.ai/artifact/McGG55hERMoPMfJy1exJJC',
    '3d-f2': 'https://claude.ai/artifact/28H1v2KMhfgMxbCvUBXe2U',
    '3d-f3': 'https://claude.ai/artifact/TtxLQreexDNjqHi2Xh63z7',
    'renders': 'https://claude.ai/artifact/NdNLScfeLo88R2JBLUzSV9',
    'alt': 'https://claude.ai/artifact/VNL75chQxkJushUKa7NC45',
}
RELS = {
    'plan': 'plans/', 'album-f2': 'album/', 'album-f3': 'floor-3/album/',
    '3d-f2': 'viz-3d/', '3d-f3': 'floor-3/viz-3d/', 'renders': 'renders/', 'alt': 'bedroom-1-alt/',
}
GO = {u.rsplit('/', 1)[1]: k for k, u in URLS.items()}

HEAD = ('<!doctype html><html lang="ru"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
        '<style>body{margin:0}[hidden]{display:none!important}img{max-width:100%}</style>')
# ссылки на другие артефакты проекта переключают раздел общей страницы, а не открывают новую вкладку
BRIDGE = ('<script>(function(){var M=%s;document.addEventListener("click",function(e){var a=e.target.closest&&e.target.closest("a[href]");'
          'if(!a)return;var m=/artifact\\/([A-Za-z0-9]+)/.exec(a.href);if(m&&M[m[1]]){e.preventDefault();parent.postMessage({bmGo:M[m[1]]},"*");}},true);})();</script>'
          % json.dumps(GO))

enc = {}
for k, f in DOCS.items():
    html = HEAD + open(f, encoding='utf-8').read() + BRIDGE
    enc[k] = base64.b64encode(html.encode('utf-8')).decode()

src = open('hub-src.html', encoding='utf-8').read()
out = src.replace('__DOCS__', json.dumps(enc)).replace('__URLS__', json.dumps(URLS)).replace('__RELS__', json.dumps(RELS))
open('belyi-mramor.html', 'w', encoding='utf-8').write(out)
print(round(len(out) / 1e6, 2), 'MB')

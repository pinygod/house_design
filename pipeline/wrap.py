# Обёртка для публикации: страницы начинаются с <!DOCTYPE html>, как требует хостинг артефактов (и как в репозитории)
import sys
HEAD=('<!DOCTYPE html>\n<html lang="ru"><head><meta charset="utf-8">'
      '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
      '<style>body{margin:0}[hidden]{display:none!important}img{max-width:100%}</style>\n')
for src, dst in zip(sys.argv[1::2], sys.argv[2::2]):
    open(dst,'w',encoding='utf-8').write(HEAD+open(src,encoding='utf-8').read())

#!/bin/bash
cd "$(dirname "$0")"
P=./bvenv/bin/python
$P render.py -- '{"glb":"scene_green.glb","mode":"day","views":["zal","zal2","kitchen","dining","bed1","bed2","cor"],"out":"rend/green_day","samples":96,"res":[1600,900],"exp":1.8}' 2>&1 | grep DONE
$P render.py -- '{"glb":"scene_green.glb","mode":"eve","views":["zal","cor","bath","bed1"],"out":"rend/green_eve","samples":96,"res":[1600,900],"exp":0.9,"exposure":{"bath":1.1}}' 2>&1 | grep DONE
echo ALLDONE

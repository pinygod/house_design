#!/bin/bash
cd "$(dirname "$0")"
P=./bvenv/bin/python
$P render.py -- '{"glb":"scene_green.glb","mode":"day","views":["bd1","bd2"],"out":"rend/green_day","samples":96,"res":[1600,900],"exp":1.3}' 2>&1 | grep -E "DONE|Error"
$P render.py -- '{"glb":"scene_open.glb","mode":"day","views":["bd1o","bd2o"],"out":"rend/green_day","samples":96,"res":[1600,900],"exp":1.3}' 2>&1 | grep -E "DONE|Error"
$P render.py -- '{"glb":"scene_green.glb","mode":"day","views":["kitchen","kitchen2","zalkit","dining2","cor"],"out":"rend/green_day","samples":96,"res":[1600,900],"exp":1.8}' 2>&1 | grep -E "DONE|Error"
$P render.py -- '{"glb":"scene_green.glb","mode":"eve","views":["bath","bath2","cor"],"out":"rend/green_eve","samples":96,"res":[1600,900],"exp":0.9,"exposure":{"bath":1.1,"bath2":1.1}}' 2>&1 | grep -E "DONE|Error"
$P render.py -- '{"glb":"scene_green.glb","mode":"day","views":["ov1","ov2","ov3"],"out":"rend/green_day","samples":96,"res":[1600,900],"exp":-0.5,"cut":2300}' 2>&1 | grep -E "DONE|Error"
$P render.py -- '{"glb":"scene_green.glb","mode":"eve","views":["ov1"],"out":"rend/green_eve","samples":128,"res":[1600,900],"exp":1.2,"cut":2300}' 2>&1 | grep -E "DONE|Error"
echo ALLDONE

#!/bin/bash
cd "$(dirname "$0")"
while pgrep -f batch3.sh >/dev/null; do sleep 20; done
P=./bvenv/bin/python
$P render.py -- '{"glb":"scene_green.glb","mode":"day","views":["ov1","ov2","ov3"],"out":"rend/green_day","samples":96,"res":[1600,900],"exp":-0.5,"cut":2300}' 2>&1 | grep -E "DONE|Error"
$P render.py -- '{"glb":"scene_green.glb","mode":"eve","views":["ov1"],"out":"rend/green_eve","samples":128,"res":[1600,900],"exp":1.2,"cut":2300}' 2>&1 | grep -E "DONE|Error"
$P render.py -- '{"floor":3,"glb":"scene3.glb","mode":"day","views":["ov1","ov2","ov3"],"out":"rend3/f3_day","samples":96,"res":[1600,900],"exp":-0.5,"cut":2300}' 2>&1 | grep -E "DONE|Error"
$P render.py -- '{"floor":3,"glb":"scene3.glb","mode":"eve","views":["ov1"],"out":"rend3/f3_eve","samples":128,"res":[1600,900],"exp":1.2,"cut":2300}' 2>&1 | grep -E "DONE|Error"
echo ALLDONE

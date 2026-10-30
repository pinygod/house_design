#!/bin/bash
cd "$(dirname "$0")"
P=./bvenv/bin/python
$P render.py -- '{"glb":"scene_green.glb","mode":"day","views":["zal3","zal4","zalkit","kitchen2","dining2","bed1b","bed2b","corzal"],"out":"rend/green_day","samples":96,"res":[1600,900],"exp":1.8}' 2>&1 | grep -E "DONE|Error"
$P render.py -- '{"glb":"scene_green.glb","mode":"eve","views":["zal4","bath2"],"out":"rend/green_eve","samples":96,"res":[1600,900],"exp":0.9,"exposure":{"bath2":1.1}}' 2>&1 | grep -E "DONE|Error"
$P render.py -- '{"floor":3,"glb":"scene3.glb","mode":"day","views":["bed3","bed4","cab1b","cab2b","cor3","gard2","bath2"],"out":"rend3/f3_day","samples":96,"res":[1600,900],"exp":1.6}' 2>&1 | grep -E "DONE|Error"
$P render.py -- '{"floor":3,"glb":"scene3.glb","mode":"eve","views":["cor3"],"out":"rend3/f3_eve","samples":96,"res":[1600,900],"exp":0.9}' 2>&1 | grep -E "DONE|Error"
echo ALLDONE

#!/bin/bash
cd "$(dirname "$0")"
P=./bvenv/bin/python
node export3.js > /dev/null 2>&1
$P render.py -- '{"glb":"scene_alt.glb","mode":"day","views":["alt1","alt2","alt3","alt4"],"out":"rend/green_day","samples":96,"res":[1600,900],"exp":1.8}' 2>&1 | grep -E "DONE|Error"
$P render.py -- '{"glb":"scene_alt.glb","mode":"eve","views":["alt1"],"out":"rend/green_eve","samples":96,"res":[1600,900],"exp":0.9}' 2>&1 | grep -E "DONE|Error"
$P render.py -- '{"glb":"scene_alt.glb","mode":"day","views":["topalt"],"out":"rend/green_day","samples":96,"res":[1600,900],"exp":-0.4,"cut":2300}' 2>&1 | grep -E "DONE|Error"
$P render.py -- '{"glb":"scene_green.glb","mode":"day","views":["zal","zal2","zal3","zal4","zalkit","kitchen","kitchen2","dining","dining2","bed1","bed1b","bed2","bed2b","cor","corzal"],"out":"rend/green_day","samples":96,"res":[1600,900],"exp":1.8}' 2>&1 | grep -E "DONE|Error"
$P render.py -- '{"glb":"scene_green.glb","mode":"eve","views":["zal","zal4","cor","bath","bath2","bed1"],"out":"rend/green_eve","samples":96,"res":[1600,900],"exp":0.9,"exposure":{"bath":1.1,"bath2":1.1}}' 2>&1 | grep -E "DONE|Error"
$P render.py -- '{"glb":"scene_green.glb","mode":"day","views":["ov1","ov2","ov3"],"out":"rend/green_day","samples":96,"res":[1600,900],"exp":-0.5,"cut":2300}' 2>&1 | grep -E "DONE|Error"
$P render.py -- '{"glb":"scene_green.glb","mode":"eve","views":["ov1"],"out":"rend/green_eve","samples":128,"res":[1600,900],"exp":1.2,"cut":2300}' 2>&1 | grep -E "DONE|Error"
$P render.py -- '{"floor":3,"glb":"scene3.glb","mode":"day","views":["cor","cor3","cab2","bath2"],"out":"rend3/f3_day","samples":96,"res":[1600,900],"exp":1.6}' 2>&1 | grep -E "DONE|Error"
$P render.py -- '{"floor":3,"glb":"scene3.glb","mode":"eve","views":["cor3"],"out":"rend3/f3_eve","samples":96,"res":[1600,900],"exp":0.9}' 2>&1 | grep -E "DONE|Error"
echo ALLDONE

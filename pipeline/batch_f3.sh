#!/bin/bash
cd "$(dirname "$0")"
P=./bvenv/bin/python
$P render.py -- '{"floor":3,"glb":"scene3.glb","mode":"day","views":["bed","bed2","cab1","cab2","cor","gard"],"out":"rend3/f3_day","samples":96,"res":[1600,900],"exp":1.6}' 2>&1 | grep -E "DONE|Error"
$P render.py -- '{"floor":3,"glb":"scene3.glb","mode":"eve","views":["bed","cor","bath"],"out":"rend3/f3_eve","samples":96,"res":[1600,900],"exp":0.9,"exposure":{"bath":1.1}}' 2>&1 | grep -E "DONE|Error"
echo ALLDONE

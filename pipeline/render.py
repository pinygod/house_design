import bpy, sys, math, json
from mathutils import Vector

args = json.loads(sys.argv[sys.argv.index('--') + 1])
GLB, MODE, VIEWS, OUT = args['glb'], args['mode'], args['views'], args['out']
SAMPLES = args.get('samples', 128)
W, H = args.get('res', [1600, 900])
EXPO = args.get('exposure', {})

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=GLB)
sc = bpy.context.scene

ROOMS = {'zal': (2766, 4764, 5946, 4026), 'kitchen': (0, 3750, 2346, 5223), 'dining': (0, 0, 2346, 3650),
         'bed1': (5578, 0, 3134, 4644), 'bed2': (2766, 0, 2692, 4644), 'cor': (0, 9327, 6800, 2000), 'bath': (6912, 9327, 1800, 2000)}
SPOT = [[3540,5560],[4980,5560],[6420,5560],[7860,5560],[3540,6777],[4980,6777],[6420,6777],[7860,6777],[3540,7994],[4980,7994],[6420,7994],[7860,7994],
  [850,7100],[850,7900],[1350,8200],[1173,4900],[1173,6000],[1800,7300],[500,1000],[1846,1000],[500,2650],[1846,2650],
  [8050,1000],[8050,2000],[8050,3000],[6200,3650],[7200,3650],[7000,550],[5150,900],[5150,1900],[4300,3000],[4300,4000],[3300,3000],[3300,4000],
  [7312,9850],[8212,10260],[7400,10950],[8250,10950]]
PEND = [[5778, 825, 1150], [5778, 3175, 1150], [2966, 450, 1150], [2966, 2550, 1150]]
CAMS = {
  'zal': ([8350, 1450, 7500], [4300, 1100, 5600]),
  'zal2': ([8050, 1450, 4950], [4400, 950, 8400]),
  'kitchen': ([1250, 1450, 3950], [700, 1050, 8400]),
  'dining': ([2100, 1450, 3450], [600, 1000, 900]),
  'bed1': ([8400, 1450, 3880], [5800, 1000, 1900]),
  'bed2': ([4300, 1450, 4400], [3000, 950, 1400]),
  'cor': ([600, 1450, 11050], [4600, 1150, 10000]),
  'cor2': ([6600, 1450, 9900], [1000, 1100, 10900]),
  'bath': ([7050, 1450, 11200], [8000, 1200, 9400]),
}
def B(x, y, z):  # three mm -> blender m
    return Vector((x / 1000, -z / 1000, y / 1000))

WARM = (1.0, 0.80, 0.58, 1)
eve = MODE == 'eve'

def principled(mat):
    for n in mat.node_tree.nodes:
        if n.type == 'BSDF_PRINCIPLED':
            return n
def setin(n, k, v):
    if k in n.inputs: n.inputs[k].default_value = v

def emission_mat(mat, strength, color=WARM):
    nt = mat.node_tree; nt.nodes.clear()
    o = nt.nodes.new('ShaderNodeOutputMaterial'); e = nt.nodes.new('ShaderNodeEmission')
    e.inputs['Color'].default_value = color; e.inputs['Strength'].default_value = strength
    nt.links.new(e.outputs[0], o.inputs[0])

def glass_mat(mat, tint=(0.9, 0.95, 0.97, 1), fac=0.12):
    nt = mat.node_tree; nt.nodes.clear()
    o = nt.nodes.new('ShaderNodeOutputMaterial'); t = nt.nodes.new('ShaderNodeBsdfTransparent'); g = nt.nodes.new('ShaderNodeBsdfGlossy')
    g.inputs['Roughness'].default_value = 0.02; t.inputs['Color'].default_value = tint
    m = nt.nodes.new('ShaderNodeMixShader'); m.inputs[0].default_value = fac
    nt.links.new(t.outputs[0], m.inputs[1]); nt.links.new(g.outputs[0], m.inputs[2]); nt.links.new(m.outputs[0], o.inputs[0])

def curtain_mat(mat):
    nt = mat.node_tree; nt.nodes.clear()
    o = nt.nodes.new('ShaderNodeOutputMaterial'); t = nt.nodes.new('ShaderNodeBsdfTransparent'); tr = nt.nodes.new('ShaderNodeBsdfTranslucent'); d = nt.nodes.new('ShaderNodeBsdfDiffuse')
    tr.inputs['Color'].default_value = (0.95, 0.93, 0.9, 1); d.inputs['Color'].default_value = (0.92, 0.9, 0.87, 1)
    m1 = nt.nodes.new('ShaderNodeMixShader'); m1.inputs[0].default_value = 0.45
    nt.links.new(d.outputs[0], m1.inputs[1]); nt.links.new(tr.outputs[0], m1.inputs[2])
    m2 = nt.nodes.new('ShaderNodeMixShader'); m2.inputs[0].default_value = 0.55
    nt.links.new(t.outputs[0], m2.inputs[1]); nt.links.new(m1.outputs[0], m2.inputs[2]); nt.links.new(m2.outputs[0], o.inputs[0])

def add_bump(mat, strength):
    nt = mat.node_tree; p = principled(mat)
    img = next((n for n in nt.nodes if n.type == 'TEX_IMAGE'), None)
    if not (p and img): return
    bw = nt.nodes.new('ShaderNodeRGBToBW'); bp = nt.nodes.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = strength; bp.inputs['Distance'].default_value = 0.002
    nt.links.new(img.outputs['Color'], bw.inputs[0]); nt.links.new(bw.outputs[0], bp.inputs['Height']); nt.links.new(bp.outputs['Normal'], p.inputs['Normal'])

for mat in bpy.data.materials:
    if not mat.use_nodes: continue
    name = mat.name.split('.')[0]
    p = principled(mat)
    if name == 'emis': emission_mat(mat, 14 if eve else 6); continue
    if name == 'glass': glass_mat(mat); continue
    if name == 'curtain': curtain_mat(mat); continue
    if name == 'shade':
        if eve: emission_mat(mat, 6)
        continue
    if not p: continue
    setin(p, 'Alpha', 1.0)
    if hasattr(mat, 'surface_render_method'): mat.surface_render_method = 'DITHERED'
    if name == 'mirror': setin(p, 'Base Color', (0.9, 0.9, 0.9, 1)); setin(p, 'Metallic', 1.0); setin(p, 'Roughness', 0.02)
    elif name == 'brass': setin(p, 'Base Color', (0.72, 0.52, 0.27, 1)); setin(p, 'Metallic', 1.0); setin(p, 'Roughness', 0.28)
    elif name == 'metalB': setin(p, 'Base Color', (0.02, 0.02, 0.02, 1)); setin(p, 'Metallic', 0.9); setin(p, 'Roughness', 0.35)
    elif name == 'gloss': setin(p, 'Base Color', (0.012, 0.012, 0.013, 1)); setin(p, 'Roughness', 0.06); setin(p, 'Coat Weight', 0.6)
    elif name == 'ceramic': setin(p, 'Roughness', 0.06); setin(p, 'Coat Weight', 0.5)
    elif name == 'water': setin(p, 'Roughness', 0.05)
    elif name == 'marble': setin(p, 'Roughness', 0.22); setin(p, 'Coat Weight', 0.1); setin(p, 'Coat Roughness', 0.2)
    elif name == 'blackmarble': setin(p, 'Roughness', 0.18); setin(p, 'Coat Weight', 0.4)
    elif name in ('wall', 'ceil'): setin(p, 'Roughness', 0.92)
    elif name == 'greenLac': setin(p, 'Roughness', 0.42); setin(p, 'Coat Weight', 0.15)
    elif name == 'white': setin(p, 'Roughness', 0.35); setin(p, 'Coat Weight', 0.2)
    elif name == 'oak': setin(p, 'Roughness', 0.55); add_bump(mat, 0.08)
    elif name in ('porcB', 'porcW'): setin(p, 'Roughness', 0.7); add_bump(mat, 0.35)
    elif name == 'velvet': setin(p, 'Sheen Weight', 0.2); setin(p, 'Roughness', 0.9)
    elif name in ('fabric', 'fabricL', 'linen', 'rug'): setin(p, 'Sheen Weight', 0.15); setin(p, 'Roughness', 1.0)

# smooth shading for curved objects, bevels for boxes
SOFT = ('fabric', 'fabricL', 'linen', 'velvet', 'rug', 'leather')
SKIP = ('wall', 'ceil', 'glass', 'curtain', 'emis', 'shadow')
for ob in list(sc.objects):
    if ob.type != 'MESH': continue
    names = [m.name.split('.')[0] for m in ob.data.materials if m]
    if len(ob.data.polygons) > 30:
        for poly in ob.data.polygons: poly.use_smooth = True
        continue
    if not names or any(n in SKIP for n in names): continue
    dims = sorted(ob.dimensions)
    soft = any(n in SOFT for n in names)
    w = min(0.035 if soft else 0.004, dims[0] * 0.45)
    if w < 0.0008: continue
    bv = ob.modifiers.new('bv', 'BEVEL'); bv.width = w; bv.segments = 4 if soft else 2; bv.limit_method = 'ANGLE'
    for poly in ob.data.polygons: poly.use_smooth = True
    try: ob.data.set_sharp_from_angle(angle=math.radians(40))
    except Exception: pass

# world + sun
world = bpy.data.worlds.new('W'); sc.world = world; world.use_nodes = True
wn = world.node_tree; bg = wn.nodes['Background']
sun_dir = Vector((9, -7.2, -10)).normalized()
if not eve:
    sky = wn.nodes.new('ShaderNodeTexSky')
    try: sky.sky_type = 'NISHITA'
    except Exception: pass
    elev = math.asin(-sun_dir.z)
    try:
        sky.sun_elevation = elev; sky.sun_rotation = math.atan2(-sun_dir.y, -sun_dir.x) + math.pi / 2; sky.sun_disc = False
    except Exception: pass
    wn.links.new(sky.outputs[0], bg.inputs[0]); bg.inputs[1].default_value = 1.0
    sd = bpy.data.lights.new('sun', 'SUN'); sd.energy = 4.0; sd.angle = math.radians(1.0); sd.color = (1.0, 0.95, 0.88)
    so = bpy.data.objects.new('sun', sd); sc.collection.objects.link(so)
    so.rotation_euler = sun_dir.to_track_quat('-Z', 'Y').to_euler()
else:
    bg.inputs[0].default_value = (0.012, 0.016, 0.03, 1); bg.inputs[1].default_value = 1.0

# artificial lights
def spot(x, z, power, size=75):
    l = bpy.data.lights.new('s', 'SPOT'); l.energy = power; l.spot_size = math.radians(size); l.spot_blend = 0.7; l.color = WARM[:3]; l.shadow_soft_size = 0.03
    o = bpy.data.objects.new('s', l); sc.collection.objects.link(o); o.location = B(x, 2675, z); o.rotation_euler = (0, 0, 0)
def point(x, y, z, power, r=0.05):
    l = bpy.data.lights.new('p', 'POINT'); l.energy = power; l.color = WARM[:3]; l.shadow_soft_size = r
    o = bpy.data.objects.new('p', l); sc.collection.objects.link(o); o.location = B(x, y, z)
if eve:
    for x, z in SPOT: spot(x, z, 22)
    for x, z, y in PEND: point(x, y - 150, z, 6)
    point(8380, 1560, 6500, 25, 0.15)  # floor lamp
else:
    for x, z in SPOT: spot(x, z, 3)

# render settings
sc.render.engine = 'CYCLES'
cy = sc.cycles
cy.device = 'CPU'; cy.samples = SAMPLES; cy.use_adaptive_sampling = True; cy.adaptive_threshold = 0.03
cy.use_denoising = True
try: cy.denoiser = 'OPENIMAGEDENOISE'
except Exception: pass
cy.max_bounces = 8; cy.diffuse_bounces = 4; cy.glossy_bounces = 4; cy.transmission_bounces = 8; cy.transparent_max_bounces = 16
cy.sample_clamp_indirect = 8; cy.caustics_reflective = False; cy.caustics_refractive = False
sc.render.resolution_x = W; sc.render.resolution_y = H; sc.render.resolution_percentage = 100
sc.render.image_settings.file_format = 'JPEG'; sc.render.image_settings.quality = 88
try: sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'None'
except Exception: pass
try:
    sc.view_settings.use_white_balance = True; sc.view_settings.white_balance_temperature = 6500 if eve else 7300
except Exception as e: print('wb', e)
sc.render.threads_mode = 'FIXED'; sc.render.threads = 4

cam_d = bpy.data.cameras.new('cam'); cam = bpy.data.objects.new('cam', cam_d); sc.collection.objects.link(cam); sc.camera = cam
cam_d.sensor_fit = 'VERTICAL'; cam_d.clip_start = 0.05
for v in VIEWS:
    pos, look = CAMS[v]
    p = B(*pos); t = B(*look)
    d = (t - p); yaw = math.atan2(d.y, d.x); horiz = math.hypot(d.x, d.y)
    pitch = max(-0.10, min(0.05, math.atan2(d.z, horiz)))
    cam.location = p
    cam.rotation_euler = (math.pi / 2 + pitch, 0, yaw - math.pi / 2)
    cam_d.angle_y = math.radians(62 if v != 'bath' else 72)
    cam_d.shift_y = -0.06
    sc.view_settings.exposure = EXPO.get(v, args.get('exp', 0.0))
    sc.render.filepath = f"{OUT}_{v}.jpg"
    bpy.ops.render.render(write_still=True)
    print('DONE', v, flush=True)

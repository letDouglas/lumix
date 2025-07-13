import bpy
import os
from mathutils import Vector

# === CONFIG ===
blend_path = r"C:\Users\NOAHDECASTRO\Desktop\backgroundtest.blend"
color_image_path = r"C:\Users\NOAHDECASTRO\Desktop\673c7db9-bdbf-491f-afc9-38ba6ad1cb2e - Copia.png"
alpha_mask_path = r"C:\Users\NOAHDECASTRO\Desktop\alpha_mask.png"
output_path = r"C:\Users\NOAHDECASTRO\Desktop\render.png"

# === OPEN BLEND FILE ===
bpy.ops.wm.open_mainfile(filepath=blend_path)

# === LOAD IMAGE DIMENSIONS ===
color_img = bpy.data.images.load(color_image_path)
img_width, img_height = color_img.size
aspect_ratio = img_width / img_height

# === ADD PLANE ===
plane_height = 2.0
plane_width = aspect_ratio * plane_height
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0))
plane = bpy.context.active_object
plane.scale = Vector((plane_width / 2, plane_height / 2, 1))
plane.location.z += plane_height / 2

# === CREATE MATERIAL WITH ALPHA MASK ===
mat = bpy.data.materials.new(name="MaskedMaterial")
mat.use_nodes = True
nodes = mat.node_tree.nodes
links = mat.node_tree.links
nodes.clear()

# Nodes
output = nodes.new(type="ShaderNodeOutputMaterial")
output.location = (400, 0)

bsdf = nodes.new(type="ShaderNodeBsdfPrincipled")
bsdf.location = (200, 0)

img_color_node = nodes.new(type="ShaderNodeTexImage")
img_color_node.image = color_img
img_color_node.location = (-400, 100)
img_color_node.interpolation = 'Smart'

alpha_img = bpy.data.images.load(alpha_mask_path)
img_alpha_node = nodes.new(type="ShaderNodeTexImage")
img_alpha_node.image = alpha_img
img_alpha_node.location = (-400, -100)
img_alpha_node.interpolation = 'Smart'

# Links
links.new(img_color_node.outputs["Color"], bsdf.inputs["Base Color"])
links.new(img_alpha_node.outputs["Color"], bsdf.inputs["Alpha"])
links.new(bsdf.outputs["BSDF"], output.inputs["Surface"])

# Material settings
mat.blend_method = 'BLEND'
mat.use_backface_culling = False

# Assign to plane
plane.data.materials.clear()
plane.data.materials.append(mat)

# === ORIENT PLANE TO CAMERA ===
camera = next((obj for obj in bpy.data.objects if obj.type == 'CAMERA'), None)
if camera:
    direction = camera.location - plane.location
    rot_quat = direction.to_track_quat('-Z', 'Y')
    plane.rotation_euler = rot_quat.to_euler()

# === RENDER SETTINGS ===
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.samples = 50
scene.render.filepath = output_path

# === TRY TO USE GPU ===
prefs = bpy.context.preferences
if hasattr(prefs, "addons") and 'cycles' in prefs.addons:
    cprefs = prefs.addons['cycles'].preferences
    cprefs.compute_device_type = 'CUDA' if 'CUDA' in cprefs.get_device_types(bpy.context) else 'NONE'
    scene.cycles.device = 'GPU'
    for device in cprefs.devices:
        device.use = True

# === RENDER ===
bpy.ops.render.render(write_still=True)
print(f"✅ Render salvato in {output_path}")

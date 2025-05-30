import bpy
import mathutils
import os
import math


def setup_scene():
    bpy.context.scene.render.engine = "CYCLES"
    bpy.context.scene.world.use_nodes = True
    world_nodes = bpy.context.scene.world.node_tree.nodes
    background_node = world_nodes.get("Background")
    if not background_node:
        bpy.context.scene.world.node_tree.nodes.clear()
        background_node = world_nodes.new(type="ShaderNodeBackground")
        output_node = world_nodes.new(type="ShaderNodeOutputWorld")
        bpy.context.scene.world.node_tree.links.new(
            background_node.outputs["Background"], output_node.inputs["Surface"]
        )
    background_node.inputs[0].default_value = (0.8, 0.8, 0.8, 1)
    bpy.context.scene.cycles.film_transparent = False


def setup_camera():
    cam_data = bpy.data.cameras.new("Camera")
    cam_obj = bpy.data.objects.new("Camera", cam_data)
    bpy.context.scene.collection.objects.link(cam_obj)
    bpy.context.scene.camera = cam_obj
    cam_obj.location = mathutils.Vector((0, -7, 2))
    cam_obj.rotation_euler = mathutils.Euler((math.radians(75), 0, 0), "XYZ")
    cam_obj.data.lens = 35


def setup_light():
    light_data = bpy.data.lights.new(name="Light", type="SUN")
    light_data.energy = 5
    light_obj = bpy.data.objects.new(name="Light", object_data=light_data)
    bpy.context.scene.collection.objects.link(light_obj)
    light_obj.location = mathutils.Vector((2, -2, 5))
    light_obj.rotation_euler = mathutils.Euler(
        (math.radians(45), math.radians(-30), 0), "XYZ"
    )


def setup_background():
    pass


def load_and_position_image_manual(image_path, scene):
    if not os.path.exists(image_path):
        print(f"Error: Image not found at {image_path}")
        bpy.ops.wm.quit_blender()
        return None

    try:
        img = bpy.data.images.load(image_path, check_existing=True)
    except RuntimeError as e:
        print(f"Error loading image '{image_path}': {e}")
        bpy.ops.wm.quit_blender()
        return None

    print(f"Image '{img.name}' loaded with size {img.size[0]}x{img.size[1]}")

    if img.size[0] == 0 or img.size[1] == 0:
        print(f"Error: Image '{img.name}' has zero dimension.")
        bpy.data.images.remove(img)
        bpy.ops.wm.quit_blender()
        return None

    base_dimension = 5.0
    aspect_ratio = img.size[0] / img.size[1]

    if aspect_ratio >= 1:
        plane_width = base_dimension
        plane_height = base_dimension / aspect_ratio
    else:
        plane_height = base_dimension
        plane_width = base_dimension * aspect_ratio

    vertices = [
        (-plane_width / 2, -plane_height / 2, 0),
        (plane_width / 2, -plane_height / 2, 0),
        (plane_width / 2, plane_height / 2, 0),
        (-plane_width / 2, plane_height / 2, 0),
    ]
    faces = [[0, 1, 2, 3]]
    mesh_data = bpy.data.meshes.new("ImagePlane_mesh")
    mesh_data.from_pydata(vertices, [], faces)
    mesh_data.update()
    plane_obj = bpy.data.objects.new("ImagePlane", mesh_data)
    scene.collection.objects.link(plane_obj)

    mat = bpy.data.materials.new(name="ImageMaterial")
    mat.use_nodes = True
    plane_obj.data.materials.append(mat)
    nodes = mat.node_tree.nodes
    nodes.clear()

    shader_principled = nodes.new(type="ShaderNodeBsdfPrincipled")
    tex_coord = nodes.new(type="ShaderNodeTexCoord")
    tex_image = nodes.new(type="ShaderNodeTexImage")
    tex_image.image = img
    node_output = nodes.new(type="ShaderNodeOutputMaterial")

    shader_principled.location = (0, 0)
    tex_coord.location = (-400, 0)
    tex_image.location = (-200, 0)
    node_output.location = (200, 0)

    links = mat.node_tree.links
    links.new(tex_coord.outputs["UV"], tex_image.inputs["Vector"])
    links.new(tex_image.outputs["Color"], shader_principled.inputs["Base Color"])
    if img.depth >= 32:
        links.new(tex_image.outputs["Alpha"], shader_principled.inputs["Alpha"])
    links.new(shader_principled.outputs["BSDF"], node_output.inputs["Surface"])

    bpy.context.view_layer.objects.active = plane_obj
    if not plane_obj.data.uv_layers:
        plane_obj.data.uv_layers.new(name="UVMap")

    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.smart_project()
    bpy.ops.object.mode_set(mode="OBJECT")

    print(
        f"Manually created plane '{plane_obj.name}' with material '{mat.name}' for image '{img.name}'."
    )
    plane_obj.location = (0, 0, 0)
    plane_obj.rotation_euler = mathutils.Euler((math.radians(90), 0, 0), "XYZ")

    return plane_obj


def setup_shadow_catcher():
    bpy.ops.mesh.primitive_plane_add(
        size=10, enter_editmode=False, align="WORLD", location=(0, 0, -0.01)
    )
    ground_plane = bpy.context.active_object
    ground_plane.name = "ShadowCatcherPlane"
    ground_plane.is_shadow_catcher = True

    if not ground_plane.data.materials:
        mat = bpy.data.materials.new(name="ShadowCatcherMaterial")
        ground_plane.data.materials.append(mat)
    else:
        mat = ground_plane.data.materials[0]

    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    for node in list(nodes):
        nodes.remove(node)
    output_node = nodes.new(type="ShaderNodeOutputMaterial")
    transparent_bsdf = nodes.new(type="ShaderNodeBsdfTransparent")
    links.new(transparent_bsdf.outputs["BSDF"], output_node.inputs["Surface"])
    print("Shadow catcher plane created and configured (explicit material).")

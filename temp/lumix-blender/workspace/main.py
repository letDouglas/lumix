import argparse
import bpy
import sys
import os

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
import utils


def main():
    if "Cube" in bpy.data.objects:
        bpy.data.objects["Cube"].select_set(True)
        bpy.ops.object.delete()
    for obj_name in ["Light", "Camera"]:
        if obj_name in bpy.data.objects:
            bpy.data.objects[obj_name].select_set(True)
            bpy.ops.object.delete()

    argv = sys.argv
    if "--" in argv:
        argv = argv[argv.index("--") + 1 :]
    else:
        argv = []

    parser = argparse.ArgumentParser(description="Blender Rendering Pipeline")
    parser.add_argument(
        "--image_path",
        type=str,
        default="../../assets/car.jpg",
        help="Path to the input image",
    )
    parser.add_argument(
        "--output_path",
        type=str,
        default="output/final.png",
        help="Path to save the rendered image",
    )
    args = parser.parse_args(argv)

    absolute_output_path = os.path.abspath(args.output_path)
    output_dir = os.path.dirname(absolute_output_path)
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            print(f"Created output directory: {output_dir}")
        except OSError as e:
            print(f"Error creating output directory {output_dir}: {e}")
            bpy.ops.wm.quit_blender()
            return

    absolute_image_path = os.path.abspath(args.image_path)
    print(f"Attempting to load image from: {absolute_image_path}")

    utils.setup_scene()
    utils.setup_camera()
    utils.setup_light()
    utils.setup_background()

    image_plane_object = utils.load_and_position_image_manual(
        absolute_image_path, bpy.context.scene
    )

    if image_plane_object is None:
        print("Failed to load and position image. Exiting main function.")
        return

    bpy.context.scene.render.image_settings.file_format = "PNG"
    bpy.context.scene.render.filepath = absolute_output_path
    bpy.context.scene.render.film_transparent = True
    bpy.context.scene.cycles.samples = 64
    print(f"Set Cycles samples to: {bpy.context.scene.cycles.samples}")

    print(f"Starting render. Output will be: {absolute_output_path}")
    try:
        bpy.ops.render.render(write_still=True)
        print(f"Rendering complete. Image saved to {absolute_output_path}")
    except Exception as e:
        print(f"Error during rendering: {e}")

    bpy.ops.wm.quit_blender()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An unhandled error occurred in main: {e}")
        try:
            bpy.ops.wm.quit_blender()
        except:
            pass

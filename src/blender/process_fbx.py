import bpy
import sys
import os
import subprocess
import importlib

def ensure_dependencies():
    try:
        # Try to import numpy
        import numpy
    except ImportError:
        print("Installing required dependencies...")
        # Get Python executable path from Blender
        python_exe = sys.executable
        # Install numpy using pip
        subprocess.check_call([python_exe, "-m", "pip", "install", "numpy"])
        print("Dependencies installed successfully")

def main():
    try:
        # Ensure dependencies are installed
        ensure_dependencies()
        
        args = sys.argv[sys.argv.index("--") + 1:]
        input_path = args[0]
        output_path = args[1]

        # Clear scene
        bpy.ops.wm.read_factory_settings(use_empty=True)

        # Import FBX
        print(f"Importing {input_path}...")
        bpy.ops.import_scene.fbx(filepath=input_path)

        # Verify import
        if not bpy.data.objects:
            print("ERROR: No objects imported")
            return 1

        # Example processing - scale all objects
        print("Processing objects...")
        for obj in bpy.data.objects:
            obj.scale = (2.0, 2.0, 2.0)

        # Export FBX
        print(f"Exporting to {output_path}...")
        bpy.ops.export_scene.fbx(
            filepath=output_path,
            use_selection=False,
            bake_anim=False
        )

        print("Processing completed successfully")
        return 0

    except Exception as e:
        print(f"ERROR: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
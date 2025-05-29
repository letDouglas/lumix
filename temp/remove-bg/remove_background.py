import io

from PIL import Image
from rembg import remove

def remove_background(input_path, output_path):
    try:
        print(f"Opening image from: {input_path}")
        with open(input_path, 'rb') as input_file:
            input_data = input_file.read()

        print("Removing background...")
        output_data = remove(input_data)

        print(f"Saving background-free image to: {output_path}")
        with open(output_path, 'wb') as output_file:
            output_file.write(output_data)

        image = Image.open(io.BytesIO(output_data))
        image.show()

    except Exception as e:
        print(f"Error during execution: {e}")

if __name__ == "__main__":
    print("Starting execution")
    input_image = "./car.jpg"
    output_image = "./output_car.jpg"
    print(f"Input: {input_image}, Output: {output_image}")
    remove_background(input_image, output_image)
    print("Execution completed")

from PIL import Image

def overlay_car_on_background(car_image_path, background_image_path, output_path):
    car_image = Image.open(car_image_path).convert("RGBA")

    background_image = Image.open(background_image_path).convert("RGBA")

    new_width = 900
    aspect_ratio = car_image.height / car_image.width
    new_height = int(new_width * aspect_ratio)
    car_image = car_image.resize((new_width, new_height))

    background_width, background_height = background_image.size
    car_width, car_height = car_image.size
    x = (background_width - car_width) // 2
    y = (background_height - car_height) // 4

    background_image.paste(car_image, (x, y), car_image)

    background_image.save(output_path)

    background_image.show()

if __name__ == "__main__":
    car_image_path = "output_car.jpg"
    background_image_path = "background.jpg"
    output_path = "final_image.png"

    overlay_car_on_background(car_image_path, background_image_path, output_path)

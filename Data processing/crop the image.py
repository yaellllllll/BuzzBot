import os
from PIL import Image

def crop_images(input_folder):
    if not os.path.exists(input_folder):
        print("Input folder does not exist.")
        return

    for filename in os.listdir(input_folder):
        if filename.endswith(('.jpg', '.jpeg', '.png', '.bmp')):
            image_path = os.path.join(input_folder, filename)
            try:
                with Image.open(image_path) as img:
                    width, height = img.size
                    left = int(width * 0.08)  
                    top = int(height * 0.06)  
                    right = width - int(width * 0.20) 
                    bottom = height - int(height * 0.09)

                    cropped_img = img.crop((left, top, right, bottom))
                    cropped_img.save(image_path)
                    print(f"Processed: {filename}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")
        else:
            print(f"Skipping non-image file: {filename}")

input_folder = 'build the model/more_data/new_pics/no'
crop_images(input_folder)

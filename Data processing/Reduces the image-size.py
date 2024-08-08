import os
from PIL import Image


def resize_images(input_directory, output_directory, target_size=(224, 224)):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Loop through all files in the input directory
    for filename in os.listdir(input_directory):
        input_path = os.path.join(input_directory, filename)

        # Check if the file is an image
        try:
            with Image.open(input_path) as img:
                # Resize the image
                img_resized = img.resize(target_size)

                # Save the resized image to the output directory
                output_path = os.path.join(output_directory, filename)
                img_resized.save(output_path)

                print(f"Resized and saved: {filename}")
        except Exception as e:
            print(f"Error processing {filename}: {e}")


# Example usage
input_dir = 'build the model/data/pics/test/yes'
output_dir = 'build the model/data/for resnet50/test/yes'
resize_images(input_dir, output_dir)

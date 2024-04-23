import os
from PIL import Image, ImageOps

def resize_images_in_folder(input_folder, output_folder, new_size):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Loop through all files in the input folder
    for filename in os.listdir(input_folder):
        # Check if the file is an image
        if filename.endswith(('.png', '.jpg', '.jpeg', '.gif')):
            input_image_path = os.path.join(input_folder, filename)
            output_image_path = os.path.join(output_folder, filename)

            # Open and resize the image with cropping
            with Image.open(input_image_path) as img:
                # Resize and crop the image while maintaining aspect ratio
                resized_img = ImageOps.fit(img, new_size, method=Image.LANCZOS, bleed=0.0, centering=(0.5, 0.5))

                # Save the resized image
                resized_img.save(output_image_path)

                print(f"Image {filename} resized and cropped successfully to {new_size} pixels.")

# Example usage:
input_folder_path = "ResizeRequiredImages"
output_folder_path = "Images"
new_size = (216, 216)  # Set your desired size

resize_images_in_folder(input_folder_path, output_folder_path, new_size)

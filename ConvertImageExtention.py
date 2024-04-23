from PIL import Image
import os

def convert_to_png(input_dir, output_dir):
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # List all files in the input directory
    files = os.listdir(input_dir)

    for file_name in files:
        # Check if the file is an image
        if file_name.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            # Open the image
            image_path = os.path.join(input_dir, file_name)
            image = Image.open(image_path)

            # Convert the image to PNG format (replace alpha with white for transparency)
            converted_image = image.convert("RGBA")

            # Save the converted image to the output directory with the same name and PNG extension
            output_path = os.path.join(output_dir, os.path.splitext(file_name)[0] + '.png')
            converted_image.save(output_path, format='PNG')

            print(f'{file_name} converted to PNG.')

# Example usage
input_directory = 'converExtentionRequired'
output_directory = 'ResizeRequiredImages'

convert_to_png(input_directory, output_directory)

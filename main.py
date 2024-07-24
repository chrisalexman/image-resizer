'''
A basic script that takes in a .jpg file and crops it to the 4:3 aspect ratio.
It considers whitespace along the image border for what to remove when cropping.

INPUT:
- .jpg file in landscape orientation
- height range: between 709 and 777
- width range: 1023 or 1024

OUTPUT:
- .jpg file at the 4:3 aspect ratio
'''

import os
from PIL import Image


# resizes all images in the /input directory to the 4:3 aspect ratio
def resize_images():

    project_path = os.path.dirname(os.path.abspath(__file__))
    input_path = f'{project_path}\input'
    output_path = f'{project_path}\output'

    for image in os.listdir(input_path):

        image_path = f'{input_path}\{image}'

        if(image == '001.jpg'):

            img = Image.open(image_path)
            height, width = img.size

            print(f'{height} | {width}')

            resized = img.resize((width, int(height / 2)))
            # resized.save(f'{output_path}\{image}')


if __name__ == '__main__':
    resize_images()

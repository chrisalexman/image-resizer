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

            # 4:3 ratio || 1 / 1.33 = height / width
            #   height = width / 1.33
            #   width - 1.33 * height
            height_ratio = round(width / 1.33)

            # set height & width to 4:3 ratio based on smaller side
            if(height_ratio > height):
                width = round(1.33 * height)
            else:
                height = height_ratio

            print(f'{height} | {width}')


if __name__ == '__main__':
    resize_images()

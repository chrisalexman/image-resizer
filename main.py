'''
A basic script that takes in a .jpg file and crops it to the 4:3 aspect ratio.
It considers whitespace along the image border for what to remove when cropping.

INPUT:
- .jpg file in landscape orientation
- height range: between 709 and 777
- width range: 1023 or 1024

OUTPUT:
- .jpg file at the 4:3 aspect ratio

SOURCES:
- https://pillow.readthedocs.io/en/stable/reference/Image.html
- https://www.mathworks.com/help/images/image-coordinate-systems.html
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

        # consider image 001 for development
        if(image == '001.jpg'):

            img = Image.open(image_path)

            # width is up/down, height is left/right
            width, height = img.size
            print(f'w: {width} | h: {height}')

            # 4:3 ratio || 1 / 1.33 = width / height
            #   width = height / 1.33
            #   height = 1.33 * width
            width_ratio = round(height / 1.33)

            # set height & width to 4:3 ratio based on smaller side
            if(width_ratio > width):
                height_ratio = round(1.33 * width)
                width_ratio = width
            else:
                height_ratio = height

            
            '''

            cartesian pixel coordinate system:
                - top left is (0,0)
                - pixel indices are [y, x]

               (0,0) ___________ (x, 0)
                    |           |
                    |           |
                    |___________|
              (0, y)             (x, y)
            
            '''

            pixel_img = img.load()
            y = width - 1
            x = height - 1   

            left_side = [round(y / 2), 0]
            right_side = [round(y / 2), x]
            top_side = [0, round(x / 2)]
            bottom_side = [y, round(x / 2)]


if __name__ == '__main__':
    resize_images()

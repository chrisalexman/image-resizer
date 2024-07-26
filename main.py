'''
A basic script that takes in a .jpg file and crops it to the 4:3 aspect ratio.
It considers whitespace along the image border for what to remove when cropping.

INPUT:
- .jpg file
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

            # NOTE: images with landscape orientation will be rotated 90 degrees clockwise
            # width is left/right, height is up/down
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
            x = width - 1
            y = height - 1

            left_x, left_y = [0, round(y / 2)]
            right_x, right_y = [x, round(y / 2)]
            top_x, top_y = [round(x / 2), 0]
            bottom_x, bottom_y = [round(x / 2), y]

            threshold = (100, 100, 100)

            left_remove = 0
            right_remove = 0
            top_remove = 0
            bottom_remove = 0

            black_pixels = 0
            pixels_in_a_row = 3

            for num in range(round(height / 8)):
                color = pixel_img[left_x + num, left_y]
                if threshold > color:
                    black_pixels += 1
                    if black_pixels > pixels_in_a_row:
                        left_remove = num - pixels_in_a_row
                        break
                else:
                    black_pixels = 0
            black_pixels = 0

            for num in range(round(height / 8)):
                color = pixel_img[right_x - num, right_y]
                if threshold > color:
                    black_pixels += 1
                    if black_pixels > pixels_in_a_row:
                        right_remove = num - pixels_in_a_row
                        break
                else:
                    black_pixels = 0
            black_pixels = 0

            for num in range(round(width / 8)):
                color = pixel_img[top_x, top_y + num]
                if threshold > color:
                    black_pixels += 1
                    if black_pixels > pixels_in_a_row:
                        top_remove = num - pixels_in_a_row
                        break
                else:
                    black_pixels = 0
            black_pixels = 0

            for num in range(round(width / 8)):
                color = pixel_img[bottom_x, bottom_y - num]
                if threshold > color:
                    black_pixels += 1
                    if black_pixels > pixels_in_a_row:
                        bottom_remove = num - pixels_in_a_row
                        break
                else:
                    black_pixels = 0
            black_pixels = 0

            print(f'left: {left_remove}')
            print(f'right: {right_remove}')
            print(f'top: {top_remove}')
            print(f'bottom: {bottom_remove}')

            left = left_remove
            top = top_remove
            right = width - right_remove
            bottom = height - bottom_remove

            # width_remove = left_remove + right_remove
            # height_remove = top_remove + bottom_remove

            img = img.crop((left, top, right, bottom))
            img.save(f'{output_path}\{image}')


if __name__ == '__main__':
    resize_images()

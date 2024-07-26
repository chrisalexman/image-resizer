'''
A basic script that takes in a .jpg file and crops it closer to the 2.5 x 3.5 inch ratio of a trading card.
It considers whitespace along the image border for what to remove when cropping.

INPUT:
- .jpg file
- height range: between 709 and 777
- width range: 1023 or 1024

OUTPUT:
- .jpg file as close to the 2.5 x 3.5 inch ratio as possible

SOURCES:
- https://pillow.readthedocs.io/en/stable/reference/Image.html
- https://www.mathworks.com/help/images/image-coordinate-systems.html
'''

import os
from PIL import Image


# resizes all images in the /input directory to the 2.5 x 3.5 inch ratio
def resize_images():

    project_path = os.path.dirname(os.path.abspath(__file__))
    input_path = f'{project_path}\input'
    output_path = f'{project_path}\output'

    aspect_ratio = 1.4

    for image in os.listdir(input_path):

        image_path = f'{input_path}\{image}'

        with Image.open(image_path) as img:

            # NOTE: images with landscape orientation will be rotated 90 degrees clockwise
            # width is left/right, height is up/down
            width, height = img.size

            # e.g. 4:3 ratio || 1 / 1.33 = width / height
            #   width = height / 1.33
            #   height = 1.33 * width
            width_ratio = round(height / aspect_ratio)

            # set height & width to 1.4 ratio based on smaller side
            if(width_ratio > width):
                height_ratio = round(aspect_ratio * width)
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

            new_width = 0
            new_height = 0
            smallest_ratio = height / width
            candidate = []

            for l in range(left_remove + 1):
                for r in range(right_remove + 1):

                    new_width = width - l - r

                    for t in range(top_remove + 1):
                        for b in range(bottom_remove + 1):

                            new_height = height - b - t
                            new_ratio = new_height / new_width

                            if new_ratio < smallest_ratio and new_ratio >= aspect_ratio:
                                smallest_ratio = new_ratio
                                candidate = [l, r, t, b]

            if candidate:
                l, r, t, b = candidate
                new_width = width - l - r
                new_height = height - b - t

                left = l
                top = t
                right = width - r
                bottom = height - b

                ratio_before = height / width
                ratio_after = new_height / new_width

                img = img.crop((left, top, right, bottom))
                print(f'reduced {image} | {ratio_before:.4f} -> {ratio_after:.4f}')

            img.save(f'{output_path}\{image}')


if __name__ == '__main__':
    resize_images()

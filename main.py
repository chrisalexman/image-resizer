'''
A basic script that crops .jpg files to be as close as possible to the 1.4:1 aspect ratio of trading cards.
It considers whitespace along the image border for what to remove (this is a specific use case for my project).

INPUT
    - .jpg file
    - height range: between 709 and 777
    - width range: 1023 or 1024

OUTPUT
    - .jpg file as close to the 1.4:1 aspect ratio as possible

SOURCES
    - https://pillow.readthedocs.io/en/stable/reference/Image.html
    - https://www.mathworks.com/help/images/image-coordinate-systems.html
'''

import os
from PIL import Image


class ResizeImage:

    def __init__(self):

        # constants
        self.aspect_ratio = 1.4
        self.color_threshold = (100, 100, 100)
        self.pixels_in_a_row = 3

        # file paths
        self.project_path = os.path.dirname(os.path.abspath(__file__))
        self.input_path = f'{self.project_path}\input'
        self.output_path = f'{self.project_path}\output'
        self.output_file = f'{self.project_path}\output.txt'

        # file data
        self.image = None
        self.pixel_image = None

        # image data
        self.width = 0
        self.height = 0
        self.width_ratio = 0
        self.height_ratio = 0

        # image pixel data
        self.x = 0
        self.y = 0
        self.left_x = 0
        self.left_y = 0
        self.right_x = 0
        self.right_y = 0
        self.top_x = 0
        self.top_y = 0
        self.bottom_x = 0
        self.bottom_y = 0

        # image crop data
        self.left_remove = 0
        self.right_remove = 0
        self.top_remove = 0
        self.bottom_remove = 0
        self.new_width = 0
        self.new_height = 0
        self.current_ratio = 0
        self.candidate = []
    
    def set_ratios(self):
        """Set ratio of width or height based on aspect ratio.

        e.g. 2.5 x 3.5 ratio:  1 / 1.4 = width / height

        width = height / 1.4
        height = 1.4 * width
        """

        self.width_ratio = round(self.height / self.aspect_ratio)

        if(self.width_ratio > self.width):
            self.height_ratio = round(self.aspect_ratio * self.width)
            self.width_ratio = self.width
        else:
            self.height_ratio = self.height
    
    def find_left_pixels(self, pixel_range):
        """Find the number of pixels to remove from the left of the image."""

        black_pixels = 0
        for num in range(pixel_range):
            color = self.pixel_img[self.left_x + num, self.left_y]
            if self.color_threshold > color:
                black_pixels += 1
                if black_pixels > self.pixels_in_a_row:
                    self.left_remove = num - self.pixels_in_a_row
                    break
            else:
                black_pixels = 0

    def find_right_pixels(self, pixel_range):
        """Find the number of pixels to remove from the right of the image."""

        black_pixels = 0
        for num in range(pixel_range):
            color = self.pixel_img[self.right_x - num, self.right_y]
            if self.color_threshold > color:
                black_pixels += 1
                if black_pixels > self.pixels_in_a_row:
                    self.right_remove = num - self.pixels_in_a_row
                    break
            else:
                black_pixels = 0

    def find_top_pixels(self, pixel_range):
        """Find the number of pixels to remove from the top of the image."""

        black_pixels = 0
        for num in range(pixel_range):
            color = self.pixel_img[self.top_x, self.top_y + num]
            if self.color_threshold > color:
                black_pixels += 1
                if black_pixels > self.pixels_in_a_row:
                    self.top_remove = num - self.pixels_in_a_row
                    break
            else:
                black_pixels = 0

    def find_bottom_pixels(self, pixel_range):
        """Find the number of pixels to remove from the bottom of the image."""

        black_pixels = 0
        for num in range(pixel_range):
            color = self.pixel_img[self.bottom_x, self.bottom_y - num]
            if self.color_threshold > color:
                black_pixels += 1
                if black_pixels > self.pixels_in_a_row:
                    self.top_remove = num - self.pixels_in_a_row
                    break
            else:
                black_pixels = 0

    def loop_images(self):
        """Loop through .jpg images in the /input directory & crop them."""

        # clear the output file
        open(self.output_file, 'w').close()

        for self.image in os.listdir(self.input_path):

            image_path = f'{self.input_path}\{self.image}'
            self.crop_image(image_path)
    
    def crop_image(self, image_path):
        """Crop image as close to the aspect ratio as possible by removing surrounding whitespace.
        
        cartesian pixel coordinate system:
            (0,0)  ___________ (x, 0)
                  |           |
                  |           |
                  |___________|
            (0, y)             (x, y)
        """

        with Image.open(image_path) as img:

            self.width, self.height = img.size
            self.set_ratios()

            self.pixel_img = img.load()

            self.x = self.width - 1
            self.y = self.height - 1

            self.left_x, self.left_y = [0, round(self.y / 2)]
            self.right_x, self.right_y = [self.x, round(self.y / 2)]
            self.top_x, self.top_y = [round(self.x / 2), 0]
            self.bottom_x, self.bottom_y = [round(self.x / 2), self.y]

            self.find_left_pixels(round(self.height / 8))
            self.find_right_pixels(round(self.height / 8))
            self.find_top_pixels(round(self.width / 8))
            self.find_bottom_pixels(round(self.width / 8))

            self.current_ratio = self.height / self.width
            below_aspect_ratio = self.aspect_ratio > self.current_ratio

            self.candidate = []

            for l in range(self.left_remove + 1):
                for r in range(self.right_remove + 1):

                    self.new_width = self.width - l - r

                    for t in range(self.top_remove + 1):
                        for b in range(self.bottom_remove + 1):

                            self.new_height = self.height - b - t
                            new_ratio = self.new_height / self.new_width

                            if below_aspect_ratio:
                                if new_ratio > self.current_ratio and new_ratio <= self.aspect_ratio:
                                    self.current_ratio = new_ratio
                                    self.candidate = [l, r, t, b]
                            else:
                                if new_ratio < self.current_ratio and new_ratio >= self.aspect_ratio:
                                    self.current_ratio = new_ratio
                                    self.candidate = [l, r, t, b]
            
            self.save_image(img)

    def save_image(self, img):
        """Save image to a .jpg file in the /output directory, regardless of if it was cropped / not."""

        if self.candidate:

            l, r, t, b = self.candidate
            self.new_width = self.width - l - r
            self.new_height = self.height - b - t

            left = l
            top = t
            right = self.width - r
            bottom = self.height - b

            ratio_before = self.height / self.width
            ratio_after = self.new_height / self.new_width

            img = img.crop((left, top, right, bottom))

            output_line = f'changed {self.image} | {ratio_before:.4f} -> {ratio_after:.4f}\n'

            with open(self.output_file, 'a') as file:
                file.write(output_line)

        img.save(f'{self.output_path}\{self.image}')


if __name__ == '__main__':

    image = ResizeImage()
    image.loop_images()

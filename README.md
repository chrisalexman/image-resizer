# image-resizer

A basic script that takes in a .jpg file and crops it closer to the 2.5 x 3.5 inch ratio of a trading card.
It considers whitespace along the image border for what to remove when cropping.

### INPUT
- .jpg file
- height range: between 709 and 777
- width range: 1023 or 1024

### OUTPUT
- .jpg file as close to the 2.5 x 3.5 inch ratio as possible

### SOURCES:
- https://pillow.readthedocs.io/en/stable/reference/Image.html
- https://www.mathworks.com/help/images/image-coordinate-systems.html

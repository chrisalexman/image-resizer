# Image Resizer

A basic script that crops .jpg files to be as close as possible to the 1.4:1 aspect ratio of trading cards.
It considers whitespace along the image border for what to remove (this is a specific use case for my project).

## INPUT
- .jpg file
- height range: between 709 and 777
- width range: 1023 or 1024

## OUTPUT
- .jpg file as close to the 1.4:1 aspect ratio as possible

### SOURCES
- https://pillow.readthedocs.io/en/stable/reference/Image.html
- https://www.mathworks.com/help/images/image-coordinate-systems.html

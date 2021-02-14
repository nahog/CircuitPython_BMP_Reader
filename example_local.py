"""
This example opens an image with a BI_RGB file (wihtout length).
"""
from lib import bmp_reader

img = bmp_reader.BMPReader('image_0_length.bmp')

img.to_string()

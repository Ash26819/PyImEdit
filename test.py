import sys, os
from assets.objects.PyImEdit import PyImEdit

input_dir = "./assets/images/test/"
output_dir = "./assets/images/test/"
image_name = "bell2.png"
pyim = PyImEdit(input_dir, output_dir, image_name)

pyim.super_compose("space_pics", pixel_size=10)
pyim.show()

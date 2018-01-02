import sys, os
from assets.objects.PyImEdit import PyImEdit

input_dir = "./assets/images/test/"
output_dir = "./assets/images/test/"
image_name = "bell2.png"
pyim = PyImEdit()
pyim.set_input_dir(input_dir)
pyim.set_output_dir(output_dir)
pyim.load_image(image_name)

pyim.compose_from_palette("base_wire_colors")
pyim.show()

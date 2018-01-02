import sys, os
from assets.objects.PyImEdit import PyImEdit

RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
SILVER = (192,192,192)
YELLOW = (255,255,0)
BLACK = (0,0,0)
WHITE = (255,255,255)
CYAN = (0,255,255)


chainmaille_colors = [CYAN, RED, GREEN, BLUE, SILVER, YELLOW, BLACK, WHITE]


input_dir = "./assets/images/test/"
output_dir = "./assets/images/test/"
image_name = "bell2.png"
pyim = PyImEdit()
pyim.set_input_dir(input_dir)
pyim.set_output_dir(output_dir)
pyim.load_image(image_name)

pyim.make_from(chainmaille_colors)
pyim.show()

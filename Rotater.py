import sys, os
from assets.objects.PyImEdit import PyImEdit

input_dir = "./assets/images/test/"
output_dir = "./assets/images/test/rotate/"
image_name = "bell.png"
pyim = PyImEdit()
pyim.set_input_dir(input_dir)
pyim.set_output_dir(output_dir)
pyim.load_image(image_name)

"""
for i in range(360):
    pyim.rotate(degrees=i)
    save_name = "{}{}".format(pyim.get_image_name(), str(i).zfill(3))
    pyim.save(save_name)"""

pyim.flip()
pyim.show()

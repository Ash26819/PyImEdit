import sys, os
from assets.objects.PyImEdit import PyImEdit

input_dir = "./assets/images/banner_create/ello_banner/input/"
output_dir = "./assets/images/banner_create/ello_banner/output/"
im1_name = "ello_banner.png"
im2_name = "background.png"
im3_name = "bellmethod11.png"
im4_name = "LH_super_compose_akatsuki_fire50.png"

banner = PyImEdit(output_dir, output_dir, im1_name)
pyim2 = PyImEdit(input_dir, output_dir, im2_name)
pyim3 = PyImEdit(input_dir, output_dir, im3_name)
pyim4 = PyImEdit(input_dir, output_dir, im4_name)

im2 = pyim2.get_image()
im3 = pyim3.get_image()
im4 = pyim4.get_image()

banner.watermark(im3, xstart=(2560//4)*1)
banner.watermark(im4, xstart=(2560//4)*2)
banner.show()
save_name = "ello_banner2"
banner.save(save_name)

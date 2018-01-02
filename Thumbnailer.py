import os
from assets.objects.PyImEdit import PyImEdit

input_dir = "./assets/images/thumbnailer/images_to_apply_thumbnail/"
output_dir = "./assets/images/thumbnailer/output/"

flashdrive_colors = ["red", "green", "blue", "yellow", "megenta", "cyan","white", "black", "gray"]
thumbnails = ["top_rated_seller", "free_shipping"]
flashdrive = PyImEdit()
flashdrive.set_image_input_dir(input_dir)
flashdrive.set_image_output_dir(output_dir)

thumbnail_name = thumbnails[0]
for color in flashdrive_colors:
    flashdrive_name = "flashdrive_{}.png".format(color)
    flashdrive.load_image(flashdrive_name)
    flashdrive.apply_thumbnail((0,0), thumbnail_name)
    save_name = "{}_thumbnailed".format(flashdrive.get_image_name())
    flashdrive.save(save_name)


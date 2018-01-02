from assets.objects.PyImEdit import PyImEdit

pyim = PyImEdit()

palette = "minecraft_blocks"
profile = "rgb_mc1.12.2.png"

input_dir = "./assets/images/test/"
output_dir = "./assets/images/test/"
image_name = "bell.png"

pyim.set_input_dir(input_dir)
pyim.set_output_dir(output_dir)
pyim.load_image(image_name)

pyim.compose_image(palette=palette)
save_name = "{}_{}".format(pyim.get_image_name(), "palette_compose")
pyim.save(save_name)

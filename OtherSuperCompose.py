from assets.objects.PyImEdit import PyImEdit

input_dir = "./assets/images/super_compose/me/log_horizon/"
output_dir = "./assets/images/super_compose/me/output/"
palettes_dir = "./assets/images/super_compose/palettes/"
palette_name = "space_pics"

image_name = "akatsuki.png"
pyim = PyImEdit()
pyim.set_input_dir(input_dir)
pyim.set_output_dir(output_dir)
pyim.load_image(image_name)

save_name = "{}_{}".format(pyim.get_image_name(), "other_super_compose")
pyim.other_super_compose(palette_name)
pyim.save(save_name)


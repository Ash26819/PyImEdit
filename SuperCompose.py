from assets.objects.PyImEdit import PyImEdit

input_dir = "./assets/images/super_compose/taneka/"
output_dir = "./assets/images/super_compose/taneka/output/"
palettes_dir = "./assets/images/super_compose/palettes/"
palette_name = "taneka_family"
palette_pixel_size = 50
images = ["taneka1.png", "taneka2.png", "taneka3.png", "taneka4.png", "taneka5.png", "taneka6.png"]

pyim = PyImEdit()
pyim.set_input_dir(input_dir)
pyim.set_output_dir(output_dir)
pyim.load_image_palette(palette_name, palette_pixel_size=palette_pixel_size)

for image_name in images:
    pyim.load_image(image_name)
    pyim.super_compose(palette_pixel_size)
    save_name = "{}_{}".format(pyim.get_image_name(), "super_compose")
    pyim.save(save_name)


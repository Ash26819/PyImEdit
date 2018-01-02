from assets.objects.PyImEdit import PyImEdit

input_dir = "./assets/images/super_compose/me/output/"
output_dir = "./assets/images/super_compose/me/output/"

image_name = "LH_super_compose_shiroe50scale5.png"
save_name = "{}black_and_white".format(image_name)

pyim = PyImEdit()
pyim.set_input_dir(input_dir)
pyim.set_output_dir(output_dir)
pyim.load_image(image_name)
pyim.grayscale(method=0)

pyim.save(save_name)

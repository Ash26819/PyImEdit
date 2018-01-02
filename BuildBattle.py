from assets.objects.PyImEdit import PyImEdit

image_name = "bell.png"

edit = PyImEdit()
edit.load_image(image_name)
edit.show_loaded_image()
edit.factor_shrink(xfact=2, yfact=6)
edit.show_canvas()

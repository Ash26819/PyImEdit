import os
from PIL import Image
import csv

import assets.modules.PixelFunctions as PF
from assets.objects.PyImEdit import PyImEdit

class Palette():
    def __init__(self):
        pass

    def load_palette(self, palette_name):
        self.palette_dir = "./assets/database/palettes/"
        self.palette_name = palette_name
        palette_fp = "{}{}.csv".format(self.palette_dir, self.palette_name)
        palette = dict()
        with open(palette_fp, "r") as palette_file_obj:
            reader = csv.DictReader(palette_file_obj)
            for row in reader:
                palette_color = row["palette_color"]
                r = int(row["r"])
                g = int(row["g"])
                b = int(row["b"])
                pixel_value = (r,g,b)
                palette[palette_color] = pixel_value

        self.palette = palette

    def load_image_palette(self, palette_name, pixel_size):
        palette_dir = "./assets/images/super_compose/palettes/{}/".format(palette_name)
        palette_image_name_list = list(os.listdir(palette_dir))
        image_palette = dict()

        print("Loading palette")
        num_pics = len(palette_image_name_list)
        for image_name in palette_image_name_list:
            pyim = PyImEdit(input_dir=palette_dir, image_name=image_name)

            pixel_value = pyim.condense()
            pyim.resize(pixel_size, pixel_size)
            image = pyim.get_image()

            image_palette[pixel_value] = image

            print("{} of {} -> Image Loaded: {}".format(
                palette_image_name_list.index(image_name)+1, num_pics, pyim.get_image_name()))

        self.image_palette = image_palette

    def get_closest_image_to_pixel(self, target_pixel):
        best_difference = PF.difference((0,0,0), (255,255,255))
        best_image = None

        for pixel in self.image_palette.keys():
            test_difference = PF.difference(target_pixel, pixel)

            if test_difference <= best_difference:
                best_difference = test_difference
                best_image = self.image_palette[pixel]

        return best_image

    def get_color_value(self, color_name):
        return self.palette[color_name]

    def get_closest_color(self, target_pixel):
        best_difference = PF.difference((0,0,0), (255,255,255))
        best_color = None

        for color_name in self.palette.keys():
            palette_color_value = self.get_color_value(color_name)
            test_difference = PF.difference(target_pixel, palette_color_value)

            if test_difference <= best_difference:
                best_difference = test_difference
                best_color = color_name

        return best_color

from PIL import Image
import csv

import assets.modules.PixelFunctions as PF

class Palette():
    def __init__(self, palette_name=None):
        #palette_dir must be a directory
        #palette_name must not have a .csv file extension

        self.palette_dir = "./assets/database/palettes/"
        self.palette_name = palette_name
        return self.load_palette()

    def load_palette(self):
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

import sys, os
import math, random, csv
from PIL import Image

import assets.modules.PixelFunctions as PF
from assets.objects.Pixel import Pixel
from assets.objects.Palette import Palette
from assets.objects.Profile import Profile
from assets.objects.TimeReporter import TimeReporter

class PyImEdit: #TODO inherit from Image
    def __init__(self,
            input_dir=None, output_dir=None, image_name=None,
            palette_dir=None):

        self.set_image_input_dir(input_dir)
        self.set_image_output_dir(output_dir)
        self.load_image(image_name)

    def load_image(self, image_name):
        self.image_name = image_name[:-4] #don't include file extension in image_name
        self.image_fp = "{}{}".format(self.image_input_dir, image_name)
        image = Image.open(self.image_fp)
        self.init_vars(image)

    def init_vars(self, image):
        self.image = image
        self.xsize, self.ysize = image.size
        self.pix = image.load()

    def show_active_directories(self):
        print("Current input directory: {}".format(self.image_input_dir))
        print("Current output directory: {}".format(self.image_output_dir), end="\n\n")

    def set_image_input_dir(self, input_dir):
        self.image_input_dir = input_dir

    def set_image_output_dir(self, output_dir):
        self.image_output_dir = output_dir

    def set_palette_dir(self, palette_dir):
        self.palette_dir = palette_dir

    def get_pix(self):
        return self.pix

    def get_size(self):
        return self.image.size

    def get_image(self):
        return self.image

    def get_image_name(self):
        return self.image_name

    def show(self):
        self.image.show()

    def create_canvas(self, xsize, ysize):
        self.canvas = Image.new("RGB", (xsize, ysize), "black")
        self.canvas_pix = self.canvas.load()
        self.canvas_xsize, self.canvas_ysize = self.canvas.size

    def use_canvas(self):
        self.init_vars(self.canvas)

    def show_canvas(self):
        self.canvas.show()

    def save(self, save_name):
        save_fp = "{}{}.png".format(self.output_dir, save_name)
        self.image.save(save_fp)
        print("Image saved at {}".format(save_fp))

    def get_pixel_region(self, point, xsize, ysize):
        pixel_list = list()
        x, y = point
        for yi in range(ysize):
            for xi in range(xsize):
                pixel_list.append(self.pix[x+xi, y+yi])
        return pixel_list

    def crop(self, p1, p2):
        xstart, ystart = p1
        xend, yend = p2
        image = self.image.crop((xstart, ystart, xend, yend))
        self.init_vars(image)

    def resize(self, xsize, ysize):
        image = self.image.resize((xsize, ysize))
        self.init_vars(image)

    def apply_thumbnail(self, point, thumbnail_name):
        thumbnail_fp = "./assets/images/thumbnailer/thumbnails/{}.png".format(thumbnail_name)
        tn_xsize = int(self.xsize * 0.20)
        tn_ysize = int(self.ysize * 0.20)
        thumbnail_im = Image.open(tnfp).resize((tn_xsize, tn_ysize))
        tn_pix = thumbnail_im.load()

        x, y = point
        for yi in range(tn_ysize):
            for xi in range(tn_ysize):
                self.pix[xi+x, yi+y] = tn_pix[xi, yi]

    def compose_from_palette(self, palette_name):
        palette = Palette(palette_name)
        for yi in range(self.ysize):
            remaining_iters = self.ysize-yi
            time_reporter = TimeReporter()
            for xi in range(self.xsize):
                target_pixel = self.pix[xi, yi]
                color_name = palette.get_closest_color(target_pixel)
                color_value = palette.get_color_value(color_name)
                self.pix[xi, yi] = color_value
            time_reporter.report(remaining_iters)

    def compose_image_from_profile(self, profile_name):
        profile = Profile(profile_name)
        for yi in range(self.ysize):
            TimeReporter = TimeReporter()
            for xi in range(self.xsize):
                target_pixel = self.pix[xi, yi]
                closest_pixel = profile.look_up(target_pixel)
                self.pix[xi, yi] = closest_pixel

    def round_to(self, from_color, to_color):
        test_distance = self.pixel_distance((255,255,0), from_color)
        for yi in range(self.ysize):
            for xi in range(self.xsize):
                target_pix = self.pix[xi,yi]
                if self.pixel_distance(target_pix, from_color) < test_distance:
                    self.pix[xi, yi] = to_color

    def colorscale(self, method=None):
        for yi in range(self.ysize):
            for xi in range(self.xsize):
                pixel = self.pix[xi, yi][0:3]
                if (self.pixel_difference(pixel, (128,128,128)) <
                    self.pixel_difference(pixel, (0,0,128))):
                    new_pixel = ()
                gray_component = pixel[0]
                blue_component = pixel[2]

                pixel_canvas = [gray_component,gray_component,blue_component]
                new_pixel = tuple(pixel_canvas)
                self.pix[xi, yi] = new_pixel

    def grayscale(self, method=None):
        if method is None:
            return
        for yi in range(self.ysize):
            remaining_iters = self.ysize-yi
            TimeReporter = TimeReporter()
            for xi in range(self.xsize):
                pixel = Pixel(self.pix[xi,yi])
                pixel.convert_to_gray(method=method)
                gray_pixel = pixel.get_rgb()
                self.pix[xi, yi] = gray_pixel
            TimeReporter.report(remaining_iters)

    def sharpen(self, sensitivity=50, itersize=10):
        xsize = self.xsize//itersize * itersize
        ysize = self.ysize//itersize * itersize
        self.resize(xsize, ysize)
        for yii in range(0, self.ysize, itersize):
            remaining_iters = self.ysize-yii
            TimeReporter = TimeReporter()
            for xii in range(0, self.xsize, itersize):
                for yi in range(itersize):
                    for xi in range(itersize):
                        #choose random pixel in itersize range to sharpen to
                        rx = random.randrange(itersize)
                        ry = random.randrange(itersize)
                        target_pix = self.pix[xii+rx, yii+ry]
                        current_pix = self.pix[xii+xi, yii+yi]
                        if PF.distance(target_pix, current_pix) <= sensitivity:
                            self.pix[xii+xi, yii+yi] = target_pix
            TimeReporter.report(remaining_iters)

    def make_from(self, color_list):
        for xi in range(self.xsize):
            for yi in range(self.ysize):
                target_pixel = self.pix[xi, yi]
                closest_pixel = self.get_closest_pixel(target_pixel, color_list)
                self.pix[xi, yi] = closest_pixel

    def super_compose(self, palette_name, pixel_size, scale=10):
        print("Super composing image: {}".format(self.image_name))
        step = pixel_size//scale
        xsize = self.xsize//step*step
        ysize = self.ysize//step*step
        self.resize(xsize, ysize)
        canvas_xsize, canvas_ysize = self.xsize*scale, self.ysize*scale
        self.create_canvas(canvas_xsize, canvas_ysize)

        palette = Palette()
        image_palette = palette.load_image_palette(palette_name, pixel_size)
        for yi in range(0, self.ysize, step):
            remaining_iters = (self.ysize-yi)//step
            time_reporter = TimeReporter()
            for xi in range(0, self.xsize, step):
                pixel_region = self.get_pixel_region((xi, yi), step, step)
                target_pixel = self.average_pixels(pixel_region)
                pixel_image = palette.get_closest_image_to_pixel(target_pixel)
                pixel_image_pix = pixel_image.load()
                for yci in range(pixel_size):
                    for xci in range(pixel_size):
                        xc = xi*scale + xci
                        yc = yi*scale + yci
                        self.canvas_pix[xc,yc] = pixel_image_pix[xci, yci]
            time_reporter.report(remaining_iters)
        self.use_canvas()

    def ripple(self, pyim2, x=None, y=None, wavelength=90):
        other_im = pyim2.get_image()
        other_pix = other_im.load()
        if x is None:
            x = self.xsize//2
        if y is None:
            y = self.ysize//2

        for yi in range(self.ysize):
            time_reporter = TimeReporter()
            remaining_iters = self.ysize-yi
            for xi in range(self.xsize):
                dist = ( (xi-x)**2 + (yi-y)**2 )**0.5
                alpha = 0.5 * math.sin((2*math.pi)/wavelength*dist) + 0.5
                this_alpha_pixel  = [int(component*alpha) for component in self.pix[xi, yi]]
                other_alpha_pixel = [int(component*(1-alpha)) for component in other_pix[xi, yi]]
                alpha_pixel = tuple(a1c+a2c for a1c, a2c in zip(this_alpha_pixel, other_alpha_pixel))
                self.pix[xi, yi] = alpha_pixel
            time_reporter.report(remaining_iters)

    def rotate(self, degrees=None):
        rads = (math.pi/180)*degrees
        xsize = int(self.xsize)
        ysize = int(self.ysize*math.cos(rads))
        if abs(ysize) < 1.0:
            ysize = 1
            self.flip()
        print(ysize, degrees)
        self.create_canvas(xsize, ysize)
        self.resize(xsize, ysize)

    def chainmaille_pattern(self):
        bg_color = (255,255,255)
        ring_color = (0,0,255)
        pattern = "e4-1"


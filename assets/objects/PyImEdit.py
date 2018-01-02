import sys, os
import math, random, csv
from PIL import Image

from assets.objects.Pixel import Pixel
from assets.objects.Palette import Palette
from assets.objects.Profile import Profile
from assets.objects.TimeReporter import TimeReporter

class PyImEdit():
    def __init__(self):
        self.input_dir = None
        self.output_dir = None
        self.database_dir = None

    def show_active_directories(self):
        print("Current input directory: {}".format(self.input_dir))
        print("Current output directory: {}".format(self.output_dir), end="\n\n")

    def set_input_dir(self, input_dir):
        self.input_dir = input_dir

    def set_output_dir(self, output_dir):
        self.output_dir = output_dir

    def get_pix(self):
        return self.pix

    def get_size(self):
        return self.image.size

    def get_image(self):
        return self.image

    def get_image_name(self):
        return self.image_name

    #############################################################
    #DAO Functions###############################################
    #############################################################

    def load_palette(self, palette_name):
        palette_dir = "./assets/database/palettes/"
        palette_fp = "{}{}.csv".format(palette_dir, palette_name)
        palette = dict()
        with open(palette_fp, "r") as palette_file:
            reader = csv.DictReader(palette_file)
            for row in reader:
                block_name = row["block_name"]
                r,g,b = int(row["r"]), int(row["g"]), int(row["b"])
                pixel_value = r,g,b
                palette[block_name] = pixel_value

        self.palette = palette

    def init_vars(self, image):
        self.image = image
        self.xsize, self.ysize = image.size
        self.pix = image.load()

    def load_image(self, image_name):
        self.image_name = image_name[:-4]
        fp = "{}{}".format(self.input_dir, image_name)
        image = Image.open(fp)
        self.init_vars(image)

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
    #######################################################################
    #End DAO Functions#####################################################
    #######################################################################

    #Helper functions#
    @staticmethod
    def pixel_distance(pixel1, pixel2):
        """Use when I need the actual distance between pixels"""
        r1, g1, b1 = pixel1[:3]
        r2, g2, b2 = pixel2[:3]
        distance = ((r2-r1)**2 + (g2-g1)**2 + (b2-b1)**2)**0.5
        return distance

    @staticmethod
    def pixel_difference(pixel1, pixel2):
        """Use when I'm searching for the closest value in a list"""
        r1, g1, b1 = pixel1[:3]
        r2, g2, b2 = pixel2[:3]
        difference = (r2-r1)**2 + (g2-g1)**2 + (b2-b1)**2
        return difference

    def get_closest_pixel(self, target_pixel, pixel_list):
        best_difference = self.pixel_difference((0,0,0), (255,255,255))
        best_pixel = None

        for test_pixel in pixel_list:
            test_difference = self.pixel_difference(target_pixel, test_pixel)

            if test_difference < best_difference:
                best_difference = test_difference
                best_pixel = test_pixel

        return best_pixel

    def get_closest_palette_color(self, target_pixel, palette):
        best_difference = self.pixel_difference((0,0,0), (255,255,255))
        best_color = None

        for color_name in palette.keys():
            test_pixel = palette[color_name]
            test_difference = self.pixel_difference(target_pixel, test_pixel)
            if test_difference < best_difference:
                best_difference = test_difference
                best_color = color_name

        return best_color

    def condense(self):
        """calculate average value of pixels in this image"""
        rt, gt, bt = 0,0,0
        for yi in range(self.ysize):
            for xi in range(self.xsize):
                ri, gi, bi, = self.pix[xi, yi][:3]
                rt += ri
                gt += gi
                bt += bi
        num_pixels = self.xsize*self.ysize
        r = rt//num_pixels
        g = gt//num_pixels
        b = bt//num_pixels
        return r,g,b

    @staticmethod
    def average_pixels(pixel_list):
        rt,gt,bt = 0,0,0
        for pixel in pixel_list:
            ri, gi, bi = pixel[:3]
            rt += ri
            gt += gi
            bt += bi
        num_pixels = len(pixel_list)
        r = rt//num_pixels
        g = gt//num_pixels
        b = bt//num_pixels
        return r,g,b

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

########################################################

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

    def compose_image_from_palette(self, palette_name):
        pass

    def compose_image_from_profile(self, profile_name):
        profile = Profile()
        profile.load_profile(profile_name)
        for yi in range(self.ysize):
            for xi in range(self.xsize):
                target_pixel = self.pix[xi, yi]
                closest_pixel = profile.look_up(target_pixel)
                self.pix[xi, yi] = closest_pixel

    def compose_image(self, profile=None, palette=None):
        if profile:
            self.compose_image_from_profile(profile)
        elif palette:
            self.compose_image_from_palette(palette)

    def compose_image_from_palette(self, palette_name):
        self.load_palette(palette_name)
        for yi in range(self.ysize):
            remaining_iters = self.ysize - yi
            start = time.time()
            for xi in range(self.xsize):
                target_pixel = self.pix[xi, yi]
                closest_color_name = self.get_closest_palette_color(target_pixel, self.palette)
                closest_pixel = self.palette[closest_color_name]
                self.pix[xi, yi] = closest_pixel
            end = time.time()
            iter_time = end-start
            print("Remaining iterations: {}, Iteration Time: {:.2f}, ETC: {:.2f}".format(
                remaining_iters, iter_time, remaining_iters*iter_time))

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
            print(self.ysize-yi)
            for xi in range(self.xsize):
                pixel = Pixel(self.pix[xi,yi])
                pixel.convert_to_gray(method=method)
                gray_pixel = pixel.get_rgb()
                self.pix[xi, yi] = gray_pixel

    def sharpen(self, sensitivity=50, itersize=10):
        #must first crop image so that edges are accounted for
        xstart = 0
        ystart = 0
        xend = self.xsize//itersize * itersize
        yend = self.ysize//itersize * itersize
        self.crop(xstart, ystart, xend, yend) #TODO should resize here isntead
        for yii in range(0, self.ysize, itersize):
            print(self.ysize-yii)
            for xii in range(0, self.xsize, itersize):
                for yi in range(itersize):
                    for xi in range(itersize):
                        rx = random.randrange(itersize)
                        ry = random.randrange(itersize)
                        target_pix = self.pix[xii+rx, yii+ry]
                        current_pix = self.pix[xii+xi, yii+yi]
                        if self.pixel_distance(target_pix, current_pix) <= sensitivity:
                            self.pix[xii+xi, yii+yi] = target_pix

    def load_image_palette(self, palette_name, palette_pixel_size):
        palette_dir = "./assets/images/super_compose/palettes/{}/".format(palette_name)
        palette_image_name_list = list(os.listdir(palette_dir))
        palette_image_list = list()
        palette_image_pixel_value_list = list()

        print("Loading palette")
        num_pics = len(palette_image_name_list)
        for image_name in palette_image_name_list:
            fp = "{}{}".format(palette_dir, image_name)
            pyim = PyImEdit()
            pyim.set_input_dir(palette_dir)
            pyim.load_image(image_name)
            pyim.resize(palette_pixel_size, palette_pixel_size)

            pixel_value = pyim.condense()
            image = pyim.get_image()
            palette_image_pixel_value_list.append(pixel_value)
            palette_image_list.append(image)
            print("{} of {} -> Image loaded: {}".format(
                palette_image_name_list.index(image_name)+1, num_pics, pyim.get_image_name()))

        self.palette_image_list = palette_image_list
        self.palette_image_pixel_value_list = palette_image_pixel_value_list

    @staticmethod
    def flatten(image):
        pix = image.load()
        xsize, ysize = image.size
        flat_pix = [pix[xi, yi] for yi in range(ysize) for xi in range(xsize)]
        return flat_pix

    def get_closest_image_to_region(self, target_region, image_list):
        image_region_list = [self.flatten(image) for image in image_list]
        distance_list = [self.pixel_list_distance(target_region, test_region)
                for test_region in image_region_list]
        min_distance_index = distance_list.index(min(distance_list))
        return image_list[min_distance_index]

    def pixel_list_distance(self, pixels1, pixels2):
        assert len(pixels1) == len(pixels2)
        distance_sum = 0
        num_pixels = len(pixels1)
        for i in range(num_pixels):
            pix1 = pixels1[i]
            pix2 = pixels2[i]
            distance_sum += self.pixel_distance(pix1, pix2)
        return distance_sum

    def other_super_compose(self, palette_name, palette_pixel_size=40):
        palette_image_list, palette_image_pixel_value_list = self.load_image_palette(palette_name, palette_pixel_size)
        self.create_canvas(self.xsize, self.ysize)

        step = palette_pixel_size
        for yi in range(0, self.ysize, step):
            remaining_iters = (self.ysize-yi)//step
            time_reporter = TimeReporter()
            for xi in range(0, self.xsize, step):
                target_region = self.get_pixel_region((xi, yi), step, step)
                closest_im = self.get_closest_image_to_region(target_region, palette_image_list)
                closest_im_pix = closest_im.load()
                for cyi in range(palette_pixel_size):
                    for cxi in range(palette_pixel_size):
                        self.canvas_pix[xi+cxi, yi+cyi] = closest_im_pix[cxi, cyi]
            time_reporter.report(remaining_iters)
        self.use_canvas()

    def make_from(self, color_list):
        for xi in range(self.xsize):
            for yi in range(self.ysize):
                target_pixel = self.pix[xi, yi]
                closest_pixel = self.get_closest_pixel(target_pixel, color_list)
                self.pix[xi, yi] = closest_pixel

    def super_compose(self, palette_pixel_size):
        print("Super composing image: {}".format(self.image_name))
        scale = 10
        step = palette_pixel_size//scale
        xsize = self.xsize//step*step
        ysize = self.ysize//step*step
        self.resize(xsize, ysize)
        canvas_xsize, canvas_ysize = self.xsize*scale, self.ysize*scale
        self.create_canvas(canvas_xsize, canvas_ysize)

        #TODO Iterate over canvas isntead of self.im?

        for yi in range(0, self.ysize, step):
            remaining_iters = (self.ysize-yi)//step
            time_reporter = TimeReporter()
            for xi in range(0, self.xsize, step):
                pixel_region = self.get_pixel_region((xi, yi), step, step)
                target_pixel = self.average_pixels(pixel_region)
                #target_pixel = self.pix[xi, yi]
                best_pixel = self.get_closest_pixel(target_pixel, self.palette_image_pixel_value_list)
                pixel_image = self.palette_image_list[self.palette_image_pixel_value_list.index(best_pixel)]
                pixel_image_pix = pixel_image.load()
                for yci in range(palette_pixel_size):
                    for xci in range(palette_pixel_size):
                        xc = xi*scale + xci
                        yc = yi*scale + yci
                        self.canvas_pix[xc,yc] = pixel_image_pix[xci, yci]
            time_reporter.report(remaining_iters)
        self.use_canvas()

    def ripple(self, pyim2, x=None, y=None, wavelength=90):
        other_im = pyim2.get_image()
        other_pix = other_im.load()
        if x is None or y is None:
            x,y = self.xsize//2, self.ysize//2

        start = time.time()
        for yi in range(self.ysize):
            for xi in range(self.xsize):
                dist = ( (xi-x)**2 + (yi-y)**2 )**0.5
                alpha = 0.5 * math.sin((2*math.pi)/wavelength*dist) + 0.5
                this_alpha_pixel  = [int(c*alpha) for c in  self.pix[xi, yi]]
                other_alpha_pixel = [int(c*(1-alpha)) for c in other_pix[xi, yi]]
                alpha_pixel = tuple(a1c+a2c for a1c, a2c in zip(this_alpha_pixel, other_alpha_pixel))
                self.pix[xi, yi] = alpha_pixel
        end = time.time()
        print(end-start)

    def flip(self):
        self.create_canvas(self.xsize, self.ysize)
        for yi in range(self.ysize):
            for xi in range(self.xsize):
                self.pix[xi,yi] = self.pix[xi, self.ysize-yi-1]

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


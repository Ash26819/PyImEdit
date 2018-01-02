import random

class Pixel():
    red = 0
    green = 1
    blue = 2

    def __init__(self, pixel_value):
        self.red, self.green, self.blue = pixel_value[0:3]

    def get_rgb(self):
        return self.red, self.green, self.blue

    def get_red(self):
        return self.red

    def get_green(self):
        return self.green

    def get_blue(self):
        return self.blue

    def set_red(self, red):
        self.red = red

    def set_green(self, green):
        self.green = green

    def set_blue(self, blue):
        self.blue = blue

    def average(self, *components):
        total = 0
        if "red" in components:
            total += self.red
        if "green" in components:
            total += self.green
        if "blue" in components:
            total += self.blue
        return total//len(components)

    def get_most_potent_color_component(self):
        return max[self.red, self.green, self.blue]

    def get_least_potent_color_component(self):
        return min[self.red, self.green, self.blue]

    def get_middle_potent_value_color_component(self):
        pixel = list(self.get_rgb())
        pixel.remove(min(pixel))
        pixel.remove(max(pixel))
        return pixel[0]

    def convert_to_gray(self, method=None):
        num_methods = 12
        if method == 12:
            method = random.randrange(num_methods) + 1
        if method == 1:
            gray_value = self.red
        elif method == 2:
            gray_value = self.green
        elif method == 3:
            gray_value = self.blue
        elif method == 4:
            gray_value = self.average("red", "green", "blue")
        elif method == 5:
            gray_value = self.average("red", "green")
        elif method == 6:
            gray_value = self.average("green", "blue")
        elif method == 7:
            gray_value = self.average("red", "blue")
        elif method == 8:
            gray_value = self.get_most_potent_color_component()
        elif method == 9:
            gray_value = self.get_least_potent_color_component()
        elif method == 10:
            gray_value = self.get_middle_potent_value_color_component()
        elif method == 11:
            gray_value = random.choice(self.get_rgb())

        self.set_red(gray_value)
        self.set_green(gray_value)
        self.set_blue(gray_value)



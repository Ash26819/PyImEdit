from PIL import Image

class Profile():
    def __init__(self):
        self.profile_dir = "./assets/database/profiles/"

    def set_profile_dir(self, profile_dir):
        self.profile_dir = profile_dir

    def get_profile_dir(self):
        return self.profile_dir

    def load_profile(self, profile_name):
        self.profile_name = profile_name
        profile_fp = "{}{}".format(self.profile_dir, profile_name)
        profile_im = Image.open(profile_fp)

        self.profile_im = profile_im
        self.profile_pix = self.profile_im.load()

    @staticmethod
    def rgb_to_xy(pixel):
        r,g,b = pixel[:3]
        size = 4096 #sqrt(256**3)
        flat_pos = r*256**2 + g*256**1 + b*256**0

        x = flat_pos%size
        y = flat_pos//size
        return x,y

    def look_up(self, target_pixel):
        x, y = self.rgb_to_xy(target_pixel)
        best_pixel = self.profile_pix[x,y]
        return best_pixel

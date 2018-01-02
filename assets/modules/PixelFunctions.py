def difference(pixel1, pixel2):
    r1, g1, b1 = pixel1[0:3]
    r2, g2, b2 = pixel2[0:3]
    difference = (r2-r1)**2 + (g2-g1)**2 + (b2-b1)**2
    return difference

def distance(pixel1, pixel2):
    return difference(pixel1, pixel2)**0.5

def get_closest_pixel(target_pixel, pixel_list):
    best_difference = difference((0,0,0), (255,255,255))
    best_pixel = None

    for test_pixel in pixel_list:
        test_difference = difference(target_pixel, test_pixel)
        if test_difference <= best_difference:
            best_difference = test_difference
            best_pixel = test_pixel

    return best_pixel

def average_pixels(pixel_list):
    rt, gt, bt = 0,0,0
    for pixel in pixel_list:
        ri, gi, bi = pixel[0:3]
        rt += ri
        gt += gi
        bt += bi
    num_pixels = len(pixel_list)
    r = rt//num_pixels
    g = gt//num_pixels
    b = bt//num_pixels
    return r,g,b

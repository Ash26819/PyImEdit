def get_pixel_value(image):
    rt, gt, bt = 0,0,0
    xsize, ysize = image.size
    pix = image.load()
    for yi in range(ysize):
        for xi in range(xsize):
            ri, gi, bi = pix[xi, yi][0:3]
            rt += ri
            gt += gi
            bt += bi
    num_pixels = xsize*ysize
    r = rt//num_pixels
    g = gt//num_pixels
    b = bt//num_pixels
    return r,g,b



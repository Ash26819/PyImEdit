import os
import csv
from assets.objects.PyImEdit import PyImEdit

input_dir = "./assets/images/blocks/screenshots_cropped/"
image_name_list = os.listdir(input_dir)
pyim = PyImEdit()
pyim.set_input_dir(input_dir)

with open("./assets/database/minecraft_blocks.csv", "w", newline="") as csvfile:
    fieldnames = ["block_name", "r", "g", "b", "block_id", "block_data"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for image_name in image_name_list:
        pyim.load_image(image_name)
        image_name = pyim.get_image_name() #Don't want to have .png file extension
        r,g,b = pyim.condense()
        block_name, block_information = image_name.split("-")
        block_id, block_data = block_information.split("~")
        entry = {"block_name": block_name,
                 "r": r, "g": g, "b": b,
                 "block_id": block_id, "block_data": block_data}
        writer.writerow(entry)

import csv

with open("minecraft_palette.csv", "r") as csvfile:
    reader = csv.DictReader(csvfile)

    pixel_value_list = list()
    for row in reader:
        r = int(row["r"])
        g = int(row["g"])
        b = int(row["g"])
        name = row["block_name"]
        pixel = (r,g,b)
        pixel_value_list.append(pixel)


index_list = list()
for target_pixel in pixel_value_list:
    indices = [(target_pixel, i) for i,test_pixel in enumerate(pixel_value_list) if test_pixel==target_pixel]
    index_list.append(indices)

for x in index_list:
    print(x)


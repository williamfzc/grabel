from grabel import Grabel
import cv2
import json
import os


file_name = "r.json"
if not os.path.isfile(file_name):
    with open(file_name, "w+") as f:
        f.write("[]")

with open(file_name) as f:
    json_list = json.load(f)

# init your android device
grab = Grabel("123456")
png_id = 1
png_name = f"{png_id}.png"

# a tree view
tree = grab.get_tree()
# and a screen shot
screen = grab.get_screen_array()
cv2.imwrite(png_name, screen)
h, w, _ = screen.shape

# flexible filter for different widgets, to get whatever you want
node_list = grab.node_filter(tree, {"@class": "android.widget.ImageView"})

h, w = int(h), int(w)

final = dict()
final["file_name"] = png_name
final["image_id"] = png_id
final["height"] = h
final["width"] = w
final["annotations"] = []

for each in node_list:
    each_dict = dict()
    top_left, bottom_right = grab.get_node_location(each)
    each_dict["bbox"] = [int(i) for i in [*top_left, *bottom_right]]
    # todo: when using this data, you need to set it to `BoxMode.XYXY_ABS`
    # from detectron2.structures import BoxMode
    each_dict["bbox_mode"] = None
    each_dict["category_id"] = 0
    each_dict["iscrowd"] = 0
    each_dict["segmentation"] = []
    each_dict["area"] = h * w
    final["annotations"].append(each_dict)

json_list.append(final)
with open("r.json", "w+") as f:
    json.dump(json_list, f)

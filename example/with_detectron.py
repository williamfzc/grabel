from grabel import Grabel
import cv2
import pprint

# init your android device
grab = Grabel("12345F")
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

final = []
for each in node_list:
    each_result = dict()

    annotations = dict()
    top_left, bottom_right = grab.get_node_location(each)
    annotations["bbox"] = [*top_left, *bottom_right]
    # todo: when using this data, you need to set it to `BoxMode.XYXY_ABS`
    # from detectron2.structures import BoxMode
    annotations["bbox_mode"] = None
    annotations["category_id"] = 0
    annotations["iscrowd"] = 0
    annotations["segmentation"] = []
    each_result["annotations"] = annotations

    each_result["file_name"] = png_name
    each_result["height"] = h
    each_result["image_id"] = png_id
    each_result["widget"] = w

    final.append(each_result)

pprint.pprint(final)

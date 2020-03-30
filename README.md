# grabel

grab label!

## goal

This repo was designed for quickly grabbing icons (or something like ImageView/TextView, etc.), as pictures, from Android screen.

I have used this repo to collect image data for training models.

## usage

It's really lightweight but effective because of its powerful dependencies.

```python
from grabel import Grabel
import cv2


# init your android device
grab = Grabel("123456F")
# a tree view
tree = grab.get_tree()
# and a screen shot
screen = grab.get_screen_array()

# flexible filter for different widgets, to get whatever you want
node_list = grab.node_filter(tree, {"@class": "android.widget.ImageView"})

# and, crop them out from screen
for i, each in enumerate(node_list):
    
    # get their locations
    location = grab.get_node_location(each)
    
    # and crop
    sub = grab.crop(screen, location[0], location[1])
    
    # sub is a np.ndarray
    # you can save it as a file
    cv2.imwrite(f"{i}.png", sub)
```

## example

This is my screen:

![temp.png](https://i.loli.net/2020/03/31/yVHfW19chNu8iRq.jpg)

and get all the ImageView from it:

![1.png](https://i.loli.net/2020/03/31/a8vrCF1SZPTh5LR.png)

## license

[MIT](LICENSE)

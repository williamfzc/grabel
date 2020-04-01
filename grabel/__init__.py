"""
MIT License
Copyright (c) 2020 williamfzc
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from fastcap import MNCDevice
from minadb import ADBDevice
import xmltodict
import typing
import re
import os
import numpy as np
import cv2
from planter import Tree, Node, Compiler

__PROJECT_NAME__ = r"grabel"
__AUTHOR__ = r"williamfzc"
__AUTHOR_EMAIL__ = r"fengzc@vip.qq.com"
__LICENSE__ = r"MIT"
__URL__ = r"https://github.com/williamfzc/grabel"
__VERSION__ = r"0.1.1"
__DESCRIPTION__ = r"grab label!"


class Grabel(object):
    def __init__(self, serial_no: str):
        self.serial_no = serial_no
        self.mnc = MNCDevice(serial_no)
        self.adb = ADBDevice(serial_no)

    def get_tree(self) -> Tree:
        raw_xml = self.adb.dump_ui()
        xml_dict = xmltodict.parse(raw_xml, encoding="utf-8")

        c = Compiler()
        return c.compile2tree(xml_dict)

    def get_screen_array(self) -> np.ndarray:
        temp = "temp.png"
        self.mnc.screen_shot()
        self.mnc.export_screen(temp)
        obj = cv2.imread(temp)
        # remove temp file
        os.remove(temp)
        return obj

    @staticmethod
    def node_filter(tree: Tree, rules: dict) -> typing.List[Node]:
        result = list()
        for each in tree.loop_from_root():
            # custom filter
            for k, v in rules.items():
                if not hasattr(each, k):
                    continue
                if getattr(each, k) != v:
                    continue
                result.append(each)
        return result

    @staticmethod
    def get_node_location(node: Node) -> typing.Tuple:
        location_str = getattr(node, "@bounds")
        return tuple(re.findall(r"\[(.*?),(.*?)\]", location_str))

    @staticmethod
    def crop(
        origin: np.ndarray, left_top: typing.Sequence, right_bottom: typing.Sequence
    ) -> np.ndarray:
        return origin[
            int(left_top[1]) : int(right_bottom[1]),
            int(left_top[0]) : int(right_bottom[0]),
        ]

    def dump_csv(self, pic_name: str, node_list: typing.List[Node], type_: str) -> typing.List[str]:
        lines = list()
        for each in node_list:
            location = self.get_node_location(each)
            line = ",".join([pic_name, *location[0], *location[1], type_])
            lines.append(line)
        return lines

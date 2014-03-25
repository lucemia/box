import inspyred
from random import Random
from time import time

def check_all_boxes_ok(container, boxes):
    """
        確認所有貨物沒有設定錯誤, 不考慮平衡問題
    """
    space = set()

    for box in boxes:
        # 確認貨物是在貨櫃的範圍內
        if not (box.x >= 0 and (box.width + box.x) <= container.width and box.width > 0):
            return False
        if not (box.y >= 0 and (box.height + box.y) <= container.height and box.height > 0):
            return False
        if not (box.z >= 0 and (box.depth + box.z) <= container.depth and box.depth > 0):
            return False

        # 確認貨物沒有互相碰撞
        for x in range(box.x, box.x + box.width):
            for y in range(box.y, box.y + box.height):
                for z in range(box.z, box.z + box.depth):
                    if (x, y, z) in space:
                        return False

                    space.add((x,y,z))

    return True

class Container:
    def __init__(self, width, height, depth):
        self.width = width
        self.depth = depth
        self.height = height

class Box:
    def __init__(self, width,height,depth, weight, rotate=0):
        self._width = width
        self._depth = depth
        self._height = height
        self.weight = weight
        self.rotate = rotate

    def set_pos(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def set_rotate(self, rotate):
        self.rotate = rotate % 6

    def copy(self):
        return Box(self._width, self._height, self._depth, self.weight, self.rotate)

    @property
    def width(self):
        return self._rotate()[0]

    @property
    def depth(self):
        return self._rotate()[1]

    @property
    def height(self):
        return self._rotate()[2]

    def _rotate(self):
        if self.rotate == 0:
            return self._width, self._depth, self._height
        elif self.rotate == 1:
            return self._width, self._height, self._depth
        elif self.rotate == 2:
            return self._height, self._depth, self._width
        elif self.rotate == 3:
            return self._depth, self._width, self._height
        elif self.rotate == 4:
            return self._depth, self._height, self._width
        elif self.rotate == 5:
            return self._height, self._width, self._depth


def calculate_box(container, boxes, gene):
    # TODO Finish this function

    used_boxes = []

    for g in gene:
        box = boxes[g]
        #(find xy min 位置)
        #x, y, z = ..
        # r =
        box.set_pos(x,y,z)
        box.set_rotate(r)

        used_boxes.append(box)


    assert check_all_boxes_ok(container, used_boxes)

    return used_boxes

container = Container(
    5,  # container's width
    6,  # container's height
    7   # container's depth
)

box1 = Box(
    1,  # box1's width
    2,  # box1's height
    3,  # box1's depth
    4   # box1's weight
)

box2 = Box(
    2,
    3,
    4,
    5
)

box3 = box1.copy()

boxes = [box1, box2, box3]

gene = [1, 0, 2]

calculate_box(container, boxes, gene)
from collections import defaultdict


class Box:
    def __init__(self, width, height, depth, weight, x, y, z):
        self.width = width
        self.height = height
        self.depth = depth
        self.weight = weight
        self.x = x
        self.y = y
        self.z = z

        self.center_x = self.x + self.width / 2.0
        self.center_y = self.y + self.height / 2.0

    def support_weight(self, x, y, weight):
        # calculate center_x, center_y offset
        self.center_x = (self.center_x * self.weight + x * weight) / (self.weight + weight)
        self.center_y = (self.center_y * self.weight + y * weight) / (self.weight + weight)

        self.weight += weight

    def can_support(self, box):
        if box.z != self.z + self.depth:
            return False
        if (box.x - self.x) * (box.x + box.width - self.x - self.width) > 0:
            return False
        if (box.y - self.y) * (box.y + box.height - self.y - self.height) > 0:
            return False

        return True

    def overlap_plane(self, box):
        # return left, right, top, bottom
        if not self.can_support(box):
            return (0, 0, 0, 0)

        xs = [self.x, self.x + self.width, box.x, box.x + box.width]
        ys = [self.y, self.y + self.height, box.y, box.y + box.height]
        xs.sort()
        ys.sort()

        return xs[1], xs[2], ys[1], ys[2]

def calculate_weight_distribution(box, overlap_planes):
    # TODO: need to work on
    return [float(box.weight) / len(overlap_planes) for k in overlap_planes]

def update_box_status(box, boxes):
    support_boxes = [k for k in boxes if k.can_support()]
    overlap_planes = [k.overlap_plane(box) for k in boxes]

    weights = calculate_weight_distribution(box, overlap_planes)

    for support_box, overlap_plane, weight in zip(support_boxes, overlap_planes, weights):
        support_box.support_weight(
            (overlap_plane[0] + overlap_plane[1]) / 2.0,
            (overlap_plane[2] + overlap_plane[3]) / 2.0,
            weight
        )


def check_all_boxes_ok(c_width, c_height, c_depth, boxes):
    space = set()

    for box in boxes:
        # check box setting correct
        if not (box.x >= 0 and (box.width + box.x) <= c_width) and box.width > 0:
            return False
        if not (box.y >= 0 and (box.height + box.y) <= c_height) and box.height > 0:
            return False
        if not (box.z >= 0 and (box.depth + box.z) <= c_depth) and box.depth > 0:
            return False

        # a very simple way to calculate collision
        for x in xrange(box.width):
            for y in xrange(box.height):
                for z in xrange(box.depth):
                    if (x, y, z) in space:
                        return False

                    space.add((x,y,z))

    return True

def check_gravity_stable(c_width, c_height, c_depth, boxes):
    if not check_all_boxes_ok(c_width, c_height, c_depth, boxes):
        return False

    boxes.sort(key=lambda i: -i.z)
    while boxes:
        if update_box_status(boxes[0], boxes[1:]):
            boxes = boxes[1:]
            continue

        return False

    return True

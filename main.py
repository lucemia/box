# -*- encoding=utf8 -*-
from collections import defaultdict
import logging

class Box(object):
    # define a box object
    def __init__(self, width, height, depth, weight, x, y, z):
        self.width = width
        self.height = height
        self.depth = depth
        self.weight = weight
        self.x = x
        self.y = y
        self.z = z

        # the mass center location, z index is ignored
        self.center_x = self.x + self.width / 2.0
        self.center_y = self.y + self.height / 2.0

    def support_weight(self, x, y, weight):
        # calculate center_x, center_y offset while the box need to support other box
        self.center_x = (self.center_x * self.weight + x * weight) / (self.weight + weight)
        self.center_y = (self.center_y * self.weight + y * weight) / (self.weight + weight)

        self.weight += weight

    def can_support(self, box):
        # raft check this box can support another box
        # which means they have intercept in a z-index
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

def calculate_mass_center_in_support_plan(box, overlap_planes):
    # calculate convex hull from overlap planes
    # check box's mass center in the poly

    from scipy.spatial import ConvexHull
    import matplotlib.nxutils as nx

    points = []
    for left, right, top, bottom in overlap_planes:
        points.extend([
            (left, top),
            (left, bottom),
            (right, top),
            (right, bottom)
        ])

    # calculate the plane cover by all possible supporting points
    # and check the box's mass center is in the plane
    hull = ConvexHull(points)
    r = nx.pnpoly(box.center_x, box.center_y, hull)
    return r and True

def update_box_status(box, boxes):
    support_boxes = [k for k in boxes if k.can_support(box)]
    overlap_planes = [k.overlap_plane(box) for k in boxes]

    calculate_mass_center_in_support_plan(box, overlap_planes)

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
        if not (box.x >= 0 and (box.width + box.x) <= c_width and box.width > 0):
            logging.error("box %s failed test" % box)
            return False
        if not (box.y >= 0 and (box.height + box.y) <= c_height and box.height > 0):
            logging.error("box %s failed test" % box)
            return False
        if not (box.z >= 0 and (box.depth + box.z) <= c_depth and box.depth > 0):
            logging.error("box %s failed test" % box)
            return False

        # a very simple way to calculate collision
        for x in xrange(box.x, box.x + box.width):
            for y in xrange(box.y, box.y + box.height):
                for z in xrange(box.z, box.z + box.depth):
                    if (x, y, z) in space:
                        return False

                    space.add((x,y,z))

    return True

def check_gravity_stable(c_width, c_height, c_depth, boxes):
    if not check_all_boxes_ok(c_width, c_height, c_depth, boxes):
        logging.error("not a phy possible setting")
        return False

    boxes.sort(key=lambda i: -i.z)
    while boxes:
        if update_box_status(boxes[0], boxes[1:]):
            boxes = boxes[1:]
            continue

        return False

    return True




# -*- encoding=utf8 -*-
from collections import defaultdict
import logging

class Box(object):
    """
        定義一個貨物
    """
    def __init__(self, width, height, depth, weight, x, y, z):
        self.width = width
        self.height = height
        self.depth = depth
        self.weight = weight
        self.x = x
        self.y = y
        self.z = z

        # the mass center location, z index is ignored
        # 貨物重心的 (x,y) 坐標
        self.center_x = self.x + self.width / 2.0
        self.center_y = self.y + self.height / 2.0

    def support_weight(self, x, y, weight):
        """
            計算目前貨物上方如果在 (x,y) 坐標被施加了 weight的力量, 對貨物的重心產生的影響
        """
        # calculate center_x, center_y offset while the box need to support other box
        self.center_x = (self.center_x * self.weight + x * weight) / (self.weight + weight)
        self.center_y = (self.center_y * self.weight + y * weight) / (self.weight + weight)

        self.weight += weight

    def can_support(self, box):
        """
            計算目前
        """
        # raft check this box can support another box
        # which means they have intercept in a z-index
        if box.z != self.z + self.depth:
            return False

        xs = [(box.x, 'x'), (box.x + box.width,'x'), (self.x, 'y'), (self.width, 'y')]
        xs.sort(key=lambda i:i[0])
        if xs[0][1] == xs[1][1]:
            return False

        ys = [(box.y, 'x'), (box.y + box.height, 'x'), (self.y, 'y'), (self.y + self.height, 'y')]
        ys.sort(key=lambda i:i[0])
        if ys[0][1] == ys[1][1]:
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
    """
        計算需要支撐目標貨物, 各支點需要負擔的重量
    """
    # TODO: need to work on
    return [float(box.weight) / len(overlap_planes) for k in overlap_planes]

def calculate_mass_center_in_support_plan(box, overlap_planes):
    """
        判斷目標貨物是否能夠被支點所支撐
        透過 ConvexHull 演算法, 檢查目標貨物的重心 (x,y) 坐標,
        是否在支點形成的凸面之中
    """
    from scipy.spatial import ConvexHull
    import matplotlib.nxutils as nx

    # 取出所有的支點
    points = []
    for left, right, top, bottom in overlap_planes:
        points.extend([
            (left, top),
            (left, bottom),
            (right, top),
            (right, bottom)
        ])

    # 計算支點形成的凸面
    hull = ConvexHull(points)
    # 確認box重心是否在凸面之中
    r = nx.pnpoly(box.center_x, box.center_y, hull)
    return r and True

def check_box_can_be_support(box, boxes):
    """
        確認目標貨物(box), 是可以被剩餘的其他貨物(boxes)支撐的
    """
    if box.z == 0:
        # 貨物在地上, 不需要被支撐
        return True

    if not boxes:
        # 沒有可以支撐的貨物
        return False

    # 篩選出有可能支撐目標box 的貨物
    support_boxes = [k for k in boxes if k.can_support(box)]
    # 計算出所有支點
    overlap_planes = [k.overlap_plane(box) for k in support_boxes]

    # 計算此貨物的重心是否在支點形成的平面之中
    can_support = calculate_mass_center_in_support_plan(box, overlap_planes)
    if not can_support:
        # 目標貨物無法被支撐
        return False

    # 計算出每一個支點應該分配到的重量
    # HINT: 有可能會有多組解
    weights = calculate_weight_distribution(box, overlap_planes)

    for support_box, overlap_plane, weight in zip(support_boxes, overlap_planes, weights):
        # 根據計算出的重量, 將此貨物的重量加權到成為支點的其餘貨物
        support_box.support_weight(
            (overlap_plane[0] + overlap_plane[1]) / 2.0,
            (overlap_plane[2] + overlap_plane[3]) / 2.0,
            weight
        )

    return True


def check_all_boxes_ok(c_width, c_height, c_depth, boxes):
    """
        確認所有貨物沒有設定錯誤, 不考慮平衡問題
    """
    space = set()

    for box in boxes:
        # 確認貨物是在貨櫃的範圍內
        if not (box.x >= 0 and (box.width + box.x) <= c_width and box.width > 0):
            logging.error("box %s failed test" % box)
            return False
        if not (box.y >= 0 and (box.height + box.y) <= c_height and box.height > 0):
            logging.error("box %s failed test" % box)
            return False
        if not (box.z >= 0 and (box.depth + box.z) <= c_depth and box.depth > 0):
            logging.error("box %s failed test" % box)
            return False

        # 確認貨物沒有互相碰撞
        for x in xrange(box.x, box.x + box.width):
            for y in xrange(box.y, box.y + box.height):
                for z in xrange(box.z, box.z + box.depth):
                    if (x, y, z) in space:
                        return False

                    space.add((x,y,z))

    return True

def check_gravity_stable(c_width, c_height, c_depth, boxes):
    """
        確認所有設定好的貨物(boxes), 在貨櫃(container)中是穩定的
        c_width: 貨櫃的寬
        c_height: 貨櫃的高
        c_depth: 貨櫃的深
        boxes: 所有放在貨櫃中的貨物
    """

    # 確認貨物設定正確
    if not check_all_boxes_ok(c_width, c_height, c_depth, boxes):
        logging.error("not a physical possible setting")
        return False

    # 由上而下, 一個一個確認貨物是能夠被支撐的.
    boxes.sort(key=lambda i: -i.z)
    while boxes:
        if check_box_can_be_support(boxes[0], boxes[1:]):
            boxes = boxes[1:]
            continue

        return False

    return True


# def place_box(boxes, genes):




# -*- encoding=utf8 -*-


import unittest
from main import *

class BoxTest(unittest.TestCase):
    def setUp(self):
        pass

    def testWeightDistributionCalculation(self):
        #weight=1,width, height, depth=2
        box = Box(2, 2, 2, 1, 0, 0, 0)

        #test 1 box
        planes = [[0, 1, 0, 1]]
        w = calculate_weight_distribution(box, planes)
        self.assertIsNone(w)

        #test 2 box
        planes = [
            [0 ,1, 0, 1],
            [1 ,2 ,1 ,2]
        ]
        w0, w1 = calculate_weight_distribution(box, planes)
        self.assertEqual(w0, 0.5)#unittest
        self.assertEqual(w1, 0.5)
        #test 3 box
        planes = [
            [0, 1, 0, 1],
            [1, 2, 1, 2],
            [0, 1, 1, 2]
        ]
        w0, w1, w2 = calculate_weight_distribution(box, planes)
        self.assertEqual(w0, 0.5)
        self.assertEqual(w1, 0.5)
        self.assertEqual(w2, 0)

        # test 4 box
        planes = [
            [0, 1, 0, 1],
            [1, 2, 1, 2],
            [0, 1, 1, 2],
            [1, 2, 0, 1]
        ]
        ws = calculate_weight_distribution(box, planes)
        self.assertIsNone(ws)

        box = Box(3, 3, 3, 1, 0, 0, 0)

        planes = [
            [1, 2, 1, 2]
        ]
        ws = calculate_weight_distribution(box, planes)

        planes = [
            [0, 1, 0, 1],
            [1, 2, 1, 2],
            [2, 3, 2, 3]
        ]
        ws = calculate_weight_distribution(box, planes)

    def testUnitbox(self):
        boxes = []
        for x in range(10):
            for y in range(10):
                for z in range(10):
                    boxes.append(Box(1, 1, 1, 1, x, y, z))


                    # self.assertTrue(check_gravity_stable(10, 10, 10, boxes))

if __name__ == '__main__':
    unittest.main()

import unittest
from main import *

class BoxTest(unittest.TestCase):
    def setUp(self):
        pass


    def testUnitbox(self):
        boxes = []
        for x in range(10):
            for y in range(10):
                for z in range(10):
                    boxes.append(Box(1, 1, 1, 1, x, y, z))


        self.assertTrue(check_gravity_stable(10, 10, 10, boxes))

if __name__ == '__main__':
    unittest.main()

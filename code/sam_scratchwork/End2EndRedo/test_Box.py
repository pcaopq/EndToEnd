'''@author Samuel Tenka
'''

import unittest
from Box import Box

class TestBox(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        self.badzero = Box(0,0,-1,-1)
        self.fancyzero = Box([[0,0],[0,0]])
        self.fancybadzero = Box([[0,0],[-1,-1]])
        self.zero = Box(0,0,0,0)
        self.square = Box(0,0,1,1)
        self.up= Box(1,0,2,1)
        self.upright = Box(1,1,2,2)
        self.center = Box(0.5,0.5,1.5,1.5)
        self.tallthin = Box(0.25,0.75,1.75,1.25)
        self.shortwide = Box(0.75,0.25,1.25,1.75)
        self.nothing = Box(1,1,1,1)
        self.small = Box(0.75,0.75,1.25,1.25)
        self.big = Box(0.25,0.25,1.75,1.75)
        self.all = Box(0,0,2,2)
        self.silouhette = Box(0,0,2,0)
        self.shadow = Box(0,0,0,2)
    def test_init(self):
        self.assertEqual(self.zero, self.badzero)
        self.assertEqual(self.zero, self.fancyzero)
        self.assertEqual(self.zero, self.fancybadzero)
    def test_area(self):
        self.assertEqual(self.zero.area(), 0.0)
        self.assertEqual(self.square.area(), 1.0)
        self.assertEqual(self.up.area(), 1.0)
        self.assertEqual(self.upright.area(), 1.0)
        self.assertEqual(self.center.area(), 1.0)
        self.assertEqual(self.tallthin.area(), 0.75)
        self.assertEqual(self.shortwide.area(), 0.75)
        self.assertEqual(self.nothing.area(), 0.0)
        self.assertEqual(self.small.area(), 0.25)
        self.assertEqual(self.big.area(), 2.25)
        self.assertEqual(self.all.area(), 4.0)
        self.assertEqual(self.shadow.area(), 0.0)
    def test_join(self):
        #reflexivity:
        self.assertEqual(self.zero.join(self.zero), self.zero)
        self.assertEqual(self.shadow.join(self.shadow), self.shadow)
        self.assertEqual(self.center.join(self.center), self.center)
        #symmetry:
        self.assertEqual(self.up.join(self.tallthin), self.tallthin.join(self.up))
        self.assertEqual(self.shadow.join(self.shortwide), self.shortwide.join(self.shadow))
        #identities:
        self.assertEqual(self.silouhette.join(self.shadow), self.all)
        self.assertEqual(self.tallthin.join(self.shortwide), self.big)
        self.assertEqual(self.square.join(self.upright), self.all)
    def test_meet(self):
        #reflexivity:
        self.assertEqual(self.zero.meet(self.zero), self.zero)
        self.assertEqual(self.shadow.meet(self.shadow), self.shadow)
        self.assertEqual(self.center.meet(self.center), self.center)
        #symmetry:
        self.assertEqual(self.up.meet(self.tallthin), self.tallthin.meet(self.up))
        self.assertEqual(self.shadow.meet(self.shortwide), self.shortwide.meet(self.shadow))
        #identities:
        self.assertEqual(self.silouhette.meet(self.shadow), self.zero)
        self.assertEqual(self.tallthin.meet(self.shortwide), self.small)
        self.assertEqual(self.square.meet(self.upright), self.nothing)
        #TODO: test the meet of disjoint, far boxes!
    def test_overlaps(self):
        #measure-0 intersections don't count as overlaps:
        self.assertFalse(self.zero.overlaps(self.square))
        self.assertFalse(self.zero.overlaps(self.up))
        self.assertFalse(self.zero.overlaps(self.upright))

        self.assertFalse(self.square.overlaps(self.up))
        self.assertFalse(self.square.overlaps(self.upright))

        self.assertFalse(self.up.overlaps(self.upright))

        self.assertFalse(self.shadow.overlaps(self.all))
        self.assertFalse(self.shadow.overlaps(self.tallthin))
        self.assertFalse(self.silouhette.overlaps(self.shortwide))
        self.assertFalse(self.silouhette.overlaps(self.all))
        self.assertFalse(self.silouhette.overlaps(self.tallthin))
        self.assertFalse(self.silouhette.overlaps(self.shortwide))

        #positive-measure intersections _do_ count as overlaps:
        self.assertTrue(self.center.overlaps(self.square))
        self.assertTrue(self.center.overlaps(self.up))
        self.assertTrue(self.center.overlaps(self.upright))
        self.assertTrue(self.center.overlaps(self.small))
        self.assertTrue(self.center.overlaps(self.tallthin))
        self.assertTrue(self.center.overlaps(self.shortwide))
        self.assertTrue(self.center.overlaps(self.big))

        self.assertTrue(self.small.overlaps(self.big))
        self.assertTrue(self.big.overlaps(self.small))
        self.assertTrue(self.tallthin.overlaps(self.shortwide))
        self.assertTrue(self.shortwide.overlaps(self.tallthin))
    def test_containment(self):
        #compare measure-0 sets:
        self.assertTrue(self.shadow in self.shadow)
        self.assertFalse(self.shadow in self.zero)
        self.assertTrue(self.zero in self.shadow)
        self.assertTrue(self.zero in self.zero)

        #what contains zero?
        self.assertFalse(self.zero in self.center)
        self.assertTrue(self.zero in self.square)

        #compare concentric positive-area boxes:
        self.assertTrue(self.small in self.center)
        self.assertFalse(self.center in self.small)
        self.assertFalse(self.big in self.center)
        self.assertTrue(self.center in self.big)
    def test_bool(self):
        self.assertFalse(self.zero)
        self.assertFalse(self.silouhette)
        self.assertFalse(self.shadow)
        self.assertFalse(self.nothing)

        self.assertTrue(self.all)
        self.assertTrue(self.shortwide)
        self.assertTrue(self.tallthin)
        self.assertTrue(self.center)
    def test_minus(self):
        pass #TODO

if __name__=='__main__':
    unittest.main()

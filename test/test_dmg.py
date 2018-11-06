import unittest

from pydmg import PyDMG


class DMGTestCase(unittest.TestCase):
    def setUp(self):
        self.dmg = PyDMG(None, None)

    def test_single_clock(self):
        self.dmg.clock()

    def test_seven_clocks(self):
        self.dmg.memory.boot_rom.data[0x0000] = 0
        self.dmg.clock()
        self.dmg.clock()
        self.dmg.clock()
        self.dmg.clock()
        self.dmg.clock()
        self.dmg.clock()
        self.dmg.clock()

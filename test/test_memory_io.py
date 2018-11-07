import unittest

from cpu import CPU
from lcd import LCD
from memory import DMGMemory


class LCDIOTestCase(unittest.TestCase):
    def setUp(self):
        self.lcd = LCD()
        self.memory = DMGMemory(self.lcd)
        self.lcd.memory = self.memory
        self.cpu = CPU(self.memory)

    def test_disable_boot_rom(self):
        self.assertTrue(self.memory.boot_rom.is_enabled)
        self.memory.write(0xFF50, 0x01)
        self.assertFalse(self.memory.boot_rom.is_enabled)

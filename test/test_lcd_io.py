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

    def test_set_scroll_y(self):
        self.memory.write(0xFF42, 0x64)
        self.assertEqual(self.lcd.scroll_y, 0x64)

    def test_enable_lcd(self):
        self.memory.write(0xFF40, 0x91)
        self.assertTrue(self.lcd.enabled)
        self.assertFalse(self.lcd.window_tile_map_display_select)
        self.assertFalse(self.lcd.window_display_enable)
        self.assertTrue(self.lcd.bg_and_window_tile_data_select)
        self.assertFalse(self.lcd.bg_tile_map_display_select)
        self.assertFalse(self.lcd.sprite_size)
        self.assertFalse(self.lcd.sprite_display)
        self.assertTrue(self.lcd.bg_and_window_display)

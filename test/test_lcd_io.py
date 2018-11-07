import unittest

from cpu import CPU
from lcd import LCD
from memory import DMGMemory
from memory_zone import MemoryZone, MemoryFault


class LCDIOTestCase(unittest.TestCase):
    def setUp(self):
        self.lcd = LCD()
        self.memory = DMGMemory(self.lcd)
        self.lcd.memory = self.memory
        self.cpu = CPU(self.memory)

    def test_set_scroll_y(self):
        # Write 0x64 to to 0xFF42, setting the Y scroll
        # LD A, 0x64
        self.memory.boot_rom.data[0x0000] = 0x3E
        self.memory.boot_rom.data[0x0001] = 0x64
        # LDH 0xFF42, A
        self.memory.boot_rom.data[0x0002] = 0xE0
        self.memory.boot_rom.data[0x0003] = 0x42

        self.cpu.step()
        self.assertEqual(self.cpu.register_a.get(), 0x64)

        self.cpu.step()
        self.assertEqual(self.lcd.scroll_y, 0x64)

    def test_enable_lcd(self):
        # Write 0x91 to to 0xFF40
        #
        # LD A, 0x91
        self.memory.boot_rom.data[0x0000] = 0x3E
        self.memory.boot_rom.data[0x0001] = 0x91
        # LDH 0xFF40, A
        self.memory.boot_rom.data[0x0002] = 0xE0
        self.memory.boot_rom.data[0x0003] = 0x40

        self.cpu.step()
        self.assertEqual(self.cpu.register_a.get(), 0x91)

        self.cpu.step()
        self.assertTrue(self.lcd.enabled)
        self.assertFalse(self.lcd.window_tile_map_display_select)
        self.assertFalse(self.lcd.window_display_enable)
        self.assertTrue(self.lcd.bg_and_window_tile_data_select)
        self.assertFalse(self.lcd.bg_tile_map_display_select)
        self.assertFalse(self.lcd.sprite_size)
        self.assertFalse(self.lcd.sprite_display)
        self.assertTrue(self.lcd.bg_and_window_display)

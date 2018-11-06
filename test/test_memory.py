import unittest

from memory_zone import MemoryZone, MemoryFault


class MemoryZoneTestCase(unittest.TestCase):
    def setUp(self):
        self.zone = MemoryZone('test zone', size=0x10, base_address=0x20)

    def test_read_empty_zone(self):
        self.assertEqual(self.zone.read(0x20), 0)

    def test_read_preceding_address(self):
        self.assertRaises(MemoryFault, self.zone.read, 0xD)

    def test_read_postceding_address(self):
        self.assertRaises(MemoryFault, self.zone.read, 0xC2)

    def test_write(self):
        self.zone.write(0x22, 0x11)
        self.assertEqual(self.zone.read(0x22), 0x11)

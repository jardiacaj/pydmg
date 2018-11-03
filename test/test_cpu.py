import unittest

from cpu import CPU


class DefaultCPUTestCase(unittest.TestCase):
    def setUp(self):
        self.cpu = CPU(None)

    def testDefaultCPU(self):
        self.assertEqual(self.cpu.total_clock_cycle_count, 0)
        self.assertEqual(self.cpu.register_af.get(), 0)
        self.assertEqual(self.cpu.register_a.get(), 0)
        self.assertEqual(self.cpu.flags.get_zero_flag(), 0)

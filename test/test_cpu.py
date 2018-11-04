import unittest

from cpu import CPU
from ram import RAM


class DefaultCPUTestCase(unittest.TestCase):
    def setUp(self):
        self.memory = RAM()
        self.cpu = CPU(self.memory)

    def testDefaultCPU(self):
        self.assertEqual(self.cpu.total_clock_cycle_count, 0)
        self.assertEqual(self.cpu.register_af.get(), 0)
        self.assertEqual(self.cpu.register_a.get(), 0)
        self.assertEqual(self.cpu.flags.get_zero_flag(), 0)

    def testNOPTick(self):
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 4)
        self.assertEqual(self.cpu.register_program_counter.get(), 1)

    def testInvalidInstruction(self):
        self.memory.data[0] = 0xFD
        self.assertRaises(NotImplementedError, self.cpu.tick)

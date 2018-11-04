import unittest

from cpu import CPU
from ram import RAM


class ControlInstructionTestCase(unittest.TestCase):
    def setUp(self):
        self.memory = RAM()
        self.cpu = CPU(self.memory)

    def testNop(self):
        self.memory.data = [0]
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 4)
        self.assertEqual(self.cpu.register_program_counter.get(), 1)

import unittest

from cpu import CPU
from ram import RAM


class JumpInstructionTestCase(unittest.TestCase):
    def setUp(self):
        self.memory = RAM()
        self.cpu = CPU(self.memory)

    def test_JR_NZ_dont_jump(self):
        self.memory.data = [0x20, 0xFE]  # JR NZ, -2
        self.cpu.flags.reset_zero_flag()
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 8)
        self.assertEqual(self.cpu.register_program_counter.get(), 2)

    def test_JR_NZ_do_jump(self):
        self.memory.data = [0x20, 0xFE]  # JR NZ, -2
        self.cpu.flags.set_zero_flag()
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 8)
        self.assertEqual(self.cpu.register_program_counter.get(), 0)

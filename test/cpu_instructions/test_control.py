import unittest

from cpu import CPU
from memory import DMGMemory


class ControlInstructionTestCase(unittest.TestCase):
    def setUp(self):
        self.memory = DMGMemory()
        self.cpu = CPU(self.memory)

    def testNop(self):
        self.memory.boot_rom.data = [0]
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 4)
        self.assertEqual(self.cpu.register_program_counter.get(), 1)

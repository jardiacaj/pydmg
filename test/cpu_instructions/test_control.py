import unittest

from cpu import CPU
from memory import DMGMemory


class ControlInstructionTestCase(unittest.TestCase):
    def setUp(self):
        self.memory = DMGMemory()
        self.cpu = CPU(self.memory)

    def testNop(self):
        self.memory.boot_rom.data = [0]
        self.cpu.step()
        self.assertEqual(self.cpu.total_clock_cycles_ran, 4)
        self.assertEqual(self.cpu.register_program_counter.get(), 1)

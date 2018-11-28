import unittest

from cpu import CPU
from memory import DMGMemory
from register import Z


class DefaultCPUTestCase(unittest.TestCase):
    def setUp(self):
        self.memory = DMGMemory()
        self.cpu = CPU(self.memory)

    def testDefaultCPU(self):
        self.assertEqual(self.cpu.total_clock_cycles_ran, 0)
        self.assertEqual(self.cpu.register_af.get(), 0)
        self.assertEqual(self.cpu.register_a.get(), 0)
        self.assertEqual(self.cpu.flags.get_flag(Z), 0)

    def testNOPTick(self):
        self.cpu.step()
        self.assertEqual(self.cpu.total_clock_cycles_ran, 4)
        self.assertEqual(self.cpu.register_program_counter.get(), 1)

    def testInvalidInstruction(self):
        self.memory.boot_rom.data[0] = 0xFD
        self.assertRaises(NotImplementedError, self.cpu.step)

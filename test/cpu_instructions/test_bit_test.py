import unittest

from cpu import CPU
from memory import DMGMemory


class BitTestInstructionTestCase(unittest.TestCase):
    def setUp(self):
        self.memory = DMGMemory()
        self.cpu = CPU(self.memory)

    def test_BIT_7_H_on_one(self):
        self.memory.boot_rom.data = [0xCB, 0x7C]
        self.cpu.register_h.set(0b10000000)
        self.cpu.step()
        self.assertEqual(self.cpu.total_clock_cycles_ran, 8)
        self.assertEqual(self.cpu.register_program_counter.get(), 2)
        self.assertFalse(self.cpu.flags.get_zero_flag())
        self.assertFalse(self.cpu.flags.get_negative_flag())
        self.assertTrue(self.cpu.flags.get_half_carry_flag())

    def test_BIT_7_H_on_zero(self):
        self.memory.boot_rom.data = [0xCB, 0x7C]
        self.cpu.register_h.set(0)
        self.cpu.step()
        self.assertEqual(self.cpu.total_clock_cycles_ran, 8)
        self.assertEqual(self.cpu.register_program_counter.get(), 2)
        self.assertTrue(self.cpu.flags.get_zero_flag())
        self.assertFalse(self.cpu.flags.get_negative_flag())
        self.assertTrue(self.cpu.flags.get_half_carry_flag())

    def test_BIT_1_HL_pointer_on_one(self):
        self.memory.boot_rom.data = [0xCB, 0x4E]
        self.cpu.register_hl.set(0x0001)
        self.cpu.step()
        self.assertEqual(self.cpu.total_clock_cycles_ran, 16)
        self.assertEqual(self.cpu.register_program_counter.get(), 2)
        self.assertFalse(self.cpu.flags.get_zero_flag())
        self.assertFalse(self.cpu.flags.get_negative_flag())
        self.assertTrue(self.cpu.flags.get_half_carry_flag())

    def test_BIT_0_HL_pointer_on_zero(self):
        self.memory.boot_rom.data = [0xCB, 0x46]
        self.cpu.register_hl.set(0x0001)
        self.cpu.step()
        self.assertEqual(self.cpu.total_clock_cycles_ran, 16)
        self.assertEqual(self.cpu.register_program_counter.get(), 2)
        self.assertTrue(self.cpu.flags.get_zero_flag())
        self.assertFalse(self.cpu.flags.get_negative_flag())
        self.assertTrue(self.cpu.flags.get_half_carry_flag())

import unittest

from cpu import CPU
from ram import RAM


class ALUInstructionTestCase(unittest.TestCase):
    def setUp(self):
        self.memory = RAM()
        self.cpu = CPU(self.memory)

    def test_XOR_A(self):
        self.memory.data = [0xAF]
        self.cpu.register_a.set(0x12)
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 4)
        self.assertEqual(self.cpu.register_program_counter.get(), 1)
        self.assertEqual(self.cpu.register_a.get(), 0)

    def test_AND_B(self):
        self.memory.data = [0xA0]
        self.cpu.register_a.set(0b10100)
        self.cpu.register_b.set(0b11001)
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 4)
        self.assertEqual(self.cpu.register_program_counter.get(), 1)
        self.assertEqual(self.cpu.register_a.get(), 0b10000)
        self.assertFalse(self.cpu.flags.get_zero_flag())
        self.assertFalse(self.cpu.flags.get_negative_flag())
        self.assertTrue(self.cpu.flags.get_half_carry_flag())
        self.assertFalse(self.cpu.flags.get_carry_flag())

    def test_CMP_A(self):
        self.memory.data[0x00] = 0xBF
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 4)
        self.assertEqual(self.cpu.register_program_counter.get(), 1)
        self.assertTrue(self.cpu.flags.get_zero_flag())
        self.assertTrue(self.cpu.flags.get_negative_flag())
        self.assertFalse(self.cpu.flags.get_half_carry_flag())
        self.assertFalse(self.cpu.flags.get_carry_flag())

    def test_CMP_B(self):
        self.memory.data[0x00] = 0xB8
        self.cpu.register_a.set(0xFF)
        self.cpu.register_b.set(0x01)
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 4)
        self.assertEqual(self.cpu.register_program_counter.get(), 1)
        self.assertFalse(self.cpu.flags.get_zero_flag())
        self.assertTrue(self.cpu.flags.get_negative_flag())
        self.assertTrue(self.cpu.flags.get_half_carry_flag())
        self.assertFalse(self.cpu.flags.get_carry_flag())

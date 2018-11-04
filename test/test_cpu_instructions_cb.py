import unittest

from cpu import CPU
from ram import RAM


class SimpleCBCPUInstructionTestCase(unittest.TestCase):
    def setUp(self):
        self.memory = RAM()
        self.cpu = CPU(self.memory)

    def test_BIT_7_H_on_one(self):
        self.memory.data = [0xCB, 0x7C]
        self.cpu.register_h.set(0b10000000)
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 8)
        self.assertEqual(self.cpu.register_program_counter.get(), 2)
        self.assertFalse(self.cpu.flags.get_zero_flag())
        self.assertFalse(self.cpu.flags.get_negative_flag())
        self.assertTrue(self.cpu.flags.get_half_carry_flag())

    def test_BIT_7_H_on_zero(self):
        self.memory.data = [0xCB, 0x7C]
        self.cpu.register_h.set(0)
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 8)
        self.assertEqual(self.cpu.register_program_counter.get(), 2)
        self.assertTrue(self.cpu.flags.get_zero_flag())
        self.assertFalse(self.cpu.flags.get_negative_flag())
        self.assertTrue(self.cpu.flags.get_half_carry_flag())

    def test_BIT_1_HL_pointer_on_one(self):
        self.memory.data = [0xCB, 0x4E]
        self.cpu.register_hl.set(0x0001)
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 16)
        self.assertEqual(self.cpu.register_program_counter.get(), 2)
        self.assertFalse(self.cpu.flags.get_zero_flag())
        self.assertFalse(self.cpu.flags.get_negative_flag())
        self.assertTrue(self.cpu.flags.get_half_carry_flag())

    def test_BIT_0_HL_pointer_on_zero(self):
        self.memory.data = [0xCB, 0x46]
        self.cpu.register_hl.set(0x0001)
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 16)
        self.assertEqual(self.cpu.register_program_counter.get(), 2)
        self.assertTrue(self.cpu.flags.get_zero_flag())
        self.assertFalse(self.cpu.flags.get_negative_flag())
        self.assertTrue(self.cpu.flags.get_half_carry_flag())

    def test_RL_A(self):
        self.memory.data = [0xCB, 0x17]
        self.cpu.register_a.set(0b10)
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 8)
        self.assertEqual(self.cpu.register_program_counter.get(), 2)
        self.assertEqual(self.cpu.register_a.get(), 0b100)
        self.assertFalse(self.cpu.flags.get_zero_flag())
        self.assertFalse(self.cpu.flags.get_negative_flag())
        self.assertFalse(self.cpu.flags.get_half_carry_flag())
        self.assertFalse(self.cpu.flags.get_carry_flag())

    def test_RL_A_zero(self):
        self.memory.data = [0xCB, 0x17]
        self.cpu.register_a.set(0b0)
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 8)
        self.assertEqual(self.cpu.register_program_counter.get(), 2)
        self.assertEqual(self.cpu.register_a.get(), 0b0)
        self.assertTrue(self.cpu.flags.get_zero_flag())
        self.assertFalse(self.cpu.flags.get_negative_flag())
        self.assertFalse(self.cpu.flags.get_half_carry_flag())
        self.assertFalse(self.cpu.flags.get_carry_flag())

    def test_RL_A_to_carry(self):
        self.memory.data = [0xCB, 0x17]
        self.cpu.register_a.set(0b10000000)
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 8)
        self.assertEqual(self.cpu.register_program_counter.get(), 2)
        self.assertEqual(self.cpu.register_a.get(), 0b0)
        self.assertTrue(self.cpu.flags.get_zero_flag())
        self.assertFalse(self.cpu.flags.get_negative_flag())
        self.assertFalse(self.cpu.flags.get_half_carry_flag())
        self.assertTrue(self.cpu.flags.get_carry_flag())

    def test_RL_A_from_carry(self):
        self.memory.data = [0xCB, 0x17]
        self.cpu.register_a.set(0b111)
        self.cpu.flags.set_carry_flag()
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 8)
        self.assertEqual(self.cpu.register_program_counter.get(), 2)
        self.assertEqual(self.cpu.register_a.get(), 0b1111)
        self.assertFalse(self.cpu.flags.get_zero_flag())
        self.assertFalse(self.cpu.flags.get_negative_flag())
        self.assertFalse(self.cpu.flags.get_half_carry_flag())
        self.assertFalse(self.cpu.flags.get_carry_flag())

    def test_RL_HL_pointer(self):
        self.memory.data = [0xCB, 0x16, 0b10]
        self.cpu.register_hl.set(0x0002)
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 16)
        self.assertEqual(self.cpu.register_program_counter.get(), 2)
        self.assertEqual(self.cpu.memory.read(0x0002), 0b100)
        self.assertFalse(self.cpu.flags.get_zero_flag())
        self.assertFalse(self.cpu.flags.get_negative_flag())
        self.assertFalse(self.cpu.flags.get_half_carry_flag())
        self.assertFalse(self.cpu.flags.get_carry_flag())

    def test_RL_HL_pointer_zero(self):
        self.memory.data = [0xCB, 0x16, 0b0]
        self.cpu.register_hl.set(0x0002)
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 16)
        self.assertEqual(self.cpu.register_program_counter.get(), 2)
        self.assertEqual(self.cpu.memory.read(0x0002), 0b0)
        self.assertTrue(self.cpu.flags.get_zero_flag())
        self.assertFalse(self.cpu.flags.get_negative_flag())
        self.assertFalse(self.cpu.flags.get_half_carry_flag())
        self.assertFalse(self.cpu.flags.get_carry_flag())

    def test_RL_HL_pointer_to_carry(self):
        self.memory.data = [0xCB, 0x16, 0b10000000]
        self.cpu.register_hl.set(0x0002)
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 16)
        self.assertEqual(self.cpu.register_program_counter.get(), 2)
        self.assertEqual(self.cpu.memory.read(0x0002), 0b0)
        self.assertTrue(self.cpu.flags.get_zero_flag())
        self.assertFalse(self.cpu.flags.get_negative_flag())
        self.assertFalse(self.cpu.flags.get_half_carry_flag())
        self.assertTrue(self.cpu.flags.get_carry_flag())

    def test_RL_HL_pointer_from_carry(self):
        self.memory.data = [0xCB, 0x16, 0b111]
        self.cpu.register_hl.set(0x0002)
        self.cpu.flags.set_carry_flag()
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 16)
        self.assertEqual(self.cpu.register_program_counter.get(), 2)
        self.assertEqual(self.cpu.memory.read(0x0002), 0b1111)
        self.assertFalse(self.cpu.flags.get_zero_flag())
        self.assertFalse(self.cpu.flags.get_negative_flag())
        self.assertFalse(self.cpu.flags.get_half_carry_flag())
        self.assertFalse(self.cpu.flags.get_carry_flag())

    def test_RLC_A(self):
        self.memory.data = [0xCB, 0x07]
        self.cpu.register_a.set(0b10)
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 8)
        self.assertEqual(self.cpu.register_program_counter.get(), 2)
        self.assertEqual(self.cpu.register_a.get(), 0b100)
        self.assertFalse(self.cpu.flags.get_zero_flag())
        self.assertFalse(self.cpu.flags.get_negative_flag())
        self.assertFalse(self.cpu.flags.get_half_carry_flag())
        self.assertFalse(self.cpu.flags.get_carry_flag())

    def test_RLC_A_zero(self):
        self.memory.data = [0xCB, 0x07]
        self.cpu.register_a.set(0b0)
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 8)
        self.assertEqual(self.cpu.register_program_counter.get(), 2)
        self.assertEqual(self.cpu.register_a.get(), 0b0)
        self.assertTrue(self.cpu.flags.get_zero_flag())
        self.assertFalse(self.cpu.flags.get_negative_flag())
        self.assertFalse(self.cpu.flags.get_half_carry_flag())
        self.assertFalse(self.cpu.flags.get_carry_flag())

    def test_RLC_A_to_carry(self):
        self.memory.data = [0xCB, 0x07]
        self.cpu.register_a.set(0b10000000)
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 8)
        self.assertEqual(self.cpu.register_program_counter.get(), 2)
        self.assertEqual(self.cpu.register_a.get(), 0b0)
        self.assertTrue(self.cpu.flags.get_zero_flag())
        self.assertFalse(self.cpu.flags.get_negative_flag())
        self.assertFalse(self.cpu.flags.get_half_carry_flag())
        self.assertTrue(self.cpu.flags.get_carry_flag())

    def test_RLC_A_from_carry(self):
        self.memory.data = [0xCB, 0x07]
        self.cpu.register_a.set(0b111)
        self.cpu.flags.set_carry_flag()
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 8)
        self.assertEqual(self.cpu.register_program_counter.get(), 2)
        self.assertEqual(self.cpu.register_a.get(), 0b1110)
        self.assertFalse(self.cpu.flags.get_zero_flag())
        self.assertFalse(self.cpu.flags.get_negative_flag())
        self.assertFalse(self.cpu.flags.get_half_carry_flag())
        self.assertFalse(self.cpu.flags.get_carry_flag())

    def test_RLC_HL_pointer(self):
        self.memory.data = [0xCB, 0x06, 0b10]
        self.cpu.register_hl.set(0x0002)
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 16)
        self.assertEqual(self.cpu.register_program_counter.get(), 2)
        self.assertEqual(self.cpu.memory.read(0x0002), 0b100)
        self.assertFalse(self.cpu.flags.get_zero_flag())
        self.assertFalse(self.cpu.flags.get_negative_flag())
        self.assertFalse(self.cpu.flags.get_half_carry_flag())
        self.assertFalse(self.cpu.flags.get_carry_flag())

    def test_RLC_HL_pointer_zero(self):
        self.memory.data = [0xCB, 0x06, 0b0]
        self.cpu.register_hl.set(0x0002)
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 16)
        self.assertEqual(self.cpu.register_program_counter.get(), 2)
        self.assertEqual(self.cpu.memory.read(0x0002), 0b0)
        self.assertTrue(self.cpu.flags.get_zero_flag())
        self.assertFalse(self.cpu.flags.get_negative_flag())
        self.assertFalse(self.cpu.flags.get_half_carry_flag())
        self.assertFalse(self.cpu.flags.get_carry_flag())

    def test_RLC_HL_pointer_to_carry(self):
        self.memory.data = [0xCB, 0x06, 0b10000000]
        self.cpu.register_hl.set(0x0002)
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 16)
        self.assertEqual(self.cpu.register_program_counter.get(), 2)
        self.assertEqual(self.cpu.memory.read(0x0002), 0b0)
        self.assertTrue(self.cpu.flags.get_zero_flag())
        self.assertFalse(self.cpu.flags.get_negative_flag())
        self.assertFalse(self.cpu.flags.get_half_carry_flag())
        self.assertTrue(self.cpu.flags.get_carry_flag())

    def test_RLC_HL_pointer_from_carry(self):
        self.memory.data = [0xCB, 0x06, 0b111]
        self.cpu.register_hl.set(0x0002)
        self.cpu.flags.set_carry_flag()
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 16)
        self.assertEqual(self.cpu.register_program_counter.get(), 2)
        self.assertEqual(self.cpu.memory.read(0x0002), 0b1110)
        self.assertFalse(self.cpu.flags.get_zero_flag())
        self.assertFalse(self.cpu.flags.get_negative_flag())
        self.assertFalse(self.cpu.flags.get_half_carry_flag())
        self.assertFalse(self.cpu.flags.get_carry_flag())

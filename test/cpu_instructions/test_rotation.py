import unittest

from cpu import CPU
from ram import RAM


class BitTestInstructionTestCase(unittest.TestCase):
    def setUp(self):
        self.memory = RAM()
        self.cpu = CPU(self.memory)

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
        self.assertEqual(self.cpu.register_a.get(), 0b1)
        self.assertFalse(self.cpu.flags.get_zero_flag())
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
        self.assertEqual(self.cpu.memory.read(0x0002), 0b1)
        self.assertFalse(self.cpu.flags.get_zero_flag())
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

    def test_RR_A(self):
        self.memory.data = [0xCB, 0x1F]
        self.cpu.register_a.set(0b10)
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 8)
        self.assertEqual(self.cpu.register_program_counter.get(), 2)
        self.assertEqual(self.cpu.register_a.get(), 0b1)
        self.assertFalse(self.cpu.flags.get_zero_flag())
        self.assertFalse(self.cpu.flags.get_negative_flag())
        self.assertFalse(self.cpu.flags.get_half_carry_flag())
        self.assertFalse(self.cpu.flags.get_carry_flag())

    def test_RR_A_zero(self):
        self.memory.data = [0xCB, 0x1F]
        self.cpu.register_a.set(0b0)
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 8)
        self.assertEqual(self.cpu.register_program_counter.get(), 2)
        self.assertEqual(self.cpu.register_a.get(), 0b0)
        self.assertTrue(self.cpu.flags.get_zero_flag())
        self.assertFalse(self.cpu.flags.get_negative_flag())
        self.assertFalse(self.cpu.flags.get_half_carry_flag())
        self.assertFalse(self.cpu.flags.get_carry_flag())

    def test_RR_A_to_carry(self):
        self.memory.data = [0xCB, 0x1F]
        self.cpu.register_a.set(0b11)
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 8)
        self.assertEqual(self.cpu.register_program_counter.get(), 2)
        self.assertEqual(self.cpu.register_a.get(), 0b1)
        self.assertFalse(self.cpu.flags.get_zero_flag())
        self.assertFalse(self.cpu.flags.get_negative_flag())
        self.assertFalse(self.cpu.flags.get_half_carry_flag())
        self.assertTrue(self.cpu.flags.get_carry_flag())

    def test_RR_A_from_carry(self):
        self.memory.data = [0xCB, 0x1F]
        self.cpu.register_a.set(0b110)
        self.cpu.flags.set_carry_flag()
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 8)
        self.assertEqual(self.cpu.register_program_counter.get(), 2)
        self.assertEqual(self.cpu.register_a.get(), 0b10000011)
        self.assertFalse(self.cpu.flags.get_zero_flag())
        self.assertFalse(self.cpu.flags.get_negative_flag())
        self.assertFalse(self.cpu.flags.get_half_carry_flag())
        self.assertFalse(self.cpu.flags.get_carry_flag())

    def test_RR_HL_pointer(self):
        self.memory.data = [0xCB, 0x1E, 0b10]
        self.cpu.register_hl.set(0x0002)
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 16)
        self.assertEqual(self.cpu.register_program_counter.get(), 2)
        self.assertEqual(self.cpu.memory.read(0x0002), 0b1)
        self.assertFalse(self.cpu.flags.get_zero_flag())
        self.assertFalse(self.cpu.flags.get_negative_flag())
        self.assertFalse(self.cpu.flags.get_half_carry_flag())
        self.assertFalse(self.cpu.flags.get_carry_flag())

    def test_RR_HL_pointer_zero(self):
        self.memory.data = [0xCB, 0x1E, 0b0]
        self.cpu.register_hl.set(0x0002)
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 16)
        self.assertEqual(self.cpu.register_program_counter.get(), 2)
        self.assertEqual(self.cpu.memory.read(0x0002), 0b0)
        self.assertTrue(self.cpu.flags.get_zero_flag())
        self.assertFalse(self.cpu.flags.get_negative_flag())
        self.assertFalse(self.cpu.flags.get_half_carry_flag())
        self.assertFalse(self.cpu.flags.get_carry_flag())

    def test_RR_HL_pointer_to_carry(self):
        self.memory.data = [0xCB, 0x1E, 0b11]
        self.cpu.register_hl.set(0x0002)
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 16)
        self.assertEqual(self.cpu.register_program_counter.get(), 2)
        self.assertEqual(self.cpu.memory.read(0x0002), 0b1)
        self.assertFalse(self.cpu.flags.get_zero_flag())
        self.assertFalse(self.cpu.flags.get_negative_flag())
        self.assertFalse(self.cpu.flags.get_half_carry_flag())
        self.assertTrue(self.cpu.flags.get_carry_flag())

    def test_RR_HL_pointer_from_carry(self):
        self.memory.data = [0xCB, 0x1E, 0b110]
        self.cpu.register_hl.set(0x0002)
        self.cpu.flags.set_carry_flag()
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 16)
        self.assertEqual(self.cpu.register_program_counter.get(), 2)
        self.assertEqual(self.cpu.memory.read(0x0002), 0b10000011)
        self.assertFalse(self.cpu.flags.get_zero_flag())
        self.assertFalse(self.cpu.flags.get_negative_flag())
        self.assertFalse(self.cpu.flags.get_half_carry_flag())
        self.assertFalse(self.cpu.flags.get_carry_flag())

    def test_RRC_A(self):
        self.memory.data = [0xCB, 0x0F]
        self.cpu.register_a.set(0b10)
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 8)
        self.assertEqual(self.cpu.register_program_counter.get(), 2)
        self.assertEqual(self.cpu.register_a.get(), 0b1)
        self.assertFalse(self.cpu.flags.get_zero_flag())
        self.assertFalse(self.cpu.flags.get_negative_flag())
        self.assertFalse(self.cpu.flags.get_half_carry_flag())
        self.assertFalse(self.cpu.flags.get_carry_flag())

    def test_RRC_A_zero(self):
        self.memory.data = [0xCB, 0x0F]
        self.cpu.register_a.set(0b0)
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 8)
        self.assertEqual(self.cpu.register_program_counter.get(), 2)
        self.assertEqual(self.cpu.register_a.get(), 0b0)
        self.assertTrue(self.cpu.flags.get_zero_flag())
        self.assertFalse(self.cpu.flags.get_negative_flag())
        self.assertFalse(self.cpu.flags.get_half_carry_flag())
        self.assertFalse(self.cpu.flags.get_carry_flag())

    def test_RRC_A_to_carry(self):
        self.memory.data = [0xCB, 0x0F]
        self.cpu.register_a.set(0b1)
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 8)
        self.assertEqual(self.cpu.register_program_counter.get(), 2)
        self.assertEqual(self.cpu.register_a.get(), 0b10000000)
        self.assertFalse(self.cpu.flags.get_zero_flag())
        self.assertFalse(self.cpu.flags.get_negative_flag())
        self.assertFalse(self.cpu.flags.get_half_carry_flag())
        self.assertTrue(self.cpu.flags.get_carry_flag())

    def test_RRC_A_from_carry(self):
        self.memory.data = [0xCB, 0x0F]
        self.cpu.register_a.set(0b111)
        self.cpu.flags.set_carry_flag()
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 8)
        self.assertEqual(self.cpu.register_program_counter.get(), 2)
        self.assertEqual(self.cpu.register_a.get(), 0b10000011)
        self.assertFalse(self.cpu.flags.get_zero_flag())
        self.assertFalse(self.cpu.flags.get_negative_flag())
        self.assertFalse(self.cpu.flags.get_half_carry_flag())
        self.assertTrue(self.cpu.flags.get_carry_flag())

    def test_RRC_HL_pointer(self):
        self.memory.data = [0xCB, 0x0E, 0b10]
        self.cpu.register_hl.set(0x0002)
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 16)
        self.assertEqual(self.cpu.register_program_counter.get(), 2)
        self.assertEqual(self.cpu.memory.read(0x0002), 0b1)
        self.assertFalse(self.cpu.flags.get_zero_flag())
        self.assertFalse(self.cpu.flags.get_negative_flag())
        self.assertFalse(self.cpu.flags.get_half_carry_flag())
        self.assertFalse(self.cpu.flags.get_carry_flag())

    def test_RRC_HL_pointer_zero(self):
        self.memory.data = [0xCB, 0x0E, 0b0]
        self.cpu.register_hl.set(0x0002)
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 16)
        self.assertEqual(self.cpu.register_program_counter.get(), 2)
        self.assertEqual(self.cpu.memory.read(0x0002), 0b0)
        self.assertTrue(self.cpu.flags.get_zero_flag())
        self.assertFalse(self.cpu.flags.get_negative_flag())
        self.assertFalse(self.cpu.flags.get_half_carry_flag())
        self.assertFalse(self.cpu.flags.get_carry_flag())

    def test_RRC_HL_pointer_to_carry(self):
        self.memory.data = [0xCB, 0x0E, 0b1]
        self.cpu.register_hl.set(0x0002)
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 16)
        self.assertEqual(self.cpu.register_program_counter.get(), 2)
        self.assertEqual(self.cpu.memory.read(0x0002), 0b10000000)
        self.assertFalse(self.cpu.flags.get_zero_flag())
        self.assertFalse(self.cpu.flags.get_negative_flag())
        self.assertFalse(self.cpu.flags.get_half_carry_flag())
        self.assertTrue(self.cpu.flags.get_carry_flag())

    def test_RRC_HL_pointer_from_carry(self):
        self.memory.data = [0xCB, 0x0E, 0b110]
        self.cpu.register_hl.set(0x0002)
        self.cpu.flags.set_carry_flag()
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 16)
        self.assertEqual(self.cpu.register_program_counter.get(), 2)
        self.assertEqual(self.cpu.memory.read(0x0002), 0b11)
        self.assertFalse(self.cpu.flags.get_zero_flag())
        self.assertFalse(self.cpu.flags.get_negative_flag())
        self.assertFalse(self.cpu.flags.get_half_carry_flag())
        self.assertFalse(self.cpu.flags.get_carry_flag())
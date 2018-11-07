import unittest

from cpu import CPU
from memory import DMGMemory


class ALUInstructionTestCase(unittest.TestCase):
    def setUp(self):
        self.memory = DMGMemory()
        self.cpu = CPU(self.memory)

    def test_XOR_A(self):
        self.memory.boot_rom.data = [0xAF]
        self.cpu.register_a.set(0x12)
        self.cpu.step()
        self.assertEqual(self.cpu.total_clock_cycles_ran, 4)
        self.assertEqual(self.cpu.register_program_counter.get(), 1)
        self.assertEqual(self.cpu.register_a.get(), 0)

    def test_AND_B(self):
        self.memory.boot_rom.data = [0xA0]
        self.cpu.register_a.set(0b10100)
        self.cpu.register_b.set(0b11001)
        self.cpu.step()
        self.assertEqual(self.cpu.total_clock_cycles_ran, 4)
        self.assertEqual(self.cpu.register_program_counter.get(), 1)
        self.assertEqual(self.cpu.register_a.get(), 0b10000)
        self.assertFalse(self.cpu.flags.get_zero_flag())
        self.assertFalse(self.cpu.flags.get_negative_flag())
        self.assertTrue(self.cpu.flags.get_half_carry_flag())
        self.assertFalse(self.cpu.flags.get_carry_flag())

    def test_CP_A(self):
        self.memory.boot_rom.data[0x0000] = 0xBF
        self.cpu.step()
        self.assertEqual(self.cpu.total_clock_cycles_ran, 4)
        self.assertEqual(self.cpu.register_program_counter.get(), 1)
        self.assertTrue(self.cpu.flags.get_zero_flag())
        self.assertTrue(self.cpu.flags.get_negative_flag())
        self.assertFalse(self.cpu.flags.get_half_carry_flag())
        self.assertFalse(self.cpu.flags.get_carry_flag())

    def test_CP_B(self):
        self.memory.boot_rom.data[0x0000] = 0xB8
        self.cpu.register_a.set(0xFF)
        self.cpu.register_b.set(0x01)
        self.cpu.step()
        self.assertEqual(self.cpu.total_clock_cycles_ran, 4)
        self.assertEqual(self.cpu.register_program_counter.get(), 1)
        self.assertFalse(self.cpu.flags.get_zero_flag())
        self.assertTrue(self.cpu.flags.get_negative_flag())
        self.assertFalse(self.cpu.flags.get_half_carry_flag())
        self.assertFalse(self.cpu.flags.get_carry_flag())

    def test_CP_pointer(self):
        self.memory.boot_rom.data[0x0000] = 0xBE
        self.memory.boot_rom.data[0x0001] = 0x01
        self.memory.boot_rom.data[0x0002] = 0x00
        self.cpu.register_a.set(0x00)
        self.cpu.step()
        self.assertEqual(self.cpu.total_clock_cycles_ran, 8)
        self.assertEqual(self.cpu.register_program_counter.get(), 1)
        self.assertFalse(self.cpu.flags.get_zero_flag())
        self.assertTrue(self.cpu.flags.get_negative_flag())
        self.assertTrue(self.cpu.flags.get_half_carry_flag())
        self.assertTrue(self.cpu.flags.get_carry_flag())

    def test_CP_immediate(self):
        self.memory.boot_rom.data[0x0000] = 0xFE
        self.memory.boot_rom.data[0x0001] = 0x80
        self.cpu.register_a.set(0x7F)
        self.cpu.step()
        self.assertEqual(self.cpu.total_clock_cycles_ran, 8)
        self.assertEqual(self.cpu.register_program_counter.get(), 2)
        self.assertFalse(self.cpu.flags.get_zero_flag())
        self.assertTrue(self.cpu.flags.get_negative_flag())
        self.assertFalse(self.cpu.flags.get_half_carry_flag())
        self.assertTrue(self.cpu.flags.get_carry_flag())

    def test_SUB_A(self):
        self.memory.boot_rom.data[0x0000] = 0x97
        self.cpu.register_a.set(0x7F)
        self.cpu.step()
        self.assertEqual(self.cpu.total_clock_cycles_ran, 4)
        self.assertEqual(self.cpu.register_program_counter.get(), 1)
        self.assertTrue(self.cpu.flags.get_zero_flag())
        self.assertTrue(self.cpu.flags.get_negative_flag())
        self.assertFalse(self.cpu.flags.get_half_carry_flag())
        self.assertFalse(self.cpu.flags.get_carry_flag())
        self.assertEqual(self.cpu.register_a.get(), 0x00)

    def test_SUB_B(self):
        self.memory.boot_rom.data[0x0000] = 0x90
        self.cpu.register_a.set(0xFF)
        self.cpu.register_b.set(0x01)
        self.cpu.step()
        self.assertEqual(self.cpu.total_clock_cycles_ran, 4)
        self.assertEqual(self.cpu.register_program_counter.get(), 1)
        self.assertFalse(self.cpu.flags.get_zero_flag())
        self.assertTrue(self.cpu.flags.get_negative_flag())
        self.assertFalse(self.cpu.flags.get_half_carry_flag())
        self.assertFalse(self.cpu.flags.get_carry_flag())
        self.assertEqual(self.cpu.register_a.get(), 0xFE)

    def test_SUB_HL(self):
        self.memory.boot_rom.data[0x0000] = 0x96
        self.memory.boot_rom.data[0x0001] = 0x00
        self.memory.boot_rom.data[0x0002] = 0x00
        self.cpu.register_a.set(0x97)
        self.cpu.step()
        self.assertEqual(self.cpu.total_clock_cycles_ran, 8)
        self.assertEqual(self.cpu.register_program_counter.get(), 1)
        self.assertFalse(self.cpu.flags.get_zero_flag())
        self.assertTrue(self.cpu.flags.get_negative_flag())
        self.assertFalse(self.cpu.flags.get_half_carry_flag())
        self.assertFalse(self.cpu.flags.get_carry_flag())
        self.assertEqual(self.cpu.register_a.get(), 0x01)

    def test_SUB_immediate(self):
        self.memory.boot_rom.data[0x0000] = 0xD6
        self.memory.boot_rom.data[0x0001] = 0x80
        self.cpu.register_a.set(0x7F)
        self.cpu.step()
        self.assertEqual(self.cpu.total_clock_cycles_ran, 8)
        self.assertEqual(self.cpu.register_program_counter.get(), 2)
        self.assertFalse(self.cpu.flags.get_zero_flag())
        self.assertTrue(self.cpu.flags.get_negative_flag())
        self.assertFalse(self.cpu.flags.get_half_carry_flag())
        self.assertTrue(self.cpu.flags.get_carry_flag())
        self.assertEqual(self.cpu.register_a.get(), 0xFF)

    def test_ADD_A(self):
        self.memory.boot_rom.data[0x0000] = 0x87
        self.cpu.register_a.set(0x7F)
        self.cpu.step()
        self.assertEqual(self.cpu.total_clock_cycles_ran, 4)
        self.assertEqual(self.cpu.register_program_counter.get(), 1)
        self.assertFalse(self.cpu.flags.get_zero_flag())
        self.assertFalse(self.cpu.flags.get_negative_flag())
        self.assertTrue(self.cpu.flags.get_half_carry_flag())
        self.assertFalse(self.cpu.flags.get_carry_flag())
        self.assertEqual(self.cpu.register_a.get(), 0xFE)

    def test_ADD_B(self):
        self.memory.boot_rom.data[0x0000] = 0x80
        self.cpu.register_a.set(0xFF)
        self.cpu.register_b.set(0x01)
        self.cpu.step()
        self.assertEqual(self.cpu.total_clock_cycles_ran, 4)
        self.assertEqual(self.cpu.register_program_counter.get(), 1)
        self.assertTrue(self.cpu.flags.get_zero_flag())
        self.assertFalse(self.cpu.flags.get_negative_flag())
        self.assertTrue(self.cpu.flags.get_half_carry_flag())
        self.assertTrue(self.cpu.flags.get_carry_flag())
        self.assertEqual(self.cpu.register_a.get(), 0x00)

    def test_ADD_HL(self):
        self.memory.boot_rom.data[0x0000] = 0x86
        self.memory.boot_rom.data[0x0001] = 0x00
        self.memory.boot_rom.data[0x0002] = 0x00
        self.cpu.register_a.set(0x04)
        self.cpu.step()
        self.assertEqual(self.cpu.total_clock_cycles_ran, 8)
        self.assertEqual(self.cpu.register_program_counter.get(), 1)
        self.assertFalse(self.cpu.flags.get_zero_flag())
        self.assertFalse(self.cpu.flags.get_negative_flag())
        self.assertFalse(self.cpu.flags.get_half_carry_flag())
        self.assertFalse(self.cpu.flags.get_carry_flag())
        self.assertEqual(self.cpu.register_a.get(), 0x8A)

    def test_ADD_immediate(self):
        self.memory.boot_rom.data[0x0000] = 0xC6
        self.memory.boot_rom.data[0x0001] = 0x80
        self.cpu.register_a.set(0x7F)
        self.cpu.step()
        self.assertEqual(self.cpu.total_clock_cycles_ran, 8)
        self.assertEqual(self.cpu.register_program_counter.get(), 2)
        self.assertFalse(self.cpu.flags.get_zero_flag())
        self.assertFalse(self.cpu.flags.get_negative_flag())
        self.assertFalse(self.cpu.flags.get_half_carry_flag())
        self.assertFalse(self.cpu.flags.get_carry_flag())
        self.assertEqual(self.cpu.register_a.get(), 0xFF)

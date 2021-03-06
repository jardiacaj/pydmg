import unittest

from cpu import CPU
from memory import DMGMemory


class INCDECCPUInstructionTestCase(unittest.TestCase):
    def setUp(self):
        self.memory = DMGMemory()
        self.cpu = CPU(self.memory)

    def test_INC_C(self):
        self.memory.boot_rom.data = [0x0C]
        self.cpu.step()
        self.assertEqual(self.cpu.total_clock_cycles_ran, 4)
        self.assertEqual(self.cpu.register_program_counter.get(), 1)
        self.assertEqual(self.cpu.register_c.get(), 0x01)
        self.assertFalse(self.cpu.flags.get_flag('Z'))
        self.assertFalse(self.cpu.flags.get_flag('N'))
        self.assertFalse(self.cpu.flags.get_flag('H'))

    def test_INC_C_half_carry(self):
        self.memory.boot_rom.data = [0x0C]
        self.cpu.register_c.set(0x0F)
        self.cpu.step()
        self.assertEqual(self.cpu.total_clock_cycles_ran, 4)
        self.assertEqual(self.cpu.register_program_counter.get(), 1)
        self.assertEqual(self.cpu.register_c.get(), 0x10)
        self.assertFalse(self.cpu.flags.get_flag('Z'))
        self.assertFalse(self.cpu.flags.get_flag('N'))
        self.assertTrue(self.cpu.flags.get_flag('H'))

    def test_INC_C_zero(self):
        self.memory.boot_rom.data = [0x0C]
        self.cpu.register_c.set(0xFF)
        self.cpu.step()
        self.assertEqual(self.cpu.total_clock_cycles_ran, 4)
        self.assertEqual(self.cpu.register_program_counter.get(), 1)
        self.assertEqual(self.cpu.register_c.get(), 0x00)
        self.assertTrue(self.cpu.flags.get_flag('Z'))
        self.assertFalse(self.cpu.flags.get_flag('N'))
        self.assertTrue(self.cpu.flags.get_flag('H'))

    def test_DEC_A(self):
        self.memory.boot_rom.data = [0x3D]
        self.cpu.step()
        self.assertEqual(self.cpu.total_clock_cycles_ran, 4)
        self.assertEqual(self.cpu.register_program_counter.get(), 1)
        self.assertEqual(self.cpu.register_a.get(), 0xFF)
        self.assertFalse(self.cpu.flags.get_flag('Z'))
        self.assertTrue(self.cpu.flags.get_flag('N'))
        self.assertFalse(self.cpu.flags.get_flag('H'))

    def test_DEC_C_zero(self):
        self.memory.boot_rom.data = [0x3D]
        self.cpu.register_a.set(0x01)
        self.cpu.step()
        self.assertEqual(self.cpu.total_clock_cycles_ran, 4)
        self.assertEqual(self.cpu.register_program_counter.get(), 1)
        self.assertEqual(self.cpu.register_a.get(), 0x00)
        self.assertTrue(self.cpu.flags.get_flag('Z'))
        self.assertTrue(self.cpu.flags.get_flag('N'))
        self.assertTrue(self.cpu.flags.get_flag('H'))

    def test_INC_BC(self):
        self.memory.boot_rom.data = [0x03, 0x03]
        self.cpu.register_bc.set(0xFFFF)
        self.cpu.step()
        self.assertEqual(self.cpu.total_clock_cycles_ran, 8)
        self.assertEqual(self.cpu.register_program_counter.get(), 1)
        self.assertEqual(self.cpu.register_bc.get(), 0x0000)
        self.cpu.step()
        self.assertEqual(self.cpu.total_clock_cycles_ran, 16)
        self.assertEqual(self.cpu.register_program_counter.get(), 2)
        self.assertEqual(self.cpu.register_bc.get(), 0x0001)

    def test_DEC_BC(self):
        self.memory.boot_rom.data = [0x0B, 0x0B]
        self.cpu.register_bc.set(0x0001)
        self.cpu.step()
        self.assertEqual(self.cpu.total_clock_cycles_ran, 8)
        self.assertEqual(self.cpu.register_program_counter.get(), 1)
        self.assertEqual(self.cpu.register_bc.get(), 0x0000)
        self.cpu.step()
        self.assertEqual(self.cpu.total_clock_cycles_ran, 16)
        self.assertEqual(self.cpu.register_program_counter.get(), 2)
        self.assertEqual(self.cpu.register_bc.get(), 0xFFFF)

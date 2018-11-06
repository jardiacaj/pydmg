import unittest

from cpu import CPU
from memory import DMGMemory


class JumpInstructionTestCase(unittest.TestCase):
    def setUp(self):
        self.memory = DMGMemory()
        self.cpu = CPU(self.memory)

    def test_JR(self):
        self.memory.boot_rom.data = [0x18, 0x10]
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 8)
        self.assertEqual(self.cpu.register_program_counter.get(), 0x12)

    def test_JR_NZ_dont_jump(self):
        self.memory.boot_rom.data = [0x20, 0xFE]
        self.cpu.flags.set_zero_flag()
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 8)
        self.assertEqual(self.cpu.register_program_counter.get(), 2)

    def test_JR_NZ_do_jump(self):
        self.memory.boot_rom.data = [0x20, 0xFE]
        self.cpu.flags.reset_zero_flag()
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 8)
        self.assertEqual(self.cpu.register_program_counter.get(), 0)

    def test_JR_Z_dont_jump(self):
        self.memory.boot_rom.data = [0x28, 0xFE]
        self.cpu.flags.reset_zero_flag()
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 8)
        self.assertEqual(self.cpu.register_program_counter.get(), 2)

    def test_JR_Z_do_jump(self):
        self.memory.boot_rom.data = [0x28, 0xFE]
        self.cpu.flags.set_zero_flag()
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 8)
        self.assertEqual(self.cpu.register_program_counter.get(), 0)

    def test_JR_NC_dont_jump(self):
        self.memory.boot_rom.data = [0x30, 0xFE]
        self.cpu.flags.set_carry_flag()
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 8)
        self.assertEqual(self.cpu.register_program_counter.get(), 2)

    def test_JR_NC_do_jump(self):
        self.memory.boot_rom.data = [0x30, 0xFE]
        self.cpu.flags.reset_carry_flag()
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 8)
        self.assertEqual(self.cpu.register_program_counter.get(), 0)

    def test_JR_C_dont_jump(self):
        self.memory.boot_rom.data = [0x38, 0xFE]
        self.cpu.flags.reset_carry_flag()
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 8)
        self.assertEqual(self.cpu.register_program_counter.get(), 2)

    def test_JR_C_do_jump(self):
        self.memory.boot_rom.data = [0x38, 0xFE]
        self.cpu.flags.set_carry_flag()
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 8)
        self.assertEqual(self.cpu.register_program_counter.get(), 0)

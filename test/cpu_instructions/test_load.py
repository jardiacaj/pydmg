import unittest

from cpu import CPU
from memory import DMGMemory


class LoadInstructionTestCase(unittest.TestCase):
    def setUp(self):
        self.memory = DMGMemory()
        self.memory.boot_rom.is_rom = False
        self.cpu = CPU(self.memory)

    def test_LD_A_E(self):
        self.memory.boot_rom.data = [0x7B]
        self.cpu.register_e.set(0x12)
        self.cpu.step()
        self.assertEqual(self.cpu.total_clock_cycles_ran, 4)
        self.assertEqual(self.cpu.register_program_counter.get(), 1)
        self.assertEqual(self.cpu.register_a.get(), 0x12)

    def test_LD_C_A(self):
        self.memory.boot_rom.data = [0x4F]
        self.cpu.register_a.set(0x12)
        self.cpu.step()
        self.assertEqual(self.cpu.total_clock_cycles_ran, 4)
        self.assertEqual(self.cpu.register_program_counter.get(), 1)
        self.assertEqual(self.cpu.register_c.get(), 0x12)

    def test_LD_BC_ADDR_A(self):
        self.memory.boot_rom.data = [0x02]
        self.cpu.register_a.set(0x12)
        self.cpu.step()
        self.assertEqual(self.cpu.total_clock_cycles_ran, 8)
        self.assertEqual(self.cpu.register_program_counter.get(), 1)
        self.assertEqual(self.memory.read(0x0000), 0x12)

    def test_LD_A_ADD_BC(self):
        self.memory.boot_rom.data = [0x0A]
        self.cpu.register_de.set(0x00)
        self.cpu.step()
        self.assertEqual(self.cpu.total_clock_cycles_ran, 8)
        self.assertEqual(self.cpu.register_program_counter.get(), 1)
        self.assertEqual(self.cpu.register_a.get(), 0x0A)

    def test_LD_A_IMM_ADDR(self):
        self.memory.boot_rom.data = [0xFA, 0x01, 0x00]
        self.cpu.step()
        self.assertEqual(self.cpu.total_clock_cycles_ran, 16)
        self.assertEqual(self.cpu.register_program_counter.get(), 3)
        self.assertEqual(self.cpu.register_a.get(), 0x01)

    def test_LD_IMM_ADDR_A(self):
        self.memory.boot_rom.data = [0xEA, 0x02, 0x00]
        self.cpu.register_a.set(0x12)
        self.cpu.step()
        self.assertEqual(self.cpu.total_clock_cycles_ran, 16)
        self.assertEqual(self.cpu.register_program_counter.get(), 3)
        self.assertEqual(self.memory.read(0x0002), 0x12)

    def test_LD__C__A(self):
        # We need big memory to make the write
        self.memory.boot_rom.data = [0xE2] + [0]*65316
        self.cpu.register_a.set(0x12)
        self.cpu.register_c.set(0x24)
        self.cpu.step()
        self.assertEqual(self.cpu.total_clock_cycles_ran, 8)
        self.assertEqual(self.cpu.register_program_counter.get(), 1)
        self.assertEqual(self.memory.read(0xFF24), 0x12)

    def test_LD_A__C(self):
        # LD A,(C)
        # We need big memory to make the read
        self.memory.boot_rom.data = [0xF2] + [0]*65316
        self.memory.write(0xFF24, 0x33)
        self.cpu.register_c.set(0x24)
        self.cpu.step()
        self.assertEqual(self.cpu.total_clock_cycles_ran, 8)
        self.assertEqual(self.cpu.register_program_counter.get(), 1)
        self.assertEqual(self.cpu.register_a.get(), 0x33)

    def test_LD_C_D8(self):
        self.memory.boot_rom.data = [0x0E, 0xFE]
        self.cpu.step()
        self.assertEqual(self.cpu.total_clock_cycles_ran, 8)
        self.assertEqual(self.cpu.register_program_counter.get(), 2)
        self.assertEqual(self.cpu.register_c.get(), 0xFE)

    def test_LDH_N_A(self):
        self.memory.boot_rom.data = [0xE0, 0x12] + [0]*65316
        self.cpu.register_a.set(0x24)
        self.cpu.step()
        self.assertEqual(self.cpu.total_clock_cycles_ran, 12)
        self.assertEqual(self.cpu.register_program_counter.get(), 2)
        self.assertEqual(self.memory.read(0xFF12), 0x24)

    def test_LD_HL_D16(self):
        self.memory.boot_rom.data = [0x21, 0x34, 0x12]
        self.cpu.step()
        self.assertEqual(self.cpu.total_clock_cycles_ran, 12)
        self.assertEqual(self.cpu.register_program_counter.get(), 3)
        self.assertEqual(self.cpu.register_hl.get(), 0x1234)

    def test_LD_SP_D16(self):
        self.memory.boot_rom.data = [0x31, 0x34, 0x12]
        self.cpu.step()
        self.assertEqual(self.cpu.total_clock_cycles_ran, 12)
        self.assertEqual(self.cpu.register_program_counter.get(), 3)
        self.assertEqual(self.cpu.register_stack_pointer.get(), 0x1234)

    def test_LDD_HL_A(self):
        self.memory.boot_rom.data = [0x32, 0x00]
        self.cpu.register_a.set(0x12)
        self.cpu.register_hl.set(0x1)
        self.cpu.step()
        self.assertEqual(self.cpu.total_clock_cycles_ran, 8)
        self.assertEqual(self.cpu.register_program_counter.get(), 1)
        self.assertEqual(self.cpu.register_hl.get(), 0)
        self.assertEqual(self.cpu.memory.read(0x1), 0x12)

    def test_LDD_A_HL(self):
        self.memory.boot_rom.data = [0x3A, 0x12]
        self.cpu.register_hl.set(0x1)
        self.cpu.step()
        self.assertEqual(self.cpu.total_clock_cycles_ran, 8)
        self.assertEqual(self.cpu.register_program_counter.get(), 1)
        self.assertEqual(self.cpu.register_hl.get(), 0)
        self.assertEqual(self.cpu.register_a.get(), 0x12)

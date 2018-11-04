import unittest

from cpu import CPU
from ram import RAM


class SimpleCPUInstructionTestCase(unittest.TestCase):
    def setUp(self):
        self.memory = RAM()
        self.cpu = CPU(self.memory)

    def testNop(self):
        self.memory.data = [0]
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 4)
        self.assertEqual(self.cpu.register_program_counter.get(), 1)

    def test_CALL(self):
        self.memory.data = [0xCD, 0x12, 0x00] + [0]*2**16
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 12)
        self.assertEqual(self.cpu.register_program_counter.get(), 0x12)
        self.assertEqual(self.cpu.stack_pop(), 0x00)
        self.assertEqual(self.cpu.stack_pop(), 0x03)

    def test_PUSH(self):
        self.memory.data = [0xF5] + [0]*2**16
        self.cpu.register_a.set(0x12)
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 16)
        self.assertEqual(self.cpu.register_program_counter.get(), 0x01)
        self.assertEqual(self.cpu.stack_pop(), 0x12)
        self.assertEqual(self.cpu.stack_pop(), 0x00)

    def test_POP(self):
        self.memory.data = [0xC1] + [0]*2**16
        self.cpu.register_stack_pointer.set(0xFFFE)
        self.cpu.stack_push(0x12)
        self.cpu.stack_push(0x34)
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 12)
        self.assertEqual(self.cpu.register_program_counter.get(), 0x01)
        self.assertEqual(self.cpu.register_bc.get(), 0x3412)

    def test_INC_C(self):
        self.memory.data = [0x0C]
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 4)
        self.assertEqual(self.cpu.register_program_counter.get(), 1)
        self.assertEqual(self.cpu.register_c.get(), 0x01)
        self.assertFalse(self.cpu.flags.get_zero_flag())
        self.assertFalse(self.cpu.flags.get_negative_flag())
        self.assertFalse(self.cpu.flags.get_half_carry_flag())

    def test_INC_C_half_carry(self):
        self.memory.data = [0x0C]
        self.cpu.register_c.set(0x0F)
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 4)
        self.assertEqual(self.cpu.register_program_counter.get(), 1)
        self.assertEqual(self.cpu.register_c.get(), 0x10)
        self.assertFalse(self.cpu.flags.get_zero_flag())
        self.assertFalse(self.cpu.flags.get_negative_flag())
        self.assertTrue(self.cpu.flags.get_half_carry_flag())

    def test_INC_C_zero(self):
        self.memory.data = [0x0C]
        self.cpu.register_c.set(0xFF)
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 4)
        self.assertEqual(self.cpu.register_program_counter.get(), 1)
        self.assertEqual(self.cpu.register_c.get(), 0x00)
        self.assertTrue(self.cpu.flags.get_zero_flag())
        self.assertFalse(self.cpu.flags.get_negative_flag())
        self.assertTrue(self.cpu.flags.get_half_carry_flag())

    def test_DEC_A(self):
        self.memory.data = [0x3D]
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 4)
        self.assertEqual(self.cpu.register_program_counter.get(), 1)
        self.assertEqual(self.cpu.register_a.get(), 0xFF)
        self.assertFalse(self.cpu.flags.get_zero_flag())
        self.assertTrue(self.cpu.flags.get_negative_flag())
        self.assertFalse(self.cpu.flags.get_half_carry_flag())

    def test_DEC_C_zero(self):
        self.memory.data = [0x3D]
        self.cpu.register_a.set(0x01)
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 4)
        self.assertEqual(self.cpu.register_program_counter.get(), 1)
        self.assertEqual(self.cpu.register_a.get(), 0x00)
        self.assertTrue(self.cpu.flags.get_zero_flag())
        self.assertTrue(self.cpu.flags.get_negative_flag())
        self.assertTrue(self.cpu.flags.get_half_carry_flag())

    def test_LD_C_A(self):
        self.memory.data = [0x4F]
        self.cpu.register_a.set(0x12)
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 4)
        self.assertEqual(self.cpu.register_program_counter.get(), 1)
        self.assertEqual(self.cpu.register_c.get(), 0x12)

    def test_LD_BC_ADDR_A(self):
        self.memory.data = [0x02]
        self.cpu.register_a.set(0x12)
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 8)
        self.assertEqual(self.cpu.register_program_counter.get(), 1)
        self.assertEqual(self.memory.read(0x0000), 0x12)

    def test_LD_A_ADD_BC(self):
        self.memory.data = [0x0A]
        self.cpu.register_de.set(0x00)
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 8)
        self.assertEqual(self.cpu.register_program_counter.get(), 1)
        self.assertEqual(self.cpu.register_a.get(), 0x0A)

    def test_LD_A_IMM_ADDR(self):
        self.memory.data = [0xFA, 0x01, 0x00]
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 16)
        self.assertEqual(self.cpu.register_program_counter.get(), 3)
        self.assertEqual(self.cpu.register_a.get(), 0x01)

    def test_LD_IMM_ADDR_A(self):
        self.memory.data = [0xEA, 0x02, 0x00]
        self.cpu.register_a.set(0x12)
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 16)
        self.assertEqual(self.cpu.register_program_counter.get(), 3)
        self.assertEqual(self.memory.read(0x0002), 0x12)

    def test_LD__C__A(self):
        # We need big memory to make the write
        self.memory.data = [0xE2] + [0]*65316
        self.cpu.register_a.set(0x12)
        self.cpu.register_c.set(0x24)
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 8)
        self.assertEqual(self.cpu.register_program_counter.get(), 1)
        self.assertEqual(self.memory.read(0xFF24), 0x12)

    def test_LD_A__C(self):
        # LD A,(C)
        # We need big memory to make the read
        self.memory.data = [0xF2] + [0]*65316
        self.memory.write(0xFF24, 0x33)
        self.cpu.register_c.set(0x24)
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 8)
        self.assertEqual(self.cpu.register_program_counter.get(), 1)
        self.assertEqual(self.cpu.register_a.get(), 0x33)

    def test_LD_C_D8(self):
        self.memory.data = [0x0E, 0xFE]
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 8)
        self.assertEqual(self.cpu.register_program_counter.get(), 2)
        self.assertEqual(self.cpu.register_c.get(), 0xFE)

    def test_LDH_N_A(self):
        self.memory.data = [0xE0, 0x12] + [0]*65316
        self.cpu.register_a.set(0x24)
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 12)
        self.assertEqual(self.cpu.register_program_counter.get(), 2)
        self.assertEqual(self.memory.read(0xFF12), 0x24)

    def test_JR_NZ_dont_jump(self):
        self.memory.data = [0x20, 0xFE]  # JR NZ, -2
        self.cpu.flags.reset_zero_flag()
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 8)
        self.assertEqual(self.cpu.register_program_counter.get(), 2)

    def test_JR_NZ_do_jump(self):
        self.memory.data = [0x20, 0xFE]  # JR NZ, -2
        self.cpu.flags.set_zero_flag()
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 8)
        self.assertEqual(self.cpu.register_program_counter.get(), 0)

    def test_LD_HL_D16(self):
        self.memory.data = [0x21, 0x34, 0x12]
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 12)
        self.assertEqual(self.cpu.register_program_counter.get(), 3)
        self.assertEqual(self.cpu.register_hl.get(), 0x1234)

    def test_LD_SP_D16(self):
        self.memory.data = [0x31, 0x34, 0x12]
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 12)
        self.assertEqual(self.cpu.register_program_counter.get(), 3)
        self.assertEqual(self.cpu.register_stack_pointer.get(), 0x1234)

    def test_LDD_HL_A(self):
        self.memory.data = [0x32, 0x00]
        self.cpu.register_a.set(0x12)
        self.cpu.register_hl.set(0x1)
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 8)
        self.assertEqual(self.cpu.register_program_counter.get(), 1)
        self.assertEqual(self.cpu.register_hl.get(), 0)
        self.assertEqual(self.cpu.memory.read(0x1), 0x12)

    def test_LDD_A_HL(self):
        self.memory.data = [0x3A, 0x12]
        self.cpu.register_hl.set(0x1)
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 8)
        self.assertEqual(self.cpu.register_program_counter.get(), 1)
        self.assertEqual(self.cpu.register_hl.get(), 0)
        self.assertEqual(self.cpu.register_a.get(), 0x12)

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

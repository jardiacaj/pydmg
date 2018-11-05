import unittest

from cpu import CPU
from ram import DMGMemory


class StackCPUInstructionTestCase(unittest.TestCase):
    def setUp(self):
        self.memory = DMGMemory()
        self.cpu = CPU(self.memory)

    def test_PUSH(self):
        self.memory.boot_rom.data[0x0000] = 0xF5
        self.cpu.register_a.set(0x12)
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 16)
        self.assertEqual(self.cpu.register_program_counter.get(), 0x01)
        self.assertEqual(self.cpu.stack_pop_byte(), 0x12)
        self.assertEqual(self.cpu.stack_pop_byte(), 0x00)

    def test_POP(self):
        self.memory.boot_rom.data[0x0000] = 0xC1
        self.cpu.register_stack_pointer.set(0xFFFE)
        self.cpu.stack_push_byte(0x12)
        self.cpu.stack_push_byte(0x34)
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 12)
        self.assertEqual(self.cpu.register_program_counter.get(), 0x01)
        self.assertEqual(self.cpu.register_bc.get(), 0x3412)

import unittest

from cpu import CPU
from ram import RAM


class StackCPUInstructionTestCase(unittest.TestCase):
    def setUp(self):
        self.memory = RAM()
        self.cpu = CPU(self.memory)

    def testNop(self):
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 4)
        self.assertEqual(self.cpu.register_program_counter.get(), 1)

    def test_CALL(self):
        self.memory.data[0x0000] = 0xCD
        self.memory.data[0x0001] = 0x12
        self.memory.data[0x0002] = 0x00
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 12)
        self.assertEqual(self.cpu.register_program_counter.get(), 0x12)
        self.assertEqual(self.cpu.stack_pop(), 0x00)
        self.assertEqual(self.cpu.stack_pop(), 0x03)

    def test_RET(self):
        self.memory.data = [0xC9, 0x12, 0x34]
        self.cpu.register_stack_pointer.set(0x01)
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 8)
        self.assertEqual(self.cpu.register_program_counter.get(), 0x1234)

    def test_PUSH(self):
        self.memory.data[0x0000] = 0xF5
        self.cpu.register_a.set(0x12)
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 16)
        self.assertEqual(self.cpu.register_program_counter.get(), 0x01)
        self.assertEqual(self.cpu.stack_pop(), 0x12)
        self.assertEqual(self.cpu.stack_pop(), 0x00)

    def test_POP(self):
        self.memory.data[0x0000] = 0xC1
        self.cpu.register_stack_pointer.set(0xFFFE)
        self.cpu.stack_push(0x12)
        self.cpu.stack_push(0x34)
        self.cpu.tick()
        self.assertEqual(self.cpu.total_clock_cycle_count, 12)
        self.assertEqual(self.cpu.register_program_counter.get(), 0x01)
        self.assertEqual(self.cpu.register_bc.get(), 0x3412)

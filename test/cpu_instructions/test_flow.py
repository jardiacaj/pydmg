import unittest

from cpu import CPU
from memory import DMGMemory


class FlowCPUInstructionTestCase(unittest.TestCase):
    def setUp(self):
        self.memory = DMGMemory()
        self.cpu = CPU(self.memory)

    def test_CALL(self):
        self.memory.boot_rom.data[0x0000] = 0xCD
        self.memory.boot_rom.data[0x0001] = 0x12
        self.memory.boot_rom.data[0x0002] = 0x00
        self.cpu.step()
        self.assertEqual(self.cpu.total_clock_cycles_ran, 12)
        self.assertEqual(self.cpu.register_program_counter.get(), 0x12)
        self.assertEqual(self.cpu.stack_pop_byte(), 0x00)
        self.assertEqual(self.cpu.stack_pop_byte(), 0x03)

    def test_RET(self):
        self.memory.boot_rom.data = [0xC9, 0x12, 0x34]
        self.cpu.register_stack_pointer.set(0x01)
        self.cpu.step()
        self.assertEqual(self.cpu.total_clock_cycles_ran, 8)
        self.assertEqual(self.cpu.register_program_counter.get(), 0x1234)

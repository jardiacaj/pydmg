import unittest

from cpu import CPU
from ram import RAM


class DefaultCPUStackTestCase(unittest.TestCase):
    def setUp(self):
        self.memory = RAM()
        self.memory.data = [0]*2**16
        self.cpu = CPU(self.memory)
        self.cpu.register_stack_pointer.set(0xFFFE)

    def testPushPopStack(self):
        self.cpu.stack_push(0x12)
        self.assertEqual(self.cpu.register_stack_pointer.get(), 0xFFFD)
        self.assertEqual(self.memory.read(0xFFFD), 0x12)
        self.cpu.stack_push(0x24)
        self.assertEqual(self.cpu.register_stack_pointer.get(), 0xFFFC)
        self.assertEqual(self.memory.read(0xFFFC), 0x24)
        popped = self.cpu.stack_pop()
        self.assertEqual(self.cpu.register_stack_pointer.get(), 0xFFFD)
        self.assertEqual(popped, 0x24)
        popped = self.cpu.stack_pop()
        self.assertEqual(self.cpu.register_stack_pointer.get(), 0xFFFE)
        self.assertEqual(popped, 0x12)

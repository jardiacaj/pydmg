import unittest

from cpu import CPU
from memory import DMGMemory
from sound import Sound


class SoundIOTestCase(unittest.TestCase):
    def setUp(self):
        self.sound = Sound()
        self.memory = DMGMemory(sound=self.sound)
        self.sound.memory = self.memory
        self.cpu = CPU(self.memory)

    def test_set_sound_length_and_duty(self):
        self.memory.write(0xFF11, 0b10101010)
        self.assertEqual(self.sound.voices[0].wave_duty, 0b10)
        self.assertEqual(self.sound.voices[0].sound_length, 0b101010)

    def test_read_sound_length_and_duty(self):
        self.sound.voices[0].sound_length = 0b101010
        self.sound.voices[0].wave_duty = 0b10
        self.assertEqual(self.memory.read(0xFF11), 0b10000000)

    def test_set_envelope_and_volume(self):
        self.memory.write(0xFF12, 0b01010001)
        self.assertEqual(self.sound.voices[0].initial_envelope_volume, 0b0101)
        self.assertEqual(self.sound.voices[0].envelope_up, False)
        self.assertEqual(self.sound.voices[0].number_envelope_sweep, 0b001)

    def test_read_envelope_and_volume(self):
        self.sound.voices[0].initial_envelope_volume = 0b1010
        self.sound.voices[0].envelope_up = True
        self.sound.voices[0].number_envelope_sweep = 0b110
        self.assertEqual(self.memory.read(0xFF12), 0b10101110)

    def test_set_frequency_low_byte(self):
        self.memory.write(0xFF13, 0b01010001)
        self.assertEqual(self.sound.voices[0].frequency, 0b01010001)

    def test_read_frequency_low_byte(self):
        self.assertRaises(NotImplementedError, self.memory.read, 0xFF13)

    def test_set_frequency_high_byte(self):
        self.memory.write(0xFF14, 0b11010001)
        self.assertTrue(self.sound.voices[0].initial_bit)
        self.assertTrue(self.sound.voices[0].counter_enabled)
        self.assertEqual(self.sound.voices[0].frequency, 1 << 8)

    def test_read_frequency_high_byte(self):
        self.assertFalse(self.memory.read(0xFF14))

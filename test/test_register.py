import unittest

from register import Register16bit


class SixteenBitRegisterTestCase(unittest.TestCase):
    def setUp(self):
        self.register = Register16bit()

    def test_default_register_data(self):
        self.assertEqual(self.register.get(), 0)

    def test_set(self):
        self.register.set(0xBEEF)
        self.assertEqual(self.register.get(), 0xBEEF)

    def test_set_overflow(self):
        self.register.set(0x3BEEF)
        self.assertEqual(self.register.get(), 0xBEEF)

    def test_add(self):
        self.register.set(0x2345)
        self.register.add(0x2345)
        self.assertEqual(self.register.get(), 0x468A)

    def test_add_overflow(self):
        self.register.set(0xF345)
        self.register.add(0xF345)
        self.assertEqual(self.register.get(), 0xE68A)


class LowerEightBitRegisterTestCase(unittest.TestCase):
    def setUp(self):
        self.combined_register = Register16bit()
        self.higher_register, self.lower_register = \
            self.combined_register.eight_bit_registers

    def test_default_register_data(self):
        self.assertEqual(self.lower_register.get(), 0)
        self.assertEqual(self.higher_register.get(), 0)

    def test_set(self):
        self.lower_register.set(0xBE)
        self.assertEqual(self.combined_register.data, 0xBE)
        self.assertEqual(self.lower_register.get(), 0xBE)
        self.assertEqual(self.higher_register.get(), 0)

    def test_set_overflow(self):
        self.lower_register.set(0x3BE)
        self.assertEqual(self.combined_register.data, 0xBE)
        self.assertEqual(self.lower_register.get(), 0xBE)
        self.assertEqual(self.higher_register.get(), 0)

    def test_add(self):
        self.lower_register.set(0x23)
        self.lower_register.add(0x23)
        self.assertEqual(self.combined_register.data, 0x46)
        self.assertEqual(self.lower_register.get(), 0x46)
        self.assertEqual(self.higher_register.get(), 0)

    def test_add_overflow(self):
        self.lower_register.set(0xFF)
        self.lower_register.add(0xFF)
        self.assertEqual(self.combined_register.data, 0xFE)
        self.assertEqual(self.lower_register.get(), 0xFE)
        self.assertEqual(self.higher_register.get(), 0)


class HigherEightBitRegisterTestCase(unittest.TestCase):
    def setUp(self):
        self.combined_register = Register16bit()
        self.higher_register, self.lower_register = \
            self.combined_register.eight_bit_registers

    def test_default_register_data(self):
        self.assertEqual(self.higher_register.get(), 0)
        self.assertEqual(self.lower_register.get(), 0)

    def test_set(self):
        self.higher_register.set(0xBE)
        self.assertEqual(self.combined_register.data, 0xBE << 8)
        self.assertEqual(self.higher_register.get(), 0xBE)
        self.assertEqual(self.lower_register.get(), 0)

    def test_set_overflow(self):
        self.higher_register.set(0x3BE)
        self.assertEqual(self.combined_register.data, 0xBE << 8)
        self.assertEqual(self.higher_register.get(), 0xBE)
        self.assertEqual(self.lower_register.get(), 0)

    def test_add(self):
        self.higher_register.set(0x23)
        self.higher_register.add(0x23)
        self.assertEqual(self.combined_register.data, 0x46 << 8)
        self.assertEqual(self.higher_register.get(), 0x46)
        self.assertEqual(self.lower_register.get(), 0)

    def test_add_overflow(self):
        self.higher_register.set(0xFF)
        self.higher_register.add(0xFF)
        self.assertEqual(self.combined_register.data, 0xFE << 8)
        self.assertEqual(self.higher_register.get(), 0xFE)
        self.assertEqual(self.lower_register.get(), 0)


class FlagRegisterTestCase(unittest.TestCase):
    def setUp(self):
        self.combined_register = Register16bit(contains_flags=True)
        self.higher_register, self.flags_register = \
            self.combined_register.eight_bit_registers

    def test_default_register_data(self):
        self.assertEqual(self.higher_register.get(), 0)
        self.assertEqual(self.flags_register.get(), 0)
        self.assertFalse(self.flags_register.get_flag('Z'))
        self.assertFalse(self.flags_register.get_flag('N'))
        self.assertFalse(self.flags_register.get_flag('H'))
        self.assertFalse(self.flags_register.get_flag('C'))

    def test_set_reset_zero(self):
        self.flags_register.reset_flag('Z')
        self.assertFalse(self.flags_register.get_flag('Z'))
        self.assertFalse(self.flags_register.get_flag('N'))
        self.assertFalse(self.flags_register.get_flag('H'))
        self.assertFalse(self.flags_register.get_flag('C'))
        self.flags_register.set_flag('Z')
        self.assertTrue(self.flags_register.get_flag('Z'))
        self.assertFalse(self.flags_register.get_flag('N'))
        self.assertFalse(self.flags_register.get_flag('H'))
        self.assertFalse(self.flags_register.get_flag('C'))
        self.flags_register.reset_flag('Z')
        self.assertFalse(self.flags_register.get_flag('Z'))
        self.assertFalse(self.flags_register.get_flag('N'))
        self.assertFalse(self.flags_register.get_flag('H'))
        self.assertFalse(self.flags_register.get_flag('C'))

    def test_set_reset_negative(self):
        self.flags_register.reset_flag('Z')
        self.assertFalse(self.flags_register.get_flag('Z'))
        self.assertFalse(self.flags_register.get_flag('N'))
        self.assertFalse(self.flags_register.get_flag('H'))
        self.assertFalse(self.flags_register.get_flag('C'))
        self.flags_register.set_flag('N')
        self.assertFalse(self.flags_register.get_flag('Z'))
        self.assertTrue(self.flags_register.get_flag('N'))
        self.assertFalse(self.flags_register.get_flag('H'))
        self.assertFalse(self.flags_register.get_flag('C'))
        self.flags_register.reset_flag('N')
        self.assertFalse(self.flags_register.get_flag('Z'))
        self.assertFalse(self.flags_register.get_flag('N'))
        self.assertFalse(self.flags_register.get_flag('H'))
        self.assertFalse(self.flags_register.get_flag('C'))

    def test_set_reset_half_carry(self):
        self.flags_register.reset_flag('Z')
        self.assertFalse(self.flags_register.get_flag('Z'))
        self.assertFalse(self.flags_register.get_flag('N'))
        self.assertFalse(self.flags_register.get_flag('H'))
        self.assertFalse(self.flags_register.get_flag('C'))
        self.flags_register.set_flag('H')
        self.assertFalse(self.flags_register.get_flag('Z'))
        self.assertFalse(self.flags_register.get_flag('N'))
        self.assertTrue(self.flags_register.get_flag('H'))
        self.assertFalse(self.flags_register.get_flag('C'))
        self.flags_register.reset_flag('H')
        self.assertFalse(self.flags_register.get_flag('Z'))
        self.assertFalse(self.flags_register.get_flag('N'))
        self.assertFalse(self.flags_register.get_flag('H'))
        self.assertFalse(self.flags_register.get_flag('C'))

    def test_set_reset_carry(self):
        self.flags_register.reset_flag('Z')
        self.assertFalse(self.flags_register.get_flag('Z'))
        self.assertFalse(self.flags_register.get_flag('N'))
        self.assertFalse(self.flags_register.get_flag('H'))
        self.assertFalse(self.flags_register.get_flag('C'))
        self.flags_register.set_flag('C')
        self.assertFalse(self.flags_register.get_flag('Z'))
        self.assertFalse(self.flags_register.get_flag('N'))
        self.assertFalse(self.flags_register.get_flag('H'))
        self.assertTrue(self.flags_register.get_flag('C'))
        self.flags_register.reset_flag('C')
        self.assertFalse(self.flags_register.get_flag('Z'))
        self.assertFalse(self.flags_register.get_flag('N'))
        self.assertFalse(self.flags_register.get_flag('H'))
        self.assertFalse(self.flags_register.get_flag('C'))

    def test_set_all(self):
        self.flags_register.set_all()
        self.assertFalse(self.flags_register.get_flag('Z'))
        self.assertFalse(self.flags_register.get_flag('N'))
        self.assertFalse(self.flags_register.get_flag('H'))
        self.assertFalse(self.flags_register.get_flag('C'))
        self.flags_register.set_all(True, True, True, True)
        self.assertTrue(self.flags_register.get_flag('Z'))
        self.assertTrue(self.flags_register.get_flag('N'))
        self.assertTrue(self.flags_register.get_flag('H'))
        self.assertTrue(self.flags_register.get_flag('C'))
        self.flags_register.set_all(zero=True, carry=True)
        self.assertTrue(self.flags_register.get_flag('Z'))
        self.assertFalse(self.flags_register.get_flag('N'))
        self.assertFalse(self.flags_register.get_flag('H'))
        self.assertTrue(self.flags_register.get_flag('C'))
        self.flags_register.set_all()
        self.assertFalse(self.flags_register.get_flag('Z'))
        self.assertFalse(self.flags_register.get_flag('N'))
        self.assertFalse(self.flags_register.get_flag('H'))
        self.assertFalse(self.flags_register.get_flag('C'))

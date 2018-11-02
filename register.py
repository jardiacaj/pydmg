class Register8bit:
    # combined_register is the 16-bit register that contains this 8-bit one
    def __init__(self, combined_register, is_lower):
        self.combined_register = combined_register
        self.is_lower = is_lower

    def get(self):
        if self.is_lower:
            return self.combined_register.data % 256
        else:
            return self.combined_register.data >> 8

    def set(self, value):
        if self.is_lower:
            self.combined_register.data = (
                (self.combined_register.data >> 8 << 8) + (value % 256)
            )
        else:
            self.combined_register.data = (
                (self.combined_register.data % 256) + ((value % 256) << 8)
            )

    def add(self, value):
        new_value = (self.get() + value) % 256
        self.set(new_value)


class FlagRegister(Register8bit):
    def set_zero_flag(self):
        self.combined_register.data |= 1 << 7

    def reset_zero_flag(self):
        self.combined_register.data &= 2**16 - (1 << 7)

    def get_zero_flag(self):
        return self.combined_register.data & (1 << 7)

    def set_negative_flag(self):
        self.combined_register.data |= 1 << 6

    def reset_negative_flag(self):
        self.combined_register.data &= 2**16 - 1 << 6

    def get_negative_flag(self):
        return self.combined_register.data & (1 << 6)

    def set_half_carry_flag(self):
        self.combined_register.data |= 1 << 5

    def reset_half_carry_flag(self):
        self.combined_register.data &= 2**16 - 1 << 5

    def get_half_carry_flag(self):
        return self.combined_register.data & (1 << 5)

    def set_carry_flag(self):
        self.combined_register.data |= 1 << 4

    def reset_carry_flag(self):
        self.combined_register.data &= 2**16 - 1 << 4

    def get_carry_flag(self):
        return self.combined_register.data & (1 << 4)


class Register16bit:
    def __init__(self, contains_flags=False):
        self.data = 0
        self.contains_flags = contains_flags

    def eight_bit_registers(self):
        # returns higher, lower
        return Register8bit(self, is_lower=False), \
               FlagRegister(self, is_lower=True) \
                   if self.contains_flags \
                   else Register8bit(self, is_lower=True)

    def get(self):
        return self.data

    def set(self, value):
        self.data = value % 2**16

    def add(self, value):
        self.data = (self.data + value) % 2**16

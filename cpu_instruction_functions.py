def nop(cpu):
    pass


def ld_sp_d16(cpu):
    immediate_1 = self.memory.read(self.program_counter + 1)
    immediate_2 = self.memory.read(self.program_counter + 2)
    self.program_counter += 2
    self.register_sp = immediate_1 << 8 + immediate_2


def xor_a(cpu):
    self.total_clock_cycle_count += 4
    self.register_a = 0
    self.flag_zero = True
    self.flag_negative = False
    self.flag_half_carry = False
    self.flag_carry = False

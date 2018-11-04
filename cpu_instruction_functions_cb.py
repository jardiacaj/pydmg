from cpu_registers import get_register


def register_bit_test(register_id, bit):
    def instruction(cpu):
        register = get_register(register_id, cpu)
        register = register.get()
        if register & (1 << bit):
            cpu.flags.reset_zero_flag()
        else:
            cpu.flags.set_zero_flag()
        cpu.flags.reset_negative_flag()
        cpu.flags.set_half_carry_flag()
    return instruction


def pointer_bit_test(register_id, bit):
    def instruction(cpu):
        register = get_register(register_id, cpu)
        value = cpu.memory.read(register.get())
        if value & (1 << bit):
            cpu.flags.reset_zero_flag()
        else:
            cpu.flags.set_zero_flag()
        cpu.flags.reset_negative_flag()
        cpu.flags.set_half_carry_flag()
    return instruction

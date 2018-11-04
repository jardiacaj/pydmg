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


def rotate_8bit_register_left(register_id, through_carry):
    def instruction(cpu):
        register = get_register(register_id, cpu)
        value = register.get()
        value = value << 1
        if through_carry and cpu.flags.get_carry_flag():
            value += 1
        cpu.flags.set_all(
            zero=(value % 256) == 0,
            negative=False,
            half_carry=False,
            carry=(value // 256)
        )
        register.set(value % 256)
    return instruction


def rotate_pointer_left(register_id, through_carry):
    def instruction(cpu):
        register = get_register(register_id, cpu)
        value = cpu.memory.read(register.get())
        value = value << 1
        if through_carry and cpu.flags.get_carry_flag():
            value += 1
        cpu.flags.set_all(
            zero=(value % 256) == 0,
            negative=False,
            half_carry=False,
            carry=(value // 256)
        )
        cpu.memory.write(register.get(), value % 256)
    return instruction

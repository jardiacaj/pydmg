from cpu_registers import get_register


def register_bit_test(register_id, bit):
    def instruction(cpu):
        register = get_register(register_id, cpu)
        register_value = register.get()
        if register_value & (1 << bit):
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
        carry = (value & 0b10000000)
        value = (value << 1) % 256
        if through_carry and cpu.flags.get_carry_flag():
            value += 1
        if not through_carry and carry:
            value += 1
        cpu.flags.set_all(
            zero=value == 0,
            negative=False,
            half_carry=False,
            carry=carry
        )
        register.set(value)
    return instruction


def rotate_pointer_left(register_id, through_carry):
    def instruction(cpu):
        register = get_register(register_id, cpu)
        value = cpu.memory.read(register.get())
        carry = (value & 0b10000000)
        value = (value << 1) % 256
        if through_carry and cpu.flags.get_carry_flag():
            value += 1
        if not through_carry and carry:
            value += 1
        cpu.flags.set_all(
            zero=value == 0,
            negative=False,
            half_carry=False,
            carry=carry
        )
        cpu.memory.write(register.get(), value)
    return instruction


def rotate_8bit_register_right(register_id, through_carry):
    def instruction(cpu):
        register = get_register(register_id, cpu)
        value = register.get()
        carry = value % 2
        value = value >> 1
        if through_carry and cpu.flags.get_carry_flag():
            value += 128
        if not through_carry and carry:
            value += 128
        cpu.flags.set_all(
            zero=value == 0,
            negative=False,
            half_carry=False,
            carry=carry
        )
        register.set(value % 256)
    return instruction


def rotate_pointer_right(register_id, through_carry):
    def instruction(cpu):
        register = get_register(register_id, cpu)
        value = cpu.memory.read(register.get())
        carry = value % 2
        value = value >> 1
        if through_carry and cpu.flags.get_carry_flag():
            value += 128
        if not through_carry and carry:
            value += 128
        cpu.flags.set_all(
            zero=value == 0,
            negative=False,
            half_carry=False,
            carry=carry
        )
        cpu.memory.write(register.get(), value % 256)
    return instruction

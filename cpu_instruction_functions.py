from cpu_registers import get_register


def immediates_to_16bit(first_immediate, second_immediate):
    return first_immediate + (second_immediate << 8)


def twos_complement(val, bits):
    if (val & (1 << (bits - 1))) != 0:
        val = val - (1 << bits)
    return val


def nop(cpu):
    pass


def call(cpu, first_immediate, second_immediate):
    cpu.stack_push(
        cpu.register_program_counter.lower_eight_bit_register.get())
    cpu.stack_push(
        cpu.register_program_counter.higher_eight_bit_register.get())
    cpu.register_program_counter.set(
        immediates_to_16bit(first_immediate, second_immediate)
    )


def push(register_id):
    def instruction(cpu):
        register = get_register(register_id, cpu)
        cpu.stack_push(register.lower_eight_bit_register.get())
        cpu.stack_push(register.higher_eight_bit_register.get())
    return instruction


def load_8bit_immediate_to_register(register_id):
    def instruction(cpu, immediate):
        register = get_register(register_id, cpu)
        register.set(immediate)
    return instruction


def ld_c_a(cpu):
    cpu.memory.write(
        0xFF00 + cpu.register_c.get(),
        cpu.register_a.get()
    )


def ld_a_c(cpu):
    cpu.register_a.set(
        cpu.memory.read(
            cpu.register_c.get() + 0xFF00
        )
    )


def load_register_to_register(target_register_id, source_register_id):
    def instruction(cpu):
        target = get_register(target_register_id, cpu)
        source = get_register(source_register_id, cpu)
        target.set(source.get())
    return instruction


def put_register_to_register_address(target_pointer_id, source_register_id):
    def instruction(cpu):
        target_pointer = get_register(target_pointer_id, cpu)
        source = get_register(source_register_id, cpu)
        cpu.memory.write(
            target_pointer.get(),
            source.get()
        )
    return instruction


def load_register_address_to_register(target_register_id, source_register_id):
    def instruction(cpu):
        source_register = get_register(source_register_id, cpu)
        target_register = get_register(target_register_id, cpu)
        target_register.set(
            cpu.memory.read(source_register.get())
        )
    return instruction


def load_immediate_address_to_register(target_register_id):
    def instruction(cpu, first_immediate, second_immediate):
        target_register = get_register(target_register_id, cpu)
        target_register.set(
            cpu.memory.read(
                immediates_to_16bit(first_immediate, second_immediate)
            )
        )
    return instruction


def put_register_to_immediate_address(register_id):
    def instruction(cpu, first_immediate, second_immediate):
        register = get_register(register_id, cpu)
        cpu.memory.write(
            immediates_to_16bit(first_immediate, second_immediate),
            register.get()
        )

    return instruction


def ldh_n_a(cpu, immediate):
    cpu.memory.write(
        0xFF00 + immediate,
        cpu.register_a.get()
    )


def ldh_a_n(cpu, immediate):
    cpu.register_a.set(
        cpu.memory.read(
            0xFF0 + immediate
        )
    )


def increment_register(register_id):
    def instruction(cpu):
        register = get_register(register_id, cpu)
        register.add(1)
        cpu.flags.write_half_carry_flag(register.get() == 0x10)
        cpu.flags.write_zero_flag(register.get() == 0x00)
        cpu.flags.reset_negative_flag()
    return instruction


def relative_jump_if_not_zero(cpu, immediate):
    if cpu.flags.get_zero_flag():
        cpu.register_program_counter.add(twos_complement(immediate, 8))


def ld_sp_d16(cpu, first_immediate, second_immediate):
    cpu.register_stack_pointer.higher_eight_bit_register.set(second_immediate)
    cpu.register_stack_pointer.lower_eight_bit_register.set(first_immediate)


def load_16bit_immediate_to_register(register_id):
    def instruction(cpu, first_immediate, second_immediate):
        register = get_register(register_id, cpu)
        register.higher_eight_bit_register.set(second_immediate)
        register.lower_eight_bit_register.set(first_immediate)
    return instruction


def ldd_hl_a(cpu):
    cpu.memory.write(cpu.register_hl.get(), cpu.register_a.get())
    cpu.register_hl.add(-1)


def ldi_hl_a(cpu):
    cpu.memory.write(cpu.register_hl.get(), cpu.register_a.get())
    cpu.register_hl.add(1)


def ldd_a_hl(cpu):
    cpu.register_a.set(
        cpu.memory.read(cpu.register_hl.get())
    )
    cpu.register_hl.add(-1)


def ldi_a_hl(cpu):
    cpu.register_a.set(
        cpu.memory.read(cpu.register_hl.get())
    )
    cpu.register_hl.add(1)


def xor(register_id):
    def instruction(cpu):
        register = get_register(register_id, cpu)
        cpu.register_a.set(
            cpu.register_a.get() ^ register.get()
        )
        cpu.flags.set_all(
            zero=(cpu.register_a.get() == 0),
            negative=False,
            half_carry=False,
            carry=False,
        )
    return instruction


def and_instruction(register_id):
    def instruction(cpu):
        register = get_register(register_id, cpu)
        result = cpu.register_a.get() & register.get()
        cpu.register_a.set(result)
        cpu.flags.set_all(
            zero=(cpu.register_a.get() == 0),
            negative=False,
            half_carry=True,
            carry=False,
        )
    return instruction


def h_register_bit_test(bit):
    def instruction(cpu):
        h = cpu.register_h.get()
        if h & (1 << bit):
            cpu.flags.reset_zero_flag()
        else:
            cpu.flags.set_zero_flag()
        cpu.flags.reset_negative_flag()
        cpu.flags.set_half_carry_flag()
    return instruction

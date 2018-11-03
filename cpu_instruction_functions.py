from cpu_registers import get_register


def twos_complement(val, bits):
    if (val & (1 << (bits - 1))) != 0:
        val = val - (1 << bits)
    return val


def nop(cpu):
    pass


def ld_c_d8(cpu, immediate):
    cpu.register_c.set(immediate)


def ld_a_d8(cpu, immediate):
    cpu.register_a.set(immediate)


def ld_c_a(cpu):
    cpu.memory.write(
        0xFF00 + cpu.register_c.get(),
        cpu.register_a.get()
    )


def ld_n_a(register_id):
    def instruction(cpu):
        register = get_register(register_id, cpu)
        register.set(cpu.register_a.get())
    return instruction


def ld_addr_a(register_id):
    def instruction(cpu):
        register = get_register(register_id, cpu)
        cpu.memory.write(
            register.get(),
            cpu.register_a.get()
        )
    return instruction


def ld_imm_add_a(cpu, first_immediate, second_immediate):
    cpu.memory.write(
        first_immediate + (second_immediate << 8),
        cpu.register_a.get()
    )


def ldh_n_a(cpu, immediate):
    cpu.memory.write(
        0xFF00 + immediate,
        cpu.register_a.get()
    )


def inc(register_id):
    def instruction(cpu):
        register = get_register(register_id, cpu)
        register.add(1)
        cpu.flags.write_half_carry_flag(register.get() == 0x10)
        cpu.flags.write_zero_flag(register.get() == 0x00)
        cpu.flags.reset_negative_flag()
    return instruction


def jr_nz(cpu, immediate):
    if cpu.flags.get_zero_flag():
        cpu.register_program_counter.add(twos_complement(immediate, 8))


def ld_sp_d16(cpu, first_immediate, second_immediate):
    cpu.register_stack_pointer.higher_eight_bit_register.set(second_immediate)
    cpu.register_stack_pointer.lower_eight_bit_register.set(first_immediate)


def ld_hl_d16(cpu, first_immediate, second_immediate):
    cpu.register_h.set(second_immediate)
    cpu.register_l.set(first_immediate)


def ldd_hl_a(cpu):
    cpu.memory.write(cpu.register_hl.get(), cpu.register_a.get())
    cpu.register_hl.add(-1)


def xor_a(cpu):
    cpu.register_a.set(0)
    cpu.flags.set_all(zero=True)


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

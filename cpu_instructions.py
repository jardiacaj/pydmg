"""
Instructions (and cb_instructions) is a dict of command descriptors keyed by
opcode

The descriptors are tuples formed like this:
 * Name
 * Mnemonic
 * Length in bytes
 * Duration in clock cycles
 * Flags affected (Z N H C)
 * Function
"""
import cpu_instruction_functions
import cpu_instruction_functions_cb
import cpu_registers


def load_8bit_immediate_to_register(register):
    return (
        "Load 8-bit immediate to {}".format(register),
        "LD {},d8".format(register), 2, 8, None,
        cpu_instruction_functions.load_8bit_immediate_to_register(register)
    )


def load_16bit_immediate_to_register(register):
    return (
        "Load 16-bit immediate to {}".format(register),
        "LD {},d16".format(register), 3, 12, None,
        cpu_instruction_functions.load_16bit_immediate_to_register(register)
     )


def load_pointer_to_register(target_register, source_pointer):
    return (
        "Put value ({}) into {}".format(source_pointer, target_register),
        "LD {}, ({})".format(target_register, source_pointer), 1, 8, None,
        cpu_instruction_functions.load_register_address_to_register(
            target_register,
            source_pointer
        )
    )


def load_immediate_pointer_to_register(target_register):
    return (
        "Put value (d16) into {}".format(target_register),
        "LD {}, (d16)".format(target_register), 3, 16, None,
        cpu_instruction_functions.load_immediate_address_to_register(
            target_register
        )
    )


def put_register_to_pointer(target_pointer, source):
    return (
        "Put value {} into address ({})".format(source, target_pointer),
        "LD ({}),{}".format(target_pointer, source), 1, 8, None,
        cpu_instruction_functions.put_register_to_register_address(
            target_pointer,
            source
        )
    )


def put_register_to_immediate_pointer(register):
    return(
        "Put value {} into immediate address".format(register),
        "LD (d16),{}".format(register), 3, 16, None,
        cpu_instruction_functions.put_register_to_immediate_address(register)
    )


def increment(register):
    return (
        "Increment {}".format(register),
        "INC {}".format(register), 1, 4, 'Z0H-',
        cpu_instruction_functions.increment_register(register)
    )


def load_8bit_register_to_register(target, source):
    return (
        "Put {} into {}".format(source, target),
        "LD {},{}".format(target, source), 1, 4, None,
        cpu_instruction_functions.load_register_to_register(target, source)
    )


def load_16bit_register_to_register(target, source):
    return (
        "Put {} into {}".format(source, target),
        "LD {},{}".format(target, source), 1, 8, None,
        cpu_instruction_functions.load_register_to_register(target, source)
    )


def xor(register):
    return (
        "XOR {} with A, store to A".format(register),
        "XOR {}".format(register), 1, 4, 'Z000',
        cpu_instruction_functions.xor(register)
    )


def and_instruction(register):
    return (
        "AND {} with A, store to A".format(register),
        "AND {}".format(register), 1, 4, 'Z010',
        cpu_instruction_functions.and_instruction(register)
    )


def push(register):
    return (
        "Push register pair {} to stack and decrement SP twice".format(
            register),
        "PUSH {}".format(register), 1, 16, None,
        cpu_instruction_functions.push(register)
    )


def pop(register):
    return (
        "Pop to register pair {} from stack and increment SP twice".format(
            register),
        "POP {}".format(register), 1, 12, None,
        cpu_instruction_functions.pop(register)
    )


instructions = {

    0x00: ("No operation", "NOP", 1, 4, None, cpu_instruction_functions.nop),

    0x07: (
        "Rotate A left", "RLCA", 1, 4, 'Z00C',
        cpu_instruction_functions_cb.rotate_8bit_register_left(
            cpu_registers.A, through_carry=False)
    ),
    0x17: (
        "Rotate A left through carry", "RLA", 1, 4, 'Z00C',
        cpu_instruction_functions_cb.rotate_8bit_register_left(
            cpu_registers.A, through_carry=True)
    ),
    0x0F: (
        "Rotate A right", "RRCA", 1, 4, 'Z00C',
        cpu_instruction_functions_cb.rotate_8bit_register_right(
            cpu_registers.A, through_carry=False)
    ),
    0x1F: (
        "Rotate A right through carry", "RRA", 1, 4, 'Z00C',
        cpu_instruction_functions_cb.rotate_8bit_register_right(
            cpu_registers.A, through_carry=True)
    ),

    0x3C: increment(cpu_registers.A),
    0x04: increment(cpu_registers.B),
    0x0C: increment(cpu_registers.C),
    0x14: increment(cpu_registers.D),
    0x1C: increment(cpu_registers.E),
    0x24: increment(cpu_registers.H),
    0x2C: increment(cpu_registers.L),

    0x7F: load_8bit_register_to_register(cpu_registers.A, cpu_registers.A),
    0x78: load_8bit_register_to_register(cpu_registers.A, cpu_registers.B),
    0x79: load_8bit_register_to_register(cpu_registers.A, cpu_registers.C),
    0x7A: load_8bit_register_to_register(cpu_registers.A, cpu_registers.D),
    0x7B: load_8bit_register_to_register(cpu_registers.A, cpu_registers.E),
    0x7C: load_8bit_register_to_register(cpu_registers.A, cpu_registers.H),
    0x7D: load_8bit_register_to_register(cpu_registers.A, cpu_registers.L),

    0x40: load_8bit_register_to_register(cpu_registers.B, cpu_registers.B),
    0x41: load_8bit_register_to_register(cpu_registers.B, cpu_registers.C),
    0x42: load_8bit_register_to_register(cpu_registers.B, cpu_registers.D),
    0x43: load_8bit_register_to_register(cpu_registers.B, cpu_registers.E),
    0x44: load_8bit_register_to_register(cpu_registers.B, cpu_registers.H),
    0x45: load_8bit_register_to_register(cpu_registers.B, cpu_registers.L),
    0x47: load_8bit_register_to_register(cpu_registers.B, cpu_registers.A),

    0x48: load_8bit_register_to_register(cpu_registers.C, cpu_registers.B),
    0x49: load_8bit_register_to_register(cpu_registers.C, cpu_registers.C),
    0x4A: load_8bit_register_to_register(cpu_registers.C, cpu_registers.D),
    0x4B: load_8bit_register_to_register(cpu_registers.C, cpu_registers.E),
    0x4C: load_8bit_register_to_register(cpu_registers.C, cpu_registers.H),
    0x4D: load_8bit_register_to_register(cpu_registers.C, cpu_registers.L),
    0x4F: load_8bit_register_to_register(cpu_registers.C, cpu_registers.A),

    0x50: load_8bit_register_to_register(cpu_registers.D, cpu_registers.B),
    0x51: load_8bit_register_to_register(cpu_registers.D, cpu_registers.C),
    0x52: load_8bit_register_to_register(cpu_registers.D, cpu_registers.D),
    0x53: load_8bit_register_to_register(cpu_registers.D, cpu_registers.E),
    0x54: load_8bit_register_to_register(cpu_registers.D, cpu_registers.H),
    0x55: load_8bit_register_to_register(cpu_registers.D, cpu_registers.L),
    0x57: load_8bit_register_to_register(cpu_registers.D, cpu_registers.A),

    0x58: load_8bit_register_to_register(cpu_registers.E, cpu_registers.B),
    0x59: load_8bit_register_to_register(cpu_registers.E, cpu_registers.C),
    0x5A: load_8bit_register_to_register(cpu_registers.E, cpu_registers.D),
    0x5B: load_8bit_register_to_register(cpu_registers.E, cpu_registers.E),
    0x5C: load_8bit_register_to_register(cpu_registers.E, cpu_registers.H),
    0x5D: load_8bit_register_to_register(cpu_registers.E, cpu_registers.L),
    0x5F: load_8bit_register_to_register(cpu_registers.E, cpu_registers.A),

    0x60: load_8bit_register_to_register(cpu_registers.H, cpu_registers.B),
    0x61: load_8bit_register_to_register(cpu_registers.H, cpu_registers.C),
    0x62: load_8bit_register_to_register(cpu_registers.H, cpu_registers.D),
    0x63: load_8bit_register_to_register(cpu_registers.H, cpu_registers.E),
    0x64: load_8bit_register_to_register(cpu_registers.H, cpu_registers.H),
    0x65: load_8bit_register_to_register(cpu_registers.H, cpu_registers.L),
    0x67: load_8bit_register_to_register(cpu_registers.H, cpu_registers.A),

    0x68: load_8bit_register_to_register(cpu_registers.L, cpu_registers.B),
    0x69: load_8bit_register_to_register(cpu_registers.L, cpu_registers.C),
    0x6A: load_8bit_register_to_register(cpu_registers.L, cpu_registers.D),
    0x6B: load_8bit_register_to_register(cpu_registers.L, cpu_registers.E),
    0x6C: load_8bit_register_to_register(cpu_registers.L, cpu_registers.H),
    0x6D: load_8bit_register_to_register(cpu_registers.L, cpu_registers.L),
    0x6F: load_8bit_register_to_register(cpu_registers.L, cpu_registers.A),

    0x02: put_register_to_pointer(cpu_registers.BC, cpu_registers.A),
    0x12: put_register_to_pointer(cpu_registers.DE, cpu_registers.A),
    0x77: put_register_to_pointer(cpu_registers.HL, cpu_registers.A),
    0xEA: put_register_to_immediate_pointer(cpu_registers.A),

    0x0A: load_pointer_to_register(cpu_registers.A, cpu_registers.BC),
    0x1A: load_pointer_to_register(cpu_registers.A, cpu_registers.DE),
    0x7E: load_pointer_to_register(cpu_registers.A, cpu_registers.HL),
    0xFA: load_immediate_pointer_to_register(cpu_registers.A),

    0x20: ("Relative jump if not zero",
           "JR NZ,d8", 2, 8, None,
           cpu_instruction_functions.relative_jump_if_not_zero),

    0x01: load_16bit_immediate_to_register(cpu_registers.BC),
    0x11: load_16bit_immediate_to_register(cpu_registers.DE),
    0x21: load_16bit_immediate_to_register(cpu_registers.HL),
    0x31: load_16bit_immediate_to_register(cpu_registers.SP),

    0xF9: load_16bit_register_to_register(cpu_registers.SP, cpu_registers.HL),

    0x32: ("Put A into memory address HL and decrement HL",
           "LDD (HL),A", 1, 8, None, cpu_instruction_functions.ldd_hl_a),

    0x3A: ("Load value at address HL into A and decrement HL",
           "LDD A,(HL)", 1, 8, None, cpu_instruction_functions.ldd_a_hl),

    0x2A: ("Load value at address HL into A and increment HL",
           "LDI A,(HL)", 1, 8, None, cpu_instruction_functions.ldi_a_hl),

    0x22: ("Put A into memory address HL and increment HL",
           "LDI (HL),A", 1, 8, None, cpu_instruction_functions.ldi_hl_a),

    0x3E: load_8bit_immediate_to_register(cpu_registers.A),
    0x06: load_8bit_immediate_to_register(cpu_registers.B),
    0x0E: load_8bit_immediate_to_register(cpu_registers.C),
    0x16: load_8bit_immediate_to_register(cpu_registers.D),
    0x1E: load_8bit_immediate_to_register(cpu_registers.E),
    0x26: load_8bit_immediate_to_register(cpu_registers.H),
    0x2E: load_8bit_immediate_to_register(cpu_registers.L),

    0xAF: xor(cpu_registers.A),
    0xA8: xor(cpu_registers.B),
    0xA9: xor(cpu_registers.C),
    0xAA: xor(cpu_registers.D),
    0xAB: xor(cpu_registers.E),
    0xAC: xor(cpu_registers.H),
    0xAD: xor(cpu_registers.L),

    0xA7: and_instruction(cpu_registers.A),
    0xA0: and_instruction(cpu_registers.B),
    0xA1: and_instruction(cpu_registers.C),
    0xA2: and_instruction(cpu_registers.D),
    0xA3: and_instruction(cpu_registers.E),
    0xA4: and_instruction(cpu_registers.H),
    0xA5: and_instruction(cpu_registers.L),

    0xE0: ("Put A into memory address $FF00+n",
           "LDH (d8),A", 2, 12, None, cpu_instruction_functions.ldh_n_a),

    0xE2: ("Put A into address $FF00 + register C",
           "LD (C),A", 1, 8, None, cpu_instruction_functions.ld_c_a),

    0xF2: ("Load value at address ($FF00 + C) into A",
           "LD A,(C)", 1, 8, None, cpu_instruction_functions.ld_a_c),

    0xF0: ("Load value at address ($FF00 + immediate) into A",
           "LD A,(d8)", 2, 12, None, cpu_instruction_functions.ldh_a_n),

    0xCD: ("Push address of next instruction onto stack and then jump to "
           "immediate address",
           "CALL d16", 3, 12, None, cpu_instruction_functions.call),

    0xF5: push(cpu_registers.AF),
    0xC5: push(cpu_registers.BC),
    0xD5: push(cpu_registers.DE),
    0xE5: push(cpu_registers.HL),

    0xF1: pop(cpu_registers.AF),
    0xC1: pop(cpu_registers.BC),
    0xD1: pop(cpu_registers.DE),
    0xE1: pop(cpu_registers.HL),

}

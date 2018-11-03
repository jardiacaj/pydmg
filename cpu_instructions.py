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
import cpu_registers


def load_8bit_immediate_to_register(register):
    return (
        "Load 8-bit immediate to {}".format(register),
        "LD {},d8".format(register), 2, 8, None,
        cpu_instruction_functions.load_8bit_immediate_to_register(register)
    )


def increment(register):
    return (
        "Increment {}".format(register),
        "INC {}".format(register), 1, 4, 'Z0H-',
        cpu_instruction_functions.increment_register(register)
    )


def load_register_to_register(target, source):
    return (
        "Put {} into {}".format(source, target),
        "LD {},{}".format(target,source), 1, 4, None,
        cpu_instruction_functions.load_register_to_register(target, source)
    )


instructions = {

    0x00: ("No operation", "NOP", 1, 4, None, cpu_instruction_functions.nop),

    0x3C: increment(cpu_registers.A),
    0x04: increment(cpu_registers.B),
    0x0C: increment(cpu_registers.C),
    0x14: increment(cpu_registers.D),
    0x1C: increment(cpu_registers.E),
    0x24: increment(cpu_registers.H),
    0x2C: increment(cpu_registers.L),

    0x7F: load_register_to_register(cpu_registers.A, cpu_registers.A),
    0x78: load_register_to_register(cpu_registers.A, cpu_registers.B),
    0x79: load_register_to_register(cpu_registers.A, cpu_registers.C),
    0x7A: load_register_to_register(cpu_registers.A, cpu_registers.D),
    0x7B: load_register_to_register(cpu_registers.A, cpu_registers.E),
    0x7C: load_register_to_register(cpu_registers.A, cpu_registers.H),
    0x7E: load_register_to_register(cpu_registers.A, cpu_registers.L),

    0x40: load_register_to_register(cpu_registers.B, cpu_registers.B),
    0x41: load_register_to_register(cpu_registers.B, cpu_registers.C),
    0x42: load_register_to_register(cpu_registers.B, cpu_registers.D),
    0x43: load_register_to_register(cpu_registers.B, cpu_registers.E),
    0x44: load_register_to_register(cpu_registers.B, cpu_registers.H),
    0x45: load_register_to_register(cpu_registers.B, cpu_registers.L),
    0x47: load_register_to_register(cpu_registers.B, cpu_registers.A),

    0x48: load_register_to_register(cpu_registers.C, cpu_registers.B),
    0x49: load_register_to_register(cpu_registers.C, cpu_registers.C),
    0x4A: load_register_to_register(cpu_registers.C, cpu_registers.D),
    0x4B: load_register_to_register(cpu_registers.C, cpu_registers.E),
    0x4C: load_register_to_register(cpu_registers.C, cpu_registers.H),
    0x4D: load_register_to_register(cpu_registers.C, cpu_registers.L),
    0x4F: load_register_to_register(cpu_registers.C, cpu_registers.A),

    0x50: load_register_to_register(cpu_registers.D, cpu_registers.B),
    0x51: load_register_to_register(cpu_registers.D, cpu_registers.C),
    0x52: load_register_to_register(cpu_registers.D, cpu_registers.D),
    0x53: load_register_to_register(cpu_registers.D, cpu_registers.E),
    0x54: load_register_to_register(cpu_registers.D, cpu_registers.H),
    0x55: load_register_to_register(cpu_registers.D, cpu_registers.L),
    0x57: load_register_to_register(cpu_registers.D, cpu_registers.A),

    0x58: load_register_to_register(cpu_registers.E, cpu_registers.B),
    0x59: load_register_to_register(cpu_registers.E, cpu_registers.C),
    0x5A: load_register_to_register(cpu_registers.E, cpu_registers.D),
    0x5B: load_register_to_register(cpu_registers.E, cpu_registers.E),
    0x5C: load_register_to_register(cpu_registers.E, cpu_registers.H),
    0x5D: load_register_to_register(cpu_registers.E, cpu_registers.L),
    0x5F: load_register_to_register(cpu_registers.E, cpu_registers.A),

    0x60: load_register_to_register(cpu_registers.H, cpu_registers.B),
    0x61: load_register_to_register(cpu_registers.H, cpu_registers.C),
    0x62: load_register_to_register(cpu_registers.H, cpu_registers.D),
    0x63: load_register_to_register(cpu_registers.H, cpu_registers.E),
    0x64: load_register_to_register(cpu_registers.H, cpu_registers.H),
    0x65: load_register_to_register(cpu_registers.H, cpu_registers.L),
    0x67: load_register_to_register(cpu_registers.H, cpu_registers.A),

    0x68: load_register_to_register(cpu_registers.L, cpu_registers.B),
    0x69: load_register_to_register(cpu_registers.L, cpu_registers.C),
    0x6A: load_register_to_register(cpu_registers.L, cpu_registers.D),
    0x6B: load_register_to_register(cpu_registers.L, cpu_registers.E),
    0x6C: load_register_to_register(cpu_registers.L, cpu_registers.H),
    0x6D: load_register_to_register(cpu_registers.L, cpu_registers.L),
    0x6F: load_register_to_register(cpu_registers.L, cpu_registers.A),

    0x02: ("Put value A into address (BC)",
           "LD (BC),A", 1, 8, None,
           cpu_instruction_functions.put_a_to_register_address(
               cpu_registers.BC)),

    0x12: ("Put value A into address (DE)",
           "LD (DE),A", 1, 8, None,
           cpu_instruction_functions.put_a_to_register_address(
               cpu_registers.DE)),

    0x77: ("Put value A into address (HL)",
           "LD (HL),A", 1, 8, None,
           cpu_instruction_functions.put_a_to_register_address(
               cpu_registers.HL)),

    0xEA: ("Put value A into immediate address",
           "LD (d16),A", 3, 16, None,
           cpu_instruction_functions.put_a_to_immediate_address),

    0x20: ("Relative jump if not zero",
           "JR NZ,d8", 2, 8, None,
           cpu_instruction_functions.relative_jump_if_not_zero),

    0x01: ("Load 16-bit immediate to BC",
           "LD BC,d16", 3, 12, None,
           cpu_instruction_functions.load_16bit_immediate_to_register(
               cpu_registers.BC)),

    0x11: ("Load 16-bit immediate to DE",
           "LD DE,d16", 3, 12, None,
           cpu_instruction_functions.load_16bit_immediate_to_register(
               cpu_registers.DE)),

    0x21: ("Load 16-bit immediate to HL",
           "LD HL,d16", 3, 12, None,
           cpu_instruction_functions.load_16bit_immediate_to_register(
               cpu_registers.HL)),

    0x31: ("Load 16-bit immediate to SP",
           "LD SP,d16", 3, 12, None,
           cpu_instruction_functions.load_16bit_immediate_to_register(
               cpu_registers.SP)),

    0x32: ("Put A into memory address HL and decrement HL",
           "LDD (HL),A", 1, 8, None, cpu_instruction_functions.ldd_hl_a),

    0x3E: load_8bit_immediate_to_register(cpu_registers.A),
    0x06: load_8bit_immediate_to_register(cpu_registers.B),
    0x0E: load_8bit_immediate_to_register(cpu_registers.C),
    0x16: load_8bit_immediate_to_register(cpu_registers.D),
    0x1E: load_8bit_immediate_to_register(cpu_registers.E),
    0x26: load_8bit_immediate_to_register(cpu_registers.H),
    0x2E: load_8bit_immediate_to_register(cpu_registers.L),

    0xAF: ("XOR A with A, store to A (effectively zeroes A)",
           "XOR A", 1, 4, 'Z000',
           cpu_instruction_functions.xor(cpu_registers.A)),

    0xA8: ("XOR A with  B, store to A",
           "XOR B", 1, 4, 'Z000',
           cpu_instruction_functions.xor(cpu_registers.B)),

    0xA9: ("XOR A with C, store to A",
           "XOR C", 1, 4, 'Z000',
           cpu_instruction_functions.xor(cpu_registers.C)),

    0xAA: ("XOR A with D, store to A",
           "XOR D", 1, 4, 'Z000',
           cpu_instruction_functions.xor(cpu_registers.D)),

    0xAB: ("XOR A with E, store to A",
           "XOR E", 1, 4, 'Z000',
           cpu_instruction_functions.xor(cpu_registers.E)),

    0xAC: ("XOR A with H, store to A",
           "XOR H", 1, 4, 'Z000',
           cpu_instruction_functions.xor(cpu_registers.H)),

    0xAD: ("XOR A with L, store to A",
           "XOR L", 1, 4, 'Z000',
           cpu_instruction_functions.xor(cpu_registers.L)),

    0xA7: ("AND A with A, store to A",
           "AND A", 1, 4, 'Z010',
           cpu_instruction_functions.and_instruction(cpu_registers.A)),

    0xA0: ("AND A with B, store to A",
           "AND B", 1, 4, 'Z010',
           cpu_instruction_functions.and_instruction(cpu_registers.B)),

    0xA1: ("AND A with C, store to A",
           "AND C", 1, 4, 'Z010',
           cpu_instruction_functions.and_instruction(cpu_registers.C)),

    0xA2: ("AND A with D, store to A",
           "AND D", 1, 4, 'Z010',
           cpu_instruction_functions.and_instruction(cpu_registers.D)),

    0xA3: ("AND A with E, store to A",
           "AND E", 1, 4, 'Z010',
           cpu_instruction_functions.and_instruction(cpu_registers.E)),

    0xA4: ("AND A with H, store to A",
           "AND H", 1, 4, 'Z010',
           cpu_instruction_functions.and_instruction(cpu_registers.H)),

    0xA5: ("AND A with L, store to A",
           "AND L", 1, 4, 'Z010',
           cpu_instruction_functions.and_instruction(cpu_registers.L)),

    0xE0: ("Put A into memory address $FF00+n",
           "LDH (d8),A", 2, 12, None, cpu_instruction_functions.ldh_n_a),

    0xE2: ("Put A into address $FF00 + register C",
           "LD (C),A", 1, 8, None, cpu_instruction_functions.ld_c_a),


}

cb_instructions = {

    0x7C: ("Test bit 7 of H",
           "BIT 7,H", 2, 8, 'Z01-',
           cpu_instruction_functions.h_register_bit_test(bit=7)),

}
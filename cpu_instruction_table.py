import cpu_instruction_implementation
import cpu_instruction_implementation_cb
import cpu_registers
from cpu_instruction_decoder import increment_8bit, increment_16bit, decrement_8bit, \
    decrement_16bit, load_8bit_register_to_register, put_register_to_pointer, \
    put_register_to_immediate_pointer, load_pointer_to_register, \
    load_immediate_pointer_to_register, load_16bit_immediate_to_register, \
    load_16bit_register_to_register, load_8bit_immediate_to_register, xor, \
    and_instruction, compare_register, compare_pointer, compare_immediate, \
    push, pop
from cpu_instruction_decoder_cb import rotate_register_left, rotate_pointer_left, \
    rotate_register_right, rotate_pointer_right, \
    rotate_register_left_through_carry, rotate_pointer_left_through_carry, \
    rotate_register_right_through_carry, rotate_pointer_right_through_carry, \
    test_register_bit, test_pointer_bit

instructions = {

    0x00: ("No operation", "NOP", 1, 4, None, cpu_instruction_implementation.nop),

    0x07: (
        "Rotate A left", "RLCA", 1, 4, 'Z00C',
        cpu_instruction_implementation_cb.rotate_8bit_register_left(
            cpu_registers.A, through_carry=False)
    ),
    0x17: (
        "Rotate A left through carry", "RLA", 1, 4, 'Z00C',
        cpu_instruction_implementation_cb.rotate_8bit_register_left(
            cpu_registers.A, through_carry=True)
    ),
    0x0F: (
        "Rotate A right", "RRCA", 1, 4, 'Z00C',
        cpu_instruction_implementation_cb.rotate_8bit_register_right(
            cpu_registers.A, through_carry=False)
    ),
    0x1F: (
        "Rotate A right through carry", "RRA", 1, 4, 'Z00C',
        cpu_instruction_implementation_cb.rotate_8bit_register_right(
            cpu_registers.A, through_carry=True)
    ),

    0x3C: increment_8bit(cpu_registers.A),
    0x04: increment_8bit(cpu_registers.B),
    0x0C: increment_8bit(cpu_registers.C),
    0x14: increment_8bit(cpu_registers.D),
    0x1C: increment_8bit(cpu_registers.E),
    0x24: increment_8bit(cpu_registers.H),
    0x2C: increment_8bit(cpu_registers.L),

    0x03: increment_16bit(cpu_registers.BC),
    0x13: increment_16bit(cpu_registers.DE),
    0x23: increment_16bit(cpu_registers.HL),
    0x33: increment_16bit(cpu_registers.SP),

    0x3D: decrement_8bit(cpu_registers.A),
    0x05: decrement_8bit(cpu_registers.B),
    0x0D: decrement_8bit(cpu_registers.C),
    0x15: decrement_8bit(cpu_registers.D),
    0x1D: decrement_8bit(cpu_registers.E),
    0x25: decrement_8bit(cpu_registers.H),
    0x2D: decrement_8bit(cpu_registers.L),

    0x0B: decrement_16bit(cpu_registers.BC),
    0x1B: decrement_16bit(cpu_registers.DE),
    0x2B: decrement_16bit(cpu_registers.HL),
    0x3B: decrement_16bit(cpu_registers.SP),

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
           cpu_instruction_implementation.relative_jump_if_not_zero),

    0x01: load_16bit_immediate_to_register(cpu_registers.BC),
    0x11: load_16bit_immediate_to_register(cpu_registers.DE),
    0x21: load_16bit_immediate_to_register(cpu_registers.HL),
    0x31: load_16bit_immediate_to_register(cpu_registers.SP),

    0xF9: load_16bit_register_to_register(cpu_registers.SP, cpu_registers.HL),

    0x32: ("Put A into memory address HL and decrement HL",
           "LDD (HL),A", 1, 8, None, cpu_instruction_implementation.ldd_hl_a),

    0x3A: ("Load value at address HL into A and decrement HL",
           "LDD A,(HL)", 1, 8, None, cpu_instruction_implementation.ldd_a_hl),

    0x2A: ("Load value at address HL into A and increment HL",
           "LDI A,(HL)", 1, 8, None, cpu_instruction_implementation.ldi_a_hl),

    0x22: ("Put A into memory address HL and increment HL",
           "LDI (HL),A", 1, 8, None, cpu_instruction_implementation.ldi_hl_a),

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

    0xBF: compare_register(cpu_registers.A),
    0xB8: compare_register(cpu_registers.B),
    0xB9: compare_register(cpu_registers.C),
    0xBA: compare_register(cpu_registers.D),
    0xBB: compare_register(cpu_registers.E),
    0xBC: compare_register(cpu_registers.H),
    0xBD: compare_register(cpu_registers.L),
    0xBE: compare_pointer(cpu_registers.HL),
    0xFE: compare_immediate(),

    0xE0: ("Put A into memory address $FF00+n",
           "LDH (d8),A", 2, 12, None, cpu_instruction_implementation.ldh_n_a),

    0xE2: ("Put A into address $FF00 + register C",
           "LD (C),A", 1, 8, None, cpu_instruction_implementation.ld_c_a),

    0xF2: ("Load value at address ($FF00 + C) into A",
           "LD A,(C)", 1, 8, None, cpu_instruction_implementation.ld_a_c),

    0xF0: ("Load value at address ($FF00 + immediate) into A",
           "LD A,(d8)", 2, 12, None, cpu_instruction_implementation.ldh_a_n),

    0xC9: ("Pop address from stack and then jump to that address",
           "RET", 1, 8, None, cpu_instruction_implementation.ret),

    0xCD: ("Push address of next instruction onto stack and then jump to "
           "immediate address",
           "CALL d16", 3, 12, None, cpu_instruction_implementation.call),

    0xF5: push(cpu_registers.AF),
    0xC5: push(cpu_registers.BC),
    0xD5: push(cpu_registers.DE),
    0xE5: push(cpu_registers.HL),

    0xF1: pop(cpu_registers.AF),
    0xC1: pop(cpu_registers.BC),
    0xD1: pop(cpu_registers.DE),
    0xE1: pop(cpu_registers.HL),

}

cb_instructions = {

    0x00: rotate_register_left(cpu_registers.B),
    0x01: rotate_register_left(cpu_registers.C),
    0x02: rotate_register_left(cpu_registers.D),
    0x03: rotate_register_left(cpu_registers.E),
    0x04: rotate_register_left(cpu_registers.H),
    0x05: rotate_register_left(cpu_registers.L),
    0x06: rotate_pointer_left(cpu_registers.HL),
    0x07: rotate_register_left(cpu_registers.A),

    0x08: rotate_register_right(cpu_registers.B),
    0x09: rotate_register_right(cpu_registers.C),
    0x0A: rotate_register_right(cpu_registers.D),
    0x0B: rotate_register_right(cpu_registers.E),
    0x0C: rotate_register_right(cpu_registers.H),
    0x0D: rotate_register_right(cpu_registers.L),
    0x0E: rotate_pointer_right(cpu_registers.HL),
    0x0F: rotate_register_right(cpu_registers.A),

    0x10: rotate_register_left_through_carry(cpu_registers.B),
    0x11: rotate_register_left_through_carry(cpu_registers.C),
    0x12: rotate_register_left_through_carry(cpu_registers.D),
    0x13: rotate_register_left_through_carry(cpu_registers.E),
    0x14: rotate_register_left_through_carry(cpu_registers.H),
    0x15: rotate_register_left_through_carry(cpu_registers.L),
    0x16: rotate_pointer_left_through_carry(cpu_registers.HL),
    0x17: rotate_register_left_through_carry(cpu_registers.A),

    0x18: rotate_register_right_through_carry(cpu_registers.B),
    0x19: rotate_register_right_through_carry(cpu_registers.C),
    0x1A: rotate_register_right_through_carry(cpu_registers.D),
    0x1B: rotate_register_right_through_carry(cpu_registers.E),
    0x1C: rotate_register_right_through_carry(cpu_registers.H),
    0x1D: rotate_register_right_through_carry(cpu_registers.L),
    0x1E: rotate_pointer_right_through_carry(cpu_registers.HL),
    0x1F: rotate_register_right_through_carry(cpu_registers.A),

    0x40: test_register_bit(cpu_registers.B, 0),
    0x41: test_register_bit(cpu_registers.C, 0),
    0x42: test_register_bit(cpu_registers.D, 0),
    0x43: test_register_bit(cpu_registers.E, 0),
    0x44: test_register_bit(cpu_registers.H, 0),
    0x45: test_register_bit(cpu_registers.L, 0),
    0x46: test_pointer_bit(cpu_registers.HL, 0),
    0x47: test_register_bit(cpu_registers.A, 0),

    0x48: test_register_bit(cpu_registers.B, 1),
    0x49: test_register_bit(cpu_registers.C, 1),
    0x4A: test_register_bit(cpu_registers.D, 1),
    0x4B: test_register_bit(cpu_registers.E, 1),
    0x4C: test_register_bit(cpu_registers.H, 1),
    0x4D: test_register_bit(cpu_registers.L, 1),
    0x4E: test_pointer_bit(cpu_registers.HL, 1),
    0x4F: test_register_bit(cpu_registers.A, 1),

    0x50: test_register_bit(cpu_registers.B, 2),
    0x51: test_register_bit(cpu_registers.C, 2),
    0x52: test_register_bit(cpu_registers.D, 2),
    0x53: test_register_bit(cpu_registers.E, 2),
    0x54: test_register_bit(cpu_registers.H, 2),
    0x55: test_register_bit(cpu_registers.L, 2),
    0x56: test_pointer_bit(cpu_registers.HL, 2),
    0x57: test_register_bit(cpu_registers.A, 2),

    0x58: test_register_bit(cpu_registers.B, 3),
    0x59: test_register_bit(cpu_registers.C, 3),
    0x5A: test_register_bit(cpu_registers.D, 3),
    0x5B: test_register_bit(cpu_registers.E, 3),
    0x5C: test_register_bit(cpu_registers.H, 3),
    0x5D: test_register_bit(cpu_registers.L, 3),
    0x5E: test_pointer_bit(cpu_registers.HL, 3),
    0x5F: test_register_bit(cpu_registers.A, 3),

    0x60: test_register_bit(cpu_registers.B, 4),
    0x61: test_register_bit(cpu_registers.C, 4),
    0x62: test_register_bit(cpu_registers.D, 4),
    0x63: test_register_bit(cpu_registers.E, 4),
    0x64: test_register_bit(cpu_registers.H, 4),
    0x65: test_register_bit(cpu_registers.L, 4),
    0x66: test_pointer_bit(cpu_registers.HL, 4),
    0x67: test_register_bit(cpu_registers.A, 4),

    0x68: test_register_bit(cpu_registers.B, 5),
    0x69: test_register_bit(cpu_registers.C, 5),
    0x6A: test_register_bit(cpu_registers.D, 5),
    0x6B: test_register_bit(cpu_registers.E, 5),
    0x6C: test_register_bit(cpu_registers.H, 5),
    0x6D: test_register_bit(cpu_registers.L, 5),
    0x6E: test_pointer_bit(cpu_registers.HL, 5),
    0x6F: test_register_bit(cpu_registers.A, 5),

    0x70: test_register_bit(cpu_registers.B, 6),
    0x71: test_register_bit(cpu_registers.C, 6),
    0x72: test_register_bit(cpu_registers.D, 6),
    0x73: test_register_bit(cpu_registers.E, 6),
    0x74: test_register_bit(cpu_registers.H, 6),
    0x75: test_register_bit(cpu_registers.L, 6),
    0x76: test_pointer_bit(cpu_registers.HL, 6),
    0x77: test_register_bit(cpu_registers.A, 6),

    0x78: test_register_bit(cpu_registers.B, 7),
    0x79: test_register_bit(cpu_registers.C, 7),
    0x7A: test_register_bit(cpu_registers.D, 7),
    0x7B: test_register_bit(cpu_registers.E, 7),
    0x7C: test_register_bit(cpu_registers.H, 7),
    0x7D: test_register_bit(cpu_registers.L, 7),
    0x7E: test_pointer_bit(cpu_registers.HL, 7),
    0x7F: test_register_bit(cpu_registers.A, 7),

}

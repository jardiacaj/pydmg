import cpu_instruction_functions_cb
import cpu_registers


def test_register_bit(register_id, bit):
    return (
        "Test bit {} of {}".format(bit, register_id),
       "BIT {},{}".format(bit, register_id), 2, 8, 'Z01-',
       cpu_instruction_functions_cb.register_bit_test(cpu_registers.H, bit=7)
    )


def test_pointer_bit(register_id, bit):
    return (
        "Test bit {} of ({})".format(bit, register_id),
       "BIT {},({})".format(bit, register_id), 2, 16, 'Z01-',
       cpu_instruction_functions_cb.pointer_bit_test(register_id, bit)
    )


cb_instructions = {
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

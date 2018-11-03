"""
Dict of tuples. Key = opcode as int
Fields:
 * Name
 * Mnemonic
 * Length in bytes
 * Duration in clock cycles
 * Flags affected (Z N H C)
 * Function
"""
import cpu_instruction_functions
import cpu_registers

instructions = {

    0x00: ("No operation",
           "NOP", 1, 4, None, cpu_instruction_functions.nop),

    0x3C: ("Increment A",
           "INC A", 1, 4, 'Z0H-',
           cpu_instruction_functions.inc(cpu_registers.C)),

    0x04: ("Increment B",
           "INC B", 1, 4, 'Z0H-',
           cpu_instruction_functions.inc(cpu_registers.B)),

    0x0C: ("Increment C",
           "INC C", 1, 4, 'Z0H-',
           cpu_instruction_functions.inc(cpu_registers.C)),

    0x14: ("Increment D",
           "INC D", 1, 4, 'Z0H-',
           cpu_instruction_functions.inc(cpu_registers.D)),

    0x1C: ("Increment E",
           "INC E", 1, 4, 'Z0H-',
           cpu_instruction_functions.inc(cpu_registers.E)),

    0x24: ("Increment H",
           "INC H", 1, 4, 'Z0H-',
           cpu_instruction_functions.inc(cpu_registers.H)),

    0x2C: ("Increment L",
           "INC L", 1, 4, 'Z0H-',
           cpu_instruction_functions.inc(cpu_registers.L)),

    0x7F: ("Put value A into A (NOP?)",
           "LD A,A", 1, 4, None,
           cpu_instruction_functions.ld_n_a(cpu_registers.A)),

    0x47: ("Put value A into B",
           "LD B,A", 1, 4, None,
           cpu_instruction_functions.ld_n_a(cpu_registers.B)),

    0x4F: ("Put value A into C",
           "LD C,A", 1, 4, None,
           cpu_instruction_functions.ld_n_a(cpu_registers.C)),

    0x57: ("Put value A into D",
           "LD D,A", 1, 4, None,
           cpu_instruction_functions.ld_n_a(cpu_registers.D)),

    0x5F: ("Put value A into E",
           "LD E,A", 1, 4, None,
           cpu_instruction_functions.ld_n_a(cpu_registers.E)),

    0x67: ("Put value A into H",
           "LD H,A", 1, 4, None,
           cpu_instruction_functions.ld_n_a(cpu_registers.H)),

    0x6F: ("Put value A into L",
           "LD L,A", 1, 4, None,
           cpu_instruction_functions.ld_n_a(cpu_registers.L)),

    0x02: ("Put value A into address (BC)",
           "LD (BC),A", 1, 8, None,
           cpu_instruction_functions.ld_addr_a(cpu_registers.BC)),

    0x12: ("Put value A into address (DE)",
           "LD (DE),A", 1, 8, None,
           cpu_instruction_functions.ld_addr_a(cpu_registers.DE)),

    0x77: ("Put value A into address (HL)",
           "LD (HL),A", 1, 8, None,
           cpu_instruction_functions.ld_addr_a(cpu_registers.HL)),

    0xEA: ("Put value A into immediate address",
           "LD (d16),A", 3, 16, None,
           cpu_instruction_functions.ld_imm_add_a),

    0x0E: ("Load 8-bit immediate to C",
           "LD C,d8", 2, 8, None, cpu_instruction_functions.ld_c_d8),

    0x20: ("Relative jump if not zero",
           "JR NZ,d8", 2, 8, None, cpu_instruction_functions.jr_nz),

    0x21: ("Load 16-bit immediate to HL",
           "LD HL,d16", 3, 12, None, cpu_instruction_functions.ld_hl_d16),

    0x31: ("Load 16-bit immediate to SP",
           "LD SP,d16", 3, 12, None, cpu_instruction_functions.ld_sp_d16),

    0x32: ("Put A into memory address HL and decrement HL",
           "LDD (HL),A", 1, 8, None, cpu_instruction_functions.ldd_hl_a),

    0x3E: ("Load 8-bit immediate to A",
           "LD A,d8", 2, 8, None, cpu_instruction_functions.ld_a_d8),

    0xAF: ("XOR A, store to A (effectively zeroes A)",
           "XOR A", 1, 4, 'Z000', cpu_instruction_functions.xor_a),

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
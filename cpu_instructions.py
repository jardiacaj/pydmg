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

instructions = {


    0x00: ("No operation",
           "NOP", 1, 4, None, cpu_instruction_functions.nop),

    0x31: ("Load 16-bit immediate to SP",
           "LD SP,d16", 3, 12, None, cpu_instruction_functions.ld_sp_d16),

    0xAF: ("XOR A, store to A (effectively zeroes A)",
           "XOR A", 1, 4, None, cpu_instruction_functions.nop),


}

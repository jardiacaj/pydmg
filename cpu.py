import cpu_instructions
from register import Register16bit


class CPU:
    def __init__(self, memory):
        self.total_clock_cycle_count = 0

        self.register_af = Register16bit()
        self.register_a, self.register_f = \
            self.register_af.eight_bit_registers()
        self.register_bc = Register16bit()
        self.register_b, self.register_c = \
            self.register_bc.eight_bit_registers()
        self.register_de = Register16bit()
        self.register_d, self.register_e = \
            self.register_de.eight_bit_registers()
        self.register_hl = Register16bit()
        self.register_h, self.register_l = \
            self.register_hl.eight_bit_registers()
        self.register_stack_pointer = Register16bit()
        self.register_program_counter = Register16bit()

        self.memory = memory

    def tick(self):
        instruction_opcode = self.memory.read(self.program_counter)

        instruction_descriptor = cpu_instructions.instructions.get(
            instruction_opcode)

        if instruction_descriptor is None:
            raise NotImplementedError(
                'Instruction 0x{instruction_opcode:02X} ({instruction_opcode})'
                ' not implemented'.format(
                    instruction_opcode=instruction_opcode
                )
            )

        instruction_name, instruction_mnemonic, instruction_length_in_bytes, \
        instruction_clock_cycles, instruction_flags_changed, \
        instruciton_implementation = \
            cpu_instructions.instructions[instruction_opcode]

        instruciton_implementation(self)

        self.total_clock_cycle_count += instruction_clock_cycles
        self.program_counter += 1

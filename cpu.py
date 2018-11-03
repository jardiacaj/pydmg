import logging

import cpu_instructions
from register import Register16bit


class CPU:
    def __init__(self, memory):
        self.memory = memory

        self.total_clock_cycle_count = 0

        self.register_af = Register16bit(contains_flags=True)
        self.register_a, self.flags = self.register_af.eight_bit_registers
        self.register_bc = Register16bit()
        self.register_b, self.register_c = self.register_bc.eight_bit_registers
        self.register_de = Register16bit()
        self.register_d, self.register_e = self.register_de.eight_bit_registers
        self.register_hl = Register16bit()
        self.register_h, self.register_l = self.register_hl.eight_bit_registers
        self.register_stack_pointer = Register16bit()
        self.register_program_counter = Register16bit()

        self.cb_prefix = False
        self.instruction_descriptor = None
        self.bytes_before_immediates = 0

    def tick(self):
        try:
            self.load_next_instruction()
            self.execute_loaded_instruction()
        except Exception as e:
            self.dump()
            raise e

    def execute_loaded_instruction(self):
        instruction_name, instruction_mnemonic, \
            instruction_length_in_bytes, instruction_clock_cycles, \
            instruction_flags_changed, instruction_implementation = \
            self.instruction_descriptor
        immediates = [
            self.memory.read(self.register_program_counter.get() + i)
            for i in range(instruction_length_in_bytes)
        ]
        for i in range(self.bytes_before_immediates):
            immediates.pop(0)

        logging.debug(
            "PC: {:02X}: {}, immediates: {}".format(
                self.register_program_counter.get(),
                instruction_mnemonic,
                immediates,
            )
        )
        instruction_implementation(self, *immediates)
        self.total_clock_cycle_count += instruction_clock_cycles
        self.register_program_counter.add(instruction_length_in_bytes)

    def load_next_instruction(self):
        pc = self.register_program_counter.get()
        next_byte = self.memory.read(pc)
        if next_byte == 0xCB:
            self.cb_prefix = True
            instruction_opcode = self.memory.read(pc + 1)
            self.instruction_descriptor = cpu_instructions.cb_instructions.get(
                instruction_opcode)
            self.bytes_before_immediates = 2
        else:
            self.cb_prefix = False
            instruction_opcode = next_byte
            self.instruction_descriptor = cpu_instructions.instructions.get(
                instruction_opcode)
            self.bytes_before_immediates = 1
        if self.instruction_descriptor is None:
            raise NotImplementedError(
                'Instruction 0x{instruction_opcode:02X} '
                '({instruction_opcode}) '
                'not implemented (CB: {cb_prefix})'.format(
                    instruction_opcode=instruction_opcode,
                    cb_prefix=self.cb_prefix,
                )
            )

    def dump(self):
        print(
            """
            {cycles} total clock cycles
            AF 0x{af:04X} Z={z} N={n} H={h} C={c}
            BC 0x{bc:04X}
            DE 0x{de:04X}
            HL 0x{hl:04X}
            SP 0x{sp:04X}
            PC 0x{pc:04X}
            """.format(
                cycles=self.total_clock_cycle_count,
                af=self.register_af.get(),
                z=self.flags.get_zero_flag(),
                n=self.flags.get_negative_flag(),
                h=self.flags.get_half_carry_flag(),
                c=self.flags.get_carry_flag(),
                bc=self.register_bc.get(),
                de=self.register_de.get(),
                hl=self.register_hl.get(),
                sp=self.register_stack_pointer.get(),
                pc=self.register_program_counter.get(),
            )
        )

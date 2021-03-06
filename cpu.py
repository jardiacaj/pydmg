import logging

import cpu_instruction_table
from memory_zone import MemoryFault
from register import Register16bit


class CPU:
    def __init__(self, memory):
        self.logger = logging.getLogger()  # Save reference for better performance
        self.memory = memory

        self.total_clock_cycles_ran = 0

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
        self.loaded_instruction_descriptor = None
        self.bytes_before_immediates = 0

        self.clock_cycles_since_last_instruction = 0

    # Gets called every 4th crystal clock
    def step(self):
        logging.warning("This should be called only in unit tests!")
        self.tick()
        while self.loaded_instruction_descriptor is not None:
            self.tick()

    def tick(self):
        if self.loaded_instruction_descriptor is None:
            self.load_next_instruction()

        self.total_clock_cycles_ran += 4
        self.clock_cycles_since_last_instruction += 4

        if self.clock_cycles_since_last_instruction >= \
                self.loaded_instruction_descriptor[3]:
            try:
                self.execute_loaded_instruction()
                self.loaded_instruction_descriptor = None
                self.clock_cycles_since_last_instruction = 0
            except Exception as e:
                logging.error(self.dump())
                raise e

    def stack_push_byte(self, byte):
        self.register_stack_pointer.add(-1)
        self.memory.write(self.register_stack_pointer.get(), byte)

    def stack_pop_byte(self):
        value = self.memory.read(self.register_stack_pointer.get())
        self.register_stack_pointer.add(1)
        return value

    def load_next_instruction(self):
        pc = self.register_program_counter.get()
        next_byte = self.memory.read(pc)
        if next_byte == 0xCB:
            self.cb_prefix = True
            instruction_opcode = self.memory.read(pc + 1)
            self.loaded_instruction_descriptor = cpu_instruction_table.cb_instructions.get(
                instruction_opcode)
            self.bytes_before_immediates = 2
        else:
            self.cb_prefix = False
            instruction_opcode = next_byte
            self.loaded_instruction_descriptor = cpu_instruction_table.instructions.get(
                instruction_opcode)
            self.bytes_before_immediates = 1
        if self.loaded_instruction_descriptor is None:
            raise NotImplementedError(
                'Instruction 0x{instruction_opcode:02X} '
                '({instruction_opcode}) '
                'not implemented (CB: {cb_prefix})'.format(
                    instruction_opcode=instruction_opcode,
                    cb_prefix=self.cb_prefix,
                )
            )

    def execute_loaded_instruction(self):
        instruction_name, instruction_mnemonic, \
            instruction_length_in_bytes, instruction_clock_cycles, \
            instruction_flags_changed, instruction_implementation = \
            self.loaded_instruction_descriptor
        instruction_bytes = [
            self.memory.read(self.register_program_counter.get() + i)
            for i in range(instruction_length_in_bytes)
        ]
        immediates = instruction_bytes[self.bytes_before_immediates:]

        if self.logger.isEnabledFor(logging.DEBUG):
            logging.debug(
                "PC {:02X}: {:12} -- {}".format(
                    self.register_program_counter.get(),
                    " ".join(["{:02X}".format(byte) for byte in instruction_bytes]),
                    instruction_mnemonic,
                    " imm:  if instruction_bytes",
                )
            )

        self.register_program_counter.add(instruction_length_in_bytes)

        instruction_implementation(self, *immediates)

    def dump(self):
        return """ # CPU Dump #
            {cycles} total CPU cycles
            AF 0x{af:04X} Z={z} N={n} H={h} C={c}
            BC 0x{bc:04X}
            DE 0x{de:04X}
            HL 0x{hl:04X}
            SP 0x{sp:04X}
            PC 0x{pc:04X}

            Stack
{stack_dump}
            """.format(
                cycles=self.total_clock_cycles_ran // 4,
                af=self.register_af.get(),
                z=self.flags.get_flag('Z'),
                n=self.flags.get_flag('N'),
                h=self.flags.get_flag('H'),
                c=self.flags.get_flag('C'),
                bc=self.register_bc.get(),
                de=self.register_de.get(),
                hl=self.register_hl.get(),
                sp=self.register_stack_pointer.get(),
                pc=self.register_program_counter.get(),
                stack_dump=self.stack_dump(),
            )

    def stack_dump(self):
        try:
            return "\n".join(
                (
                    "            {:04X}".format(self.memory.read(address))
                    for address
                    in range(self.register_stack_pointer.get(), 0xFFFE)
                )
            )
        except MemoryFault as e:
            return "Dump failed to {}".format(e)

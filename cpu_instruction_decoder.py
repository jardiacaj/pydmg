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
import cpu_instruction_implementation


def load_8bit_immediate_to_register(register):
    return (
        "Load 8-bit immediate to {}".format(register),
        "LD {},d8".format(register), 2, 8, None,
        cpu_instruction_implementation.load_8bit_immediate_to_register(register)
    )


def load_16bit_immediate_to_register(register):
    return (
        "Load 16-bit immediate to {}".format(register),
        "LD {},d16".format(register), 3, 12, None,
        cpu_instruction_implementation.load_16bit_immediate_to_register(register)
     )


def load_pointer_to_register(target_register, source_pointer):
    return (
        "Put value ({}) into {}".format(source_pointer, target_register),
        "LD {}, ({})".format(target_register, source_pointer), 1, 8, None,
        cpu_instruction_implementation.load_register_address_to_register(
            target_register,
            source_pointer
        )
    )


def load_immediate_pointer_to_register(target_register):
    return (
        "Put value (d16) into {}".format(target_register),
        "LD {}, (d16)".format(target_register), 3, 16, None,
        cpu_instruction_implementation.load_immediate_address_to_register(
            target_register
        )
    )


def put_register_to_pointer(target_pointer, source):
    return (
        "Put value {} into address ({})".format(source, target_pointer),
        "LD ({}),{}".format(target_pointer, source), 1, 8, None,
        cpu_instruction_implementation.put_register_to_register_address(
            target_pointer,
            source
        )
    )


def put_register_to_immediate_pointer(register):
    return(
        "Put value {} into immediate address".format(register),
        "LD (d16),{}".format(register), 3, 16, None,
        cpu_instruction_implementation.put_register_to_immediate_address(register)
    )


def increment_8bit(register):
    return (
        "Increment {}".format(register),
        "INC {}".format(register), 1, 4, 'Z0H-',
        cpu_instruction_implementation.increment_8bit_register(register)
    )


def decrement_8bit(register):
    return (
        "Decrement {}".format(register),
        "DEC {}".format(register), 1, 4, 'Z1H-',
        cpu_instruction_implementation.decrement_8bit_register(register)
    )


def increment_16bit(register):
    return (
        "Increment {}".format(register),
        "INC {}".format(register), 1, 8, None,
        cpu_instruction_implementation.increment_16bit_register(register)
    )


def decrement_16bit(register):
    return (
        "Decrement {}".format(register),
        "DEC {}".format(register), 1, 8, None,
        cpu_instruction_implementation.decrement_16bit_register(register)
    )


def load_8bit_register_to_register(target, source):
    return (
        "Put {} into {}".format(source, target),
        "LD {},{}".format(target, source), 1, 4, None,
        cpu_instruction_implementation.load_register_to_register(target, source)
    )


def load_16bit_register_to_register(target, source):
    return (
        "Put {} into {}".format(source, target),
        "LD {},{}".format(target, source), 1, 8, None,
        cpu_instruction_implementation.load_register_to_register(target, source)
    )


def xor(register):
    return (
        "XOR {} with A, store to A".format(register),
        "XOR {}".format(register), 1, 4, 'Z000',
        cpu_instruction_implementation.xor(register)
    )


def and_instruction(register):
    return (
        "AND {} with A, store to A".format(register),
        "AND {}".format(register), 1, 4, 'Z010',
        cpu_instruction_implementation.and_instruction(register)
    )


def push(register):
    return (
        "Push register pair {} to stack and decrement SP twice".format(
            register),
        "PUSH {}".format(register), 1, 16, None,
        cpu_instruction_implementation.push(register)
    )


def pop(register):
    return (
        "Pop to register pair {} from stack and increment SP twice".format(
            register),
        "POP {}".format(register), 1, 12, None,
        cpu_instruction_implementation.pop(register)
    )


def compare_register(register):
    return (
        "Compare A with {} (like A - n without result)".format(register),
        "CP {}".format(register), 1, 4, "Z1HC",
        cpu_instruction_implementation.compare_register_to_a(register)
    )


def compare_pointer(register):
    return (
        "Compare A with ({}) (like A - n without result)".format(register),
        "CP ({})".format(register), 1, 8, "Z1HC",
        cpu_instruction_implementation.compare_pointer_to_a(register)
    )


def compare_immediate():
    return (
        "Compare A with d8 (like A - n without result)",
        "CP d8", 2, 8, "Z1HC",
        cpu_instruction_implementation.compare_immediate_to_a
    )

import cpu_instruction_implementation_cb
import cpu_registers


def test_register_bit(register_id, bit):
    return (
        "Test bit {} of {}".format(bit, register_id),
        "BIT {},{}".format(bit, register_id), 2, 8, 'Z01-',
        cpu_instruction_implementation_cb.register_bit_test(cpu_registers.H, bit=7)
    )


def test_pointer_bit(register_id, bit):
    return (
        "Test bit {} of ({})".format(bit, register_id),
        "BIT {},({})".format(bit, register_id), 2, 16, 'Z01-',
        cpu_instruction_implementation_cb.pointer_bit_test(register_id, bit)
    )


def rotate_register_left_through_carry(register_id):
    return (
        "Rotate {} left through carry".format(register_id),
        "RL {}".format(register_id), 2, 8, 'Z00C',
        cpu_instruction_implementation_cb.rotate_8bit_register_left(
            register_id, through_carry=True)
    )


def rotate_pointer_left_through_carry(register_id):
    return (
        "Rotate pointer {} left through carry".format(register_id),
        "RL ({})".format(register_id), 2, 16, 'Z00C',
        cpu_instruction_implementation_cb.rotate_pointer_left(
            register_id, through_carry=True)
    )


def rotate_register_left(register_id):
    return (
        "Rotate {} left".format(register_id),
        "RLC {}".format(register_id), 2, 8, 'Z00C',
        cpu_instruction_implementation_cb.rotate_8bit_register_left(
            register_id, through_carry=False)
    )


def rotate_pointer_left(register_id):
    return (
        "Rotate pointer {} left".format(register_id),
        "RLC ({})".format(register_id), 2, 16, 'Z00C',
        cpu_instruction_implementation_cb.rotate_pointer_left(
            register_id, through_carry=False)
    )


def rotate_register_right(register_id):
    return (
        "Rotate {} right".format(register_id),
        "RRC {}".format(register_id), 2, 8, 'Z00C',
        cpu_instruction_implementation_cb.rotate_8bit_register_right(
            register_id, through_carry=False)
    )


def rotate_pointer_right(register_id):
    return (
        "Rotate pointer {} right".format(register_id),
        "RRC ({})".format(register_id), 2, 16, 'Z00C',
        cpu_instruction_implementation_cb.rotate_pointer_right(
            register_id, through_carry=False)
    )


def rotate_register_right_through_carry(register_id):
    return (
        "Rotate {} right through carry".format(register_id),
        "RR {}".format(register_id), 2, 8, 'Z00C',
        cpu_instruction_implementation_cb.rotate_8bit_register_right(
            register_id, through_carry=True)
    )


def rotate_pointer_right_through_carry(register_id):
    return (
        "Rotate pointer {} right through carry".format(register_id),
        "RR ({})".format(register_id), 2, 16, 'Z00C',
        cpu_instruction_implementation_cb.rotate_pointer_right(
            register_id, through_carry=True)
    )

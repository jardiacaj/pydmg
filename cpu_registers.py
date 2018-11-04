A = 'A'
F = 'E'
B = 'B'
C = 'C'
D = 'D'
E = 'E'
H = 'H'
L = 'L'
AF = 'AF'
BC = 'BC'
DE = 'DE'
HL = 'HL'
SP = 'SP'


class InvalidRegisterIndex(Exception):
    pass


def get_register(index, cpu):
    if index == A:
        return cpu.register_a
    elif index == F:
        return cpu.flags
    elif index == B:
        return cpu.register_b
    elif index == C:
        return cpu.register_c
    elif index == D:
        return cpu.register_d
    elif index == E:
        return cpu.register_e
    elif index == H:
        return cpu.register_h
    elif index == L:
        return cpu.register_l
    elif index == AF:
        return cpu.register_af
    elif index == BC:
        return cpu.register_bc
    elif index == DE:
        return cpu.register_de
    elif index == HL:
        return cpu.register_hl
    elif index == SP:
        return cpu.register_stack_pointer
    else:
        raise InvalidRegisterIndex(
            "Invalid register index: {}".format(index)
        )

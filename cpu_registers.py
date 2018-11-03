A = 'A'
F = 'E'
B = 'B'
C = 'C'
D = 'D'
E = 'E'
H = 'H'
L = 'L'
BC = 'BC'
DE = 'DE'
HL = 'HL'


class InvalidRegisterIndex(Exception):
    pass


def get_register(index, cpu):
    if index == A:
        return cpu.register_a
    elif index == F:
        return cpu.register_f
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
    elif index == BC:
        return cpu.register_bc
    elif index == DE:
        return cpu.register_de
    elif index == HL:
        return cpu.register_hl
    else:
        raise InvalidRegisterIndex(
            "Invalid register index: {}".format(index)
        )

import logging


class MemoryFault(Exception):
    pass


class MemoryZone:
    def __init__(self, name, size, base_address, alt_base_address=None,
                 is_rom=False, is_implemented=True):
        self.name = name
        self.data = [0] * size
        self.base_address = base_address
        self.alt_base_address = alt_base_address
        self.is_rom = is_rom
        self.is_implemented = is_implemented
        self.is_enabled = True

    def read(self, address):
        if not self.is_implemented:
            logging.error('Memory {} not implmemented'.format(self.name))
        try:
            return self.data[address - self.base_address]
        except IndexError as e:
            try:
                if self.alt_base_address is not None:
                    return self.data[address - self.alt_base_address]
                else:
                    raise e
            except IndexError:
                raise MemoryFault(
                    "Tried to read invalid "
                    "memory address 0x{address:04X} ({address})".format(
                        address=address
                    ))

    def write(self, address, value):
        if not self.is_implemented:
            logging.error('Memory {} not implmemented'.format(self.name))
        if self.is_rom:
            raise MemoryFault("Wrote to ROM address {:04X}".format(address))
        try:
            self.data[address - self.base_address] = value % 256
        except IndexError as e:
            try:
                if self.alt_base_address is not None:
                    self.data[address - self.alt_base_address] = value % 256
                else:
                    raise e
            except IndexError:
                raise MemoryFault(
                    "Tried to write 0x{value:02X} ({value}) to invalid "
                    "memory address 0x{address:04X} ({address})".format(
                        value=value, address=address
                    ))

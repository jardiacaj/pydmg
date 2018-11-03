import logging

from binreader import bytes_from_file


class MemoryFault(Exception):
    pass


class RAM:
    def __init__(self):
        self.data = [0] * 0x10000  # 16-bit address space

    def load_boot_rom(self, bootromfile_path):
        print("Reading boot ROM {}".format(bootromfile_path))

        for address, rom_byte in enumerate(bytes_from_file(bootromfile_path)):
            self.data[address] = rom_byte

        logging.debug("Loaded {} boot rom bytes".format(address+1))

    def load_main_rom(self, romfile_path):
        logging.warning("Main ROM loading not implemented.")

    def read(self, address):
        try:
            return self.data[address]
        except IndexError:
            raise MemoryFault(
                "Tried to read invalid "
                "memory address 0x{address:02X} ({address})".format(
                    address=address
                ))

    def write(self, address, value):
        try:
            self.data[address] = value % 255
        except IndexError:
            raise MemoryFault(
                "Tried to write 0x{value:02X} ({value}) to invalid "
                "memory address 0x{address:02X} ({address})".format(
                    value=value, address=address
                ))

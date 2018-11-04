import logging

from binreader import bytes_from_file


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
            raise NotImplementedError('Memory {} not implmemented'.format(
                self.name))
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
            raise NotImplementedError('Memory {} not implmemented'.format(
                self.name))
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


class DMGMemory:
    def __init__(self):
        self.boot_rom = MemoryZone(
            'boot ROM', size=0x0100, base_address=0x0000, is_rom=True)
        self.cartridge_rom = MemoryZone(
            'cartridge ROM', size=0x8000, base_address=0x0000,
            is_implemented=False, is_rom=True)
        self.video_ram = MemoryZone(
            'video RAM', size=0x2000, base_address=0x8000)
        self.external_ram = MemoryZone(
            'external RAM', size=0x2000, base_address=0xA000,
            is_implemented=False)
        self.internal_ram = MemoryZone(
            'internal RAM', size=0x2000, base_address=0xC000,
            is_implemented=False,
            alt_base_address=0xE000)
        self.oam_ram = MemoryZone(
            'OAM RAM', size=0xA0, base_address=0xFE00,
            is_implemented=False)
        self.io_ram = MemoryZone(
            'IO RAM', size=0x80, base_address=0xFF00)
        self.hram = MemoryZone(
            'HRAM', size=0x80, base_address=0xFF80)

    def load_boot_rom(self, bootromfile_path):
        print("Reading boot ROM {}".format(bootromfile_path))
        for address, rom_byte in enumerate(bytes_from_file(bootromfile_path)):
            self.boot_rom.data[address] = rom_byte
        logging.debug("Loaded {} boot rom bytes".format(address+1))

    def load_cartridge_rom(self, romfile_path):
        logging.warning("Cartridge ROM loading not implemented.")

    def address_to_memory(self, address):
        if address > 0xFFFF:
            raise MemoryFault('Unknown memory address {:04x}'.format(address))
        if address >= self.hram.base_address:
            return self.hram
        if address >= self.io_ram.base_address:
            return self.io_ram
        if address >= 0xFEA0:
            raise MemoryFault('Unknown memory address {:04x}'.format(address))
        if address >= self.oam_ram.base_address:
            return self.oam_ram
        if address >= self.internal_ram.alt_base_address:
            return self.internal_ram
        if address >= self.internal_ram.base_address:
            return self.internal_ram
        if address >= self.external_ram.base_address:
            return self.external_ram
        if address >= self.video_ram.base_address:
            return self.video_ram
        if address > len(self.boot_rom.data):
            return self.cartridge_rom
        if address >= 0:
            return self.boot_rom if self.boot_rom.is_enabled else self.cartridge_rom
        raise MemoryFault('Unknown memory address {:04x}'.format(address))

    def read(self, address):
        return self.address_to_memory(address).read(address)

    def write(self, address, value):
        return self.address_to_memory(address).write(address, value)

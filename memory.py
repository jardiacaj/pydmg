import logging

from binreader import bytes_from_file
from memory_cartridge_rom import MemoryZoneCartridgeRom
from memory_mapped_io import MemoryMappedIO


# CODE: name, supported
from memory_video_ram import MemoryZoneVRAM
from memory_zone import MemoryZone, MemoryFault

BOOT_ROM_SIZE = 0x100


class DMGMemory:
    def __init__(self,
                 lcd=None,
                 sound=None,
                 boot_romfile_path=None,
                 cartridge_romfile_path=None,
                 ):
        self.boot_rom = MemoryZone(
            'boot ROM', size=BOOT_ROM_SIZE, base_address=0x0000, is_rom=True)
        self.cartridge_rom = MemoryZoneCartridgeRom(
            'cartridge ROM', size=0x8000, base_address=0x0000, is_rom=True)
        self.video_ram = MemoryZoneVRAM(
            'video RAM', size=0x2000, base_address=0x8000)
        self.external_ram = MemoryZone(
            'external RAM', size=0x2000, base_address=0xA000,
            is_implemented=False)
        self.internal_ram = MemoryZone(
            'internal RAM', size=0x2000, base_address=0xC000,
            alt_base_address=0xE000)
        self.oam_ram = MemoryZone(
            'OAM RAM', size=0xA0, base_address=0xFE00,
            is_implemented=False)
        self.io_ram = MemoryMappedIO(
            'IO RAM', size=0x80, base_address=0xFF00,
            lcd=lcd, sound=sound, memory=self)
        self.hram = MemoryZone(
            'HRAM', size=0x80, base_address=0xFF80)

        if boot_romfile_path is not None:
            self.load_boot_rom(boot_romfile_path)
        if cartridge_romfile_path is not None:
            self.cartridge_rom.load_cartridge_rom(cartridge_romfile_path)

    def load_boot_rom(self, boot_romfile_path):
        print("Reading boot ROM {}".format(boot_romfile_path))
        for address, rom_byte in enumerate(bytes_from_file(boot_romfile_path)):
            self.boot_rom.data[address] = rom_byte
        loaded_byte_count = address + 1
        logging.debug("Loaded {} boot rom bytes".format(loaded_byte_count))
        if loaded_byte_count != BOOT_ROM_SIZE:
            logging.error("Bad boot ROM size, should be 0x{:04x} but is 0x{:04x}")

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
        if address > BOOT_ROM_SIZE:
            return self.cartridge_rom
        if address >= 0:
            return self.boot_rom if self.boot_rom.is_enabled else self.cartridge_rom
        raise MemoryFault('Unknown memory address {:04x}'.format(address))

    def read(self, address):
        return self.address_to_memory(address).read(address)

    def write(self, address, value):
        return self.address_to_memory(address).write(address, value)

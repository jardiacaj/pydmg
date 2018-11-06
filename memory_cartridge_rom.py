import logging

from binreader import bytes_from_file


# CODE: name, supported
from memory_zone import MemoryZone

CARTRIDGE_TYPES = {
    0x00: ("ROM ONLY", True),
    0x01: ("ROM+MBC1", False),
    0x02: ("ROM+MBC1+RAM", False),
    0x03: ("ROM+MBC1+RAM+BATT", False),
    0x05: ("ROM+MBC2", False),
    0x06: ("ROM+MBC2+BATTERY", False),
    0x08: ("ROM+RAM", False),
    0x09: ("ROM+RAM+BATTERY", False),
    0x0B: ("ROM+MMM01", False),
    0x0C: ("ROM+MMM01+SRAM", False),
    0x0D: ("ROM+MMM01+SRAM+BATT", False),
    0x0F: ("ROM+MBC3+TIMER+BATT", False),
    0x10: ("ROM+MBC3+TIMER+RAM+BATT", False),
    0x11: ("ROM+MBC", False),
    0x12: ("ROM+MBC3+RAM", False),
    0x13: ("ROM+MBC3+RAM+BATT", False),
    0x19: ("ROM+MBC5", False),
    0x1A: ("ROM+MBC5+RAM", False),
    0x1B: ("ROM+MBC5+RAM+BATT", False),
    0x1C: ("ROM+MBC5+RUMBLE", False),
    0x1D: ("ROM+MBC5+RUMBLE+SRAM", False),
    0x1E: ("ROM+MBC5+RUMBLE+SRAM+BATT", False),
    0x1F: ("Pocket Camera", False),
    0xFD: ("Bandai TAMA5", False),
    0xFE: ("Hudson HuC-3", False),
    0xFF: ("Hudson HuC-1", False),
}

# CODE: bits, bytes, banks
CARTRIDGE_ROM_SIZES = {
    0x00: ("256Kbit", "32KByte", 2),
    0x01: ("512Kbit", "64KByte", 4),
    0x02: ("1Mbit", "128KByte", 8),
    0x03: ("2Mbit", "256KByte", 16),
    0x04: ("4Mbit", "512KByte", 32),
    0x05: ("8Mbit", "1MByte", 64),
    0x06: ("16Mbit", "2MByte", 128),
    0x52: ("9Mbit", "1.1MByte", 72),
    0x53: ("10Mbit", "1.2MByte", 80),
    0x54: ("12Mbit", "1.5MByte", 96),
}

# CODE: bits, bytes, banks
CARTRIDGE_RAM_SIZE = {
    0x00: ("None", "None", 0),
    0x01: ("16Kbit", "2KByte", 1),
    0x02: ("64Kbit", "8KByte", 1),
    0x03: ("256Kbit", "32KByte", 4),
    0x04: ("1Kbit", "128KByte", 16),
}

DESTINATION_CODE = {
    0x00: "Japanese",
    0x01: "Non-japanese",
}


class MemoryZoneCartridgeRom(MemoryZone):
    def load_cartridge_rom(self, cartridge_romfile_path):
        for address, rom_byte in enumerate(
                bytes_from_file(cartridge_romfile_path)):
            self.data[address] = rom_byte

        logging.debug("Loaded {} cartridge rom bytes".format(address+1))
        logging.info(
            "Cartridge name: {}".format(
                self.read_cartridge_name()
            )
        )
        if self.cartridge_is_gbc():
            logging.info("GBC cart")
        else:
            logging.info("Non-GBC cart")

        if self.cartridge_is_sgb():
            logging.info("SGB cart")
        else:
            logging.info("Non-SGB cart")

        cartridge_type_descriptor = self.cartridge_type_descriptor()
        if cartridge_type_descriptor is None:
            raise NotImplementedError("Unknown cartridge type {:02X}".format(self.data[0x0147]))
        logging.info("Cartridge type: {}".format(cartridge_type_descriptor[0]))
        if not cartridge_type_descriptor[1]:
            raise NotImplementedError("Cartridge type {} not implemented".format(cartridge_type_descriptor[0]))

        logging.info("Cartridge ROM size: {} = {}, {} banks".format(*self.cartridge_rom_size_descriptor()))
        logging.info("Cartridge RAM size: {} = {}, {} banks".format(*self.cartridge_ram_size_descriptor()))
        logging.info("Destination: {}".format(self.destination()))
        logging.info("Checksum: {:04X} should be {:04X}".format(self.actual_checksum(), self.stated_checksum()))
        if self.stated_checksum() != self.actual_checksum():
            logging.warning("Cartridge checksum mismatch")


    def read_cartridge_name(self):
        return "".join(chr(byte) for byte
                       in self.data[0x0134:0x0142])

    def cartridge_is_gbc(self):
        return self.data[0x0143] == 0x80

    def cartridge_is_sgb(self):
        return self.data[0x0146] == 0x03

    def cartridge_type_descriptor(self):
        return CARTRIDGE_TYPES.get(self.data[0x0147])

    def cartridge_rom_size_descriptor(self):
        return CARTRIDGE_ROM_SIZES.get(self.data[0x0148])

    def cartridge_ram_size_descriptor(self):
        return CARTRIDGE_RAM_SIZE.get(self.data[0x0149])

    def destination(self):
        return DESTINATION_CODE.get(self.data[0x014A])

    def mask_rom_version_number(self):
        return self.data[0x014C]

    def stated_checksum(self):
        return (self.data[0x014E] << 8) + self.data[0x014F]

    def actual_checksum(self):
        return sum(
            (
                0 if address in (0x014E, 0x014F) else value
                for address, value
                in enumerate(self.data)
            )
         ) % 2**16

class IOMemoryFault(Exception):
    pass




class MemoryMappedIO:
    def __init__(self, name, size, base_address, lcd, sound):
        self.name = name
        self.base_address = base_address
        self.is_enabled = True
        self.lcd = lcd
        self.sound = sound
        self.mapping = self.generate_mapping()

    def generate_mapping(self):
        return {
            0xFF26: (
                "NR 52",
                read_NR52,
            )
        }

    def read(self, address):
        if address == 0xFF26:  # NR 52

        if address == 0xFF44:  # LCDC Y-Coordinate
            return self.lcd.current_line
        raise NotImplementedError("Read IO address {:04X}".format(address))

    def write(self, address, value):
        if address == 0xFF44:  # LCDC Y-Coordinate
            self.lcd.current_line = 0
        raise NotImplementedError("Write IO address {:04X}".format(address))

import logging


class IOMemoryFault(Exception):
    pass


def read_NR11(io):
    return io.sound.voices[0].wave_duty << 6


def write_NR11(io, value):
    io.sound.voices[0].wave_duty = value >> 6
    io.sound.voices[0].sound_length = value & 0b00111111


def read_NR12(io):
    value = io.sound.voices[0].initial_envelope_volume << 4
    if io.sound.voices[0].envelope_up:
        value |= 1 << 3
    value += io.sound.voices[0].number_envelope_sweep
    return value


def write_NR12(io, value):
    io.sound.voices[0].initial_envelope_volume = value >> 4
    io.sound.voices[0].envelope_up = (value & (1 << 3))
    io.sound.voices[0].number_envelope_sweep = value & 0b111


def write_NR13(io, value):
    io.sound.voices[0].frequency &= 0xF0
    io.sound.voices[0].frequency += value


def write_NR14(io, value):
    io.sound.voices[0].initial_bit = value &  (1 << 7)
    io.sound.voices[0].counter_enabled = value & (1 << 6)
    io.sound.voices[0].frequency %= 256
    io.sound.voices[0].frequency += (value & 0b111) << 8


def read_NR14(io):
    if io.sound.voices[0].counter_enabled:
        return 1 << 6
    return 0


def read_NR50(io):
    value = 0
    if io.sound.so1_powered:
        value |= 1 << 3
    if io.sound.so2_powered:
        value |= 1 << 7
    value |= io.sound.so1_output_level
    value |= io.sound.so2_output_level << 4
    return value


def write_NR50(io, value):
    io.sound.so1_powered = value | 1
    io.sound.so2_powered = value | (1 << 4)
    io.sound.so1_output_level = value | 0b00000111
    io.sound.so2_output_level = (value | 0b01110000) >> 4


def read_NR51(io):
    value = 0
    for i in range(4):
        if io.sound.voices[i].output_to_so1:
            value |= (1 << i)
        if io.sound.voices[i].output_to_so2:
            value |= (1 << (i + 4))
    return value


def write_NR51(io, value):
    for i in range(4):
        io.sound.voices[i].output_to_so1 = (value | (1 << i))
        io.sound.voices[i].output_to_so2 = (value | (1 << (i + 4)))


def read_NR52(io):
    value = 0
    if io.sound.powered:
        value |= 1 << 7
    for i in range(4):
        if io.sound.voices[i].enabled:
            value |= 1 << i
    return value


def write_NR52(io, value):
    io.sound.powered = value & 0b10000000


def write_LCDC_Y_Coord(io, value):
    io.lcd.current_line = 0


def read_BGP(io):
    value = 0
    for i in reversed(range(4)):
        value <<= 2
        value += io.lcd.background_palette[i]
    return value


def write_BGP(io, value):
    for i in range(4):
        io.lcd.background_palette[i] = value % 4
        value >>= 2
    return value


def write_SCY(io, value):
    io.lcd.scroll_y = value


def write_SCX(io, value):
    io.lcd.scroll_x = value

"""
  LCDC
  Bit 7 - LCD Display Enable             (0=Off, 1=On)
  Bit 6 - Window Tile Map Display Select (0=9800-9BFF, 1=9C00-9FFF)
  Bit 5 - Window Display Enable          (0=Off, 1=On)
  Bit 4 - BG & Window Tile Data Select   (0=8800-97FF, 1=8000-8FFF)
  Bit 3 - BG Tile Map Display Select     (0=9800-9BFF, 1=9C00-9FFF)
  Bit 2 - OBJ (Sprite) Size              (0=8x8, 1=8x16)
  Bit 1 - OBJ (Sprite) Display Enable    (0=Off, 1=On)
  Bit 0 - BG Display (for CGB see below) (0=Off, 1=On)
"""

def read_LCDC(io):
    value = 0
    if io.lcd.enabled:
        value |= 1 << 7
    if io.lcd.window_tile_map_display_select:
        value |= 1 << 6
    if io.lcd.window_display_enable:
        value |= 1 << 5
    if io.lcd.bg_and_window_tile_data_select:
        value |= 1 << 4
    if io.lcd.bg_tile_map_display_select:
        value |= 1 << 3
    if io.lcd.sprite_size:
        value |= 1 << 2
    if io.lcd.sprite_display:
        value |= 1 << 1
    if io.lcd.bg_and_window_display:
        value |= 1 << 0


def write_LCDC(io, value):
    io.lcd.enabled = value & (1 << 7)
    io.lcd.window_tile_map_display_select = value & (1 << 6)
    io.lcd.window_display_enable = value & (1 << 5)
    io.lcd.bg_and_window_tile_data_select = value & (1 << 4)
    io.lcd.bg_tile_map_display_select = value & (1 << 3)
    io.lcd.sprite_size = value & (1 << 2)
    io.lcd.sprite_display = value & (1 << 1)
    io.lcd.bg_and_window_display = value & (1 << 0)



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
            0xFF11: ("NR 11 Channel 1 Sound length/Wave pattern duty (R/W)", read_NR11, write_NR11),
            0xFF12: ("NR 12 Channel 1 Volume Envelope (R/W)", read_NR12, write_NR12),
            0xFF13: ("NR 13 Channel 1 Frequency lo (W)", None, write_NR13),
            0xFF14: ("NR 14 Channel 1 Frequency hi (R/W)", read_NR14, write_NR14),
            0xFF24: ("NR 50 Channel control / ON-OFF / Volume (R/W)", read_NR50, write_NR50),
            0xFF25: ("NR 51 Selection of Sound output terminal (R/W)", read_NR51, write_NR51),
            0xFF26: ("NR 52 Sound on/off", read_NR52, write_NR52),
            0xFF40: ("LCDC LDC Control (R / W)", read_LCDC, write_LCDC),
            0xFF42: ("SCY Scroll Y (R / W)", lambda io: io.lcd.scroll_y, write_SCY),
            0xFF43: ("SCX Scroll X (R / W)", lambda io: io.lcd.scroll_x, write_SCX),
            0xFF44: ("LCDC Y-Coordinate (current line)", lambda io: io.lcd.current_line, write_LCDC_Y_Coord),
            0xFF47: ("BGP - BG Palette Data (R/W) - Non CGB Mode Only", read_BGP, write_BGP),
        }

    def read(self, address):
        implementation = self.mapping.get(address)
        if not implementation or not implementation[1]:
            raise NotImplementedError("Read IO address {:04X}".format(address))
        value = implementation[1](self)
        logging.debug("Read I/O address {:04X} value {:02X}".format(address, value))
        return value

    def write(self, address, value):
        implementation = self.mapping.get(address)
        if not implementation or not implementation[2]:
            raise NotImplementedError("Write IO address {:04X}".format(address))
        logging.debug("Write I/O address {:04X} value {:02X}".format(address, value))
        implementation[2](self, value)

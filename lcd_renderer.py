import logging
import math

import numpy as np
import pygame

color_code_to_screen_color = [
    0,
    0x555555,
    0xAAAAAA,
    0xFFFFFF,
]

color_map = []
for input_byte_1 in range(256):
    color_map.append([])
    for input_byte_2 in range(256):
        tmp_color_list = []
        byte_1_copy = input_byte_1
        byte_2_copy = input_byte_2
        for dot_in_line in range(8):
            bit_from_byte_1 = byte_1_copy % 2
            bit_from_byte_2 = byte_2_copy % 2
            code_color = (bit_from_byte_1 * 2) + bit_from_byte_2
            byte_1_copy >>= 1
            byte_2_copy >>= 1
            tmp_color_list.append(color_code_to_screen_color[code_color])
        color_map[input_byte_1].append(tmp_color_list)


def get_color_code(byte1, byte2, offset):
    return (((byte2 >> offset) & 1) << 1) + ((byte1 >> offset) & 1)


def draw_vertical_line(screen, x, length, color):
    for i in range(length):
        screen[x][0:] = [color] * length


def draw_horizontal_line(screen, y, length, color):
    for i in range(length):
        screen[i][y] = color


class LCDRenderer:
    def __init__(self, lcd):
        self.lcd = lcd
        self.tiles_per_row_in_tile_window = 16
        self.tile_window_size = (
            (self.tiles_per_row_in_tile_window * 9),
            math.ceil(192 / self.tiles_per_row_in_tile_window * 9)
        )

        pygame.init()
        self.screen = pygame.display.set_mode(self.tile_window_size)

    def render(self):
        logging.debug("Rendering frame")
        self.render_tile_view()

    def render_tile_view(self):
        screenarray = np.full(shape=self.tile_window_size,
                              fill_value=2 ** 32 - 1)
        for tile_idx in range(192):
            tile_base_address = tile_idx * 16 + 0x8000
            x_offset = (tile_idx % self.tiles_per_row_in_tile_window) * 9
            for tile_line_number in range(8):
                y_offset = ((tile_idx // self.tiles_per_row_in_tile_window) * 9 + tile_line_number)
                line_base_address = tile_base_address + tile_line_number * 2
                color_byte_1 = self.lcd.memory.read(line_base_address)
                color_byte_2 = self.lcd.memory.read(line_base_address + 1)
                line_output_colors = color_map[color_byte_1][color_byte_2]
                for i in range(len(line_output_colors)):
                    screenarray[x_offset+i][y_offset] = line_output_colors[7-i]

        for i in range(1, self.tiles_per_row_in_tile_window):
            draw_vertical_line(screenarray, i*9-1, self.tile_window_size[1], 255)
        for i in range(1, math.ceil(192 / self.tiles_per_row_in_tile_window)):
            draw_horizontal_line(screenarray, i*9-1, self.tile_window_size[0], 255)

        pygame.surfarray.blit_array(self.screen, screenarray)
        pygame.display.flip()

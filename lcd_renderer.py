import logging
import math

import numpy as np
import pygame

color_code_to_gl_color = [
    (0, 0, 0),
    (0x55, 0x55, 0x55),
    (0xAA, 0xAA, 0xAA),
    (0xFF, 0xFF, 0xFF),
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
            tmp_color_list.append(color_code_to_gl_color[code_color])
        color_map[input_byte_1].append([item for sublist in tmp_color_list for item in sublist])


def get_color_code(byte1, byte2, offset):
    return (((byte2 >> offset) & 1) << 1) + ((byte1 >> offset) & 1)


class LCDRenderer:
    def __init__(self, lcd, zoom=4):
        self.lcd = lcd
        self.zoom = zoom
        self.tiles_per_row_in_tile_window = 16
        self.tile_window_size = (
            (self.tiles_per_row_in_tile_window * 8 + 1) * self.zoom,
            math.ceil(192 / self.tiles_per_row_in_tile_window * 8) * self.zoom
        )

        pygame.init()
        self.screen = pygame.display.set_mode(self.tile_window_size)


    def render(self):
        logging.debug("Rendering frame")

        screenarray = np.zeros(self.tile_window_size)
        screenarray = np.random.randint(self.tile_window_size[0]*self.tile_window_size[1], size=self.tile_window_size).astype('uint32')
        pygame.surfarray.blit_array(self.screen, screenarray)
        pygame.display.flip()

    def draw_tile(self, tile_idx):
        tile_base_address = tile_idx * 16 + 0x8000
        x_offset = (tile_idx % 16) * 8 * self.zoom
        for tile_line_number in range(8):
            line_base_address = tile_base_address + tile_line_number * 2
            color_byte_1 = self.memory.read(line_base_address)
            color_byte_2 = self.memory.read(line_base_address + 1)
            line_output_colors = color_map[color_byte_1][color_byte_2]

            y_offset = ((tile_idx // 16 + 1) * 8 - tile_line_number) * self.zoom

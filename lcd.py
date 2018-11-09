import pyglet
from pyglet.gl import *

TILE_ZOOM = 4

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
        for color_output in range(8):
            code_color = (input_byte_1 >> 7 << 1) + (input_byte_2 >> 7)
            tmp_color_list.append(color_code_to_gl_color[code_color])
        color_map[input_byte_1].append([item for sublist in tmp_color_list for item in sublist])


class LCD:
    def __init__(self, memory=None):
        self.memory = memory
        self.total_clock_cycles_ran = 0
        self.clock_cycles_since_last_hblank_end = 0

        self.enabled = 0
        self.scroll_x = 0
        self.scroll_y = 0
        self.window_tile_map_display_select = 0
        self.window_display_enable = 0
        self.bg_and_window_tile_data_select = 0
        self.bg_tile_map_display_select = 0
        self.sprite_size = 0
        self.sprite_display = 0
        self.bg_and_window_display = 0
        self.current_line = 0
        self.background_palette = [0] * 4  # maps 2-bit color numbers to 2-bit color shades

        tile_window = pyglet.window.Window(
            width=8 * 8 * TILE_ZOOM,
            height=24 * 8 * TILE_ZOOM,
            caption="tile_viewer",
            resizable=True
        )

        @tile_window.event
        def on_draw():
            tile_window.clear()
            glClear(GL_COLOR_BUFFER_BIT)
            glLoadIdentity()
            glLineWidth(4)
            for tile_idx in range(256):
                self.draw_tile(tile_idx)

    def draw_tile(self, tile_idx):
        tile_base_address = tile_idx * 16 + 0x8000
        x_offset = (tile_idx % 8) * 8 * TILE_ZOOM
        for tile_line_number in range(8):
            line_base_address = tile_base_address + tile_line_number * 2
            color_byte_1 = self.memory.read(line_base_address)
            color_byte_2 = self.memory.read(line_base_address + 1)
            line_output_colors = color_map[color_byte_1][color_byte_2]

            y_offset = ((tile_idx // 8 + 1) * 8 - tile_line_number) * TILE_ZOOM

            pyglet.graphics.draw(
                8, pyglet.gl.GL_LINES,
                ('v2i', (
                    x_offset + TILE_ZOOM * 0, y_offset,
                    x_offset + TILE_ZOOM * 1, y_offset,
                    x_offset + TILE_ZOOM * 2, y_offset,
                    x_offset + TILE_ZOOM * 3, y_offset,
                    x_offset + TILE_ZOOM * 4, y_offset,
                    x_offset + TILE_ZOOM * 5, y_offset,
                    x_offset + TILE_ZOOM * 6, y_offset,
                    x_offset + TILE_ZOOM * 7, y_offset)
                 ),
                ('c3B', line_output_colors)
            )

    def clock(self):
        if not self.enabled:
            return

        self.total_clock_cycles_ran += 1
        self.clock_cycles_since_last_hblank_end += 1

        if self.clock_cycles_since_last_hblank_end == (20 + 43 + 51) * 4:
            self.clock_cycles_since_last_hblank_end = 0
            self.current_line += 1
            if self.current_line == 154:
                self.current_line = 0
                pyglet.clock.tick()

                for window in pyglet.app.windows:
                    window.switch_to()
                    window.dispatch_events()
                    window.dispatch_event('on_draw')
                    window.flip()

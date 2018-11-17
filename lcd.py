class LCD:
    def __init__(self, memory=None, renderer=None):
        self.memory = memory
        self.renderer = renderer
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
                if self.renderer:
                    self.renderer.render()

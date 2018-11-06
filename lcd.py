class LCD:
    def __init__(self, memory=None):
        self.memory = memory
        self.total_clock_cycles_ran = 0
        self.clock_cycles_since_last_hblank_end = 0
        self.current_line = 0

    def clock(self):
        self.total_clock_cycles_ran += 1
        self.clock_cycles_since_last_hblank_end += 1

        if self.clock_cycles_since_last_hblank_end == (20 + 43 + 51):
            self.clock_cycles_since_last_hblank_end = 0
            self.current_line += 1
            if self.current_line == 154:
                self.current_line = 0

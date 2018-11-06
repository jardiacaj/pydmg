class Sound:
    def __init__(self, memory=None):
        self.memory = memory
        self.total_clock_cycles_ran = 0
        self.powered = False

    def clock(self):
        self.total_clock_cycles_ran += 1

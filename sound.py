class Voice:
    def __init__(self):
        self.wave_duty = 0
        self.sound_length = 0
        self.enabled = False
        self.initial_envelope_volume = 0
        self.envelope_up = 0
        self.number_envelope_sweep = 0
        self.frequency = 0
        self.initial_bit = 0
        self.counter_enabled = 0
        self.output_to_so1 = False
        self.output_to_so2 = False


class Sound:
    def __init__(self, memory=None):
        self.memory = memory
        self.total_clock_cycles_ran = 0
        self.powered = False
        self.voices = [Voice(), Voice(), Voice(), Voice()]

    def clock(self):
        self.total_clock_cycles_ran += 1

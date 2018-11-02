from cpu import CPU
from ram import RAM


class PyDMG:
    def __init__(self, bootromfile_path, romfile_path):
        self.memory = RAM(bootromfile_path, romfile_path)
        self.cpu = CPU(self.memory)

    def run(self):
        while True:
            self.cpu.tick()

from cpu import CPU
from ram import RAM


class PyDMG:
    def __init__(self, bootromfile_path, romfile_path):
        self.memory = RAM()
        self.memory.load_boot_rom(bootromfile_path)
        self.memory.load_main_rom(romfile_path)
        self.cpu = CPU(self.memory)

    def run(self):
        while True:
            self.cpu.tick()

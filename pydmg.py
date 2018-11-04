import argparse
import logging

from cpu import CPU
from debugger import DMGDebugger
from ram import RAM


class PyDMG:
    def __init__(self, bootromfile_path, romfile_path):
        self.memory = RAM()
        self.memory.load_boot_rom(bootromfile_path)
        self.memory.load_main_rom(romfile_path)
        self.cpu = CPU(self.memory)

    def step(self):
        self.cpu.tick()

    def run(self):
        while True:
            self.step()


if __name__ == "__main__":
    print("PyDMG starting")

    parser = argparse.ArgumentParser()
    parser.add_argument("romfile")
    parser.add_argument("--boot-romfile", default="dmg_boot.bin")
    parser.add_argument("--log-level",
                        default=logging._levelToName[logging.DEBUG],
                        choices=(
                            logging._levelToName[logging.DEBUG],
                            logging._levelToName[logging.INFO],
                            logging._levelToName[logging.WARNING],
                            logging._levelToName[logging.ERROR],
                            logging._levelToName[logging.CRITICAL],
                        ))
    parser.add_argument("--debugger", action='store_true')
    args = parser.parse_args()

    logging.basicConfig(level=logging._nameToLevel[args.log_level])

    emulator = PyDMG(
        bootromfile_path=args.boot_romfile,
        romfile_path=args.romfile
    )

    if not args.debugger:
        emulator.run()
    else:
        debugger = DMGDebugger(emulator)
        debugger.run()

import argparse
import logging
import time

from cpu import CPU
from debugger import DMGDebugger
from lcd import LCD
from memory import DMGMemory
from sound import Sound

DMG_CLOCK_FREQUENCY = 4194304
DMG_SECONDS_PER_CLOCK = 1 / DMG_CLOCK_FREQUENCY


class PyDMG:
    def __init__(self, boot_romfile_path = None, cartridge_romfile_path = None, clocked = True):
        self.last_cycle_start_time = 0
        self.total_clock_cycles_ran = 0
        self.clocked = clocked
        self.lcd = LCD()
        self.sound = Sound()
        self.memory = DMGMemory(
            self.lcd, self.sound, boot_romfile_path, cartridge_romfile_path)
        self.lcd.memory = self.memory
        self.sound.memory = self.memory
        self.cpu = CPU(self.memory)

    # DMG CPU instructions take at least 4 clocks
    def cpu_step(self):
        self.clock()
        self.clock()
        self.clock()
        self.clock()
        while self.cpu.loaded_instruction_descriptor is not None:
            self.clock()

    def clock(self):
        if self.clocked:
            while self.time_since_last_cycle() < DMG_SECONDS_PER_CLOCK:
                time_to_sleep = DMG_SECONDS_PER_CLOCK - self.time_since_last_cycle()
                if time_to_sleep > 0:
                    time.sleep(time_to_sleep)
        self.last_cycle_start_time = time.monotonic()
        # First increase, then run as first instruction needs cycles to run
        self.total_clock_cycles_ran += 1
        self.lcd.clock()
        if self.total_clock_cycles_ran % 4 == 0:
            self.cpu.tick()

    def time_since_last_cycle(self):
        time_since_last_cycle = time.monotonic() - self.last_cycle_start_time
        return time_since_last_cycle

    def run(self):
        while True:
            self.clock()


if __name__ == "__main__":
    print("PyDMG starting")

    parser = argparse.ArgumentParser()
    parser.add_argument("cartridge_romfile")
    parser.add_argument("--boot-romfile", default="dmg_boot.bin")
    parser.add_argument("--log-level",
                        default=logging._levelToName[logging.INFO],
                        choices=(
                            logging._levelToName[logging.DEBUG],
                            logging._levelToName[logging.INFO],
                            logging._levelToName[logging.WARNING],
                            logging._levelToName[logging.ERROR],
                            logging._levelToName[logging.CRITICAL],
                        ))
    parser.add_argument("--disable-clock", action='store_true')
    parser.add_argument("--debugger", action='store_true')
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.debugger
                        else logging._nameToLevel[args.log_level])

    emulator = PyDMG(
        boot_romfile_path=args.boot_romfile,
        cartridge_romfile_path=args.cartridge_romfile,
        clocked=not args.disable_clock,
    )

    if not args.debugger:
        emulator.run()
    else:
        debugger = DMGDebugger(emulator)
        debugger.run()

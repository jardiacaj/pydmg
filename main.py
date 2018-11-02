import argparse
import logging

from pydmg import PyDMG

if __name__ == "__main__":
    print("PyDMG starting")

    parser = argparse.ArgumentParser()
    parser.add_argument("romfile")
    parser.add_argument("--boot-romfile", default="dmg_boot.bin")
    parser.add_argument("--log-level", default=logging.DEBUG,
                        choices=(
                            logging.DEBUG,
                            logging.INFO,
                            logging.WARNING,
                            logging.ERROR,
                            logging.CRITICAL,
                        ))
    args = parser.parse_args()

    logging.basicConfig(level=args.log_level)

    emulator = PyDMG(
        bootromfile_path=args.boot_romfile,
        romfile_path=args.romfile
    )

    emulator.run()

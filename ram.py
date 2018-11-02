import logging

from binreader import bytes_from_file


class RAM:
    def __init__(self, bootromfile_path, romfile_path):
        print("Reading boot ROM {}".format(bootromfile_path))

        self.memory = []
        for b in bytes_from_file(bootromfile_path):
            self.memory.append(b)

        logging.debug(self.memory)
        logging.debug("Total memory size: {} bytes".format(len(self.memory)))

    def read(self, address):
        return self.memory[address]

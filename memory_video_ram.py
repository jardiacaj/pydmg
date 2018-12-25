from memory_zone import MemoryZone


class MemoryZoneVRAM(MemoryZone):
    def write(self, address, value):
        MemoryZone.write(self, address, value)

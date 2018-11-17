import ctypes
import logging
import math

import numpy
import sdl2
import sdl2.ext
from sdl2 import SDL_MUSTLOCK, SDL_UnlockSurface, SDL_Surface, SDL_LockSurface
from sdl2.ext import SoftwareSprite

color_code_to_gl_color = [
    (0, 0, 0),
    (0x55, 0x55, 0x55),
    (0xAA, 0xAA, 0xAA),
    (0xFF, 0xFF, 0xFF),
]

color_map = []
for input_byte_1 in range(256):
    color_map.append([])
    for input_byte_2 in range(256):
        tmp_color_list = []
        byte_1_copy = input_byte_1
        byte_2_copy = input_byte_2
        for dot_in_line in range(8):
            bit_from_byte_1 = byte_1_copy % 2
            bit_from_byte_2 = byte_2_copy % 2
            code_color = (bit_from_byte_1 * 2) + bit_from_byte_2
            byte_1_copy >>= 1
            byte_2_copy >>= 1
            tmp_color_list.append(color_code_to_gl_color[code_color])
        color_map[input_byte_1].append([item for sublist in tmp_color_list for item in sublist])


def get_color_code(byte1, byte2, offset):
    return (((byte2 >> offset) & 1) << 1) + ((byte1 >> offset) & 1)


class SurfaceArray(numpy.ndarray):
    """Wrapper class around numpy.ndarray.

    Used to keep track of the original source object for pixels2d()
    and pixels3d() to avoid the deletion of the source object.
    """
    def __new__(cls, shape, dtype=float, buffer_=None, offset=0,
                strides=None, order=None, source=None, surface=None):
        sfarray = numpy.ndarray.__new__(cls, shape, dtype, buffer_,
                                        offset, strides, order)
        sfarray._source = source
        sfarray._surface = surface
        return sfarray

    def __array_finalize__(self, sfarray):
        if sfarray is None:
            return
        self._source = getattr(sfarray, '_source', None)
        self._surface = getattr(sfarray, '_surface', None)

    def __del__(self):
        if self._surface:
            if SDL_MUSTLOCK(self._surface):
                SDL_UnlockSurface(self._surface)


def pixels2d(source):
    """Creates a 2D pixel array from the passed source."""
    if isinstance(source, SoftwareSprite):
        psurface = source.surface
    elif isinstance(source, SDL_Surface):
        psurface = source
    else:
        raise TypeError("source must be a Sprite or SDL_Surface")

    bpp = psurface.format.contents.BytesPerPixel
    if bpp < 1 or bpp > 4:
        raise ValueError("unsupported bpp")
    strides = (psurface.pitch, bpp)
    srcsize = psurface.h * psurface.pitch
    shape = psurface.h, psurface.w   # surface.pitch // bpp

    dtypes = {1: numpy.uint8,
              2: numpy.uint16,
              3: numpy.uint32,
              4: numpy.uint32
             }

    if SDL_MUSTLOCK(psurface):
        SDL_LockSurface(psurface)
    pxbuf = ctypes.cast(psurface.pixels,
                        ctypes.POINTER(ctypes.c_ubyte * srcsize)).contents
    return SurfaceArray(shape, dtypes[bpp], pxbuf, 0, strides, "C", source,
                        psurface).transpose()


def ownpixels2d(psurface):
    bpp = psurface.format.contents.BytesPerPixel
    if bpp < 1 or bpp > 4:
        raise ValueError("unsupported bpp")
    strides = (psurface.pitch, bpp)
    srcsize = psurface.h * psurface.pitch
    shape = psurface.h, psurface.w   # surface.pitch // bpp

    dtypes = {1: numpy.uint8,
              2: numpy.uint16,
              3: numpy.uint32,
              4: numpy.uint32
             }

    if SDL_MUSTLOCK(psurface):
        SDL_LockSurface(psurface)
    pxbuf = ctypes.cast(psurface.pixels,
                        ctypes.POINTER(ctypes.c_ubyte * srcsize)).contents
    return numpy.ctypeslib.as_array((ctypes.c_ubyte * srcsize).from_address(ctypes.addressof(pxbuf)))

    return SurfaceArray(shape, dtypes[bpp], pxbuf, 0, strides, "C", psurface,
                        psurface).transpose()


class LCDRenderer:
    def __init__(self, lcd, zoom=4):
        self.lcd = lcd
        self.zoom = zoom
        self.tiles_per_row_in_tile_window = 16
        tile_window_width = (self.tiles_per_row_in_tile_window * 8 + 1) * self.zoom
        tile_window_height = \
            math.ceil(192 / self.tiles_per_row_in_tile_window * 8) * self.zoom
        logging.info("PySDL2 version {}".format(sdl2.__version__))
        sdl_version = sdl2.SDL_version()
        sdl2.SDL_GetVersion(sdl_version)
        logging.info("SDL2 version {}.{}.{}".format(
            sdl_version.major, sdl_version.minor, sdl_version.patch))

        sdl2.ext.init()
        self.tile_window = sdl2.ext.Window(
            "Tile window", size=(tile_window_width, tile_window_height))
        self.tile_window.show()

    def render(self):
        logging.debug("Rendering frame")
        surface = self.tile_window.get_surface()
        pixels = ownpixels2d(surface)
        pixels = numpy.reshape(pixels, (surface.h, surface.pitch))

        for x in range(surface.pitch):
            for y in range(surface.h):
                pixels[y][x] = y % 256

        del pixels

        self.tile_window.refresh()

    def draw_tile(self, tile_idx):
        tile_base_address = tile_idx * 16 + 0x8000
        x_offset = (tile_idx % 16) * 8 * self.zoom
        for tile_line_number in range(8):
            line_base_address = tile_base_address + tile_line_number * 2
            color_byte_1 = self.memory.read(line_base_address)
            color_byte_2 = self.memory.read(line_base_address + 1)
            line_output_colors = color_map[color_byte_1][color_byte_2]

            y_offset = ((tile_idx // 16 + 1) * 8 - tile_line_number) * self.zoom

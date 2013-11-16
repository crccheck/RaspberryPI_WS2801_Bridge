# Simple Python Library for accessing WS2801 LED stripes
# Copyright (C) 2013  Philipp Tiefenbacher <wizards23@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# For more information about this project please visit:
# http://www.hackerspaceshop.com/ledstrips/raspberrypi-ws2801.html

# import binascii
import spidev


gamma = [int(pow(float(i) / 255.0, 2.5) * 255.0) for i in range(256)]


class LedStrip_WS2801(object):
    """Access to SPI with python spidev library."""
    index_map = None

    # spiDevice has format [
    def __init__(self, nLeds, nBuffers=1):
        self.spi = spidev.SpiDev()  # create spi object
        self.spi.open(0, 1)
        self.spi.max_speed_hz = 1000000
        self.nLeds = nLeds
        self.nBuffers = nBuffers
        self.buffers = []
        self.index_map = range(nLeds)  # TODO add a .set_index_map method
        for i in range(0, nBuffers):
            ba = []
            for l in range(0, nLeds):
                ba.extend([0, 0, 0])
            self.buffers.append(ba)

    def close(self):
        if (self.spi != None):
            self.spi.close()
            self.spi = None

    def update(self, bufferNr=0):
        buffer = self.buffers[bufferNr]
        # print binascii.hexlify(bytearray(buffer))
        self.spi.writebytes(buffer)

    def setAll(self, color, bufferNr=0):
        for i in range(0, self.nLeds):
            self.setPixel(i, color, bufferNr)

    def get_index(self, index):
        return self.index_map[index]

    def setPixel(self, index, color, bufferNr=0):
        idx = self.get_index(index)
        self.buffers[bufferNr][idx * 3:idx * 3 + 3] = (
                gamma[color[0]],
                gamma[color[1]],
                gamma[color[2]])


class LedStrip_WS2801_FileBased(LedStrip_WS2801):
    """Filebased acces to SPI."""
    def __init__(self, nLeds, spiDevice, nBuffers=1):
        self.spi = open(spiDevice, "w")
        self.nLeds = nLeds
        self.nBuffers = nBuffers
        self.buffers = []
        for i in range(0, nBuffers):
            ba = bytearray()
            for l in range(0, nLeds):
                ba.extend([0, 0, 0])
            self.buffers.append(ba)

    def update(self, bufferNr=0):
        self.spi.write(self.buffers[bufferNr])
        self.spi.flush()

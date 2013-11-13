# Simple Example for accessing WS2801 LED stripes
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

import math
import sys
import time

from LedStrip_WS2801 import LedStrip_WS2801


def c(rgb):
    """Convert rgb syntax to ints: 'aaff0a' -> [170, 255, 10]"""
    return list(bytearray.fromhex(rgb))


def mySin(a, min, max):
    return min + ((max - min) / 2.) * (math.sin(a) + 1)


def rainbow(a):
    intense = 255
    return [int(mySin(a, 0, intense)), int(mySin(a + math.pi / 2, 0, intense)), int(mySin(a + math.pi, 0, intense))]


def fillAll(ledStrip, color, sleep):
    for i in range(0, ledStrip.nLeds):
        ledStrip.setPixel(i, color)
        ledStrip.update()
        time.sleep(sleep)


def rainbowAll(ledStrip, times, sleep):
    for t in range(0, times):
        for i in range(0, ledStrip.nLeds):
            ledStrip.setPixel(i, rainbow((1.1 * math.pi * (i + t)) / ledStrip.nLeds))
        ledStrip.update()
        if (sleep != 0):
            time.sleep(sleep)


def gradient(ledStrip, sleep=1):
    for i in range(1, ledStrip.nLeds + 1):
        color = 255 * i / ledStrip.nLeds
        ledStrip.setPixel(i, [color, 0, 0])
    ledStrip.update()
    time.sleep(sleep)
    for i in range(1, ledStrip.nLeds + 1):
        color = 255 * i / ledStrip.nLeds
        ledStrip.setPixel(i, [0, color, 0])
    ledStrip.update()
    time.sleep(sleep)
    for i in range(1, ledStrip.nLeds + 1):
        color = 255 * i / ledStrip.nLeds
        ledStrip.setPixel(i, [0, 0, color])
    ledStrip.update()
    time.sleep(sleep)
    for i in range(1, ledStrip.nLeds + 1):
        color = 255 * i / ledStrip.nLeds
        ledStrip.setPixel(i, [color, 0, color])
    ledStrip.update()
    time.sleep(sleep)
    for i in range(1, ledStrip.nLeds + 1):
        color = 255 * i / ledStrip.nLeds
        ledStrip.setPixel(i, [0, color, color])
    ledStrip.update()
    time.sleep(sleep)
    for i in range(1, ledStrip.nLeds + 1):
        color = 255 * i / ledStrip.nLeds
        ledStrip.setPixel(i, [color, color, 0])
    ledStrip.update()
    time.sleep(sleep)


def antialisedPoint(ledStrip, color, step, dscale, sleep=0):
    rr = color[0]
    gg = color[1]
    bb = color[2]
    screenOffset = int(1.0 / (step * dscale)) + 1
    for j in range(-screenOffset, int(ledStrip.nLeds / step + screenOffset)):
        for i in range(0, ledStrip.nLeds):
            delta = 1 - abs(i - j * step) * dscale
            if delta < 0:
                delta = 0
            ledStrip.setPixel(i, [int(delta * rr), int(delta * gg), int(delta * bb)])
        ledStrip.update()
        #   time.sleep(sleep)


def test(ledStrip):
    # oldStrip = LedStrip_WS2801_FileBased(nrOfleds, "/dev/spidev0.0")
    # fillAll(oldStrip, [255, 0, 0], delayTime)
    # oldStrip.close()

    while 1:
        fillAll(ledStrip, [0, 255, 0], delayTime)
        rainbowAll(ledStrip, 200, delayTime)
        fillAll(ledStrip, [255, 0, 0], delayTime)
        fillAll(ledStrip, [0, 255, 0], delayTime)
        fillAll(ledStrip, [0, 0, 255], delayTime)
        antialisedPoint(ledStrip, [255, 0, 0], 0.5, 0.3)
        antialisedPoint(ledStrip, [0, 255, 0], 0.5, 0.3)
        antialisedPoint(ledStrip, [0, 0, 255], 0.5, 0.3)
        rainbowAll(ledStrip, 500, delayTime)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        nrOfleds = 160
    else:
        nrOfleds = int(sys.argv[1])
    delayTime = 0.05

    strip = LedStrip_WS2801(nrOfleds)
    test(strip)

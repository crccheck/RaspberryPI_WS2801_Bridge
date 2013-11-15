import binascii


gamma = [int(pow(float(i) / 255.0, 2.5) * 255.0) for i in range(256)]


class LedStrip_WS2801(object):
    def __init__(self, nLeds, nBuffers=1):
        self.nLeds = nLeds
        self.nBuffers = nBuffers
        self.buffers = []
        for i in range(0, nBuffers):
            ba = []
            for l in range(0, nLeds):
                ba.extend([0, 0, 0])
            self.buffers.append(ba)

    def close(self):
        pass

    def update(self, bufferNr=0):
        buffer = self.buffers[bufferNr]
        print binascii.hexlify(bytearray(buffer))

    def setAll(self, color, bufferNr=0):
        for i in range(0, self.nLeds):
            self.setPixel(i, color, bufferNr)

    def setPixel(self, index, color, bufferNr=0):
        self.buffers[bufferNr][index * 3:index * 3 + 3] = (
                gamma[color[0]],
                gamma[color[1]],
                gamma[color[2]])

# Mario de Leon 19019
# Graficos por computadora basado en lo escrito por Ing. Dennis Aldana / Ing. Carlos Alonso
import struct


class Texture(object):
    def __init__(this, filename):

        with open(filename, "rb") as image:
            image.seek(10)
            headerSize = struct.unpack('=l', image.read(4))[0]

            image.seek(18)
            this.width = struct.unpack('=l', image.read(4))[0]
            this.height = struct.unpack('=l', image.read(4))[0]

            image.seek(headerSize)

            this.pixels = []

            for y in range(this.height):
                pixelRow = []

                for x in range(this.width):
                    b = ord(image.read(1)) / 255
                    g = ord(image.read(1)) / 255
                    r = ord(image.read(1)) / 255
                    pixelRow.append([r, g, b])

                this.pixels.append(pixelRow)

    def getColor(this, u, v):
        if 0 <= u < 1 and 0 <= v < 1:
            return this.pixels[int(v * this.height)][int(u * this.width)]
        else:
            return None

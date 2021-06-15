import spidev


class SPI:
    def __init__(self, bus=0, device=0):
        self.__bus = bus
        self.__device = device
        global spi
        spi = spidev.SpiDev()
        spi.open(bus, device)  # Bus SPI0, slave op CE 0
        spi.max_speed_hz = 10 ** 5  # 100 kHz

    def read_channel(self, channel):
        val = spi.xfer2([1, (8+channel) << 4, 0])
        data = ((val[1] & 3) << 8) + val[2]
        return data

    def close_spi(self):
        self.spi.close()

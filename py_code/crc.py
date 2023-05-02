
class crc8:
    def __init__(self, initial_value = 0, poly = 0x07):
        self.crc = initial_value
        self.poly = poly

    def get_crc8(self, message):
        tmp_crc = self.crc
        for msg_idx in range(len(message)):
            tmp_crc = tmp_crc ^ message[msg_idx]
            for bit_idx in range(8):
                if (tmp_crc & 0x80 == 0x80):
                    tmp_crc = self.poly ^ (tmp_crc << 1)
                else:
                    tmp_crc = tmp_crc << 1
        return (tmp_crc & 0xFF)

class crc16:
    def __init__(self, initial_value = 0, poly = 0x8005):
        self.crc = initial_value
        self.poly = poly

    def get_crc8(self, message):
        tmp_crc = self.crc
        for msg_idx in range(len(message)):
            tmp_crc = tmp_crc ^ message[msg_idx]
            for bit_idx in range(16):
                if (tmp_crc & 0x8000 == 0x8000):
                    tmp_crc = self.poly ^ (tmp_crc << 1)
                else:
                    tmp_crc = tmp_crc << 1
        return (tmp_crc & 0xFFFF)


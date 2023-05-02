import time
import digitalio
from digitalio import *
from crc import crc8

def is_bit_one(data, bit_idx):
    if (data & (0x01 << bit_idx)) != 0x00:
        return True
    else:
        return False

def calculate_crc8(data_24_bit):
    first_byte = data_24_bit & 0x000000FF
    second_byte = (data_24_bit & 0x0000FF00) >> 8
    third_byte = (data_24_bit & 0x00FF0000) >> 16
    message = (first_byte, second_byte, third_byte)
    crc_obj = crc8(0xFF, 0x9B)
    return crc_obj.get_crc8(message)

def add_crc(data):
    check_sum = calculate_crc8(data)
    return ((data & 0x00FFFFFF) | (check_sum << 24))

def validate_data(data):
    received_crc = (data&0xFF000000) >> 24
    calc_crc = calculate_crc8(data)
    if(received_crc == calc_crc):
        return True
    else:
        return False

class gpio_com:
    FIRST_READ_TIME_OUT_COUNTER_MAX = 1000
    READ_TIME_OUT_COUNTER_MAX       = 500
    WRITE_WAIT_TIME = 0.00055

    def __init__(self, scl, sda):

        self.scl = DigitalInOut(scl)
        self.scl.direction = Direction.OUTPUT
        self.scl.drive_mode = DriveMode.OPEN_DRAIN
        self.scl.value = False # block state

        self.sda = DigitalInOut(sda)
        self.sda.direction = Direction.OUTPUT
        self.sda.drive_mode = DriveMode.OPEN_DRAIN
        self.sda.value = True

        self.prev_read_data = 0

    def __sync(self):
        """ This method block the program until the communication partner also execute this method.
            After getting out of this method, the read/write process is activated.
        """

        # Turn scl output high level
        self.scl.value = True

        # Wait until the partner turns the port high level as well
        while (self.scl.value == False):
            pass

    def __block_read_write(self):
        self.scl.value = False


    def read_24_bit(self):

        bit_idx          = 0
        read_data        = 0
        prev_scl_value   = True
        cur_scl_value    = True
        time_out_counter = self.FIRST_READ_TIME_OUT_COUNTER_MAX

        # Wait for the writer excuting "write_32_bit"
        self.__sync()

        while True:
            # Get the clock level
            cur_scl_value = self.scl.value

            # Raising edege detected?
            if (prev_scl_value == False) and (cur_scl_value == True):
                # Initialize the time out counter
                time_out_counter = self.READ_TIME_OUT_COUNTER_MAX

                # Check the data bit value
                if (self.sda.value == True):
                    # Tareget bit is "1"
                    read_data |= (1 << bit_idx)
                    bit_idx += 1
                else:
                    # Tareget bit is "0"
                    read_data &= ~(1 << bit_idx)
                    bit_idx += 1

            # 32 bit received?
            if(bit_idx == 32):
                # Return the result
                break

            # Checking the time out
            if(time_out_counter == 0):
                break

            time_out_counter -= 1

            # Store previous clock value to detect the rising edge
            prev_scl_value = cur_scl_value

        # Change scl port to blocking state to sync with the partner at the next communication
        self.__block_read_write()

        if(time_out_counter == 0):
            # time out occur
            return self.prev_read_data
        elif validate_data(read_data) == False:
            return self.prev_read_data
        else:
            self.prev_read_data = read_data & (0x00FFFFFF)
            return (read_data & (0x00FFFFFF))

    def write_24_bit(self, data):
        # Wait for the reader excuting "read_32_bit"
        self.__sync()

        time.sleep(0.001)

        data_with_crc = add_crc(data)
        for bit_idx in range(32):

            time.sleep(self.WRITE_WAIT_TIME)

            self.scl.value = False

            self.sda.value = is_bit_one(data_with_crc, bit_idx)

            self.scl.value = True

        # Change scl port to blocking state to sync with the partner at the next communication
        self.__block_read_write()



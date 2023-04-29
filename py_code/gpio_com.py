import time
import digitalio
from digitalio import *

def calculate_checksum(data_24_byte):
    first_byte = data_24_byte & 0x000000FF
    second_byte = (data_24_byte & 0x0000FF00) >> 8
    third_byte = (data_24_byte & 0x00FF0000) >> 16
    check_sum = 0x100 - ((first_byte + second_byte + third_byte) & 0x000000FF)
    return check_sum

def add_checksum(data):
    check_sum = calculate_checksum(data)
    return ((data & 0x00FFFFFF) | (check_sum << 24))

def validate_data(data):
    received_checksum = (data&0xFF000000) >> 24
    calc_check_sum = calculate_checksum(data)
    if(received_checksum == calc_check_sum):
        return True
    else:
        return False

class gpio_com:
    READ_TIME_OUT_COUNTER_MAX = 5000
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
        time_out_counter = self.READ_TIME_OUT_COUNTER_MAX

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
            return 0
        elif(validate_data(read_data) == False):
            # Communication failed
            return 0
        else:
            return (read_data & (0x00FFFFFF))

    def write_24_bit(self, data):
        def is_bit_one(data, bit_idx):
            if (data & (0x01 << bit_idx)) != 0x00:
                return True
            else:
                return False

        # Wait for the reader excuting "read_32_bit"
        self.__sync()

        time.sleep(0.001)

        data_with_checksum = add_checksum(data)
        for bit_idx in range(32):

            time.sleep(self.WRITE_WAIT_TIME)

            self.scl.value = False

            self.sda.value = is_bit_one(data_with_checksum, bit_idx)

            self.scl.value = True

        # Change scl port to blocking state to sync with the partner at the next communication
        self.__block_read_write()


import time
import digitalio
from digitalio import *

def calculate_checksum(data_24_byte):
    first_byte = data_24_byte & 0x000000FF
    second_byte = (data_24_byte & 0x0000FF00) >> 8
    third_byte = (data_24_byte & 0x00FF0000) >> 16
    check_sum = 0x100 - ((first_byte + second_byte + third_byte) & 0x000000FF)
    return check_sum

def add_checksum(data):
    check_sum = calculate_checksum(data)
    return ((data & 0x00FFFFFF) | (check_sum << 24))

def validate_data(data):
    received_checksum = (data&0xFF000000) >> 24
    calc_check_sum = calculate_checksum(data)
    if(received_checksum == calc_check_sum):
        return True
    else:
        return False

class gpio_com:
    READ_TIME_OUT_COUNTER_MAX = 5000
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
        time_out_counter = self.READ_TIME_OUT_COUNTER_MAX

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
            return 0
        elif(validate_data(read_data) == False):
            # Communication failed
            return 0
        else:
            return (read_data & (0x00FFFFFF))

    def write_24_bit(self, data):
        def is_bit_one(data, bit_idx):
            if (data & (0x01 << bit_idx)) != 0x00:
                return True
            else:
                return False

        # Wait for the reader excuting "read_32_bit"
        self.__sync()

        time.sleep(0.001)

        data_with_checksum = add_checksum(data)
        for bit_idx in range(32):

            time.sleep(self.WRITE_WAIT_TIME)

            self.scl.value = False

            self.sda.value = is_bit_one(data_with_checksum, bit_idx)

            self.scl.value = True

        # Change scl port to blocking state to sync with the partner at the next communication
        self.__block_read_write()


import time
import digitalio
from digitalio import *

class gpio_com_master:
    TIME_OUT_COUNTER_MAX = 5000

    def __init__(self, scl, sda):

        self.scl = DigitalInOut(scl)
        self.scl.direction = Direction.OUTPUT
        self.scl.drive_mode = DriveMode.OPEN_DRAIN
        self.scl.value = True

        self.sda = DigitalInOut(sda)
        self.sda.direction = Direction.OUTPUT
        self.sda.drive_mode = DriveMode.OPEN_DRAIN
        self.sda.value = True

    def start_slave_scan_keybord(self):
        self.sda.value = False

    def is_slave_scanning_keybord(self):
        self.sda.value = True
        return (self.sda.value == False)

    def start_listening_slave_data(self):
        self.scl.value = True

    def stop_listening_slave_data(self):
        self.scl.value = False


    def read_32_bit(self):

        bit_idx          = 0
        read_data        = 0
        prev_scl_value   = True
        cur_scl_value    = True
        time_out_counter = self.TIME_OUT_COUNTER_MAX
        while True:
            cur_scl_value = self.scl.value

            if (prev_scl_value == False) and (cur_scl_value == True):
                time_out_counter = self.TIME_OUT_COUNTER_MAX
                if (self.sda.value == True):
                    read_data |= (1 << bit_idx)
                    bit_idx += 1
                else:
                    read_data &= ~(1 << bit_idx)
                    bit_idx += 1

            if(bit_idx == 32):
                return read_data

            if(bit_idx != 0): # TODO: no need?
                if(time_out_counter == 0):
                    return 0
                time_out_counter -= 1

            prev_scl_value = cur_scl_value

class gpio_com_slave:
    WAIT_TIME = 0.00055

    def __init__(self, scl, sda):

        self.scl = DigitalInOut(scl)
        self.scl.direction = Direction.OUTPUT
        self.scl.drive_mode = DriveMode.OPEN_DRAIN
        self.scl.value = True

        self.sda = DigitalInOut(sda)
        self.sda.direction = Direction.OUTPUT
        self.sda.drive_mode = DriveMode.OPEN_DRAIN
        self.sda.value = True

    def set_scanning_state(self):
        self.sda.value = False

    def set_scanning_finished_state(self):
        self.sda.value = True

    def is_master_listening(self):
        self.scl.value = True
        return (self.scl.value == True)

    def send_32_bit(self, data):
        def is_bit_one(data, bit_idx):
            if (data & (0x01 << bit_idx)) != 0x00:
                return True
            else:
                return False

        for bit_idx in range(32):

            time.sleep(self.WAIT_TIME)
            self.scl.value = False

            self.sda.value = is_bit_one(data, bit_idx)

            self.scl.value = True


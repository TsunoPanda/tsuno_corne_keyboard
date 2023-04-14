import digitalio
from digitalio import *
from board import *

class corne_board():
    ### corne PCB mapping ###
    # keybord matrix column
    CORNE_COL0 = A3
    CORNE_COL1 = A2
    CORNE_COL2 = A1
    CORNE_COL3 = A0
    CORNE_COL4 = SCK
    CORNE_COL5 = D20

    # keybord matrix raw
    CORNE_ROW0 = D4
    CORNE_ROW1 = D5
    CORNE_ROW2 = D6
    CORNE_ROW3 = D7

    # I2C communication with the OLED
    CORNE_SDA = D2
    CORNE_SCL = D3

    # uart with LEDs?
    CORNE_LED = TX

    # uart with the other corne keyboard
    CORNE_DATA = RX

    CORNE_COL_NUMBER = 6
    CORNE_ROW_NUMBER = 4

    DIGITAL_HIGH = True
    DIGITAL_LOW  = False

    column_douts = None
    row_dins     = None

    def __digital_out_port(self, port):
        dout           = digitalio.DigitalInOut(port)
        dout.direction = digitalio.Direction.OUTPUT
        dout.value     = self.DIGITAL_LOW
        return dout

    def __digital_in_port(self, port):
        din           = digitalio.DigitalInOut(port)
        din.direction = digitalio.Direction.INPUT
        din.pull      = Pull.DOWN
        return din

    def __init__(self):
        self.column_douts = [
            self.__digital_out_port(self.CORNE_COL0),
            self.__digital_out_port(self.CORNE_COL1),
            self.__digital_out_port(self.CORNE_COL2),
            self.__digital_out_port(self.CORNE_COL3),
            self.__digital_out_port(self.CORNE_COL4),
            self.__digital_out_port(self.CORNE_COL5)
            ]

        self.row_dins = [
            self.__digital_in_port(self.CORNE_ROW0),
            self.__digital_in_port(self.CORNE_ROW1),
            self.__digital_in_port(self.CORNE_ROW2),
            self.__digital_in_port(self.CORNE_ROW3)
            ]


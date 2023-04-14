
class keyboard_scanner():

    SW_RELEASED = 0
    SW_PRESSED  = 1

    def __init__(self, digital_high, digital_low, dout_ports, din_ports):
        self.digital_high = digital_high
        self.digital_low  = digital_low
        self.dout_ports  = dout_ports
        self.din_ports   = din_ports

    def scan_keyboad(self):
        """ This function get the keyboard state (pressed or released) matrix.
            Assuming column GPIOs are digital output, and row GPIOs are digital input.
        """

        # Get keyboard column number
        column_number = len(self.dout_ports)

        # Get keyboard row number
        row_number    = len(self.din_ports)

        # Initialize the matrix where the scan result to be saved.
        keyboard_state_matrix = [ [self.SW_RELEASED] * column_number for i in range (row_number)]

        # Loop for each column (digital output)
        for column_idx, column_dout in enumerate(self.dout_ports):
            # Output high level to scan the column.
            column_dout.value = self.digital_high

            # Loop for each row (digital input)
            for row_idx, row_din in enumerate(self.din_ports):
                # If high level detected..
                if row_din.value == self.digital_high:
                    # Then it means the key is being pressed.
                    keyboard_state_matrix[row_idx][column_idx] = self.SW_PRESSED
                else:
                    # Else key is not pressed.
                    keyboard_state_matrix[row_idx][column_idx] = self.SW_RELEASED

            #Return the port level into low, since the column scan has been done.
            column_dout.value = self.digital_low

        # Return the result
        return keyboard_state_matrix


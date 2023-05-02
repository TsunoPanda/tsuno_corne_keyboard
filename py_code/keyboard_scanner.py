
class keyboard_scanner():

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

        # Initialize the the scan result.
        scan_result = 0

        # Loop for each column (digital output)
        for column_idx, column_dout in enumerate(self.dout_ports):
            # Output high level to scan the column.
            column_dout.value = self.digital_high

            # Loop for each row (digital input)
            for row_idx, row_din in enumerate(self.din_ports):
                # If high level detected..
                if row_din.value == self.digital_high:

                    # Caluculate bit index
                    bit_idx = row_idx*column_number + column_idx

                    # Then it means the key is being pressed.
                    scan_result |= (1 << bit_idx)


            #Return the port level into low, since the column scan has been done.
            column_dout.value = self.digital_low

        # Return the result
        return scan_result


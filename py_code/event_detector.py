
def get_bit(data, bit_idx):
    return ((data >> bit_idx) & 1)

class event_detector():
    EVENT_NOT_HAPPENNED = 0
    EVENT_HAPPENNED     = 1
    KEY_EVENT_PRESSED   = 0
    KEY_EVENT_RELEASED  = 1

    def __init__(self, bit_length, released_value = 0):
        self.bit_length            = bit_length
        self.sw_released           = released_value
        self.sw_pressed            = 1 if (released_value == 0) else 0
        self.prev_scan_result      = 0

    def get_event(self, scan_result):
        key_event_list = []

        # In this variable, if the bit is one, it means the pressed or released event happenned
        event_exist = scan_result ^ self.prev_scan_result

        for bit_idx in range(self.bit_length):
            if (get_bit(event_exist, bit_idx) == self.EVENT_HAPPENNED):
                if(get_bit(scan_result, bit_idx) == self.sw_pressed):
                    key_event_list.append((bit_idx, self.KEY_EVENT_PRESSED))
                elif(get_bit(scan_result, bit_idx) == self.sw_released):
                    key_event_list.append((bit_idx, self.KEY_EVENT_RELEASED))

        self.prev_scan_result = scan_result

        return key_event_list

if __name__ == "__main__":

    ed = event_detector(32)

    print(ed.get_event(0x00000000))
    print(ed.get_event(0x00000001))
    print(ed.get_event(0x00000000))
    print(ed.get_event(0x90000000))


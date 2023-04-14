
class event_detector():
    KEY_NO_EVENT  = 0
    KEY_PRESSED   = 1
    KEY_RELEASED  = 2

    def __init__(self, released_value, pressed_value):
        self.sw_released           = released_value
        self.sw_pressed            = pressed_value
        self.number_of_columns     = 0
        self.number_of_raws        = 0
        self.prev_key_state_matrix = None

    def __empty_event_list(self):
        key_event_list = [
                            [self.KEY_NO_EVENT]*self.number_of_columns
                            for tmp in range(self.number_of_rows)
                         ]

        return key_event_list

    def get_event(self, key_state_matrix):

        if self.prev_key_state_matrix is None:
            self.number_of_rows        = len(key_state_matrix)
            self.number_of_columns     = len(key_state_matrix[0])
            self.prev_key_state_matrix = key_state_matrix

            return self.__empty_event_list()
        else:
            if self.number_of_rows != len(key_state_matrix):
                pass # exception

            if self.number_of_columns != len(key_state_matrix[0]):
                pass # exception

        key_event_list = self.__empty_event_list()

        for row_idx in range(self.number_of_rows):
            for column_idx in range(self.number_of_columns):
                switch_state = key_state_matrix[row_idx][column_idx]

                prev_switch_state = self.prev_key_state_matrix[row_idx][column_idx]

                key_event_list[row_idx][column_idx] = (self.KEY_NO_EVENT if (switch_state == prev_switch_state) else
                                                       self.KEY_PRESSED  if (switch_state == self.sw_pressed)   else
                                                       self.KEY_RELEASED)

        self.prev_key_state_matrix = key_state_matrix

        return key_event_list

if __name__ == "__main__":

    test_matrix = [[0,0],
                   [0,0]]

    test_matrix2 = [[0,1],
                    [1,0]]

    ed = event_detector(0, 1)

    print(ed.get_event(test_matrix))
    print(ed.get_event(test_matrix2))
    print(ed.get_event(test_matrix2))
    print(ed.get_event(test_matrix))


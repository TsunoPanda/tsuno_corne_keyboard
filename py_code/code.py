from corne_board import corne_board
from keyboard_scanner import keyboard_scanner
from event_detector import event_detector
import time

corne = corne_board()
scanner = keyboard_scanner(corne.DIGITAL_HIGH,
                           corne.DIGITAL_LOW,
                           corne.column_douts,
                           corne.row_dins)

keyboard_event = event_detector(keyboard_scanner.SW_RELEASED, keyboard_scanner.SW_PRESSED)

while True:
    time.sleep(0.01)
    key_state_matrix = scanner.scan_keyboad()

    event_matrix = keyboard_event.get_event(key_state_matrix)

    for raw_idx, raw_event in enumerate(event_matrix):
        for col_idx, event in enumerate(raw_event):
            if event == event_detector.KEY_PRESSED:
                    print(f"BTN_L{col_idx}{raw_idx} is pressed.")
            elif event == event_detector.KEY_RELEASED:
                    print(f"BTN_L{col_idx}{raw_idx} is released.")
            else:
                pass


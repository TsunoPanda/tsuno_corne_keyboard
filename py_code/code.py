from corne_board      import corne_board
from keyboard_scanner import keyboard_scanner
from event_detector   import event_detector
from gpio_com         import gpio_com
import time

corne = corne_board()
scanner = keyboard_scanner(corne.DIGITAL_HIGH,
                           corne.DIGITAL_LOW,
                           corne.column_douts,
                           corne.row_dins)

self_keyboard_event = event_detector(32)
partner_keyboard_event = event_detector(32)

com = gpio_com(corne_board.CORNE_PAIR_SCL, corne_board.CORNE_PAIR_SDA)

while True:
    time.sleep(0.01)
    key_scan_result = scanner.scan_keyboad()
    partner_scan_result = com.read_24_bit()

    self_event_list = self_keyboard_event.get_event(key_scan_result)
    partner_event_list = partner_keyboard_event.get_event(partner_scan_result)

    for key_idx, event in self_event_list:
        if event == event_detector.KEY_EVENT_PRESSED:
            print(f"Left Key index {key_idx}, is pressed")
        else:
            print(f"Left Key index {key_idx}, is released")

    for key_idx, event in partner_event_list:
        if event == event_detector.KEY_EVENT_PRESSED:
            print(f"Right Key index {key_idx}, is pressed")
        else:
            print(f"Right Key index {key_idx}, is released")


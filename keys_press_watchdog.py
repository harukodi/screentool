import threading
from classes.DisplayState import display_state
from pynput import keyboard
from time import sleep

CTRL_KEYS = {keyboard.Key.ctrl_l, keyboard.Key.ctrl_r}

def is_shift_f4(pressed_keys):
    return (keyboard.Key.f4 in pressed_keys 
            and keyboard.Key.shift in pressed_keys 
            and not (pressed_keys & CTRL_KEYS))

def is_ctrl_shift_f4(pressed_keys):
    return (keyboard.Key.f4 in pressed_keys 
            and (pressed_keys & CTRL_KEYS)
            and keyboard.Key.shift in pressed_keys)

def keys_press_watchdog():
    pressed_keys = set()
    
    keyboard_listener = keyboard.Listener(
        on_press=lambda key: pressed_keys.add(key),
        on_release=lambda key: pressed_keys.discard(key)
    )
    keyboard_listener.start()

    def worker():
        while True:
            if is_ctrl_shift_f4(pressed_keys):
                display_state.windows_watchdog_enabled = not display_state.windows_watchdog_enabled
                display_state.change_display_mode("extend")
                display_state.previous_app_active = None
                while is_ctrl_shift_f4(pressed_keys):
                    sleep(0.08)
                    
            elif is_shift_f4(pressed_keys):
                if (keyboard.Key.f4 in pressed_keys and keyboard.Key.shift in pressed_keys):
                    if display_state.get_current_display_state() == "extend":
                        display_state.change_display_mode("internal")
                    elif display_state.get_current_display_state() == "internal":
                        display_state.change_display_mode("extend")
                        
                    while (keyboard.Key.f4 in pressed_keys or keyboard.Key.shift in pressed_keys):
                        sleep(0.08)
                sleep(0.08)
            else:
                sleep(0.08)
        
    key_press_watchdog_thread = threading.Thread(target=worker, daemon=True)
    key_press_watchdog_thread.start()
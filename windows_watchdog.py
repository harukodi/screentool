import json, threading
from pynput import keyboard
from ctypes import create_unicode_buffer, windll
from time import sleep
from classes.DisplayState import display_state

BROWSER_MARKERS = ["chrome", "vivaldi", "firefox", "edge", "opera", "brave"]
_alt_pressed = False

def _on_key_press(key):
    global _alt_pressed
    if key in (keyboard.Key.alt_l, keyboard.Key.alt_r, keyboard.Key.alt):
        _alt_pressed = True

def _on_key_release(key):
    global _alt_pressed
    if key in (keyboard.Key.alt_l, keyboard.Key.alt_r, keyboard.Key.alt):
        _alt_pressed = False

def start_alt_key_listener():
    listener = keyboard.Listener(
        on_press=_on_key_press,
        on_release=_on_key_release
    )
    listener.daemon = True
    listener.start()

def is_alt_tab_active() -> bool:
    # Alt stays held down for the entire duration of an alt-tab switch,
    # even while Tab is pressed multiple times in quick succession.
    return _alt_pressed

def get_user_defined_apps():
    global native_apps, browser_sites
    with open("./display_settings.json", "r") as settings_file:
        settings = json.load(settings_file)
    native_apps = [app.lower() for app in settings["native_apps"]]
    browser_sites = [site.lower() for site in settings["browser_sites"]]

def get_foreground_window_title() -> str | None:
    hWnd = windll.user32.GetForegroundWindow()
    length = windll.user32.GetWindowTextLengthW(hWnd)
    active_window_title_buf = create_unicode_buffer(length + 1)
    windll.user32.GetWindowTextW(hWnd, active_window_title_buf, length + 1)
    if active_window_title_buf.value:
        return active_window_title_buf.value.lower()
        
def is_user_app_active():
    active_window_title = get_foreground_window_title()
    if not active_window_title:
        return None

    is_browser_tab = any(browser in active_window_title for browser in BROWSER_MARKERS)
    if is_browser_tab:
        # Title belongs to a browser window: only match against browser_sites,
        # since a native app's name (e.g. "stremio") could appear in an unrelated
        # tab title and cause a false positive.
        return any(site in active_window_title for site in browser_sites)
    else:
        # Title belongs to a standalone app: match against native_apps.
        # Safe to use substring matching here since there's no browser tab
        # text to accidentally match against.
        return any(app in active_window_title for app in native_apps)
    
def windows_watchdog():
    start_alt_key_listener()
    
    def worker():
        get_user_defined_apps()
        previous_app_active = None
        while True:
            sleep(0.08)
            if not display_state.windows_watchdog_enabled:
                continue
            
            if is_alt_tab_active():
                sleep(0.2)
                continue

            app_active = is_user_app_active()
            if app_active is None:
                continue
            
            if app_active != previous_app_active:
                target_mode = "internal" if app_active else "extend"
                # Skip the switch entirely if we're already on the target mode
                if display_state.get_current_display_state != target_mode:
                    display_state.change_display_mode(target_mode)
                        
                previous_app_active = app_active
                
    processes_watchdog_thread = threading.Thread(target=worker, daemon=True)
    processes_watchdog_thread.start()
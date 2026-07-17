import psutil, os
from classes.DisplayState import display_state
from check_if_display_mode_is_changed import check_if_display_mode_is_changed
from windows_watchdog import windows_watchdog
from keys_press_watchdog import keys_press_watchdog
from create_windows_task import create_windows_task
from time import sleep

def kill_old_process_instances():
    sleep(2)
    process_name = "screen_tool_aiyo.exe"
    instances = [process for process in psutil.process_iter(["name"]) if process.info["name"] and process_name in process.info["name"].lower()]
    instances.sort(key= lambda process : process.create_time())
    for process in instances[:-1]:
        try:
            process.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
def main():
    kill_old_process_instances()
    create_windows_task()
    check_if_display_mode_is_changed()
    
    if display_state.get_default_display_mode() != "internal":
        windows_watchdog()
        keys_press_watchdog()
    else:
        keys_press_watchdog()

    while True:
        sleep(300)

if __name__ == "__main__":
    main()
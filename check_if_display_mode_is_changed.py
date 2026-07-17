from classes.DisplayState import display_state

def check_if_display_mode_is_changed():
    current_display_state = display_state.get_current_display_state()
    default_display_state = display_state.get_default_display_mode()

    if current_display_state != default_display_state:
        display_state.change_display_mode(default_display_state)
    else:
        pass
import os, shutil, subprocess, sys
from string import Template
from classes.TaskState import task_state

def get_bundle_resources_path(file: str):
    try:
        base_path = sys._MEIPASS # pyright: ignore[reportAttributeAccessIssue]
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, file)

def create_temp_folder():
    os.mkdir("./temp")
    
def delete_temp_folder():
    shutil.rmtree("./temp")

def create_task_file():
    task_parms = {
        "CURRENT_USER": os.getlogin(),
        "SCREEN_TOOL_BINARY_PATH": rf"{os.path.abspath(".")}\screen_tool_aiyo.exe",
        "SCREEN_TOOL_WORKING_DIR_PATH": os.path.abspath(".")
    }
    
    with open(get_bundle_resources_path("task_template/task_screen_tool_aiyo.xml"), "r") as task_file:
        task_file = task_file.read()
        
    template = Template(task_file)
    task_file = template.substitute(task_parms)
    with open(f"./temp/task_screen_tool_aiyo_temp.xml", "w") as task_file_temp:
        task_file_temp.write(task_file)

def create_windows_task():
    if task_state.is_user_admin() and not task_state.is_task_already_created():
        create_temp_folder()
        create_task_file()
        # recreates the task if it already exists
        try:
            delete_task_command = ["schtasks", "/delete", "/tn", "start screen_tool_aiyo", "/f"]
            print(subprocess.run(delete_task_command, stdout=subprocess.DEVNULL))
        except Exception:
            pass
        create_task_command = ["schtasks", "/create", "/tn", "start screen_tool_aiyo", "/xml", "./temp/task_screen_tool_aiyo_temp.xml"]
        print(subprocess.run(create_task_command, stdout=subprocess.DEVNULL))
        delete_temp_folder()
        task_state.mark_task_created()
    elif not task_state.is_user_admin() and not task_state.is_task_already_created():
        os._exit(1)
    else:
        pass
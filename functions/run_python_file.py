import os, subprocess

def run_python_file(working_directory, file_path, args=None):
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
    try:
        if valid_target_dir == False:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_dir):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if ".py" != target_dir[-3:]:
            return f'Error: "{file_path}" is not a Python file'
        commands = ["python", target_dir]
        if args != None:
            for arg in args:
                commands.extend(arg)
        process = subprocess.run(commands, capture_output=True, text=True, timeout=30)
        output = ""
        if process.returncode != 0:
            output += f"Process exited with {process.returncode}\n"
        if process.stderr == "" and process.stdout == "":
            output += "No output produced\n"
        else:
            output += f"STDOUT: {process.stdout}\n"
            output += f"STDERR: {process.stderr}\n"
        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"
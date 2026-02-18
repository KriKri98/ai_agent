import os, subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="executes a function in a specified file in a directory relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path and file to the python file that should be executed, relative to the working directory (default is the working directory itself)",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Arguments to be passed to the python function",
                items=types.Schema(
                    type=types.Type.STRING,
                ),

                    
                
            ),
        },
    ),
)

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
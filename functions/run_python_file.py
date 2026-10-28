import os
import subprocess
from sys import stderr, stdin, stdout


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        is_valid_target_file = (
            os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        )

        if not is_valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not target_file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]

        if args:
            for arg in args:
                command.append(arg)

        completed_process = subprocess.run(
            command, text=True, timeout=30, cwd=working_dir_abs, capture_output=True
        )

        output_string = ""

        if completed_process.returncode:
            output_string += f"Process exited with code {completed_process.returncode}"

        if completed_process.stdout:
            output_string += f"STDOUT: {completed_process.stdout}"
        elif completed_process.stderr:
            output_string += f"STDERR: {completed_process.stderr}"
        else:
            output_string += "No output produced"

        return output_string

    except Exception as e:
        return f"Error: executing Python file: {e}"

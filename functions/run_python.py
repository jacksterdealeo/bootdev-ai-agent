import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path, args=[]):
    working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    if not os.path.splitext(abs_file_path)[1] == '.py':
        return f'Error: "{file_path}" is not a Python file.'

    """
    subprocess.run(args, *, stdin=None, input=None,
        stdout=None, stderr=None, capture_output=False,
        shell=False, cwd=None, timeout=None, check=False,
        encoding=None, errors=None, text=None, env=None,
        universal_newlines=None, **other_popen_kwargs)
    """
    try:
        process_result = subprocess.run(
            args=['python', file_path] + args,
            timeout=30,
            capture_output=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=working_directory,
        )
    except Exception as e:
        return f'Error: executing Python file: {e}'

    stdout_str = process_result.stdout
    stderr_str = process_result.stderr

    result = (f'STDOUT: {stdout_str}\nSTDERR: {stderr_str}\n')
    if process_result.returncode != 0:
        result += f'Process exited with code {process_result.returncode}\n'
    if stdout_str == '':
        result += 'No output produced.'

    return result


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description='Executes a Python file, constrained to the working directory.',
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.TYPE_UNSPECIFIED,
                description="Arguments to pass to the Python file.",
            ),
        },
    ),
)

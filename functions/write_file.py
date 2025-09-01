import os
from google.genai import types


def write_file(working_directory, file_path, content):
    working_directory = os.path.abspath(working_directory)
    current_file = os.path.abspath(os.path.join(working_directory, file_path))
    dir_of_file = os.path.split(current_file)[0]

    if not current_file.startswith(working_directory):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(dir_of_file):
        try:
            os.makedirs(dir_of_file)
        except Exception as e:
            return f'Error: {e}'

    if os.path.isfile(file_path):
        try:
            os.remove(file_path)
        except Exception as e:
            return f'Error: {e}'

    if os.path.isdir(file_path):
        try:
            os.rmdir(file_path)
        except Exception as e:
            return f'Error: {e}'

    try:
        with open(file_path, "x") as f:
            f.write(content)
    except Exception as e:
        return f'Error: {e}'

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

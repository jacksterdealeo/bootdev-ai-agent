import os
from google.genai import types


def get_files_info(working_directory, directory="."):
    result = ""
    if directory == ".":
        result += ("Result for current directory:\n")
    else:
        result += (f"Result for '{directory}' directory:\n")

    working_directory = os.path.abspath(working_directory)
    current_directory = os.path.abspath(os.path.join(working_directory, directory))

    if not current_directory.startswith(working_directory):
        result += (f'    Error: Cannot list "{directory}" as it is outside the permitted working directory')
        return result
    if not os.path.isdir(current_directory):
        result += (f'    Error: "{directory}" is not a directory')
        return result

    files = os.listdir(current_directory)
    for file in files:
        file_path = os.path.join(current_directory, file)
        try:
            file_size = os.path.getsize(file_path)
        except OSError as e:
            result += f"Error: {e}"
            return result
        is_dir = os.path.isdir(file_path)
        result += f" - {file}: file_size={file_size} bytes, is_dir={is_dir}\n"

    result = result.rstrip()
    return result


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)

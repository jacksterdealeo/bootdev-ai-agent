import os


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

    return result.rstrip()

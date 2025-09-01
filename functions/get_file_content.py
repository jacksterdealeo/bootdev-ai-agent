import os
from google.genai import types


MAX_CHARS = 10_000


def get_file_content(working_directory, file_path):
    working_directory = os.path.abspath(working_directory)
    current_file = os.path.abspath(os.path.join(working_directory, file_path))

    if not current_file.startswith(working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(current_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(current_file, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if len(file_content_string) == MAX_CHARS:
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return file_content_string
    except Exception as e:
        return f'Error: {e}'


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f'Gets the contents of a text file, truncated at {MAX_CHARS}, constrained to the working directory.',
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to read from, relative to the working directory.",
            ),
        },
    ),
)

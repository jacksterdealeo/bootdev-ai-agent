import os
import sys

from google import genai
from google.genai import types
from dotenv import load_dotenv
from functions.get_files_info import available_functions
from functions.get_files_info import get_files_info
from functions.run_python import run_python_file


system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

model_name = 'gemini-2.0-flash-001'


if len(sys.argv) < 2:
    print("No Prompt Provided!")
    exit(1)
user_prompt = sys.argv[1]

verbose_flag = False
if len(sys.argv) >= 3:
    if sys.argv[2] == "--verbose":
        verbose_flag = True

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model=model_name,
    contents=messages,
    config=types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=system_prompt
    ),
)

if response.function_calls is not None:
    for function_call in (response.function_calls):
        print(f"Calling function: {function_call.name}({function_call.args})")
        working_directory = os.path.abspath(".")
        directory = function_call.args['directory']
        if directory is None:
            directory = "."
        match function_call.name:
            case 'get_files_info':
                print(get_files_info(working_directory, directory))
else:
    if verbose_flag:
        print(f"User prompt: {response.text}")
    else:
        print(response.text)
if verbose_flag:
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

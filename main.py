import os
import sys

from google import genai
from google.genai import types
from dotenv import load_dotenv

from functions.get_files_info import get_files_info
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import get_file_content
from functions.get_file_content import schema_get_file_content
from functions.run_python import run_python_file
from functions.run_python import schema_run_python_file
from functions.write_file import write_file
from functions.write_file import schema_write_file

available_functions = types.Tool(
    function_declarations=[
        schema_get_file_content,
        schema_get_files_info,
        schema_run_python_file,
        schema_write_file,
    ]
)


working_directory = os.path.abspath("./calculator")

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

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


def get_generated_content():
    return client.models.generate_content(
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        ),
    )


def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    function_args = function_call_part.args
    function_args['working_directory'] = working_directory
    if 'args' not in function_args:
        function_args['args'] = []
    invalid_function_name_error = types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"error": f"Unknown function: {function_name}"},
            )
        ],
    )
    invalid_function_args_error = types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"error": f"Invalid function arguments: {function_args}"},
            )
        ],
    )

    result = 'Empty Result'
    try:
        match function_name:
            case 'get_file_content':
                result = get_file_content(
                    working_directory,
                    function_args['file_path']
                )
            case 'get_files_info':
                if 'directory' not in function_args:
                    function_args['directory'] = '.'
                result = get_files_info(
                    working_directory,
                    directory=function_args['directory']
                )
            case 'run_python_file':
                result = run_python_file(
                        working_directory,
                        file_path=function_args['file_path'],
                        args=function_args['args'],
                )
            case 'write_file':
                result = write_file(
                    working_directory,
                    file_path=function_args['file_path'],
                    content=function_args['content'],
                )
            case _:
                return invalid_function_name_error
    except TypeError:
        return invalid_function_args_error
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": result},
            )
        ],
    )


def dispatcher():
    for cand in response.candidates:
        for part in cand.content.parts:
            if part.function_call:
                fn = part.function_call
                print(f'- Calling function: {fn.name}')
                # append tool result as a user message
                result = call_function(fn)
                messages.append(types.Content(role="user", parts=result.parts))
    if verbose_flag:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    '''
    function_calls = response.function_calls
    if function_calls is not None:
        for call in (function_calls):
            print(f"Calling function: {call.name}({call.args})")
            result = call_function(call)
            if result.parts[0].function_response.response is not None:
                function_response = result.parts[0].function_response.response
                messages.append(types.Content(role="user", parts=result.parts))
                if verbose_flag:
                    print(f"-> {function_response}")
            else:
                err = 'No function response.'
                # messages.append(types.Content(role="user", parts=[types.Part(text=err)]))
                raise Exception(err)
    else:
        if verbose_flag:
            print(f"User prompt: {response.text}")
        else:
            print(response.text)
    '''


for i in range(20):
    response = get_generated_content()

    # append the model’s message(s)
    for cand in response.candidates:
        messages.append(types.Content(role="model", parts=cand.content.parts))

    # dispatch any function calls found in parts
    made_call = False
    for cand in response.candidates:
        for part in cand.content.parts:
            if getattr(part, "function_call", None):
                fn = part.function_call
                print(f"- Calling function: {fn.name}")
                result = call_function(fn)  # pass the full call (name + args)
                messages.append(types.Content(role="user", parts=result.parts))
                made_call = True

    # if no calls, check for text and finish
    if not made_call:
        has_text = any(getattr(p, "text", None) for c in response.candidates for p in c.content.parts)
        if has_text:
            print(f"Final response:\n{response.text}")
            break

import os, sys
from dotenv import load_dotenv

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

from google import genai
from google.genai import types

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

client = genai.Client(api_key=api_key)


response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents=messages,
)

if verbose_flag:
    print(f"User prompt: {response.text}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
else:
    print(response.text)


'''
def main():
    print("Hello from bootdev-ai-agent!")


if __name__ == "__main__":
    main()
'''

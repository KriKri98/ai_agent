import os
from dotenv import load_dotenv

import argparse

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
# Now we can access `args.user_prompt`



load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key == None:
    raise RuntimeError("api key not found")

from google import genai
client = genai.Client(api_key=api_key)
from google.genai import types

from google.genai import types

messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

response = client.models.generate_content(model="gemini-2.5-flash", contents=messages)
if response.usage_metadata == None:
    raise RuntimeError("failed API request")
if args.verbose == True:
    print(f"User prompt: {messages}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

print(response.text)


def main():
    pass


if __name__ == "__main__":
    main()

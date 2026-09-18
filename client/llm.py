import os

from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY is not set.")

client = genai.Client(api_key=api_key)


def ask_gemini(prompt, tools):
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=tools
        )
    )

    return response

def send_tool_result(contents, tool_name, tool_result, tools):
    contents.append(
        types.Content(
            role="user",
            parts=[
                types.Part.from_function_response(
                    name=tool_name,
                    response={
                        "result": str(tool_result)
                    }
                )
            ]
        )
    )

    return client.models.generate_content(
        model="gemini-3.6-flash",
        contents=contents,
        config=types.GenerateContentConfig(
            tools=tools
        )
    )
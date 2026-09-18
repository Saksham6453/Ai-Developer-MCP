import asyncio

from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from google.genai import types

from client.gemini_adapter import mcp_tools_to_gemini_tools
from client.llm import ask_gemini, send_tool_result


async def main():
    transport = StdioTransport(
        command="uv",
        args=["run", "python", "-m", "server.main"]
    )

    client = Client(transport)

    async with client:
        tools = await client.list_tools()

        gemini_tools = mcp_tools_to_gemini_tools(tools)

        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(
                        text="Explain how the login flow works in this project."
                    )
                ]
            )
        ]

        response = ask_gemini(
            "Explain how the login flow works in this project. Use the available tools to inspect the relevant code before answering.",
            gemini_tools
        )

        while True:
            function_call = None

            if not response.candidates:
                print("\nGemini returned no candidates.")
                break

            content = response.candidates[0].content

            if content and content.parts:
                for part in content.parts:
                    if part.function_call:
                        function_call = part.function_call
                        break

            if not function_call:
                print("\nFinal Answer:")
                print(response.text)
                break

            print(f"\nGemini → {function_call.name}")
            print(f"Arguments → {function_call.args}")

            tool_result = await client.call_tool(
                function_call.name,
                function_call.args
            )

            print("MCP → Tool executed")

            if content:
                contents.append(content)

            response = send_tool_result(
                contents,
                function_call.name,
                tool_result,
                gemini_tools
            )


if __name__ == "__main__":
    asyncio.run(main())
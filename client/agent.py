#Extract the agentic loop
from fastmcp import Client
from fastmcp.client.transports import StdioTransport
from google.genai import types

from client.gemini_adapter import mcp_tools_to_gemini_tools
from client.llm import ask_gemini, send_tool_result


async def run_agent(user_query):
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
                    types.Part.from_text(text=user_query)
                ]
            )
        ]

        response = ask_gemini(
            user_query,
            gemini_tools
        )

        tool_activity = []

        while True:
            function_call = None

            if not response.candidates:
                return "Gemini returned no response.", tool_activity

            content = response.candidates[0].content

            if content and content.parts:
                for part in content.parts:
                    if part.function_call:
                        function_call = part.function_call
                        break

            if not function_call:
                return response.text, tool_activity

            tool_activity.append({
                "tool": function_call.name,
                "arguments": dict(function_call.args)
            })

            tool_result = await client.call_tool(
                function_call.name,
                function_call.args
            )

            if content:
                contents.append(content)

            response = send_tool_result(
                contents,
                function_call.name,
                tool_result,
                gemini_tools
            )
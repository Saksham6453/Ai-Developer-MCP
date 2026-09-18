from google.genai import types
def mcp_tools_to_gemini_tools(tools):
    declarations = []

    for tool in tools:
        declarations.append(
            types.FunctionDeclaration(
                name=tool.name,
                description=tool.description or "",
                parameters_json_schema=tool.input_schema,
            )
        )

    return [
        types.Tool(
            function_declarations=declarations
        )
    ]
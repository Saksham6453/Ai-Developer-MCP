def mcp_tools_to_llm_tools(tools):
    llm_tools = []

    for tool in tools:
        llm_tools.append({
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description or "",
                "parameters": tool.input_schema,
            }
        })

    return llm_tools
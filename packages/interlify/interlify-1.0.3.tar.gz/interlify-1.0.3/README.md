# Interlify Client

A Python client for the [Interlify API](https://www.interlify.com).

## Installation

Install via pip:

```bash
pip install interlify
```

Usage:

```python
from openai import OpenAI
from interlify import Interlify


client = OpenAI()

# Initialize the client
interlify = Interlify(
    api_key="YOUR_API_KEY", 
    project_id="YOUR_PROJECT_ID", 
    auth_headers=[
        {"Authorization": "Bearer YOUR_TOKEN"}
        ]
    )

# Prepare tools
tools = client.tools()

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "What is the weather like in Paris today?"}],
    # Use tools
    tools=tools
)

response_message = response.choices[0].message
tool_calls = response_message.tool_calls

messages.append(response_message)


for tool_call in tool_calls:
    function_name = tool_call.function.name
 
    function_args = json.loads(tool_call.function.arguments)

    # Call the tool using interlify
    function_response = interlify.call_tool(function_name, function_args)

    print(f"function_response: {function_response}")

    messages.append(
        {
            "role": "tool",
            "content": str(function_response),
            "tool_call_id": tool_call.id,
        }
    )

final_response = client.chat.completions.create(
    model=model, messages=messages, tools=tools, tool_choice="auto"
)

print(final_response.choices[0].message.content)

```

To setup the tools and projects, please visit to [interlify](https://www.interlify.com) website. 
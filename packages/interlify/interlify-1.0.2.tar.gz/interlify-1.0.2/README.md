# Interlify Client

A Python client for the [Interlify API](https://www.interlify.com).

## Installation

Install via pip:

```bash
pip install interlify-client
```

Usage:

```python
from interlify.client import Interlify

client = Interlify(
    api_key="YOUR_API_KEY", 
    project_id="YOUR_PROJECT_ID", 
    auth_headers=[
        {"Authorization": "Bearer YOUR_TOKEN"}
        ]
    )

tools = client.tools()

print("Available Tools:", tools)

```


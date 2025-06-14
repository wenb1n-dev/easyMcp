[![简体中文](https://img.shields.io/badge/简体中文-点击查看-orange)](README-zh.md)
[![English](https://img.shields.io/badge/English-Click-yellow)](README.md)

# easyMcp
### Just two steps to quickly build an easily extensible mcp server framework that supports all Model Context Protocol (MCP) transmission modes (STDIO, SSE, Streamable Http).
Please give a like, friends!

## User Manual

### 1. Step One [Optional] Define the required configuration information
Define the configuration information needed for your project in `src/config/.env`, for example, if you need database configuration:
```aiignore
 # MySQL Database Configuration
MYSQL_HOST=192.168.3.229
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=root
MYSQL_DATABASE=a_llm
MYSQL_ROLE=admin
```


### 2. Step Two Create Your Own Tool
Add your own tool class in the `src/handles` directory, refer to the example.py sample

* Inherit from BaseHandler
* Define the `name` property, which is the name of the tool
* Define the `description` property, which is the description of the tool
* Implement the `get_tool_description` method, which tells the mcp client what your tool does
* Implement the `run_tool` method, which is the method called by the mcp client to use the tool; implement your tool logic here
* Import the new tool in `__init__.py`

example.py
```aiignore
from typing import Dict, Any, Sequence

from mcp import Tool
from mcp.types import TextContent
from .base import BaseHandler
from config import get_config


class Example(BaseHandler):
    name = "get_Example"
    description = (
        "this is Example xxxx"
    )

    def get_tool_description(self) -> Tool:
        return Tool(
            name=self.name,
            description=self.description,
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "This is the text that must be entered for the example"
                    }
                },
                "required": ["text"]
            }
        )

    async def run_tool(self, arguments: Dict[str, Any]) -> Sequence[TextContent]:

            try:
                if "text" not in arguments:
                    raise ValueError("Missing text content")

                text = arguments["text"]

                # Reference configuration information
                config = get_config()

                ## todo something

                result = "xxxxxxx"

                # Join all results with commas
                return [TextContent(type="text", text=','.join(result))]

            except Exception as e:
                return [TextContent(type="text", text=f"error: {str(e)}")]

```

__init__.py 
```aiignore
from .example import Example


__all__ = [
    "Example",
]
```

### 3. Start
Currently, this framework supports all Model Context Protocol (MCP) transmission modes (STDIO, SSE, Streamable Http).

#### 1. Streamable Http Mode

- Use uv to start the service

Add the following content to your mcp client tool, such as cursor, cline, etc.

mcp json example:
````
{
  "mcpServers": {
    "easyMcp": {
      "name": "easyMcp",
      "type": "streamableHttp",
      "description": "",
      "isActive": true,
      "baseUrl": "http://localhost:3000/mcp/"
    }
  }
}
````

Start command
```
# Install dependencies
uv sync

# Start
uv run src/server.py

```


#### 2. SSE Mode

- Use uv to start the service

Add the following content to your mcp client tool, such as cursor, cline, etc.

mcp json example:
````
{
  "mcpServers": {
    "easyMcp": {
      "name": "easyMcp",
      "description": "",
      "isActive": true,
      "baseUrl": "http://localhost:9000/sse"
    }
  }
}
````

Start command
```
# Install dependencies
uv sync

# Start
uv run src/server.py --sse
```

#### 3. STDIO Mode

Add the following content to your mcp client tool, such as cursor, cline, etc.

mcp json example:
```
{
  "mcpServers": {
      "operateMysql": {
        "isActive": true,
        "name": "operateMysql",
        "command": "uv",
        "args": [
          "--directory",
          "G:\\python\\mysql_mcp\\src",  # Replace this with your project path
          "run",
          "server.py",
          "--stdio"
        ],
        "env": {
          "MYSQL_HOST": "192.168.xxx.xxx",
          "MYSQL_PORT": "3306",
          "MYSQL_USER": "root",
          "MYSQL_PASSWORD": "root",
          "MYSQL_DATABASE": "a_llm",
          "MYSQL_ROLE": "admin"
       }
    }
  }
}    
```

## Screenshot
![image](https://github.com/user-attachments/assets/72854681-16ad-4dc8-a095-5e6e63e07deb)



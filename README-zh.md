[![简体中文](https://img.shields.io/badge/简体中文-点击查看-orange)](README-zh.md)
[![English](https://img.shields.io/badge/English-Click-yellow)](README.md)

# easyMcp
### 仅需两步，使开发者快速的搭建一个易扩展且支持stdio与sse两种启动模式的mcp server服务框架。
帮忙点个赞啊，朋友们。

## 使用手册

### 1. 第一步【可选】定义所需的配置信息
在 src/config/.env 定义自己项目所需配置信息，例如需要数据库配置：
```aiignore
 # MySQL数据库配置
MYSQL_HOST=192.168.3.229
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=root
MYSQL_DATABASE=a_llm
MYSQL_ROLE=admin
```


### 2. 第二步 创建自己的工具
在 src/handles 目录下新增自己的工具类，参考 example.py 示例

* 继承 BaseHandler 
* 定义 name 属性，及工具的名称
* 定义 description 属性，及工具的描述
* 实现 get_tool_description 方法，这是告诉mcp client 你有一个什么作用的工具
* 实现 run_tool 方法，这是mcp client 调用工具的方法，在这里实现你工具的逻辑
* 将新增的工具在 __init__.py 引用

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

                # 引用配置信息
                config = get_config()

                ## todo something

                result = "xxxxxxx"

                # 用逗号连接所有结果
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

### 3. 启动
目前该框架支持两种模式的启动，stdio 和 sse 。

#### 1. SSE 方式

- 使用 uv 启动服务

将以下内容添加到你的 mcp client 工具中，例如cursor、cline等

mcp json 如下
````
{
  "mcpServers": {
    "operateMysql": {
      "name": "operateMysql",
      "description": "",
      "isActive": true,
      "baseUrl": "http://localhost:9000/sse"
    }
  }
}
````

启动命令
```
# 下载依赖
uv sync

# 启动
uv run server.py
```

#### 2. STDIO 方式 

将以下内容添加到你的 mcp client 工具中，例如cursor、cline等

mcp json 如下
```
{
  "mcpServers": {
      "operateMysql": {
        "isActive": true,
        "name": "operateMysql",
        "command": "uv",
        "args": [
          "--directory",
          "G:\\python\\mysql_mcp\\src",  # 这里需要替换为你的项目路径
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

## 效果图
![image](https://github.com/user-attachments/assets/72854681-16ad-4dc8-a095-5e6e63e07deb)



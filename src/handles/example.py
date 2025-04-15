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
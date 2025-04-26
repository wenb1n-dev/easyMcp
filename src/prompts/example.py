from typing import Dict, Any

from mcp import GetPromptResult
from mcp.types import Prompt, PromptArgument, TextContent, PromptMessage

from prompts.BasePrompt import BasePrompt


class MysqlExample(BasePrompt):
    name = "mysql-prompt"
    description = (
        "这是mysql相关问题的提示词"
    )

    def get_prompt(self) -> Prompt:
        return Prompt(
            name= self.name,
            description= self.description,
            arguments=[
                PromptArgument(
                    name="arg1", description="mysql的问题描述", required=True
                )
            ],
        )

    async def run_prompt(self, arguments: Dict[str, Any]) -> GetPromptResult:

        if "arg1" not in arguments:
            raise ValueError("Missing arg1 content")

        arg1 = arguments["arg1"]

        prompt = f"你是一个资深的mysql专家，目前有一个问题：{arg1},"
        prompt += "请分析原因，并以markdown格式返回结果，要求包含问题分析、解决方案、风险点"

        return GetPromptResult(
            description="mysql prompt",
            messages=[
                PromptMessage(
                    role="user",
                    content=TextContent(type="text", text=prompt),
                )
            ],
        )
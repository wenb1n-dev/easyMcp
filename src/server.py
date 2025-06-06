import asyncio
import uvicorn
import contextlib

from collections.abc import AsyncIterator

from typing import Sequence, Dict, Any

from mcp import types
from mcp.server.sse import SseServerTransport

from mcp.server.lowlevel import Server
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
from mcp.types import  Tool, TextContent
from pydantic import AnyUrl

from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.types import Scope, Receive, Send

from config.event_store import InMemoryEventStore
from handles.base import ToolRegistry
from prompts.BasePrompt import PromptRegistry

# 初始化服务器
app = Server("easyMcp")

@app.list_prompts()
async def handle_list_prompts() -> list[types.Prompt]:
    return PromptRegistry.get_all__prompts()


@app.get_prompt()
async def handle_get_prompt(name: str, arguments: Dict[str, Any] | None) -> types.GetPromptResult:
   prompt = PromptRegistry.get_prompt(name)
   return await prompt.run_prompt(arguments)


@app.list_tools()
async def list_tools() -> list[Tool]:
    """
        列出所有可用的MySQL操作工具
    """
    return ToolRegistry.get_all_tools()

@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> Sequence[TextContent]:
    """调用指定的工具执行操作
    
    Args:
        name (str): 工具名称
        arguments (dict): 工具参数

    Returns:
        Sequence[TextContent]: 工具执行结果

    Raises:
        ValueError: 当指定了未知的工具名称时抛出异常
    """
    tool = ToolRegistry.get_tool(name)

    return await tool.run_tool(arguments)


async def run_stdio():
    """运行标准输入输出模式的服务器
    
    使用标准输入输出流(stdio)运行服务器，主要用于命令行交互模式
    
    Raises:
        Exception: 当服务器运行出错时抛出异常
    """
    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        try:
            await app.run(
                read_stream,
                write_stream,
                app.create_initialization_options()
            )
        except Exception as e:
            print(f"服务器错误: {str(e)}")
            raise

def run_sse():
    """运行SSE(Server-Sent Events)模式的服务器
    
    启动一个支持SSE的Web服务器，允许客户端通过HTTP长连接接收服务器推送的消息
    服务器默认监听0.0.0.0:9000
    """
    sse = SseServerTransport("/messages/")

    async def handle_sse(request):
        """处理SSE连接请求
        
        Args:
            request: HTTP请求对象
        """
        async with sse.connect_sse(
                request.scope, request.receive, request._send
        ) as streams:
            await app.run(streams[0], streams[1], app.create_initialization_options())

    starlette_app = Starlette(
        debug=True,
        routes=[
            Route("/sse", endpoint=handle_sse),
            Mount("/messages/", app=sse.handle_post_message)
        ],
    )
    uvicorn.run(starlette_app, host="0.0.0.0", port=9000)

def run_streamable_http(json_response: bool):
    event_store = InMemoryEventStore()

    session_manager = StreamableHTTPSessionManager(
        app=app,
        event_store=event_store,
        json_response=json_response,
    )

    async def handle_streamable_http(
            scope: Scope, receive: Receive, send: Send
    ) -> None:
        await session_manager.handle_request(scope, receive, send)

    @contextlib.asynccontextmanager
    async def lifespan(app: Starlette) -> AsyncIterator[None]:
        async with session_manager.run():
            yield


    starlette = Starlette(
        debug=True,
        routes=[
            Mount("/mcp", app=handle_streamable_http)
        ],
        lifespan=lifespan,
    )
    uvicorn.run(starlette, host="0.0.0.0", port=3000)

if __name__ == "__main__":
    import sys

    # 根据命令行参数选择启动模式
    if len(sys.argv) > 1 and sys.argv[1] == "--stdio":
        # 标准输入输出模式
        asyncio.run(run_stdio())
    elif len(sys.argv) > 1 and sys.argv[1] == "--sse":
        # SSE 模式
        run_sse()
    else:
        # Streamable Http 模式
        run_streamable_http(False)

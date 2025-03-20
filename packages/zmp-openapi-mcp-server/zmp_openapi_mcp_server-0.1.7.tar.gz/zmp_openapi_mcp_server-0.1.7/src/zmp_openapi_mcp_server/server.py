import logging
import logging.config
from typing import List

import anyio
import click
import httpx
import mcp.types as types
from mcp.server.lowlevel import Server
from mcp.types import TextContent, Tool
from pydantic import FileUrl
from zmp_openapi_toolkit import AuthenticationType, MixedAPISpecConfig, ZmpAPIWrapper
from zmp_openapi_toolkit.models.operation import ZmpAPIOperation

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler()
    ]
)
logging.getLogger("zmp_openapi_toolkit.openapi.zmpapi_models").setLevel(logging.INFO)
logging.getLogger("zmp_openapi_toolkit.toolkits.toolkit").setLevel(logging.INFO)
logger = logging.getLogger("appLogger")
logger.setLevel(logging.DEBUG)

SAMPLE_RESOURCES = {
    "greeting": "Hello! This is a sample text resource.",
    "help": "This server provides a few sample text resources for testing.",
    "about": "This is the simple-resource MCP server implementation.",
}

def get_zmp_api_wrapper(endpoint: str, access_key: str, spec_path: str):
    logger.info(f":::: endpoint: {endpoint}")
    logger.info(f":::: access_key: {access_key}")
    logger.info(f":::: spec_path: {spec_path}")

    try:
        mixed_api_spec_config = MixedAPISpecConfig.from_mixed_spec_file(
            file_path=spec_path
        )
    except Exception as e:
        raise ValueError(f"Failed to load OpenAPI spec file: {e}")

    zmp_api_wrapper = ZmpAPIWrapper(
        endpoint,
        auth_type=AuthenticationType.ACCESS_KEY,
        access_key=access_key,
        mixed_api_spec_config=mixed_api_spec_config,
    )

    return zmp_api_wrapper


async def fetch_website(
    url: str,
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    headers = {
        "User-Agent": "MCP Test Server (github.com/modelcontextprotocol/python-sdk)"
    }
    async with httpx.AsyncClient(follow_redirects=True, headers=headers) as client:
        response = await client.get(url)
        response.raise_for_status()
        return [types.TextContent(type="text", text=response.text)]


@click.command()
@click.option("--port", default=8000, help="Port to listen on for SSE")
@click.option("--transport", type=click.Choice(["stdio", "sse"]), default="stdio", help="Transport type")
@click.option("--endpoint", "-e", type=str, required=True, help="ZMP OpenAPI endpoint")
@click.option("--access-key", "-s", type=str, required=True, help="ZMP OpenAPI access key")
@click.option("--spec-path", "-p", type=click.Path(exists=True), required=True, help="Path to the OpenAPI spec file")
@click.option("-v", "--verbose", count=True)
def main(
    port: int, transport: str, endpoint: str, access_key: str, spec_path: str, verbose: int = 2
) -> int:
    app = Server("zmp-openapi-mcp-server")
    zmp_api_wrapper = get_zmp_api_wrapper(
        endpoint=endpoint, access_key=access_key, spec_path=spec_path
    )
    operations: List[ZmpAPIOperation] = zmp_api_wrapper.get_operations()

    @app.list_resources()
    async def list_resources() -> list[types.Resource]:
        return [
            types.Resource(
                uri=FileUrl(f"file:///{name}.txt"),
                name=name,
                description=f"A sample text resource named {name}",
                mimeType="text/plain",
            )
            for name in SAMPLE_RESOURCES.keys()
        ]

    @app.read_resource()
    async def read_resource(uri: FileUrl) -> str | bytes:
        name = uri.path.replace(".txt", "").lstrip("/")

        if name not in SAMPLE_RESOURCES:
            raise ValueError(f"Unknown resource: {uri}")

        return SAMPLE_RESOURCES[name]

    @app.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        operation = next((op for op in operations if op.name == name), None)
        if operation is None:
            raise ValueError(f"Unknown tool: {name}")

        logger.debug(f"arguments: {arguments}")

        path_params = operation.path_params(**arguments) if operation.path_params else None
        query_params = operation.query_params(**arguments) if operation.query_params else None
        request_body = operation.request_body(**arguments) if operation.request_body else None

        logger.debug(f"path_params: {path_params}")
        logger.debug(f"query_params: {query_params}")
        logger.debug(f"request_body: {request_body}")


        result = zmp_api_wrapper.run(
            operation.method,
            operation.path,
            path_params=path_params,
            query_params=query_params,
            request_body=request_body,
        )

        return [TextContent(type="text", text=f"result: {result}")]
    

    @app.list_tools()
    async def list_tools() -> list[Tool]:
        tools: List[Tool] = []
        for operation in operations:
            tool: Tool = Tool(
                name=operation.name,
                description=operation.description,
                inputSchema=operation.args_schema.model_json_schema(),
            )
            tools.append(tool)

            logger.debug("-" * 100)
            logger.debug(f":::: tool: {tool.name}\n{tool.inputSchema}")

        return tools

    if transport == "sse":
        from mcp.server.sse import SseServerTransport
        from starlette.applications import Starlette
        from starlette.routing import Mount, Route

        sse = SseServerTransport("/messages/")

        async def handle_sse(request):
            async with sse.connect_sse(
                request.scope, request.receive, request._send
            ) as streams:
                await app.run(
                    streams[0], streams[1], app.create_initialization_options()
                )

        starlette_app = Starlette(
            debug=True,
            routes=[
                Route("/sse", endpoint=handle_sse),
                Mount("/messages/", app=sse.handle_post_message),
            ],
        )

        import uvicorn

        uvicorn.run(starlette_app, host="0.0.0.0", port=port)
    else:
        from mcp.server.stdio import stdio_server

        async def arun():
            async with stdio_server() as streams:
                await app.run(
                    streams[0], streams[1], app.create_initialization_options()
                )

        anyio.run(arun)

    return 0

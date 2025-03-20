import importlib
import logging
from typing import List
from click import Path
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    TextContent,
    Tool,
)
from zmp_openapi_toolkit import AuthenticationType, MixedAPISpecConfig, ZmpAPIWrapper
from zmp_openapi_toolkit.models.operation import ZmpAPIOperation


def get_alert_manager_agent(endpoint: str, access_key: str, spec_path: Path):
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


async def serve(endpoint: str, access_key: str, spec_path: Path) -> None:
    logger = logging.getLogger(__name__)

    logger.debug(f"endpoint: {endpoint}, access_key: {access_key}")

    if endpoint is not None and access_key is not None:
        zmp_api_wrapper = get_alert_manager_agent(endpoint, access_key, spec_path)
        logger.info(f"Using endpoint {endpoint} and access key {access_key}")

    operations: List[ZmpAPIOperation] = zmp_api_wrapper.get_operations()

    server = Server("zmp-openapi-mcp-server")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        tools: List[Tool] = []
        for operation in operations:
            tools.append(
                Tool(
                    name=operation.name,
                    description=operation.description,
                    inputSchema=operation.args_schema.model_json_schema(),
                )
            )

        return tools

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        operation = next((op for op in operations if op.name == name), None)
        if operation is None:
            raise ValueError(f"Unknown tool: {name}")

        path_params = operation.path_params(**arguments)
        query_params = operation.query_params(**arguments)
        request_body = operation.request_body(**arguments)

        result = zmp_api_wrapper.run(
            operation.method,
            operation.path,
            path_params=path_params,
            query_params=query_params,
            request_body=request_body,
        )

        return [TextContent(type="text", text=result)]

    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options, raise_exceptions=True)

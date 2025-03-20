import click
import logging
import sys
from .server import serve

@click.command()
@click.option("--endpoint", "-e", type=str, required=True, help="ZMP OpenAPI endpoint")
@click.option("--access-key", "-a", type=str, required=True, help="ZMP OpenAPI access key")
@click.option("-v", "--verbose", count=True)
def main(endpoint: str, access_key: str, verbose: int = 2) -> None:
    """ZMP OpenAPI MCP Server"""
    import asyncio

    logging_level = logging.WARN
    if verbose == 1:
        logging_level = logging.INFO
    elif verbose >= 2:
        logging_level = logging.DEBUG

    logging.basicConfig(level=logging_level, stream=sys.stdout)
    asyncio.run(serve(endpoint, access_key))

if __name__ == "__main__":
    main()

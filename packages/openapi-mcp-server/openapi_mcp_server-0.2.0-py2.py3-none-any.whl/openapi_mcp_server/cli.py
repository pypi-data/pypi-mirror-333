"""
Command line interface for the OpenAPI MCP Server.
"""
import argparse
import os
from .env_loader import load_env_file
from . import __main__


def main():
    """
    Main entry point for the CLI.
    """
    parser = argparse.ArgumentParser(
        description="OpenAPI MCP Server CLI",
        prog="openapi_mcp_server"
    )
    parser.add_argument(
        "--env",
        help="Path to .env file to load environment variables from",
        default=None
    )

    args = parser.parse_args()

    # Load environment variables
    env_path = args.env if args.env else os.path.join(os.getcwd(), ".env")
    load_env_file(env_path)

    # # Here you would start your server or run whatever functionality you need
    # print(f"OpenAPI MCP Server started with environment loaded from: {env_path}")

    # Call the main function from __main__.py
    __main__.main(env_path)

    return 0

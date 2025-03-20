#!/usr/bin/env python3
import asyncio
import os
import sys
import aiohttp
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio

# Constants
SERVER_URL =  "https://stingray-app-gb2an.ondigitalocean.app/pearai-server-api2"
SERVER_URL = "http://localhost:8000"

# Get auth token from command line argument
if len(sys.argv) < 2:
    raise ValueError("Auth token must be provided as command line argument")
AUTH_TOKEN = sys.argv[1]

server = Server("pearai-mcp")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    List available tools.
    Each tool specifies its arguments using JSON Schema validation.
    """
    return [
        types.Tool(
            name="deploy-from-path",
            description="Deploy a website from a zip file path",
            inputSchema={
                "type": "object",
                "properties": {
                    "zip_file_path": {
                        "type": "string",
                        "description": "Absolute path to the zip file to deploy"
                    },
                },
                "required": ["zip_file_path"],
            },
        )
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    Handle tool execution requests.
    """
    if name != "deploy-from-path":
        raise ValueError(f"Unknown tool: {name}")

    if not arguments:
        raise ValueError("Missing arguments")

    zip_file_path = arguments.get("zip_file_path")
    if not zip_file_path:
        raise ValueError("Missing zip_file_path")

    if not os.path.isabs(zip_file_path):
        raise ValueError("zip_file_path must be an absolute path")

    try:
        # Read zip file content
        with open(zip_file_path, 'rb') as f:
            zip_content = f.read()

        # Prepare form data
        form = aiohttp.FormData()
        form.add_field('zip_file',
                      zip_content,
                      filename='dist.zip',
                      content_type='application/zip')

        # Make POST request to deployment endpoint
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f'{SERVER_URL}/deploy-netlify',
                headers={
                    "Authorization": f"Bearer {AUTH_TOKEN}"
                },
                data=form
            ) as response:
                result = await response.text()
                return [
                    types.TextContent(
                        type="text",
                        text=result
                    )
                ]

    except FileNotFoundError:
        return [
            types.TextContent(
                type="text",
                text=str({"error": f"Zip file not found at path: {zip_file_path}"})
            )
        ]
    except Exception as e:
        return [
            types.TextContent(
                type="text",
                text=str({"error": str(e)})
            )
        ]

async def main():
    # Run the server using stdin/stdout streams
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="pearai-mcp",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
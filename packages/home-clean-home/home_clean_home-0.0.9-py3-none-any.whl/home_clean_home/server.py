from enum import StrEnum
from typing import Literal

import mcp.server.stdio
from mcp.server.models import InitializationOptions
from mcp.types import TextContent, Tool
from mcp.server import NotificationOptions, Server
from pydantic import BaseModel, Field

from .load import load_hch_service_details_info, load_hch_service_price_info

SERVICE_OPTS = Literal[
    "Detail Cleaning",
    "Move In Cleaning",
    "Move Out Cleaning",
    "Post-Renovation Cleaning",
    "Spring Cleaning (Occupied Unit)",
    "Floor Cleaning or Floor Care",
    "Formaldehyde (VOC)",
    "Disinfecting",
    "Household Accessory Cleaning (e.g. Sofa, Mattress, Carpet, Curtains)",
    "Customised or Combination Cleaning",
    "Commercial Cleaning",
]


class HchTools(StrEnum):
    GREETS = "get_greetings"
    RESIDENTIAL_SUB_SERVICES = "get_residential_sub_services"
    SERVICE_DETAILS = "get_service_details"
    SERVICE_PRICE_INFO = "get_service_price_info"


class HchResidentialServices(StrEnum):
    DETAIL = "Detail Cleaning"
    MOVE_IN = "Move In Cleaning"
    MOVE_OUT = "Move Out Cleaning"
    POST_RENOVATION = "Post-Renovation Cleaning"
    SPRING = "Spring Cleaning (Occupied Unit)"
    FLOOR = "Floor Cleaning or Floor Care"
    FORMALDEHYDE = "Formaldehyde (VOC)"
    DISINFECTING = "Disinfecting"
    HOUSEHOLD_ACCESSORY = "Household Accessory Cleaning (e.g. Sofa, Mattress, Carpet, Curtains)"
    CUSTOMISED = "Customised or Combination Cleaning"


class HchGetGreetings(BaseModel):
    scope: str = "default"


class HchGetResidentialServices(BaseModel):
    scope: str = "default"


class HchGetServiceDetailsInfo(BaseModel):
    service: SERVICE_OPTS = Field(description="Sub-service under residential cleaing or commercial cleaning service.")


class HchGetServicePriceInfo(BaseModel):
    service: SERVICE_OPTS = Field(description="Sub-service under residential cleaing or commercial cleaning service.")


server = Server("home-clean-home")
service2details_info = load_hch_service_details_info()
service2price_info = load_hch_service_price_info()


def get_greetings(scope: str = "default") -> str:
    """Get greetings message when user sends a greeting/requests a price quotation/inquires about booking/sends an
    image without context.

    Args:
        scope (str, optional): Scope of greetings message. Defaults to "default".

    Returns:
        str: Greetings message.
    """
    match scope:
        case "default":
            return (
                "Hi, I'm Minnie from Home Clean Home. Thanks for messaging us!\n\n"
                "May I check if you're enquiring for residential cleaning service or commercial cleaning service?"
            )
        case _:
            raise ValueError(f"Unknown scope: {scope}")


def get_residential_sub_services(scope: str = "default") -> list[str]:
    """Get all sub-services under residential cleaning service.

    Args:
        scope (str, optional): Scope of residential sub-services. Defaults to "default".

    Returns:
        list[str]: A list of sub-services under residential cleaning service.
    """
    match scope:
        case "default":
            return [service.value for service in HchResidentialServices]
        case _:
            raise ValueError(f"Unknown scope: {scope}")


def get_service_details(service: SERVICE_OPTS) -> str:
    """Get service details with respect to the user selected service. Service can be either the sub-service under
    residential cleaning or commercial cleaning service.

    Args:
        service (SERVICE_OPTS): Sub-service under residential cleaing or commercial cleaning service.

    Returns:
        str: Service details.
    """
    details_info = service2details_info.get(service, None)
    if not details_info:
        return f"No details found for {service}."

    return f"{'='*50}\n".join(details_info)


def get_service_price_info(service: SERVICE_OPTS) -> str:
    """Get service price info with respect to the user selected service.Service can be either the sub-service under
    residential cleaning or commercial cleaning service.

    Args:
        service (SERVICE_OPTS): Sub-service under residential cleaing or commercial cleaning service.

    Returns:
        str: Service price info.
    """
    price_info = service2price_info.get(service, None)
    if not price_info:
        return f"No price info found for {service}."

    return f"{'='*50}\n".join(price_info)


@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available tools. Each tool specifies its arguments using JSON Schema validation.

    Returns:
        list[Tool]: A list of tools available for the server.
    """
    return [
        Tool(
            name=HchTools.GREETS,
            description="Get greetings message when user sends a greeting/requests a price quotation/inquires about booking/sends an image without context.",
            inputSchema=HchGetGreetings.model_json_schema(),
        ),
        Tool(
            name=HchTools.RESIDENTIAL_SUB_SERVICES,
            description="Get all sub-services under residential cleaning service.",
            inputSchema=HchGetResidentialServices.model_json_schema(),
        ),
        Tool(
            name=HchTools.SERVICE_DETAILS,
            description="Get service details with respect to the user selected service. Service can be either the sub-service under residential cleaning or commercial cleaning service.",
            inputSchema=HchGetServiceDetailsInfo.model_json_schema(),
        ),
        Tool(
            name=HchTools.SERVICE_PRICE_INFO,
            description="Get service price info with respect to the user selected service. Service can be either the sub-service under residential cleaning or commercial cleaning service.",
            inputSchema=HchGetServicePriceInfo.model_json_schema(),
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool execution requests. Tools can modify server state and notify clients of changes.

    Args:
        name (str): Tool name.
        arguments (dict): Tool arguments.

    Returns:
        list[TextContent]: A list of text content to be sent to the client.
    """
    match name:
        case HchTools.GREETS:
            scope = arguments.get("scope", "default")
            greetings = get_greetings(scope)
            return [TextContent(type="text", text=greetings)]

        case HchTools.RESIDENTIAL_SUB_SERVICES:
            scope = arguments.get("scope", "default")
            services = get_residential_sub_services(scope)
            formatted_output = "\n".join(f"{index+1}. {service}" for index, service in enumerate(services))
            return [TextContent(type="text", text=f"Available services:\n{formatted_output}")]

        case HchTools.SERVICE_DETAILS:
            service = arguments["service"]
            service_details_info = get_service_details(service)
            return [
                TextContent(
                    type="text",
                    text=f"{service_details_info}",
                )
            ]

        case HchTools.SERVICE_PRICE_INFO:
            service = arguments["service"]
            price_info = get_service_price_info(service)
            return [
                TextContent(
                    type="text",
                    text=f"{price_info}",
                )
            ]

        case _:
            raise ValueError(f"Unknown tool: {name}")


async def main():
    # Run the server using stdin/stdout streams
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="home-clean-home",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

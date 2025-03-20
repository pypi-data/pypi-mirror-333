from typing import Annotated
from mcp.server.fastmcp import Context
from pydantic import Field
from ..lib.utils import get_setting


def get_current_region(
    ctx: Context,
) -> Annotated[str, Field(description="Current region")]:
    """
    Get the current region setting.
    """
    setting = get_setting(ctx)
    return setting.region.value.lower()

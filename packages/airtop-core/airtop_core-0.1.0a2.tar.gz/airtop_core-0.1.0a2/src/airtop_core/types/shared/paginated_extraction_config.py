# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from ..._models import BaseModel
from .scrape_config import ScrapeConfig

__all__ = ["PaginatedExtractionConfig"]


class PaginatedExtractionConfig(BaseModel):
    interaction_mode: Optional[str] = FieldInfo(alias="interactionMode", default=None)
    """The mode to use for interaction.

    If set to 'auto', Airtop AI will automatically choose the most cost-effective
    interaction mode. If set to 'accurate', the request might be slower, but more
    likely to be accurate. Whereas, 'cost-efficient' will be cheaper and speed
    things up, but may reduce accuracy.
    """

    output_schema: Optional[str] = FieldInfo(alias="outputSchema", default=None)
    """JSON schema defining the structure of the output.

    If not provided, the format of the output might vary.
    """

    pagination_mode: Optional[str] = FieldInfo(alias="paginationMode", default=None)
    """The mode to use for pagination.

    If set to 'auto', Airtop AI will automatically look for pagination links first
    and then attempt infinite scrolling to load more content. If set to 'paginated',
    Airtop AI will follow pagination links to load more content. If set to
    'infinite-scroll', Airtop AI will scroll the page to load more content.
    """

    scrape: Optional[ScrapeConfig] = None
    """Optional configuration to customize and tweak how the web page is scraped."""

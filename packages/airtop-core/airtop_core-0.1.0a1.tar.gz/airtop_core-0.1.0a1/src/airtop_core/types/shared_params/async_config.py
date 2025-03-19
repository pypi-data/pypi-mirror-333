# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["AsyncConfig"]


class AsyncConfig(TypedDict, total=False):
    webhook_url: Annotated[str, PropertyInfo(alias="webhookUrl")]
    """The URL to send the response to when the request is complete."""

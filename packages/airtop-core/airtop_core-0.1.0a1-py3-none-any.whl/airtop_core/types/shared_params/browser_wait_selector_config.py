# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["BrowserWaitSelectorConfig"]


class BrowserWaitSelectorConfig(TypedDict, total=False):
    hidden: bool
    """
    If true, Airtop AI will wait for the element to not be in the DOM or to be
    hidden.
    """

    timeout_seconds: Annotated[int, PropertyInfo(alias="timeoutSeconds")]
    """The maximum time to wait for the selector to be present, in seconds.

    Defaults to 30 (30 seconds).
    """

    visible: bool
    """
    If true, Airtop AI will wait for the element to be visible and present in the
    DOM.
    """

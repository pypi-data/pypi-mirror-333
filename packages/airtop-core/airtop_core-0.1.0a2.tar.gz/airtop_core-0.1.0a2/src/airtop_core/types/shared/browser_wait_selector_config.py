# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["BrowserWaitSelectorConfig"]


class BrowserWaitSelectorConfig(BaseModel):
    hidden: Optional[bool] = None
    """
    If true, Airtop AI will wait for the element to not be in the DOM or to be
    hidden.
    """

    timeout_seconds: Optional[int] = FieldInfo(alias="timeoutSeconds", default=None)
    """The maximum time to wait for the selector to be present, in seconds.

    Defaults to 30 (30 seconds).
    """

    visible: Optional[bool] = None
    """
    If true, Airtop AI will wait for the element to be visible and present in the
    DOM.
    """

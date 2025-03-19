# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from ..._models import BaseModel
from .micro_interaction_config import MicroInteractionConfig

__all__ = ["SessionTypeHandlerRequestBody"]


class SessionTypeHandlerRequestBody(BaseModel):
    text: str
    """The text to type into the browser window."""

    clear_input_field: Optional[bool] = FieldInfo(alias="clearInputField", default=None)
    """
    If true, and an HTML input field is active, clears the input field before typing
    the text.
    """

    client_request_id: Optional[str] = FieldInfo(alias="clientRequestId", default=None)

    configuration: Optional[MicroInteractionConfig] = None
    """Request configuration"""

    cost_threshold_credits: Optional[int] = FieldInfo(alias="costThresholdCredits", default=None)
    """A credit threshold that, once exceeded, will cause the operation to be
    cancelled.

    Note that this is _not_ a hard limit, but a threshold that is checked
    periodically during the course of fulfilling the request. A default threshold is
    used if not specified, but you can use this option to increase or decrease as
    needed. Set to 0 to disable this feature entirely (not recommended).
    """

    element_description: Optional[str] = FieldInfo(alias="elementDescription", default=None)
    """A natural language description of where to type (e.g.

    'the search box', 'username field'). The interaction will be aborted if the
    target element cannot be found.
    """

    press_enter_key: Optional[bool] = FieldInfo(alias="pressEnterKey", default=None)
    """If true, simulates pressing the Enter key after typing the text."""

    press_tab_key: Optional[bool] = FieldInfo(alias="pressTabKey", default=None)
    """If true, simulates pressing the Tab key after typing the text.

    Note that the tab key will be pressed after the Enter key if both options are
    configured.
    """

    time_threshold_seconds: Optional[int] = FieldInfo(alias="timeThresholdSeconds", default=None)
    """
    A time threshold in seconds that, once exceeded, will cause the operation to be
    cancelled. Note that this is _not_ a hard limit, but a threshold that is checked
    periodically during the course of fulfilling the request. A default threshold is
    used if not specified, but you can use this option to increase or decrease as
    needed. Set to 0 to disable this feature entirely (not recommended).

    This setting does not extend the maximum session duration provided at the time
    of session creation.
    """

    wait_for_navigation: Optional[bool] = FieldInfo(alias="waitForNavigation", default=None)
    """
    If true, Airtop AI will wait for the navigation to complete after clicking the
    element.
    """

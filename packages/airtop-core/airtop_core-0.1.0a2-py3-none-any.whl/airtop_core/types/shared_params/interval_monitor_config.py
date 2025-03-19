# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Annotated, TypedDict

from ..._utils import PropertyInfo

__all__ = ["IntervalMonitorConfig"]


class IntervalMonitorConfig(TypedDict, total=False):
    interval_seconds: Annotated[int, PropertyInfo(alias="intervalSeconds")]
    """The interval in seconds between condition checks.

    Only used when monitorType is 'interval'.
    """

    timeout_seconds: Annotated[int, PropertyInfo(alias="timeoutSeconds")]
    """
    The timeout in seconds after which the monitor will stop checking the condition.
    """

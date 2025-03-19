# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["IntervalMonitorConfig"]


class IntervalMonitorConfig(BaseModel):
    interval_seconds: Optional[int] = FieldInfo(alias="intervalSeconds", default=None)
    """The interval in seconds between condition checks.

    Only used when monitorType is 'interval'.
    """

    timeout_seconds: Optional[int] = FieldInfo(alias="timeoutSeconds", default=None)
    """
    The timeout in seconds after which the monitor will stop checking the condition.
    """

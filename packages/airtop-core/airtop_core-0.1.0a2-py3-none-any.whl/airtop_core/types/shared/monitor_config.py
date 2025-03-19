# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ..._models import BaseModel
from .interval_monitor_config import IntervalMonitorConfig
from .browser_wait_selector_config import BrowserWaitSelectorConfig

__all__ = ["MonitorConfig"]


class MonitorConfig(BaseModel):
    monitor_type: Literal["interval", "selector"] = FieldInfo(alias="monitorType")
    """The type of monitoring to perform.

    Interval executes the condition check at a regular, specified interval. Selector
    waits for a selector to be present before completing.
    """

    include_visual_analysis: Optional[Literal["auto", "disabled", "enabled"]] = FieldInfo(
        alias="includeVisualAnalysis", default=None
    )
    """
    If set to 'enabled', Airtop AI will also analyze the web page visually when
    executing the condition check. If set to 'disabled', no visual analysis will be
    conducted.
    """

    interval: Optional[IntervalMonitorConfig] = None
    """Configuration for the interval monitor.

    Only used when monitorType is 'interval'.
    """

    monitor_selector_options: Optional[BrowserWaitSelectorConfig] = FieldInfo(
        alias="monitorSelectorOptions", default=None
    )
    """Configuration for the browser wait selector."""

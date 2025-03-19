# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, Annotated, TypedDict

from ..._utils import PropertyInfo
from .interval_monitor_config import IntervalMonitorConfig
from .browser_wait_selector_config import BrowserWaitSelectorConfig

__all__ = ["MonitorConfig"]


class MonitorConfig(TypedDict, total=False):
    monitor_type: Required[Annotated[Literal["interval", "selector"], PropertyInfo(alias="monitorType")]]
    """The type of monitoring to perform.

    Interval executes the condition check at a regular, specified interval. Selector
    waits for a selector to be present before completing.
    """

    include_visual_analysis: Annotated[
        Literal["auto", "disabled", "enabled"], PropertyInfo(alias="includeVisualAnalysis")
    ]
    """
    If set to 'enabled', Airtop AI will also analyze the web page visually when
    executing the condition check. If set to 'disabled', no visual analysis will be
    conducted.
    """

    interval: IntervalMonitorConfig
    """Configuration for the interval monitor.

    Only used when monitorType is 'interval'.
    """

    monitor_selector_options: Annotated[BrowserWaitSelectorConfig, PropertyInfo(alias="monitorSelectorOptions")]
    """Configuration for the browser wait selector."""

# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Annotated, TypedDict

from ..._utils import PropertyInfo
from .visual_analysis_config import VisualAnalysisConfig
from .browser_wait_navigation_config import BrowserWaitNavigationConfig

__all__ = ["ClickConfig"]


class ClickConfig(TypedDict, total=False):
    click_type: Annotated[Literal["click", "doubleClick", "rightClick"], PropertyInfo(alias="clickType")]
    """The type of click to perform. Defaults to left click."""

    visual_analysis: Annotated[VisualAnalysisConfig, PropertyInfo(alias="visualAnalysis")]
    """Optional configuration for visual analysis when locating specified content."""

    wait_for_navigation_config: Annotated[BrowserWaitNavigationConfig, PropertyInfo(alias="waitForNavigationConfig")]
    """
    Optional configuration for waiting for navigation to complete after clicking the
    element.
    """

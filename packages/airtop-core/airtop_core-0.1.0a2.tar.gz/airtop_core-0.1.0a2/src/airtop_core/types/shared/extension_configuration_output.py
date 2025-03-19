# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["ExtensionConfigurationOutput"]


class ExtensionConfigurationOutput(BaseModel):
    created_at: Optional[datetime] = FieldInfo(alias="createdAt", default=None)
    """The date and time the configuration was created.

    Might be null for old configurations
    """

    extension_ids: Optional[List[str]] = FieldInfo(alias="extensionIds", default=None)
    """The ids of the extensions in configuration."""

    name: str
    """Name of the extension configuration."""

    updated_at: Optional[datetime] = FieldInfo(alias="updatedAt", default=None)
    """The date and time the configuration was last updated.

    Might be null for configurations not updated recently
    """

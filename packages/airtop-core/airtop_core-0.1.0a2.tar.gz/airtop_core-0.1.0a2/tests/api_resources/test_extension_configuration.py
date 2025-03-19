# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from airtop_core import Airtop, AsyncAirtop
from tests.utils import assert_matches_type
from airtop_core.types.shared import ExtensionConfigurationOutput

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestExtensionConfiguration:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_get(self, client: Airtop) -> None:
        extension_configuration = client.extension_configuration.get(
            "my-configuration",
        )
        assert_matches_type(ExtensionConfigurationOutput, extension_configuration, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_get(self, client: Airtop) -> None:
        response = client.extension_configuration.with_raw_response.get(
            "my-configuration",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        extension_configuration = response.parse()
        assert_matches_type(ExtensionConfigurationOutput, extension_configuration, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_get(self, client: Airtop) -> None:
        with client.extension_configuration.with_streaming_response.get(
            "my-configuration",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            extension_configuration = response.parse()
            assert_matches_type(ExtensionConfigurationOutput, extension_configuration, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_get(self, client: Airtop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `name` but received ''"):
            client.extension_configuration.with_raw_response.get(
                "",
            )


class TestAsyncExtensionConfiguration:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_get(self, async_client: AsyncAirtop) -> None:
        extension_configuration = await async_client.extension_configuration.get(
            "my-configuration",
        )
        assert_matches_type(ExtensionConfigurationOutput, extension_configuration, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_get(self, async_client: AsyncAirtop) -> None:
        response = await async_client.extension_configuration.with_raw_response.get(
            "my-configuration",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        extension_configuration = await response.parse()
        assert_matches_type(ExtensionConfigurationOutput, extension_configuration, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_get(self, async_client: AsyncAirtop) -> None:
        async with async_client.extension_configuration.with_streaming_response.get(
            "my-configuration",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            extension_configuration = await response.parse()
            assert_matches_type(ExtensionConfigurationOutput, extension_configuration, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_get(self, async_client: AsyncAirtop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `name` but received ''"):
            await async_client.extension_configuration.with_raw_response.get(
                "",
            )

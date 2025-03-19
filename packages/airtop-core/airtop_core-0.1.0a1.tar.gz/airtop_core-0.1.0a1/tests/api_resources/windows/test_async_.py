# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from airtop_core import Airtop, AsyncAirtop
from tests.utils import assert_matches_type
from airtop_core.types.shared import AsyncSessionAIResponseEnvelope

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestAsync:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_click(self, client: Airtop) -> None:
        async_ = client.windows.async_.click(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            element_description="The login button",
        )
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_click_with_all_params(self, client: Airtop) -> None:
        async_ = client.windows.async_.click(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            element_description="The login button",
            async_={"webhook_url": "webhookUrl"},
            client_request_id="clientRequestId",
            configuration={
                "click_type": "click",
                "visual_analysis": {
                    "max_scan_scrolls": 0,
                    "overlap_percentage": 0,
                    "partition_direction": "vertical",
                    "result_selection_strategy": "first",
                    "scan_scroll_delay": 0,
                    "scope": "viewport",
                },
                "wait_for_navigation_config": {
                    "timeout_seconds": 10,
                    "wait_until": "load",
                },
            },
            cost_threshold_credits=0,
            time_threshold_seconds=0,
            wait_for_navigation=True,
        )
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_click(self, client: Airtop) -> None:
        response = client.windows.async_.with_raw_response.click(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            element_description="The login button",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        async_ = response.parse()
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_click(self, client: Airtop) -> None:
        with client.windows.async_.with_streaming_response.click(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            element_description="The login button",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            async_ = response.parse()
            assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_click(self, client: Airtop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.windows.async_.with_raw_response.click(
                window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
                session_id="",
                element_description="The login button",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `window_id` but received ''"):
            client.windows.async_.with_raw_response.click(
                window_id="",
                session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
                element_description="The login button",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_create_automation(self, client: Airtop) -> None:
        async_ = client.windows.async_.create_automation(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
        )
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_automation_with_all_params(self, client: Airtop) -> None:
        async_ = client.windows.async_.create_automation(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            async_={"webhook_url": "webhookUrl"},
            client_request_id="clientRequestId",
            configuration={},
            cost_threshold_credits=0,
            time_threshold_seconds=0,
        )
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create_automation(self, client: Airtop) -> None:
        response = client.windows.async_.with_raw_response.create_automation(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        async_ = response.parse()
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create_automation(self, client: Airtop) -> None:
        with client.windows.async_.with_streaming_response.create_automation(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            async_ = response.parse()
            assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_create_automation(self, client: Airtop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.windows.async_.with_raw_response.create_automation(
                window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
                session_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `window_id` but received ''"):
            client.windows.async_.with_raw_response.create_automation(
                window_id="",
                session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_execute_automation(self, client: Airtop) -> None:
        async_ = client.windows.async_.execute_automation(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            automation_id="automationId",
        )
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_execute_automation_with_all_params(self, client: Airtop) -> None:
        async_ = client.windows.async_.execute_automation(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            automation_id="automationId",
            async_={"webhook_url": "webhookUrl"},
            client_request_id="clientRequestId",
            cost_threshold_credits=0,
            parameters={"foo": "bar"},
            time_threshold_seconds=0,
        )
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_execute_automation(self, client: Airtop) -> None:
        response = client.windows.async_.with_raw_response.execute_automation(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            automation_id="automationId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        async_ = response.parse()
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_execute_automation(self, client: Airtop) -> None:
        with client.windows.async_.with_streaming_response.execute_automation(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            automation_id="automationId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            async_ = response.parse()
            assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_execute_automation(self, client: Airtop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.windows.async_.with_raw_response.execute_automation(
                window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
                session_id="",
                automation_id="automationId",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `window_id` but received ''"):
            client.windows.async_.with_raw_response.execute_automation(
                window_id="",
                session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
                automation_id="automationId",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_hover(self, client: Airtop) -> None:
        async_ = client.windows.async_.hover(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            element_description="The search box input in the top right corner",
        )
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_hover_with_all_params(self, client: Airtop) -> None:
        async_ = client.windows.async_.hover(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            element_description="The search box input in the top right corner",
            async_={"webhook_url": "webhookUrl"},
            client_request_id="clientRequestId",
            configuration={
                "visual_analysis": {
                    "max_scan_scrolls": 0,
                    "overlap_percentage": 0,
                    "partition_direction": "vertical",
                    "result_selection_strategy": "first",
                    "scan_scroll_delay": 0,
                    "scope": "viewport",
                },
                "wait_for_navigation_config": {
                    "timeout_seconds": 10,
                    "wait_until": "load",
                },
            },
            cost_threshold_credits=0,
            time_threshold_seconds=0,
        )
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_hover(self, client: Airtop) -> None:
        response = client.windows.async_.with_raw_response.hover(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            element_description="The search box input in the top right corner",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        async_ = response.parse()
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_hover(self, client: Airtop) -> None:
        with client.windows.async_.with_streaming_response.hover(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            element_description="The search box input in the top right corner",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            async_ = response.parse()
            assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_hover(self, client: Airtop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.windows.async_.with_raw_response.hover(
                window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
                session_id="",
                element_description="The search box input in the top right corner",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `window_id` but received ''"):
            client.windows.async_.with_raw_response.hover(
                window_id="",
                session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
                element_description="The search box input in the top right corner",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_monitor(self, client: Airtop) -> None:
        async_ = client.windows.async_.monitor(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
        )
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_monitor_with_all_params(self, client: Airtop) -> None:
        async_ = client.windows.async_.monitor(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            async_={"webhook_url": "webhookUrl"},
            client_request_id="clientRequestId",
            condition="Determine if the user appears to be signed in to the website",
            configuration={
                "monitor_type": "interval",
                "include_visual_analysis": "auto",
                "interval": {
                    "interval_seconds": 5,
                    "timeout_seconds": 30,
                },
                "monitor_selector_options": {
                    "hidden": True,
                    "timeout_seconds": 10000,
                    "visible": True,
                },
            },
            cost_threshold_credits=0,
            selector="#search-box",
            time_threshold_seconds=0,
        )
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_monitor(self, client: Airtop) -> None:
        response = client.windows.async_.with_raw_response.monitor(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        async_ = response.parse()
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_monitor(self, client: Airtop) -> None:
        with client.windows.async_.with_streaming_response.monitor(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            async_ = response.parse()
            assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_monitor(self, client: Airtop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.windows.async_.with_raw_response.monitor(
                window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
                session_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `window_id` but received ''"):
            client.windows.async_.with_raw_response.monitor(
                window_id="",
                session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_page_query(self, client: Airtop) -> None:
        async_ = client.windows.async_.page_query(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            prompt="What is the main idea of this page?",
        )
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_page_query_with_all_params(self, client: Airtop) -> None:
        async_ = client.windows.async_.page_query(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            prompt="What is the main idea of this page?",
            async_={"webhook_url": "webhookUrl"},
            client_request_id="clientRequestId",
            configuration={
                "experimental": {"include_visual_analysis": "auto,disabled,enabled"},
                "output_schema": '{"type":"object","properties":{"response":{"type":"string","description":"The response from Airtop AI. Should be an empty string if an error occurred."},"error":{"type":"string","description":"An error message if an error occurred; otherwise, this can be an empty string."}},"required":["summary"]}',
                "scrape": {"optimize_urls": "auto"},
            },
            cost_threshold_credits=0,
            follow_pagination_links=False,
            time_threshold_seconds=0,
        )
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_page_query(self, client: Airtop) -> None:
        response = client.windows.async_.with_raw_response.page_query(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            prompt="What is the main idea of this page?",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        async_ = response.parse()
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_page_query(self, client: Airtop) -> None:
        with client.windows.async_.with_streaming_response.page_query(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            prompt="What is the main idea of this page?",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            async_ = response.parse()
            assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_page_query(self, client: Airtop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.windows.async_.with_raw_response.page_query(
                window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
                session_id="",
                prompt="What is the main idea of this page?",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `window_id` but received ''"):
            client.windows.async_.with_raw_response.page_query(
                window_id="",
                session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
                prompt="What is the main idea of this page?",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_paginated_extraction(self, client: Airtop) -> None:
        async_ = client.windows.async_.paginated_extraction(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            prompt="This site contains a list of results about <provide details about the list>. Navigate through 3 pages of results and return the title and <provide details about the data you want to extract> about each result in this list.",
        )
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_paginated_extraction_with_all_params(self, client: Airtop) -> None:
        async_ = client.windows.async_.paginated_extraction(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            prompt="This site contains a list of results about <provide details about the list>. Navigate through 3 pages of results and return the title and <provide details about the data you want to extract> about each result in this list.",
            async_={"webhook_url": "webhookUrl"},
            client_request_id="clientRequestId",
            configuration={
                "interaction_mode": "auto,accurate,cost-efficient",
                "output_schema": '{"type":"object","properties":{"response":{"type":"string","description":"The response from Airtop AI. Should be an empty string if an error occurred."},"error":{"type":"string","description":"An error message if an error occurred; otherwise, this can be an empty string."}},"required":["summary"]}',
                "pagination_mode": "auto,paginated,infinite-scroll",
                "scrape": {"optimize_urls": "auto"},
            },
            cost_threshold_credits=0,
            time_threshold_seconds=0,
        )
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_paginated_extraction(self, client: Airtop) -> None:
        response = client.windows.async_.with_raw_response.paginated_extraction(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            prompt="This site contains a list of results about <provide details about the list>. Navigate through 3 pages of results and return the title and <provide details about the data you want to extract> about each result in this list.",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        async_ = response.parse()
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_paginated_extraction(self, client: Airtop) -> None:
        with client.windows.async_.with_streaming_response.paginated_extraction(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            prompt="This site contains a list of results about <provide details about the list>. Navigate through 3 pages of results and return the title and <provide details about the data you want to extract> about each result in this list.",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            async_ = response.parse()
            assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_paginated_extraction(self, client: Airtop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.windows.async_.with_raw_response.paginated_extraction(
                window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
                session_id="",
                prompt="This site contains a list of results about <provide details about the list>. Navigate through 3 pages of results and return the title and <provide details about the data you want to extract> about each result in this list.",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `window_id` but received ''"):
            client.windows.async_.with_raw_response.paginated_extraction(
                window_id="",
                session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
                prompt="This site contains a list of results about <provide details about the list>. Navigate through 3 pages of results and return the title and <provide details about the data you want to extract> about each result in this list.",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_prompt_content(self, client: Airtop) -> None:
        async_ = client.windows.async_.prompt_content(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            prompt="What is the main idea of this page?",
        )
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_prompt_content_with_all_params(self, client: Airtop) -> None:
        async_ = client.windows.async_.prompt_content(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            prompt="What is the main idea of this page?",
            async_={"webhook_url": "webhookUrl"},
            client_request_id="clientRequestId",
            configuration={
                "experimental": {"include_visual_analysis": "auto,disabled,enabled"},
                "output_schema": '{"type":"object","properties":{"response":{"type":"string","description":"The response from Airtop AI. Should be an empty string if an error occurred."},"error":{"type":"string","description":"An error message if an error occurred; otherwise, this can be an empty string."}},"required":["summary"]}',
                "scrape": {"optimize_urls": "auto"},
            },
            cost_threshold_credits=0,
            follow_pagination_links=False,
            time_threshold_seconds=0,
        )
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_prompt_content(self, client: Airtop) -> None:
        response = client.windows.async_.with_raw_response.prompt_content(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            prompt="What is the main idea of this page?",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        async_ = response.parse()
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_prompt_content(self, client: Airtop) -> None:
        with client.windows.async_.with_streaming_response.prompt_content(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            prompt="What is the main idea of this page?",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            async_ = response.parse()
            assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_prompt_content(self, client: Airtop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.windows.async_.with_raw_response.prompt_content(
                window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
                session_id="",
                prompt="What is the main idea of this page?",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `window_id` but received ''"):
            client.windows.async_.with_raw_response.prompt_content(
                window_id="",
                session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
                prompt="What is the main idea of this page?",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_screenshot(self, client: Airtop) -> None:
        async_ = client.windows.async_.screenshot(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
        )
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_screenshot_with_all_params(self, client: Airtop) -> None:
        async_ = client.windows.async_.screenshot(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            async_={"webhook_url": "webhookUrl"},
            client_request_id="clientRequestId",
            configuration={
                "screenshot": {
                    "max_height": 720,
                    "max_width": 1280,
                    "quality": 80,
                    "scope": "viewport",
                }
            },
            cost_threshold_credits=0,
            time_threshold_seconds=0,
        )
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_screenshot(self, client: Airtop) -> None:
        response = client.windows.async_.with_raw_response.screenshot(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        async_ = response.parse()
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_screenshot(self, client: Airtop) -> None:
        with client.windows.async_.with_streaming_response.screenshot(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            async_ = response.parse()
            assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_screenshot(self, client: Airtop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.windows.async_.with_raw_response.screenshot(
                window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
                session_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `window_id` but received ''"):
            client.windows.async_.with_raw_response.screenshot(
                window_id="",
                session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_summarize_content(self, client: Airtop) -> None:
        async_ = client.windows.async_.summarize_content(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
        )
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_summarize_content_with_all_params(self, client: Airtop) -> None:
        async_ = client.windows.async_.summarize_content(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            async_={"webhook_url": "webhookUrl"},
            client_request_id="clientRequestId",
            configuration={
                "experimental": {"include_visual_analysis": "auto,disabled,enabled"},
                "output_schema": '{"type":"object","properties":{"summary":{"type":"string","description":"A summary of the content. Should be an empty string if an error occurred."},"error":{"type":"string","description":"An error message if an error occurred; otherwise, this can be an empty string."}},"required":["summary"]}',
            },
            cost_threshold_credits=0,
            prompt="Please summarize the content of this web page in a few sentences.",
            time_threshold_seconds=0,
        )
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_summarize_content(self, client: Airtop) -> None:
        response = client.windows.async_.with_raw_response.summarize_content(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        async_ = response.parse()
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_summarize_content(self, client: Airtop) -> None:
        with client.windows.async_.with_streaming_response.summarize_content(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            async_ = response.parse()
            assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_summarize_content(self, client: Airtop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.windows.async_.with_raw_response.summarize_content(
                window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
                session_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `window_id` but received ''"):
            client.windows.async_.with_raw_response.summarize_content(
                window_id="",
                session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_type(self, client: Airtop) -> None:
        async_ = client.windows.async_.type(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            text="Example text",
        )
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_type_with_all_params(self, client: Airtop) -> None:
        async_ = client.windows.async_.type(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            text="Example text",
            async_={"webhook_url": "webhookUrl"},
            clear_input_field=True,
            client_request_id="clientRequestId",
            configuration={
                "visual_analysis": {
                    "max_scan_scrolls": 0,
                    "overlap_percentage": 0,
                    "partition_direction": "vertical",
                    "result_selection_strategy": "first",
                    "scan_scroll_delay": 0,
                    "scope": "viewport",
                },
                "wait_for_navigation_config": {
                    "timeout_seconds": 10,
                    "wait_until": "load",
                },
            },
            cost_threshold_credits=0,
            element_description="The search box input in the top right corner",
            press_enter_key=True,
            press_tab_key=True,
            time_threshold_seconds=0,
            wait_for_navigation=True,
        )
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_type(self, client: Airtop) -> None:
        response = client.windows.async_.with_raw_response.type(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            text="Example text",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        async_ = response.parse()
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_type(self, client: Airtop) -> None:
        with client.windows.async_.with_streaming_response.type(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            text="Example text",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            async_ = response.parse()
            assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_type(self, client: Airtop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.windows.async_.with_raw_response.type(
                window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
                session_id="",
                text="Example text",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `window_id` but received ''"):
            client.windows.async_.with_raw_response.type(
                window_id="",
                session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
                text="Example text",
            )


class TestAsyncAsync:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_click(self, async_client: AsyncAirtop) -> None:
        async_ = await async_client.windows.async_.click(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            element_description="The login button",
        )
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_click_with_all_params(self, async_client: AsyncAirtop) -> None:
        async_ = await async_client.windows.async_.click(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            element_description="The login button",
            async_={"webhook_url": "webhookUrl"},
            client_request_id="clientRequestId",
            configuration={
                "click_type": "click",
                "visual_analysis": {
                    "max_scan_scrolls": 0,
                    "overlap_percentage": 0,
                    "partition_direction": "vertical",
                    "result_selection_strategy": "first",
                    "scan_scroll_delay": 0,
                    "scope": "viewport",
                },
                "wait_for_navigation_config": {
                    "timeout_seconds": 10,
                    "wait_until": "load",
                },
            },
            cost_threshold_credits=0,
            time_threshold_seconds=0,
            wait_for_navigation=True,
        )
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_click(self, async_client: AsyncAirtop) -> None:
        response = await async_client.windows.async_.with_raw_response.click(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            element_description="The login button",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        async_ = await response.parse()
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_click(self, async_client: AsyncAirtop) -> None:
        async with async_client.windows.async_.with_streaming_response.click(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            element_description="The login button",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            async_ = await response.parse()
            assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_click(self, async_client: AsyncAirtop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.windows.async_.with_raw_response.click(
                window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
                session_id="",
                element_description="The login button",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `window_id` but received ''"):
            await async_client.windows.async_.with_raw_response.click(
                window_id="",
                session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
                element_description="The login button",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_automation(self, async_client: AsyncAirtop) -> None:
        async_ = await async_client.windows.async_.create_automation(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
        )
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_automation_with_all_params(self, async_client: AsyncAirtop) -> None:
        async_ = await async_client.windows.async_.create_automation(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            async_={"webhook_url": "webhookUrl"},
            client_request_id="clientRequestId",
            configuration={},
            cost_threshold_credits=0,
            time_threshold_seconds=0,
        )
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create_automation(self, async_client: AsyncAirtop) -> None:
        response = await async_client.windows.async_.with_raw_response.create_automation(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        async_ = await response.parse()
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create_automation(self, async_client: AsyncAirtop) -> None:
        async with async_client.windows.async_.with_streaming_response.create_automation(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            async_ = await response.parse()
            assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_create_automation(self, async_client: AsyncAirtop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.windows.async_.with_raw_response.create_automation(
                window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
                session_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `window_id` but received ''"):
            await async_client.windows.async_.with_raw_response.create_automation(
                window_id="",
                session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_execute_automation(self, async_client: AsyncAirtop) -> None:
        async_ = await async_client.windows.async_.execute_automation(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            automation_id="automationId",
        )
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_execute_automation_with_all_params(self, async_client: AsyncAirtop) -> None:
        async_ = await async_client.windows.async_.execute_automation(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            automation_id="automationId",
            async_={"webhook_url": "webhookUrl"},
            client_request_id="clientRequestId",
            cost_threshold_credits=0,
            parameters={"foo": "bar"},
            time_threshold_seconds=0,
        )
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_execute_automation(self, async_client: AsyncAirtop) -> None:
        response = await async_client.windows.async_.with_raw_response.execute_automation(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            automation_id="automationId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        async_ = await response.parse()
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_execute_automation(self, async_client: AsyncAirtop) -> None:
        async with async_client.windows.async_.with_streaming_response.execute_automation(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            automation_id="automationId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            async_ = await response.parse()
            assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_execute_automation(self, async_client: AsyncAirtop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.windows.async_.with_raw_response.execute_automation(
                window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
                session_id="",
                automation_id="automationId",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `window_id` but received ''"):
            await async_client.windows.async_.with_raw_response.execute_automation(
                window_id="",
                session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
                automation_id="automationId",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_hover(self, async_client: AsyncAirtop) -> None:
        async_ = await async_client.windows.async_.hover(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            element_description="The search box input in the top right corner",
        )
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_hover_with_all_params(self, async_client: AsyncAirtop) -> None:
        async_ = await async_client.windows.async_.hover(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            element_description="The search box input in the top right corner",
            async_={"webhook_url": "webhookUrl"},
            client_request_id="clientRequestId",
            configuration={
                "visual_analysis": {
                    "max_scan_scrolls": 0,
                    "overlap_percentage": 0,
                    "partition_direction": "vertical",
                    "result_selection_strategy": "first",
                    "scan_scroll_delay": 0,
                    "scope": "viewport",
                },
                "wait_for_navigation_config": {
                    "timeout_seconds": 10,
                    "wait_until": "load",
                },
            },
            cost_threshold_credits=0,
            time_threshold_seconds=0,
        )
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_hover(self, async_client: AsyncAirtop) -> None:
        response = await async_client.windows.async_.with_raw_response.hover(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            element_description="The search box input in the top right corner",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        async_ = await response.parse()
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_hover(self, async_client: AsyncAirtop) -> None:
        async with async_client.windows.async_.with_streaming_response.hover(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            element_description="The search box input in the top right corner",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            async_ = await response.parse()
            assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_hover(self, async_client: AsyncAirtop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.windows.async_.with_raw_response.hover(
                window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
                session_id="",
                element_description="The search box input in the top right corner",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `window_id` but received ''"):
            await async_client.windows.async_.with_raw_response.hover(
                window_id="",
                session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
                element_description="The search box input in the top right corner",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_monitor(self, async_client: AsyncAirtop) -> None:
        async_ = await async_client.windows.async_.monitor(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
        )
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_monitor_with_all_params(self, async_client: AsyncAirtop) -> None:
        async_ = await async_client.windows.async_.monitor(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            async_={"webhook_url": "webhookUrl"},
            client_request_id="clientRequestId",
            condition="Determine if the user appears to be signed in to the website",
            configuration={
                "monitor_type": "interval",
                "include_visual_analysis": "auto",
                "interval": {
                    "interval_seconds": 5,
                    "timeout_seconds": 30,
                },
                "monitor_selector_options": {
                    "hidden": True,
                    "timeout_seconds": 10000,
                    "visible": True,
                },
            },
            cost_threshold_credits=0,
            selector="#search-box",
            time_threshold_seconds=0,
        )
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_monitor(self, async_client: AsyncAirtop) -> None:
        response = await async_client.windows.async_.with_raw_response.monitor(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        async_ = await response.parse()
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_monitor(self, async_client: AsyncAirtop) -> None:
        async with async_client.windows.async_.with_streaming_response.monitor(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            async_ = await response.parse()
            assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_monitor(self, async_client: AsyncAirtop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.windows.async_.with_raw_response.monitor(
                window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
                session_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `window_id` but received ''"):
            await async_client.windows.async_.with_raw_response.monitor(
                window_id="",
                session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_page_query(self, async_client: AsyncAirtop) -> None:
        async_ = await async_client.windows.async_.page_query(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            prompt="What is the main idea of this page?",
        )
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_page_query_with_all_params(self, async_client: AsyncAirtop) -> None:
        async_ = await async_client.windows.async_.page_query(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            prompt="What is the main idea of this page?",
            async_={"webhook_url": "webhookUrl"},
            client_request_id="clientRequestId",
            configuration={
                "experimental": {"include_visual_analysis": "auto,disabled,enabled"},
                "output_schema": '{"type":"object","properties":{"response":{"type":"string","description":"The response from Airtop AI. Should be an empty string if an error occurred."},"error":{"type":"string","description":"An error message if an error occurred; otherwise, this can be an empty string."}},"required":["summary"]}',
                "scrape": {"optimize_urls": "auto"},
            },
            cost_threshold_credits=0,
            follow_pagination_links=False,
            time_threshold_seconds=0,
        )
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_page_query(self, async_client: AsyncAirtop) -> None:
        response = await async_client.windows.async_.with_raw_response.page_query(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            prompt="What is the main idea of this page?",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        async_ = await response.parse()
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_page_query(self, async_client: AsyncAirtop) -> None:
        async with async_client.windows.async_.with_streaming_response.page_query(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            prompt="What is the main idea of this page?",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            async_ = await response.parse()
            assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_page_query(self, async_client: AsyncAirtop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.windows.async_.with_raw_response.page_query(
                window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
                session_id="",
                prompt="What is the main idea of this page?",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `window_id` but received ''"):
            await async_client.windows.async_.with_raw_response.page_query(
                window_id="",
                session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
                prompt="What is the main idea of this page?",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_paginated_extraction(self, async_client: AsyncAirtop) -> None:
        async_ = await async_client.windows.async_.paginated_extraction(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            prompt="This site contains a list of results about <provide details about the list>. Navigate through 3 pages of results and return the title and <provide details about the data you want to extract> about each result in this list.",
        )
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_paginated_extraction_with_all_params(self, async_client: AsyncAirtop) -> None:
        async_ = await async_client.windows.async_.paginated_extraction(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            prompt="This site contains a list of results about <provide details about the list>. Navigate through 3 pages of results and return the title and <provide details about the data you want to extract> about each result in this list.",
            async_={"webhook_url": "webhookUrl"},
            client_request_id="clientRequestId",
            configuration={
                "interaction_mode": "auto,accurate,cost-efficient",
                "output_schema": '{"type":"object","properties":{"response":{"type":"string","description":"The response from Airtop AI. Should be an empty string if an error occurred."},"error":{"type":"string","description":"An error message if an error occurred; otherwise, this can be an empty string."}},"required":["summary"]}',
                "pagination_mode": "auto,paginated,infinite-scroll",
                "scrape": {"optimize_urls": "auto"},
            },
            cost_threshold_credits=0,
            time_threshold_seconds=0,
        )
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_paginated_extraction(self, async_client: AsyncAirtop) -> None:
        response = await async_client.windows.async_.with_raw_response.paginated_extraction(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            prompt="This site contains a list of results about <provide details about the list>. Navigate through 3 pages of results and return the title and <provide details about the data you want to extract> about each result in this list.",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        async_ = await response.parse()
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_paginated_extraction(self, async_client: AsyncAirtop) -> None:
        async with async_client.windows.async_.with_streaming_response.paginated_extraction(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            prompt="This site contains a list of results about <provide details about the list>. Navigate through 3 pages of results and return the title and <provide details about the data you want to extract> about each result in this list.",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            async_ = await response.parse()
            assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_paginated_extraction(self, async_client: AsyncAirtop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.windows.async_.with_raw_response.paginated_extraction(
                window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
                session_id="",
                prompt="This site contains a list of results about <provide details about the list>. Navigate through 3 pages of results and return the title and <provide details about the data you want to extract> about each result in this list.",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `window_id` but received ''"):
            await async_client.windows.async_.with_raw_response.paginated_extraction(
                window_id="",
                session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
                prompt="This site contains a list of results about <provide details about the list>. Navigate through 3 pages of results and return the title and <provide details about the data you want to extract> about each result in this list.",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_prompt_content(self, async_client: AsyncAirtop) -> None:
        async_ = await async_client.windows.async_.prompt_content(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            prompt="What is the main idea of this page?",
        )
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_prompt_content_with_all_params(self, async_client: AsyncAirtop) -> None:
        async_ = await async_client.windows.async_.prompt_content(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            prompt="What is the main idea of this page?",
            async_={"webhook_url": "webhookUrl"},
            client_request_id="clientRequestId",
            configuration={
                "experimental": {"include_visual_analysis": "auto,disabled,enabled"},
                "output_schema": '{"type":"object","properties":{"response":{"type":"string","description":"The response from Airtop AI. Should be an empty string if an error occurred."},"error":{"type":"string","description":"An error message if an error occurred; otherwise, this can be an empty string."}},"required":["summary"]}',
                "scrape": {"optimize_urls": "auto"},
            },
            cost_threshold_credits=0,
            follow_pagination_links=False,
            time_threshold_seconds=0,
        )
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_prompt_content(self, async_client: AsyncAirtop) -> None:
        response = await async_client.windows.async_.with_raw_response.prompt_content(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            prompt="What is the main idea of this page?",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        async_ = await response.parse()
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_prompt_content(self, async_client: AsyncAirtop) -> None:
        async with async_client.windows.async_.with_streaming_response.prompt_content(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            prompt="What is the main idea of this page?",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            async_ = await response.parse()
            assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_prompt_content(self, async_client: AsyncAirtop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.windows.async_.with_raw_response.prompt_content(
                window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
                session_id="",
                prompt="What is the main idea of this page?",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `window_id` but received ''"):
            await async_client.windows.async_.with_raw_response.prompt_content(
                window_id="",
                session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
                prompt="What is the main idea of this page?",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_screenshot(self, async_client: AsyncAirtop) -> None:
        async_ = await async_client.windows.async_.screenshot(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
        )
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_screenshot_with_all_params(self, async_client: AsyncAirtop) -> None:
        async_ = await async_client.windows.async_.screenshot(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            async_={"webhook_url": "webhookUrl"},
            client_request_id="clientRequestId",
            configuration={
                "screenshot": {
                    "max_height": 720,
                    "max_width": 1280,
                    "quality": 80,
                    "scope": "viewport",
                }
            },
            cost_threshold_credits=0,
            time_threshold_seconds=0,
        )
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_screenshot(self, async_client: AsyncAirtop) -> None:
        response = await async_client.windows.async_.with_raw_response.screenshot(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        async_ = await response.parse()
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_screenshot(self, async_client: AsyncAirtop) -> None:
        async with async_client.windows.async_.with_streaming_response.screenshot(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            async_ = await response.parse()
            assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_screenshot(self, async_client: AsyncAirtop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.windows.async_.with_raw_response.screenshot(
                window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
                session_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `window_id` but received ''"):
            await async_client.windows.async_.with_raw_response.screenshot(
                window_id="",
                session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_summarize_content(self, async_client: AsyncAirtop) -> None:
        async_ = await async_client.windows.async_.summarize_content(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
        )
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_summarize_content_with_all_params(self, async_client: AsyncAirtop) -> None:
        async_ = await async_client.windows.async_.summarize_content(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            async_={"webhook_url": "webhookUrl"},
            client_request_id="clientRequestId",
            configuration={
                "experimental": {"include_visual_analysis": "auto,disabled,enabled"},
                "output_schema": '{"type":"object","properties":{"summary":{"type":"string","description":"A summary of the content. Should be an empty string if an error occurred."},"error":{"type":"string","description":"An error message if an error occurred; otherwise, this can be an empty string."}},"required":["summary"]}',
            },
            cost_threshold_credits=0,
            prompt="Please summarize the content of this web page in a few sentences.",
            time_threshold_seconds=0,
        )
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_summarize_content(self, async_client: AsyncAirtop) -> None:
        response = await async_client.windows.async_.with_raw_response.summarize_content(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        async_ = await response.parse()
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_summarize_content(self, async_client: AsyncAirtop) -> None:
        async with async_client.windows.async_.with_streaming_response.summarize_content(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            async_ = await response.parse()
            assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_summarize_content(self, async_client: AsyncAirtop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.windows.async_.with_raw_response.summarize_content(
                window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
                session_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `window_id` but received ''"):
            await async_client.windows.async_.with_raw_response.summarize_content(
                window_id="",
                session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_type(self, async_client: AsyncAirtop) -> None:
        async_ = await async_client.windows.async_.type(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            text="Example text",
        )
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_type_with_all_params(self, async_client: AsyncAirtop) -> None:
        async_ = await async_client.windows.async_.type(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            text="Example text",
            async_={"webhook_url": "webhookUrl"},
            clear_input_field=True,
            client_request_id="clientRequestId",
            configuration={
                "visual_analysis": {
                    "max_scan_scrolls": 0,
                    "overlap_percentage": 0,
                    "partition_direction": "vertical",
                    "result_selection_strategy": "first",
                    "scan_scroll_delay": 0,
                    "scope": "viewport",
                },
                "wait_for_navigation_config": {
                    "timeout_seconds": 10,
                    "wait_until": "load",
                },
            },
            cost_threshold_credits=0,
            element_description="The search box input in the top right corner",
            press_enter_key=True,
            press_tab_key=True,
            time_threshold_seconds=0,
            wait_for_navigation=True,
        )
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_type(self, async_client: AsyncAirtop) -> None:
        response = await async_client.windows.async_.with_raw_response.type(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            text="Example text",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        async_ = await response.parse()
        assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_type(self, async_client: AsyncAirtop) -> None:
        async with async_client.windows.async_.with_streaming_response.type(
            window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
            session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
            text="Example text",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            async_ = await response.parse()
            assert_matches_type(AsyncSessionAIResponseEnvelope, async_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_type(self, async_client: AsyncAirtop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.windows.async_.with_raw_response.type(
                window_id="0334da2a-91b0-42c5-6156-76a5eba87430",
                session_id="",
                text="Example text",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `window_id` but received ''"):
            await async_client.windows.async_.with_raw_response.type(
                window_id="",
                session_id="6aac6f73-bd89-4a76-ab32-5a6c422e8b0b",
                text="Example text",
            )

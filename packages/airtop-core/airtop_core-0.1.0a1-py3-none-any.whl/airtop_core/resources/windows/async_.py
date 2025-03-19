# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import (
    maybe_transform,
    async_maybe_transform,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.windows import (
    async_type_params,
    async_click_params,
    async_hover_params,
    async_monitor_params,
    async_page_query_params,
    async_screenshot_params,
    async_prompt_content_params,
    async_create_automation_params,
    async_summarize_content_params,
    async_execute_automation_params,
    async_paginated_extraction_params,
)
from ...types.shared_params.async_config import AsyncConfig
from ...types.shared_params.click_config import ClickConfig
from ...types.shared_params.monitor_config import MonitorConfig
from ...types.shared_params.summary_config import SummaryConfig
from ...types.shared_params.page_query_config import PageQueryConfig
from ...types.shared_params.micro_interaction_config import MicroInteractionConfig
from ...types.shared_params.create_automation_request import CreateAutomationRequest
from ...types.shared_params.screenshot_request_config import ScreenshotRequestConfig
from ...types.shared.async_session_ai_response_envelope import AsyncSessionAIResponseEnvelope
from ...types.shared_params.paginated_extraction_config import PaginatedExtractionConfig

__all__ = ["AsyncResource", "AsyncAsyncResource"]


class AsyncResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/airtop-ai/airtop-core-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/airtop-ai/airtop-core-sdk-python#with_streaming_response
        """
        return AsyncResourceWithStreamingResponse(self)

    def click(
        self,
        window_id: str,
        *,
        session_id: str,
        element_description: str,
        async_: AsyncConfig | NotGiven = NOT_GIVEN,
        client_request_id: str | NotGiven = NOT_GIVEN,
        configuration: ClickConfig | NotGiven = NOT_GIVEN,
        cost_threshold_credits: int | NotGiven = NOT_GIVEN,
        time_threshold_seconds: int | NotGiven = NOT_GIVEN,
        wait_for_navigation: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncSessionAIResponseEnvelope:
        """
        Execute a click interaction in a specific browser window asynchronously

        Args:
          session_id: The session id for the window.

          window_id: The Airtop window id of the browser window.

          element_description: A natural language description of the element to click.

          async_: Async configuration options.

          configuration: Request configuration

          cost_threshold_credits: A credit threshold that, once exceeded, will cause the operation to be
              cancelled. Note that this is _not_ a hard limit, but a threshold that is checked
              periodically during the course of fulfilling the request. A default threshold is
              used if not specified, but you can use this option to increase or decrease as
              needed. Set to 0 to disable this feature entirely (not recommended).

          time_threshold_seconds: A time threshold in seconds that, once exceeded, will cause the operation to be
              cancelled. Note that this is _not_ a hard limit, but a threshold that is checked
              periodically during the course of fulfilling the request. A default threshold is
              used if not specified, but you can use this option to increase or decrease as
              needed. Set to 0 to disable this feature entirely (not recommended).

              This setting does not extend the maximum session duration provided at the time
              of session creation.

          wait_for_navigation: If true, Airtop AI will wait for the navigation to complete after clicking the
              element.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        if not window_id:
            raise ValueError(f"Expected a non-empty value for `window_id` but received {window_id!r}")
        return self._post(
            f"/async/sessions/{session_id}/windows/{window_id}/click",
            body=maybe_transform(
                {
                    "element_description": element_description,
                    "async_": async_,
                    "client_request_id": client_request_id,
                    "configuration": configuration,
                    "cost_threshold_credits": cost_threshold_credits,
                    "time_threshold_seconds": time_threshold_seconds,
                    "wait_for_navigation": wait_for_navigation,
                },
                async_click_params.AsyncClickParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncSessionAIResponseEnvelope,
        )

    def create_automation(
        self,
        window_id: str,
        *,
        session_id: str,
        async_: AsyncConfig | NotGiven = NOT_GIVEN,
        client_request_id: str | NotGiven = NOT_GIVEN,
        configuration: CreateAutomationRequest | NotGiven = NOT_GIVEN,
        cost_threshold_credits: int | NotGiven = NOT_GIVEN,
        time_threshold_seconds: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncSessionAIResponseEnvelope:
        """
        Create an automation of a browser window asynchronously

        Args:
          session_id: The session id for the window.

          window_id: The Airtop window id of the browser window.

          async_: Async configuration options.

          configuration: Request configuration

          cost_threshold_credits: A credit threshold that, once exceeded, will cause the operation to be
              cancelled. Note that this is _not_ a hard limit, but a threshold that is checked
              periodically during the course of fulfilling the request. A default threshold is
              used if not specified, but you can use this option to increase or decrease as
              needed. Set to 0 to disable this feature entirely (not recommended).

          time_threshold_seconds: A time threshold in seconds that, once exceeded, will cause the operation to be
              cancelled. Note that this is _not_ a hard limit, but a threshold that is checked
              periodically during the course of fulfilling the request. A default threshold is
              used if not specified, but you can use this option to increase or decrease as
              needed. Set to 0 to disable this feature entirely (not recommended).

              This setting does not extend the maximum session duration provided at the time
              of session creation.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        if not window_id:
            raise ValueError(f"Expected a non-empty value for `window_id` but received {window_id!r}")
        return self._post(
            f"/async/sessions/{session_id}/windows/{window_id}/create-automation",
            body=maybe_transform(
                {
                    "async_": async_,
                    "client_request_id": client_request_id,
                    "configuration": configuration,
                    "cost_threshold_credits": cost_threshold_credits,
                    "time_threshold_seconds": time_threshold_seconds,
                },
                async_create_automation_params.AsyncCreateAutomationParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncSessionAIResponseEnvelope,
        )

    def execute_automation(
        self,
        window_id: str,
        *,
        session_id: str,
        automation_id: str,
        async_: AsyncConfig | NotGiven = NOT_GIVEN,
        client_request_id: str | NotGiven = NOT_GIVEN,
        cost_threshold_credits: int | NotGiven = NOT_GIVEN,
        parameters: Dict[str, object] | NotGiven = NOT_GIVEN,
        time_threshold_seconds: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncSessionAIResponseEnvelope:
        """
        Execute an automation of a browser window asynchronously

        Args:
          session_id: The session id for the window.

          window_id: The Airtop window id of the browser window.

          automation_id: The ID of the automation to execute

          async_: Async configuration options.

          cost_threshold_credits: A credit threshold that, once exceeded, will cause the operation to be
              cancelled. Note that this is _not_ a hard limit, but a threshold that is checked
              periodically during the course of fulfilling the request. A default threshold is
              used if not specified, but you can use this option to increase or decrease as
              needed. Set to 0 to disable this feature entirely (not recommended).

          parameters: Optional parameters to pass to the automation execution

          time_threshold_seconds: A time threshold in seconds that, once exceeded, will cause the operation to be
              cancelled. Note that this is _not_ a hard limit, but a threshold that is checked
              periodically during the course of fulfilling the request. A default threshold is
              used if not specified, but you can use this option to increase or decrease as
              needed. Set to 0 to disable this feature entirely (not recommended).

              This setting does not extend the maximum session duration provided at the time
              of session creation.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        if not window_id:
            raise ValueError(f"Expected a non-empty value for `window_id` but received {window_id!r}")
        return self._post(
            f"/async/sessions/{session_id}/windows/{window_id}/execute-automation",
            body=maybe_transform(
                {
                    "automation_id": automation_id,
                    "async_": async_,
                    "client_request_id": client_request_id,
                    "cost_threshold_credits": cost_threshold_credits,
                    "parameters": parameters,
                    "time_threshold_seconds": time_threshold_seconds,
                },
                async_execute_automation_params.AsyncExecuteAutomationParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncSessionAIResponseEnvelope,
        )

    def hover(
        self,
        window_id: str,
        *,
        session_id: str,
        element_description: str,
        async_: AsyncConfig | NotGiven = NOT_GIVEN,
        client_request_id: str | NotGiven = NOT_GIVEN,
        configuration: MicroInteractionConfig | NotGiven = NOT_GIVEN,
        cost_threshold_credits: int | NotGiven = NOT_GIVEN,
        time_threshold_seconds: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncSessionAIResponseEnvelope:
        """
        Execute a hover interaction in a specific browser window asynchronously

        Args:
          session_id: The session id for the window.

          window_id: The Airtop window id of the browser window.

          element_description: A natural language description of where to hover (e.g. 'the search box',
              'username field'). The interaction will be aborted if the target element cannot
              be found.

          async_: Async configuration options.

          configuration: Request configuration

          cost_threshold_credits: A credit threshold that, once exceeded, will cause the operation to be
              cancelled. Note that this is _not_ a hard limit, but a threshold that is checked
              periodically during the course of fulfilling the request. A default threshold is
              used if not specified, but you can use this option to increase or decrease as
              needed. Set to 0 to disable this feature entirely (not recommended).

          time_threshold_seconds: A time threshold in seconds that, once exceeded, will cause the operation to be
              cancelled. Note that this is _not_ a hard limit, but a threshold that is checked
              periodically during the course of fulfilling the request. A default threshold is
              used if not specified, but you can use this option to increase or decrease as
              needed. Set to 0 to disable this feature entirely (not recommended).

              This setting does not extend the maximum session duration provided at the time
              of session creation.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        if not window_id:
            raise ValueError(f"Expected a non-empty value for `window_id` but received {window_id!r}")
        return self._post(
            f"/async/sessions/{session_id}/windows/{window_id}/hover",
            body=maybe_transform(
                {
                    "element_description": element_description,
                    "async_": async_,
                    "client_request_id": client_request_id,
                    "configuration": configuration,
                    "cost_threshold_credits": cost_threshold_credits,
                    "time_threshold_seconds": time_threshold_seconds,
                },
                async_hover_params.AsyncHoverParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncSessionAIResponseEnvelope,
        )

    def monitor(
        self,
        window_id: str,
        *,
        session_id: str,
        async_: AsyncConfig | NotGiven = NOT_GIVEN,
        client_request_id: str | NotGiven = NOT_GIVEN,
        condition: str | NotGiven = NOT_GIVEN,
        configuration: MonitorConfig | NotGiven = NOT_GIVEN,
        cost_threshold_credits: int | NotGiven = NOT_GIVEN,
        selector: str | NotGiven = NOT_GIVEN,
        time_threshold_seconds: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncSessionAIResponseEnvelope:
        """
        Monitor a specific browser window for a condition using AI asynchronously

        Args:
          session_id: The session id for the window.

          window_id: The Airtop window id of the browser window.

          async_: Async configuration options.

          condition: A natural language description of the condition to monitor for in the browser
              window. Required when monitorType is 'interval'.

          configuration: Monitor configuration. If not specified, defaults to an interval monitor with a
              5 second interval.

          cost_threshold_credits: A credit threshold that, once exceeded, will cause the operation to be
              cancelled. Note that this is _not_ a hard limit, but a threshold that is checked
              periodically during the course of fulfilling the request. A default threshold is
              used if not specified, but you can use this option to increase or decrease as
              needed. Set to 0 to disable this feature entirely (not recommended).

          selector: The selector to wait for. Required when monitorType is 'selector'.

          time_threshold_seconds: A time threshold in seconds that, once exceeded, will cause the operation to be
              cancelled. Note that this is _not_ a hard limit, but a threshold that is checked
              periodically during the course of fulfilling the request. A default threshold is
              used if not specified, but you can use this option to increase or decrease as
              needed. Set to 0 to disable this feature entirely (not recommended).

              This setting does not extend the maximum session duration provided at the time
              of session creation.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        if not window_id:
            raise ValueError(f"Expected a non-empty value for `window_id` but received {window_id!r}")
        return self._post(
            f"/async/sessions/{session_id}/windows/{window_id}/monitor",
            body=maybe_transform(
                {
                    "async_": async_,
                    "client_request_id": client_request_id,
                    "condition": condition,
                    "configuration": configuration,
                    "cost_threshold_credits": cost_threshold_credits,
                    "selector": selector,
                    "time_threshold_seconds": time_threshold_seconds,
                },
                async_monitor_params.AsyncMonitorParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncSessionAIResponseEnvelope,
        )

    def page_query(
        self,
        window_id: str,
        *,
        session_id: str,
        prompt: str,
        async_: AsyncConfig | NotGiven = NOT_GIVEN,
        client_request_id: str | NotGiven = NOT_GIVEN,
        configuration: PageQueryConfig | NotGiven = NOT_GIVEN,
        cost_threshold_credits: int | NotGiven = NOT_GIVEN,
        follow_pagination_links: bool | NotGiven = NOT_GIVEN,
        time_threshold_seconds: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncSessionAIResponseEnvelope:
        """
        Submit async prompt that queries the content of a specific browser window.

        Args:
          session_id: The session id for the window.

          window_id: The Airtop window id of the browser window.

          prompt: The prompt to submit about the content in the browser window.

          async_: Async configuration options.

          configuration: Request configuration

          cost_threshold_credits: A credit threshold that, once exceeded, will cause the operation to be
              cancelled. Note that this is _not_ a hard limit, but a threshold that is checked
              periodically during the course of fulfilling the request. A default threshold is
              used if not specified, but you can use this option to increase or decrease as
              needed. Set to 0 to disable this feature entirely (not recommended).

          follow_pagination_links: Make a best effort attempt to load more content items than are originally
              displayed on the page, e.g. by following pagination links, clicking controls to
              load more content, utilizing infinite scrolling, etc. This can be quite a bit
              more costly, but may be necessary for sites that require additional interaction
              to show the needed results. You can provide constraints in your prompt (e.g. on
              the total number of pages or results to consider).

          time_threshold_seconds: A time threshold in seconds that, once exceeded, will cause the operation to be
              cancelled. Note that this is _not_ a hard limit, but a threshold that is checked
              periodically during the course of fulfilling the request. A default threshold is
              used if not specified, but you can use this option to increase or decrease as
              needed. Set to 0 to disable this feature entirely (not recommended).

              This setting does not extend the maximum session duration provided at the time
              of session creation.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        if not window_id:
            raise ValueError(f"Expected a non-empty value for `window_id` but received {window_id!r}")
        return self._post(
            f"/async/sessions/{session_id}/windows/{window_id}/page-query",
            body=maybe_transform(
                {
                    "prompt": prompt,
                    "async_": async_,
                    "client_request_id": client_request_id,
                    "configuration": configuration,
                    "cost_threshold_credits": cost_threshold_credits,
                    "follow_pagination_links": follow_pagination_links,
                    "time_threshold_seconds": time_threshold_seconds,
                },
                async_page_query_params.AsyncPageQueryParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncSessionAIResponseEnvelope,
        )

    def paginated_extraction(
        self,
        window_id: str,
        *,
        session_id: str,
        prompt: str,
        async_: AsyncConfig | NotGiven = NOT_GIVEN,
        client_request_id: str | NotGiven = NOT_GIVEN,
        configuration: PaginatedExtractionConfig | NotGiven = NOT_GIVEN,
        cost_threshold_credits: int | NotGiven = NOT_GIVEN,
        time_threshold_seconds: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncSessionAIResponseEnvelope:
        """
        Submit async prompt that queries the content of a specific browser window.

        Args:
          session_id: The session id for the window.

          window_id: The Airtop window id of the browser window.

          prompt: A prompt providing the Airtop AI model with additional direction or constraints
              about the page and the details you want to extract from the page.

          async_: Async configuration options.

          configuration: Request configuration

          cost_threshold_credits: A credit threshold that, once exceeded, will cause the operation to be
              cancelled. Note that this is _not_ a hard limit, but a threshold that is checked
              periodically during the course of fulfilling the request. A default threshold is
              used if not specified, but you can use this option to increase or decrease as
              needed. Set to 0 to disable this feature entirely (not recommended).

          time_threshold_seconds: A time threshold in seconds that, once exceeded, will cause the operation to be
              cancelled. Note that this is _not_ a hard limit, but a threshold that is checked
              periodically during the course of fulfilling the request. A default threshold is
              used if not specified, but you can use this option to increase or decrease as
              needed. Set to 0 to disable this feature entirely (not recommended).

              This setting does not extend the maximum session duration provided at the time
              of session creation.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        if not window_id:
            raise ValueError(f"Expected a non-empty value for `window_id` but received {window_id!r}")
        return self._post(
            f"/async/sessions/{session_id}/windows/{window_id}/paginated-extraction",
            body=maybe_transform(
                {
                    "prompt": prompt,
                    "async_": async_,
                    "client_request_id": client_request_id,
                    "configuration": configuration,
                    "cost_threshold_credits": cost_threshold_credits,
                    "time_threshold_seconds": time_threshold_seconds,
                },
                async_paginated_extraction_params.AsyncPaginatedExtractionParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncSessionAIResponseEnvelope,
        )

    def prompt_content(
        self,
        window_id: str,
        *,
        session_id: str,
        prompt: str,
        async_: AsyncConfig | NotGiven = NOT_GIVEN,
        client_request_id: str | NotGiven = NOT_GIVEN,
        configuration: PageQueryConfig | NotGiven = NOT_GIVEN,
        cost_threshold_credits: int | NotGiven = NOT_GIVEN,
        follow_pagination_links: bool | NotGiven = NOT_GIVEN,
        time_threshold_seconds: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncSessionAIResponseEnvelope:
        """This endpoint is deprecated.

        Please use the `pageQuery` endpoint instead.

        Args:
          session_id: The session id for the window.

          window_id: The Airtop window id of the browser window.

          prompt: The prompt to submit about the content in the browser window.

          async_: Async configuration options.

          configuration: Request configuration

          cost_threshold_credits: A credit threshold that, once exceeded, will cause the operation to be
              cancelled. Note that this is _not_ a hard limit, but a threshold that is checked
              periodically during the course of fulfilling the request. A default threshold is
              used if not specified, but you can use this option to increase or decrease as
              needed. Set to 0 to disable this feature entirely (not recommended).

          follow_pagination_links: Make a best effort attempt to load more content items than are originally
              displayed on the page, e.g. by following pagination links, clicking controls to
              load more content, utilizing infinite scrolling, etc. This can be quite a bit
              more costly, but may be necessary for sites that require additional interaction
              to show the needed results. You can provide constraints in your prompt (e.g. on
              the total number of pages or results to consider).

          time_threshold_seconds: A time threshold in seconds that, once exceeded, will cause the operation to be
              cancelled. Note that this is _not_ a hard limit, but a threshold that is checked
              periodically during the course of fulfilling the request. A default threshold is
              used if not specified, but you can use this option to increase or decrease as
              needed. Set to 0 to disable this feature entirely (not recommended).

              This setting does not extend the maximum session duration provided at the time
              of session creation.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        if not window_id:
            raise ValueError(f"Expected a non-empty value for `window_id` but received {window_id!r}")
        return self._post(
            f"/async/sessions/{session_id}/windows/{window_id}/prompt-content",
            body=maybe_transform(
                {
                    "prompt": prompt,
                    "async_": async_,
                    "client_request_id": client_request_id,
                    "configuration": configuration,
                    "cost_threshold_credits": cost_threshold_credits,
                    "follow_pagination_links": follow_pagination_links,
                    "time_threshold_seconds": time_threshold_seconds,
                },
                async_prompt_content_params.AsyncPromptContentParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncSessionAIResponseEnvelope,
        )

    def screenshot(
        self,
        window_id: str,
        *,
        session_id: str,
        async_: AsyncConfig | NotGiven = NOT_GIVEN,
        client_request_id: str | NotGiven = NOT_GIVEN,
        configuration: ScreenshotRequestConfig | NotGiven = NOT_GIVEN,
        cost_threshold_credits: int | NotGiven = NOT_GIVEN,
        time_threshold_seconds: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncSessionAIResponseEnvelope:
        """
        Take a screenshot of the current viewport of a browser window asynchronously

        Args:
          session_id: The session id for the window.

          window_id: The Airtop window id of the browser window.

          async_: Async configuration options.

          configuration: Request configuration

          cost_threshold_credits: A credit threshold that, once exceeded, will cause the operation to be
              cancelled. Note that this is _not_ a hard limit, but a threshold that is checked
              periodically during the course of fulfilling the request. A default threshold is
              used if not specified, but you can use this option to increase or decrease as
              needed. Set to 0 to disable this feature entirely (not recommended).

          time_threshold_seconds: A time threshold in seconds that, once exceeded, will cause the operation to be
              cancelled. Note that this is _not_ a hard limit, but a threshold that is checked
              periodically during the course of fulfilling the request. A default threshold is
              used if not specified, but you can use this option to increase or decrease as
              needed. Set to 0 to disable this feature entirely (not recommended).

              This setting does not extend the maximum session duration provided at the time
              of session creation.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        if not window_id:
            raise ValueError(f"Expected a non-empty value for `window_id` but received {window_id!r}")
        return self._post(
            f"/async/sessions/{session_id}/windows/{window_id}/screenshot",
            body=maybe_transform(
                {
                    "async_": async_,
                    "client_request_id": client_request_id,
                    "configuration": configuration,
                    "cost_threshold_credits": cost_threshold_credits,
                    "time_threshold_seconds": time_threshold_seconds,
                },
                async_screenshot_params.AsyncScreenshotParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncSessionAIResponseEnvelope,
        )

    def summarize_content(
        self,
        window_id: str,
        *,
        session_id: str,
        async_: AsyncConfig | NotGiven = NOT_GIVEN,
        client_request_id: str | NotGiven = NOT_GIVEN,
        configuration: SummaryConfig | NotGiven = NOT_GIVEN,
        cost_threshold_credits: int | NotGiven = NOT_GIVEN,
        prompt: str | NotGiven = NOT_GIVEN,
        time_threshold_seconds: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncSessionAIResponseEnvelope:
        """This endpoint is deprecated.

        Please use the `pageQuery` endpoint and ask for a
        summary in the prompt instead.

        Args:
          session_id: The session id for the window.

          window_id: The Airtop window id of the browser window to summarize.

          async_: Async configuration options.

          configuration: Request configuration

          cost_threshold_credits: A credit threshold that, once exceeded, will cause the operation to be
              cancelled. Note that this is _not_ a hard limit, but a threshold that is checked
              periodically during the course of fulfilling the request. A default threshold is
              used if not specified, but you can use this option to increase or decrease as
              needed. Set to 0 to disable this feature entirely (not recommended).

          prompt: An optional prompt providing the Airtop AI model with additional direction or
              constraints about the summary (such as desired length).

          time_threshold_seconds: A time threshold in seconds that, once exceeded, will cause the operation to be
              cancelled. Note that this is _not_ a hard limit, but a threshold that is checked
              periodically during the course of fulfilling the request. A default threshold is
              used if not specified, but you can use this option to increase or decrease as
              needed. Set to 0 to disable this feature entirely (not recommended).

              This setting does not extend the maximum session duration provided at the time
              of session creation.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        if not window_id:
            raise ValueError(f"Expected a non-empty value for `window_id` but received {window_id!r}")
        return self._post(
            f"/async/sessions/{session_id}/windows/{window_id}/summarize-content",
            body=maybe_transform(
                {
                    "async_": async_,
                    "client_request_id": client_request_id,
                    "configuration": configuration,
                    "cost_threshold_credits": cost_threshold_credits,
                    "prompt": prompt,
                    "time_threshold_seconds": time_threshold_seconds,
                },
                async_summarize_content_params.AsyncSummarizeContentParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncSessionAIResponseEnvelope,
        )

    def type(
        self,
        window_id: str,
        *,
        session_id: str,
        text: str,
        async_: AsyncConfig | NotGiven = NOT_GIVEN,
        clear_input_field: bool | NotGiven = NOT_GIVEN,
        client_request_id: str | NotGiven = NOT_GIVEN,
        configuration: MicroInteractionConfig | NotGiven = NOT_GIVEN,
        cost_threshold_credits: int | NotGiven = NOT_GIVEN,
        element_description: str | NotGiven = NOT_GIVEN,
        press_enter_key: bool | NotGiven = NOT_GIVEN,
        press_tab_key: bool | NotGiven = NOT_GIVEN,
        time_threshold_seconds: int | NotGiven = NOT_GIVEN,
        wait_for_navigation: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncSessionAIResponseEnvelope:
        """
        Execute a type interaction in a specific browser window asynchronously

        Args:
          session_id: The session id for the window.

          window_id: The Airtop window id of the browser window.

          text: The text to type into the browser window.

          async_: Async configuration options.

          clear_input_field: If true, and an HTML input field is active, clears the input field before typing
              the text.

          configuration: Request configuration

          cost_threshold_credits: A credit threshold that, once exceeded, will cause the operation to be
              cancelled. Note that this is _not_ a hard limit, but a threshold that is checked
              periodically during the course of fulfilling the request. A default threshold is
              used if not specified, but you can use this option to increase or decrease as
              needed. Set to 0 to disable this feature entirely (not recommended).

          element_description: A natural language description of where to type (e.g. 'the search box',
              'username field'). The interaction will be aborted if the target element cannot
              be found.

          press_enter_key: If true, simulates pressing the Enter key after typing the text.

          press_tab_key: If true, simulates pressing the Tab key after typing the text. Note that the tab
              key will be pressed after the Enter key if both options are configured.

          time_threshold_seconds: A time threshold in seconds that, once exceeded, will cause the operation to be
              cancelled. Note that this is _not_ a hard limit, but a threshold that is checked
              periodically during the course of fulfilling the request. A default threshold is
              used if not specified, but you can use this option to increase or decrease as
              needed. Set to 0 to disable this feature entirely (not recommended).

              This setting does not extend the maximum session duration provided at the time
              of session creation.

          wait_for_navigation: If true, Airtop AI will wait for the navigation to complete after clicking the
              element.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        if not window_id:
            raise ValueError(f"Expected a non-empty value for `window_id` but received {window_id!r}")
        return self._post(
            f"/async/sessions/{session_id}/windows/{window_id}/type",
            body=maybe_transform(
                {
                    "text": text,
                    "async_": async_,
                    "clear_input_field": clear_input_field,
                    "client_request_id": client_request_id,
                    "configuration": configuration,
                    "cost_threshold_credits": cost_threshold_credits,
                    "element_description": element_description,
                    "press_enter_key": press_enter_key,
                    "press_tab_key": press_tab_key,
                    "time_threshold_seconds": time_threshold_seconds,
                    "wait_for_navigation": wait_for_navigation,
                },
                async_type_params.AsyncTypeParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncSessionAIResponseEnvelope,
        )


class AsyncAsyncResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncAsyncResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/airtop-ai/airtop-core-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncAsyncResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAsyncResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/airtop-ai/airtop-core-sdk-python#with_streaming_response
        """
        return AsyncAsyncResourceWithStreamingResponse(self)

    async def click(
        self,
        window_id: str,
        *,
        session_id: str,
        element_description: str,
        async_: AsyncConfig | NotGiven = NOT_GIVEN,
        client_request_id: str | NotGiven = NOT_GIVEN,
        configuration: ClickConfig | NotGiven = NOT_GIVEN,
        cost_threshold_credits: int | NotGiven = NOT_GIVEN,
        time_threshold_seconds: int | NotGiven = NOT_GIVEN,
        wait_for_navigation: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncSessionAIResponseEnvelope:
        """
        Execute a click interaction in a specific browser window asynchronously

        Args:
          session_id: The session id for the window.

          window_id: The Airtop window id of the browser window.

          element_description: A natural language description of the element to click.

          async_: Async configuration options.

          configuration: Request configuration

          cost_threshold_credits: A credit threshold that, once exceeded, will cause the operation to be
              cancelled. Note that this is _not_ a hard limit, but a threshold that is checked
              periodically during the course of fulfilling the request. A default threshold is
              used if not specified, but you can use this option to increase or decrease as
              needed. Set to 0 to disable this feature entirely (not recommended).

          time_threshold_seconds: A time threshold in seconds that, once exceeded, will cause the operation to be
              cancelled. Note that this is _not_ a hard limit, but a threshold that is checked
              periodically during the course of fulfilling the request. A default threshold is
              used if not specified, but you can use this option to increase or decrease as
              needed. Set to 0 to disable this feature entirely (not recommended).

              This setting does not extend the maximum session duration provided at the time
              of session creation.

          wait_for_navigation: If true, Airtop AI will wait for the navigation to complete after clicking the
              element.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        if not window_id:
            raise ValueError(f"Expected a non-empty value for `window_id` but received {window_id!r}")
        return await self._post(
            f"/async/sessions/{session_id}/windows/{window_id}/click",
            body=await async_maybe_transform(
                {
                    "element_description": element_description,
                    "async_": async_,
                    "client_request_id": client_request_id,
                    "configuration": configuration,
                    "cost_threshold_credits": cost_threshold_credits,
                    "time_threshold_seconds": time_threshold_seconds,
                    "wait_for_navigation": wait_for_navigation,
                },
                async_click_params.AsyncClickParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncSessionAIResponseEnvelope,
        )

    async def create_automation(
        self,
        window_id: str,
        *,
        session_id: str,
        async_: AsyncConfig | NotGiven = NOT_GIVEN,
        client_request_id: str | NotGiven = NOT_GIVEN,
        configuration: CreateAutomationRequest | NotGiven = NOT_GIVEN,
        cost_threshold_credits: int | NotGiven = NOT_GIVEN,
        time_threshold_seconds: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncSessionAIResponseEnvelope:
        """
        Create an automation of a browser window asynchronously

        Args:
          session_id: The session id for the window.

          window_id: The Airtop window id of the browser window.

          async_: Async configuration options.

          configuration: Request configuration

          cost_threshold_credits: A credit threshold that, once exceeded, will cause the operation to be
              cancelled. Note that this is _not_ a hard limit, but a threshold that is checked
              periodically during the course of fulfilling the request. A default threshold is
              used if not specified, but you can use this option to increase or decrease as
              needed. Set to 0 to disable this feature entirely (not recommended).

          time_threshold_seconds: A time threshold in seconds that, once exceeded, will cause the operation to be
              cancelled. Note that this is _not_ a hard limit, but a threshold that is checked
              periodically during the course of fulfilling the request. A default threshold is
              used if not specified, but you can use this option to increase or decrease as
              needed. Set to 0 to disable this feature entirely (not recommended).

              This setting does not extend the maximum session duration provided at the time
              of session creation.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        if not window_id:
            raise ValueError(f"Expected a non-empty value for `window_id` but received {window_id!r}")
        return await self._post(
            f"/async/sessions/{session_id}/windows/{window_id}/create-automation",
            body=await async_maybe_transform(
                {
                    "async_": async_,
                    "client_request_id": client_request_id,
                    "configuration": configuration,
                    "cost_threshold_credits": cost_threshold_credits,
                    "time_threshold_seconds": time_threshold_seconds,
                },
                async_create_automation_params.AsyncCreateAutomationParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncSessionAIResponseEnvelope,
        )

    async def execute_automation(
        self,
        window_id: str,
        *,
        session_id: str,
        automation_id: str,
        async_: AsyncConfig | NotGiven = NOT_GIVEN,
        client_request_id: str | NotGiven = NOT_GIVEN,
        cost_threshold_credits: int | NotGiven = NOT_GIVEN,
        parameters: Dict[str, object] | NotGiven = NOT_GIVEN,
        time_threshold_seconds: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncSessionAIResponseEnvelope:
        """
        Execute an automation of a browser window asynchronously

        Args:
          session_id: The session id for the window.

          window_id: The Airtop window id of the browser window.

          automation_id: The ID of the automation to execute

          async_: Async configuration options.

          cost_threshold_credits: A credit threshold that, once exceeded, will cause the operation to be
              cancelled. Note that this is _not_ a hard limit, but a threshold that is checked
              periodically during the course of fulfilling the request. A default threshold is
              used if not specified, but you can use this option to increase or decrease as
              needed. Set to 0 to disable this feature entirely (not recommended).

          parameters: Optional parameters to pass to the automation execution

          time_threshold_seconds: A time threshold in seconds that, once exceeded, will cause the operation to be
              cancelled. Note that this is _not_ a hard limit, but a threshold that is checked
              periodically during the course of fulfilling the request. A default threshold is
              used if not specified, but you can use this option to increase or decrease as
              needed. Set to 0 to disable this feature entirely (not recommended).

              This setting does not extend the maximum session duration provided at the time
              of session creation.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        if not window_id:
            raise ValueError(f"Expected a non-empty value for `window_id` but received {window_id!r}")
        return await self._post(
            f"/async/sessions/{session_id}/windows/{window_id}/execute-automation",
            body=await async_maybe_transform(
                {
                    "automation_id": automation_id,
                    "async_": async_,
                    "client_request_id": client_request_id,
                    "cost_threshold_credits": cost_threshold_credits,
                    "parameters": parameters,
                    "time_threshold_seconds": time_threshold_seconds,
                },
                async_execute_automation_params.AsyncExecuteAutomationParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncSessionAIResponseEnvelope,
        )

    async def hover(
        self,
        window_id: str,
        *,
        session_id: str,
        element_description: str,
        async_: AsyncConfig | NotGiven = NOT_GIVEN,
        client_request_id: str | NotGiven = NOT_GIVEN,
        configuration: MicroInteractionConfig | NotGiven = NOT_GIVEN,
        cost_threshold_credits: int | NotGiven = NOT_GIVEN,
        time_threshold_seconds: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncSessionAIResponseEnvelope:
        """
        Execute a hover interaction in a specific browser window asynchronously

        Args:
          session_id: The session id for the window.

          window_id: The Airtop window id of the browser window.

          element_description: A natural language description of where to hover (e.g. 'the search box',
              'username field'). The interaction will be aborted if the target element cannot
              be found.

          async_: Async configuration options.

          configuration: Request configuration

          cost_threshold_credits: A credit threshold that, once exceeded, will cause the operation to be
              cancelled. Note that this is _not_ a hard limit, but a threshold that is checked
              periodically during the course of fulfilling the request. A default threshold is
              used if not specified, but you can use this option to increase or decrease as
              needed. Set to 0 to disable this feature entirely (not recommended).

          time_threshold_seconds: A time threshold in seconds that, once exceeded, will cause the operation to be
              cancelled. Note that this is _not_ a hard limit, but a threshold that is checked
              periodically during the course of fulfilling the request. A default threshold is
              used if not specified, but you can use this option to increase or decrease as
              needed. Set to 0 to disable this feature entirely (not recommended).

              This setting does not extend the maximum session duration provided at the time
              of session creation.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        if not window_id:
            raise ValueError(f"Expected a non-empty value for `window_id` but received {window_id!r}")
        return await self._post(
            f"/async/sessions/{session_id}/windows/{window_id}/hover",
            body=await async_maybe_transform(
                {
                    "element_description": element_description,
                    "async_": async_,
                    "client_request_id": client_request_id,
                    "configuration": configuration,
                    "cost_threshold_credits": cost_threshold_credits,
                    "time_threshold_seconds": time_threshold_seconds,
                },
                async_hover_params.AsyncHoverParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncSessionAIResponseEnvelope,
        )

    async def monitor(
        self,
        window_id: str,
        *,
        session_id: str,
        async_: AsyncConfig | NotGiven = NOT_GIVEN,
        client_request_id: str | NotGiven = NOT_GIVEN,
        condition: str | NotGiven = NOT_GIVEN,
        configuration: MonitorConfig | NotGiven = NOT_GIVEN,
        cost_threshold_credits: int | NotGiven = NOT_GIVEN,
        selector: str | NotGiven = NOT_GIVEN,
        time_threshold_seconds: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncSessionAIResponseEnvelope:
        """
        Monitor a specific browser window for a condition using AI asynchronously

        Args:
          session_id: The session id for the window.

          window_id: The Airtop window id of the browser window.

          async_: Async configuration options.

          condition: A natural language description of the condition to monitor for in the browser
              window. Required when monitorType is 'interval'.

          configuration: Monitor configuration. If not specified, defaults to an interval monitor with a
              5 second interval.

          cost_threshold_credits: A credit threshold that, once exceeded, will cause the operation to be
              cancelled. Note that this is _not_ a hard limit, but a threshold that is checked
              periodically during the course of fulfilling the request. A default threshold is
              used if not specified, but you can use this option to increase or decrease as
              needed. Set to 0 to disable this feature entirely (not recommended).

          selector: The selector to wait for. Required when monitorType is 'selector'.

          time_threshold_seconds: A time threshold in seconds that, once exceeded, will cause the operation to be
              cancelled. Note that this is _not_ a hard limit, but a threshold that is checked
              periodically during the course of fulfilling the request. A default threshold is
              used if not specified, but you can use this option to increase or decrease as
              needed. Set to 0 to disable this feature entirely (not recommended).

              This setting does not extend the maximum session duration provided at the time
              of session creation.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        if not window_id:
            raise ValueError(f"Expected a non-empty value for `window_id` but received {window_id!r}")
        return await self._post(
            f"/async/sessions/{session_id}/windows/{window_id}/monitor",
            body=await async_maybe_transform(
                {
                    "async_": async_,
                    "client_request_id": client_request_id,
                    "condition": condition,
                    "configuration": configuration,
                    "cost_threshold_credits": cost_threshold_credits,
                    "selector": selector,
                    "time_threshold_seconds": time_threshold_seconds,
                },
                async_monitor_params.AsyncMonitorParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncSessionAIResponseEnvelope,
        )

    async def page_query(
        self,
        window_id: str,
        *,
        session_id: str,
        prompt: str,
        async_: AsyncConfig | NotGiven = NOT_GIVEN,
        client_request_id: str | NotGiven = NOT_GIVEN,
        configuration: PageQueryConfig | NotGiven = NOT_GIVEN,
        cost_threshold_credits: int | NotGiven = NOT_GIVEN,
        follow_pagination_links: bool | NotGiven = NOT_GIVEN,
        time_threshold_seconds: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncSessionAIResponseEnvelope:
        """
        Submit async prompt that queries the content of a specific browser window.

        Args:
          session_id: The session id for the window.

          window_id: The Airtop window id of the browser window.

          prompt: The prompt to submit about the content in the browser window.

          async_: Async configuration options.

          configuration: Request configuration

          cost_threshold_credits: A credit threshold that, once exceeded, will cause the operation to be
              cancelled. Note that this is _not_ a hard limit, but a threshold that is checked
              periodically during the course of fulfilling the request. A default threshold is
              used if not specified, but you can use this option to increase or decrease as
              needed. Set to 0 to disable this feature entirely (not recommended).

          follow_pagination_links: Make a best effort attempt to load more content items than are originally
              displayed on the page, e.g. by following pagination links, clicking controls to
              load more content, utilizing infinite scrolling, etc. This can be quite a bit
              more costly, but may be necessary for sites that require additional interaction
              to show the needed results. You can provide constraints in your prompt (e.g. on
              the total number of pages or results to consider).

          time_threshold_seconds: A time threshold in seconds that, once exceeded, will cause the operation to be
              cancelled. Note that this is _not_ a hard limit, but a threshold that is checked
              periodically during the course of fulfilling the request. A default threshold is
              used if not specified, but you can use this option to increase or decrease as
              needed. Set to 0 to disable this feature entirely (not recommended).

              This setting does not extend the maximum session duration provided at the time
              of session creation.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        if not window_id:
            raise ValueError(f"Expected a non-empty value for `window_id` but received {window_id!r}")
        return await self._post(
            f"/async/sessions/{session_id}/windows/{window_id}/page-query",
            body=await async_maybe_transform(
                {
                    "prompt": prompt,
                    "async_": async_,
                    "client_request_id": client_request_id,
                    "configuration": configuration,
                    "cost_threshold_credits": cost_threshold_credits,
                    "follow_pagination_links": follow_pagination_links,
                    "time_threshold_seconds": time_threshold_seconds,
                },
                async_page_query_params.AsyncPageQueryParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncSessionAIResponseEnvelope,
        )

    async def paginated_extraction(
        self,
        window_id: str,
        *,
        session_id: str,
        prompt: str,
        async_: AsyncConfig | NotGiven = NOT_GIVEN,
        client_request_id: str | NotGiven = NOT_GIVEN,
        configuration: PaginatedExtractionConfig | NotGiven = NOT_GIVEN,
        cost_threshold_credits: int | NotGiven = NOT_GIVEN,
        time_threshold_seconds: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncSessionAIResponseEnvelope:
        """
        Submit async prompt that queries the content of a specific browser window.

        Args:
          session_id: The session id for the window.

          window_id: The Airtop window id of the browser window.

          prompt: A prompt providing the Airtop AI model with additional direction or constraints
              about the page and the details you want to extract from the page.

          async_: Async configuration options.

          configuration: Request configuration

          cost_threshold_credits: A credit threshold that, once exceeded, will cause the operation to be
              cancelled. Note that this is _not_ a hard limit, but a threshold that is checked
              periodically during the course of fulfilling the request. A default threshold is
              used if not specified, but you can use this option to increase or decrease as
              needed. Set to 0 to disable this feature entirely (not recommended).

          time_threshold_seconds: A time threshold in seconds that, once exceeded, will cause the operation to be
              cancelled. Note that this is _not_ a hard limit, but a threshold that is checked
              periodically during the course of fulfilling the request. A default threshold is
              used if not specified, but you can use this option to increase or decrease as
              needed. Set to 0 to disable this feature entirely (not recommended).

              This setting does not extend the maximum session duration provided at the time
              of session creation.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        if not window_id:
            raise ValueError(f"Expected a non-empty value for `window_id` but received {window_id!r}")
        return await self._post(
            f"/async/sessions/{session_id}/windows/{window_id}/paginated-extraction",
            body=await async_maybe_transform(
                {
                    "prompt": prompt,
                    "async_": async_,
                    "client_request_id": client_request_id,
                    "configuration": configuration,
                    "cost_threshold_credits": cost_threshold_credits,
                    "time_threshold_seconds": time_threshold_seconds,
                },
                async_paginated_extraction_params.AsyncPaginatedExtractionParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncSessionAIResponseEnvelope,
        )

    async def prompt_content(
        self,
        window_id: str,
        *,
        session_id: str,
        prompt: str,
        async_: AsyncConfig | NotGiven = NOT_GIVEN,
        client_request_id: str | NotGiven = NOT_GIVEN,
        configuration: PageQueryConfig | NotGiven = NOT_GIVEN,
        cost_threshold_credits: int | NotGiven = NOT_GIVEN,
        follow_pagination_links: bool | NotGiven = NOT_GIVEN,
        time_threshold_seconds: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncSessionAIResponseEnvelope:
        """This endpoint is deprecated.

        Please use the `pageQuery` endpoint instead.

        Args:
          session_id: The session id for the window.

          window_id: The Airtop window id of the browser window.

          prompt: The prompt to submit about the content in the browser window.

          async_: Async configuration options.

          configuration: Request configuration

          cost_threshold_credits: A credit threshold that, once exceeded, will cause the operation to be
              cancelled. Note that this is _not_ a hard limit, but a threshold that is checked
              periodically during the course of fulfilling the request. A default threshold is
              used if not specified, but you can use this option to increase or decrease as
              needed. Set to 0 to disable this feature entirely (not recommended).

          follow_pagination_links: Make a best effort attempt to load more content items than are originally
              displayed on the page, e.g. by following pagination links, clicking controls to
              load more content, utilizing infinite scrolling, etc. This can be quite a bit
              more costly, but may be necessary for sites that require additional interaction
              to show the needed results. You can provide constraints in your prompt (e.g. on
              the total number of pages or results to consider).

          time_threshold_seconds: A time threshold in seconds that, once exceeded, will cause the operation to be
              cancelled. Note that this is _not_ a hard limit, but a threshold that is checked
              periodically during the course of fulfilling the request. A default threshold is
              used if not specified, but you can use this option to increase or decrease as
              needed. Set to 0 to disable this feature entirely (not recommended).

              This setting does not extend the maximum session duration provided at the time
              of session creation.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        if not window_id:
            raise ValueError(f"Expected a non-empty value for `window_id` but received {window_id!r}")
        return await self._post(
            f"/async/sessions/{session_id}/windows/{window_id}/prompt-content",
            body=await async_maybe_transform(
                {
                    "prompt": prompt,
                    "async_": async_,
                    "client_request_id": client_request_id,
                    "configuration": configuration,
                    "cost_threshold_credits": cost_threshold_credits,
                    "follow_pagination_links": follow_pagination_links,
                    "time_threshold_seconds": time_threshold_seconds,
                },
                async_prompt_content_params.AsyncPromptContentParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncSessionAIResponseEnvelope,
        )

    async def screenshot(
        self,
        window_id: str,
        *,
        session_id: str,
        async_: AsyncConfig | NotGiven = NOT_GIVEN,
        client_request_id: str | NotGiven = NOT_GIVEN,
        configuration: ScreenshotRequestConfig | NotGiven = NOT_GIVEN,
        cost_threshold_credits: int | NotGiven = NOT_GIVEN,
        time_threshold_seconds: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncSessionAIResponseEnvelope:
        """
        Take a screenshot of the current viewport of a browser window asynchronously

        Args:
          session_id: The session id for the window.

          window_id: The Airtop window id of the browser window.

          async_: Async configuration options.

          configuration: Request configuration

          cost_threshold_credits: A credit threshold that, once exceeded, will cause the operation to be
              cancelled. Note that this is _not_ a hard limit, but a threshold that is checked
              periodically during the course of fulfilling the request. A default threshold is
              used if not specified, but you can use this option to increase or decrease as
              needed. Set to 0 to disable this feature entirely (not recommended).

          time_threshold_seconds: A time threshold in seconds that, once exceeded, will cause the operation to be
              cancelled. Note that this is _not_ a hard limit, but a threshold that is checked
              periodically during the course of fulfilling the request. A default threshold is
              used if not specified, but you can use this option to increase or decrease as
              needed. Set to 0 to disable this feature entirely (not recommended).

              This setting does not extend the maximum session duration provided at the time
              of session creation.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        if not window_id:
            raise ValueError(f"Expected a non-empty value for `window_id` but received {window_id!r}")
        return await self._post(
            f"/async/sessions/{session_id}/windows/{window_id}/screenshot",
            body=await async_maybe_transform(
                {
                    "async_": async_,
                    "client_request_id": client_request_id,
                    "configuration": configuration,
                    "cost_threshold_credits": cost_threshold_credits,
                    "time_threshold_seconds": time_threshold_seconds,
                },
                async_screenshot_params.AsyncScreenshotParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncSessionAIResponseEnvelope,
        )

    async def summarize_content(
        self,
        window_id: str,
        *,
        session_id: str,
        async_: AsyncConfig | NotGiven = NOT_GIVEN,
        client_request_id: str | NotGiven = NOT_GIVEN,
        configuration: SummaryConfig | NotGiven = NOT_GIVEN,
        cost_threshold_credits: int | NotGiven = NOT_GIVEN,
        prompt: str | NotGiven = NOT_GIVEN,
        time_threshold_seconds: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncSessionAIResponseEnvelope:
        """This endpoint is deprecated.

        Please use the `pageQuery` endpoint and ask for a
        summary in the prompt instead.

        Args:
          session_id: The session id for the window.

          window_id: The Airtop window id of the browser window to summarize.

          async_: Async configuration options.

          configuration: Request configuration

          cost_threshold_credits: A credit threshold that, once exceeded, will cause the operation to be
              cancelled. Note that this is _not_ a hard limit, but a threshold that is checked
              periodically during the course of fulfilling the request. A default threshold is
              used if not specified, but you can use this option to increase or decrease as
              needed. Set to 0 to disable this feature entirely (not recommended).

          prompt: An optional prompt providing the Airtop AI model with additional direction or
              constraints about the summary (such as desired length).

          time_threshold_seconds: A time threshold in seconds that, once exceeded, will cause the operation to be
              cancelled. Note that this is _not_ a hard limit, but a threshold that is checked
              periodically during the course of fulfilling the request. A default threshold is
              used if not specified, but you can use this option to increase or decrease as
              needed. Set to 0 to disable this feature entirely (not recommended).

              This setting does not extend the maximum session duration provided at the time
              of session creation.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        if not window_id:
            raise ValueError(f"Expected a non-empty value for `window_id` but received {window_id!r}")
        return await self._post(
            f"/async/sessions/{session_id}/windows/{window_id}/summarize-content",
            body=await async_maybe_transform(
                {
                    "async_": async_,
                    "client_request_id": client_request_id,
                    "configuration": configuration,
                    "cost_threshold_credits": cost_threshold_credits,
                    "prompt": prompt,
                    "time_threshold_seconds": time_threshold_seconds,
                },
                async_summarize_content_params.AsyncSummarizeContentParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncSessionAIResponseEnvelope,
        )

    async def type(
        self,
        window_id: str,
        *,
        session_id: str,
        text: str,
        async_: AsyncConfig | NotGiven = NOT_GIVEN,
        clear_input_field: bool | NotGiven = NOT_GIVEN,
        client_request_id: str | NotGiven = NOT_GIVEN,
        configuration: MicroInteractionConfig | NotGiven = NOT_GIVEN,
        cost_threshold_credits: int | NotGiven = NOT_GIVEN,
        element_description: str | NotGiven = NOT_GIVEN,
        press_enter_key: bool | NotGiven = NOT_GIVEN,
        press_tab_key: bool | NotGiven = NOT_GIVEN,
        time_threshold_seconds: int | NotGiven = NOT_GIVEN,
        wait_for_navigation: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncSessionAIResponseEnvelope:
        """
        Execute a type interaction in a specific browser window asynchronously

        Args:
          session_id: The session id for the window.

          window_id: The Airtop window id of the browser window.

          text: The text to type into the browser window.

          async_: Async configuration options.

          clear_input_field: If true, and an HTML input field is active, clears the input field before typing
              the text.

          configuration: Request configuration

          cost_threshold_credits: A credit threshold that, once exceeded, will cause the operation to be
              cancelled. Note that this is _not_ a hard limit, but a threshold that is checked
              periodically during the course of fulfilling the request. A default threshold is
              used if not specified, but you can use this option to increase or decrease as
              needed. Set to 0 to disable this feature entirely (not recommended).

          element_description: A natural language description of where to type (e.g. 'the search box',
              'username field'). The interaction will be aborted if the target element cannot
              be found.

          press_enter_key: If true, simulates pressing the Enter key after typing the text.

          press_tab_key: If true, simulates pressing the Tab key after typing the text. Note that the tab
              key will be pressed after the Enter key if both options are configured.

          time_threshold_seconds: A time threshold in seconds that, once exceeded, will cause the operation to be
              cancelled. Note that this is _not_ a hard limit, but a threshold that is checked
              periodically during the course of fulfilling the request. A default threshold is
              used if not specified, but you can use this option to increase or decrease as
              needed. Set to 0 to disable this feature entirely (not recommended).

              This setting does not extend the maximum session duration provided at the time
              of session creation.

          wait_for_navigation: If true, Airtop AI will wait for the navigation to complete after clicking the
              element.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_id:
            raise ValueError(f"Expected a non-empty value for `session_id` but received {session_id!r}")
        if not window_id:
            raise ValueError(f"Expected a non-empty value for `window_id` but received {window_id!r}")
        return await self._post(
            f"/async/sessions/{session_id}/windows/{window_id}/type",
            body=await async_maybe_transform(
                {
                    "text": text,
                    "async_": async_,
                    "clear_input_field": clear_input_field,
                    "client_request_id": client_request_id,
                    "configuration": configuration,
                    "cost_threshold_credits": cost_threshold_credits,
                    "element_description": element_description,
                    "press_enter_key": press_enter_key,
                    "press_tab_key": press_tab_key,
                    "time_threshold_seconds": time_threshold_seconds,
                    "wait_for_navigation": wait_for_navigation,
                },
                async_type_params.AsyncTypeParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncSessionAIResponseEnvelope,
        )


class AsyncResourceWithRawResponse:
    def __init__(self, async_: AsyncResource) -> None:
        self._async_ = async_

        self.click = to_raw_response_wrapper(
            async_.click,
        )
        self.create_automation = to_raw_response_wrapper(
            async_.create_automation,
        )
        self.execute_automation = to_raw_response_wrapper(
            async_.execute_automation,
        )
        self.hover = to_raw_response_wrapper(
            async_.hover,
        )
        self.monitor = to_raw_response_wrapper(
            async_.monitor,
        )
        self.page_query = to_raw_response_wrapper(
            async_.page_query,
        )
        self.paginated_extraction = to_raw_response_wrapper(
            async_.paginated_extraction,
        )
        self.prompt_content = to_raw_response_wrapper(
            async_.prompt_content,
        )
        self.screenshot = to_raw_response_wrapper(
            async_.screenshot,
        )
        self.summarize_content = to_raw_response_wrapper(
            async_.summarize_content,
        )
        self.type = to_raw_response_wrapper(
            async_.type,
        )


class AsyncAsyncResourceWithRawResponse:
    def __init__(self, async_: AsyncAsyncResource) -> None:
        self._async_ = async_

        self.click = async_to_raw_response_wrapper(
            async_.click,
        )
        self.create_automation = async_to_raw_response_wrapper(
            async_.create_automation,
        )
        self.execute_automation = async_to_raw_response_wrapper(
            async_.execute_automation,
        )
        self.hover = async_to_raw_response_wrapper(
            async_.hover,
        )
        self.monitor = async_to_raw_response_wrapper(
            async_.monitor,
        )
        self.page_query = async_to_raw_response_wrapper(
            async_.page_query,
        )
        self.paginated_extraction = async_to_raw_response_wrapper(
            async_.paginated_extraction,
        )
        self.prompt_content = async_to_raw_response_wrapper(
            async_.prompt_content,
        )
        self.screenshot = async_to_raw_response_wrapper(
            async_.screenshot,
        )
        self.summarize_content = async_to_raw_response_wrapper(
            async_.summarize_content,
        )
        self.type = async_to_raw_response_wrapper(
            async_.type,
        )


class AsyncResourceWithStreamingResponse:
    def __init__(self, async_: AsyncResource) -> None:
        self._async_ = async_

        self.click = to_streamed_response_wrapper(
            async_.click,
        )
        self.create_automation = to_streamed_response_wrapper(
            async_.create_automation,
        )
        self.execute_automation = to_streamed_response_wrapper(
            async_.execute_automation,
        )
        self.hover = to_streamed_response_wrapper(
            async_.hover,
        )
        self.monitor = to_streamed_response_wrapper(
            async_.monitor,
        )
        self.page_query = to_streamed_response_wrapper(
            async_.page_query,
        )
        self.paginated_extraction = to_streamed_response_wrapper(
            async_.paginated_extraction,
        )
        self.prompt_content = to_streamed_response_wrapper(
            async_.prompt_content,
        )
        self.screenshot = to_streamed_response_wrapper(
            async_.screenshot,
        )
        self.summarize_content = to_streamed_response_wrapper(
            async_.summarize_content,
        )
        self.type = to_streamed_response_wrapper(
            async_.type,
        )


class AsyncAsyncResourceWithStreamingResponse:
    def __init__(self, async_: AsyncAsyncResource) -> None:
        self._async_ = async_

        self.click = async_to_streamed_response_wrapper(
            async_.click,
        )
        self.create_automation = async_to_streamed_response_wrapper(
            async_.create_automation,
        )
        self.execute_automation = async_to_streamed_response_wrapper(
            async_.execute_automation,
        )
        self.hover = async_to_streamed_response_wrapper(
            async_.hover,
        )
        self.monitor = async_to_streamed_response_wrapper(
            async_.monitor,
        )
        self.page_query = async_to_streamed_response_wrapper(
            async_.page_query,
        )
        self.paginated_extraction = async_to_streamed_response_wrapper(
            async_.paginated_extraction,
        )
        self.prompt_content = async_to_streamed_response_wrapper(
            async_.prompt_content,
        )
        self.screenshot = async_to_streamed_response_wrapper(
            async_.screenshot,
        )
        self.summarize_content = async_to_streamed_response_wrapper(
            async_.summarize_content,
        )
        self.type = async_to_streamed_response_wrapper(
            async_.type,
        )

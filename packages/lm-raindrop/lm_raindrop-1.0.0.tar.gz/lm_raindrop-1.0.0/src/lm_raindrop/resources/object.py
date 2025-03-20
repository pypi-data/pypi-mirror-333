# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import object_upload_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven, FileTypes
from .._utils import (
    maybe_transform,
    async_maybe_transform,
)
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    BinaryAPIResponse,
    AsyncBinaryAPIResponse,
    StreamedBinaryAPIResponse,
    AsyncStreamedBinaryAPIResponse,
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    to_custom_raw_response_wrapper,
    async_to_streamed_response_wrapper,
    to_custom_streamed_response_wrapper,
    async_to_custom_raw_response_wrapper,
    async_to_custom_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.object_delete_response import ObjectDeleteResponse
from ..types.object_upload_response import ObjectUploadResponse

__all__ = ["ObjectResource", "AsyncObjectResource"]


class ObjectResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ObjectResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/LiquidMetal-AI/raindrop-python-sdk#accessing-raw-response-data-eg-headers
        """
        return ObjectResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ObjectResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/LiquidMetal-AI/raindrop-python-sdk#with_streaming_response
        """
        return ObjectResourceWithStreamingResponse(self)

    def delete(
        self,
        key: str,
        *,
        bucket: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ObjectDeleteResponse:
        """Delete a file from the storage system.

        The bucket parameter is used for access
        control, while the key determines which object to delete.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bucket:
            raise ValueError(f"Expected a non-empty value for `bucket` but received {bucket!r}")
        if not key:
            raise ValueError(f"Expected a non-empty value for `key` but received {key!r}")
        return self._delete(
            f"/v1/object/{bucket}/{key}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ObjectDeleteResponse,
        )

    def download(
        self,
        key: str,
        *,
        bucket: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BinaryAPIResponse:
        """Download a file from the storage system.

        The bucket parameter is used for access
        control, while the key determines which object to retrieve. Supports streaming
        downloads.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bucket:
            raise ValueError(f"Expected a non-empty value for `bucket` but received {bucket!r}")
        if not key:
            raise ValueError(f"Expected a non-empty value for `key` but received {key!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            f"/v1/object/{bucket}/{key}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def upload(
        self,
        key: str,
        *,
        bucket: str,
        body: FileTypes,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ObjectUploadResponse:
        """Upload a file to the storage system.

        The bucket parameter is used for access
        control, while the key determines the storage path. Supports streaming uploads
        for files of any size.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bucket:
            raise ValueError(f"Expected a non-empty value for `bucket` but received {bucket!r}")
        if not key:
            raise ValueError(f"Expected a non-empty value for `key` but received {key!r}")
        return self._put(
            f"/v1/object/{bucket}/{key}",
            body=maybe_transform(body, object_upload_params.ObjectUploadParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ObjectUploadResponse,
        )


class AsyncObjectResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncObjectResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/LiquidMetal-AI/raindrop-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncObjectResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncObjectResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/LiquidMetal-AI/raindrop-python-sdk#with_streaming_response
        """
        return AsyncObjectResourceWithStreamingResponse(self)

    async def delete(
        self,
        key: str,
        *,
        bucket: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ObjectDeleteResponse:
        """Delete a file from the storage system.

        The bucket parameter is used for access
        control, while the key determines which object to delete.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bucket:
            raise ValueError(f"Expected a non-empty value for `bucket` but received {bucket!r}")
        if not key:
            raise ValueError(f"Expected a non-empty value for `key` but received {key!r}")
        return await self._delete(
            f"/v1/object/{bucket}/{key}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ObjectDeleteResponse,
        )

    async def download(
        self,
        key: str,
        *,
        bucket: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncBinaryAPIResponse:
        """Download a file from the storage system.

        The bucket parameter is used for access
        control, while the key determines which object to retrieve. Supports streaming
        downloads.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bucket:
            raise ValueError(f"Expected a non-empty value for `bucket` but received {bucket!r}")
        if not key:
            raise ValueError(f"Expected a non-empty value for `key` but received {key!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            f"/v1/object/{bucket}/{key}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def upload(
        self,
        key: str,
        *,
        bucket: str,
        body: FileTypes,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ObjectUploadResponse:
        """Upload a file to the storage system.

        The bucket parameter is used for access
        control, while the key determines the storage path. Supports streaming uploads
        for files of any size.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not bucket:
            raise ValueError(f"Expected a non-empty value for `bucket` but received {bucket!r}")
        if not key:
            raise ValueError(f"Expected a non-empty value for `key` but received {key!r}")
        return await self._put(
            f"/v1/object/{bucket}/{key}",
            body=await async_maybe_transform(body, object_upload_params.ObjectUploadParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ObjectUploadResponse,
        )


class ObjectResourceWithRawResponse:
    def __init__(self, object: ObjectResource) -> None:
        self._object = object

        self.delete = to_raw_response_wrapper(
            object.delete,
        )
        self.download = to_custom_raw_response_wrapper(
            object.download,
            BinaryAPIResponse,
        )
        self.upload = to_raw_response_wrapper(
            object.upload,
        )


class AsyncObjectResourceWithRawResponse:
    def __init__(self, object: AsyncObjectResource) -> None:
        self._object = object

        self.delete = async_to_raw_response_wrapper(
            object.delete,
        )
        self.download = async_to_custom_raw_response_wrapper(
            object.download,
            AsyncBinaryAPIResponse,
        )
        self.upload = async_to_raw_response_wrapper(
            object.upload,
        )


class ObjectResourceWithStreamingResponse:
    def __init__(self, object: ObjectResource) -> None:
        self._object = object

        self.delete = to_streamed_response_wrapper(
            object.delete,
        )
        self.download = to_custom_streamed_response_wrapper(
            object.download,
            StreamedBinaryAPIResponse,
        )
        self.upload = to_streamed_response_wrapper(
            object.upload,
        )


class AsyncObjectResourceWithStreamingResponse:
    def __init__(self, object: AsyncObjectResource) -> None:
        self._object = object

        self.delete = async_to_streamed_response_wrapper(
            object.delete,
        )
        self.download = async_to_custom_streamed_response_wrapper(
            object.download,
            AsyncStreamedBinaryAPIResponse,
        )
        self.upload = async_to_streamed_response_wrapper(
            object.upload,
        )

# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import httpx
import pytest
from respx import MockRouter

from lm_raindrop import Raindrop, AsyncRaindrop
from tests.utils import assert_matches_type
from lm_raindrop.types import ObjectDeleteResponse, ObjectUploadResponse
from lm_raindrop._response import (
    BinaryAPIResponse,
    AsyncBinaryAPIResponse,
    StreamedBinaryAPIResponse,
    AsyncStreamedBinaryAPIResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestObject:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_delete(self, client: Raindrop) -> None:
        object_ = client.object.delete(
            key="key",
            bucket="bucket",
        )
        assert_matches_type(ObjectDeleteResponse, object_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_delete(self, client: Raindrop) -> None:
        response = client.object.with_raw_response.delete(
            key="key",
            bucket="bucket",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        object_ = response.parse()
        assert_matches_type(ObjectDeleteResponse, object_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_delete(self, client: Raindrop) -> None:
        with client.object.with_streaming_response.delete(
            key="key",
            bucket="bucket",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            object_ = response.parse()
            assert_matches_type(ObjectDeleteResponse, object_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_delete(self, client: Raindrop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bucket` but received ''"):
            client.object.with_raw_response.delete(
                key="key",
                bucket="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `key` but received ''"):
            client.object.with_raw_response.delete(
                key="",
                bucket="bucket",
            )

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_download(self, client: Raindrop, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/object/bucket/key").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        object_ = client.object.download(
            key="key",
            bucket="bucket",
        )
        assert object_.is_closed
        assert object_.json() == {"foo": "bar"}
        assert cast(Any, object_.is_closed) is True
        assert isinstance(object_, BinaryAPIResponse)

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_download(self, client: Raindrop, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/object/bucket/key").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        object_ = client.object.with_raw_response.download(
            key="key",
            bucket="bucket",
        )

        assert object_.is_closed is True
        assert object_.http_request.headers.get("X-Stainless-Lang") == "python"
        assert object_.json() == {"foo": "bar"}
        assert isinstance(object_, BinaryAPIResponse)

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_download(self, client: Raindrop, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/object/bucket/key").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.object.with_streaming_response.download(
            key="key",
            bucket="bucket",
        ) as object_:
            assert not object_.is_closed
            assert object_.http_request.headers.get("X-Stainless-Lang") == "python"

            assert object_.json() == {"foo": "bar"}
            assert cast(Any, object_.is_closed) is True
            assert isinstance(object_, StreamedBinaryAPIResponse)

        assert cast(Any, object_.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_download(self, client: Raindrop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bucket` but received ''"):
            client.object.with_raw_response.download(
                key="key",
                bucket="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `key` but received ''"):
            client.object.with_raw_response.download(
                key="",
                bucket="bucket",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_upload(self, client: Raindrop) -> None:
        object_ = client.object.upload(
            key="key",
            bucket="bucket",
            body=b"raw file contents",
        )
        assert_matches_type(ObjectUploadResponse, object_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_upload(self, client: Raindrop) -> None:
        response = client.object.with_raw_response.upload(
            key="key",
            bucket="bucket",
            body=b"raw file contents",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        object_ = response.parse()
        assert_matches_type(ObjectUploadResponse, object_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_upload(self, client: Raindrop) -> None:
        with client.object.with_streaming_response.upload(
            key="key",
            bucket="bucket",
            body=b"raw file contents",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            object_ = response.parse()
            assert_matches_type(ObjectUploadResponse, object_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_upload(self, client: Raindrop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bucket` but received ''"):
            client.object.with_raw_response.upload(
                key="key",
                bucket="",
                body=b"raw file contents",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `key` but received ''"):
            client.object.with_raw_response.upload(
                key="",
                bucket="bucket",
                body=b"raw file contents",
            )


class TestAsyncObject:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_delete(self, async_client: AsyncRaindrop) -> None:
        object_ = await async_client.object.delete(
            key="key",
            bucket="bucket",
        )
        assert_matches_type(ObjectDeleteResponse, object_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncRaindrop) -> None:
        response = await async_client.object.with_raw_response.delete(
            key="key",
            bucket="bucket",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        object_ = await response.parse()
        assert_matches_type(ObjectDeleteResponse, object_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncRaindrop) -> None:
        async with async_client.object.with_streaming_response.delete(
            key="key",
            bucket="bucket",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            object_ = await response.parse()
            assert_matches_type(ObjectDeleteResponse, object_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncRaindrop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bucket` but received ''"):
            await async_client.object.with_raw_response.delete(
                key="key",
                bucket="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `key` but received ''"):
            await async_client.object.with_raw_response.delete(
                key="",
                bucket="bucket",
            )

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_download(self, async_client: AsyncRaindrop, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/object/bucket/key").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        object_ = await async_client.object.download(
            key="key",
            bucket="bucket",
        )
        assert object_.is_closed
        assert await object_.json() == {"foo": "bar"}
        assert cast(Any, object_.is_closed) is True
        assert isinstance(object_, AsyncBinaryAPIResponse)

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_download(self, async_client: AsyncRaindrop, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/object/bucket/key").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        object_ = await async_client.object.with_raw_response.download(
            key="key",
            bucket="bucket",
        )

        assert object_.is_closed is True
        assert object_.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await object_.json() == {"foo": "bar"}
        assert isinstance(object_, AsyncBinaryAPIResponse)

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_download(self, async_client: AsyncRaindrop, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/object/bucket/key").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.object.with_streaming_response.download(
            key="key",
            bucket="bucket",
        ) as object_:
            assert not object_.is_closed
            assert object_.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await object_.json() == {"foo": "bar"}
            assert cast(Any, object_.is_closed) is True
            assert isinstance(object_, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, object_.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_download(self, async_client: AsyncRaindrop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bucket` but received ''"):
            await async_client.object.with_raw_response.download(
                key="key",
                bucket="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `key` but received ''"):
            await async_client.object.with_raw_response.download(
                key="",
                bucket="bucket",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_upload(self, async_client: AsyncRaindrop) -> None:
        object_ = await async_client.object.upload(
            key="key",
            bucket="bucket",
            body=b"raw file contents",
        )
        assert_matches_type(ObjectUploadResponse, object_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_upload(self, async_client: AsyncRaindrop) -> None:
        response = await async_client.object.with_raw_response.upload(
            key="key",
            bucket="bucket",
            body=b"raw file contents",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        object_ = await response.parse()
        assert_matches_type(ObjectUploadResponse, object_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_upload(self, async_client: AsyncRaindrop) -> None:
        async with async_client.object.with_streaming_response.upload(
            key="key",
            bucket="bucket",
            body=b"raw file contents",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            object_ = await response.parse()
            assert_matches_type(ObjectUploadResponse, object_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_upload(self, async_client: AsyncRaindrop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `bucket` but received ''"):
            await async_client.object.with_raw_response.upload(
                key="key",
                bucket="",
                body=b"raw file contents",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `key` but received ''"):
            await async_client.object.with_raw_response.upload(
                key="",
                bucket="bucket",
                body=b"raw file contents",
            )

# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from raindrop import Raindrop, AsyncRaindrop
from tests.utils import assert_matches_type
from raindrop.types import SearchResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSearch:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_get_results(self, client: Raindrop) -> None:
        search = client.search.get_results(
            request_id="request_id",
        )
        assert_matches_type(SearchResponse, search, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_get_results_with_all_params(self, client: Raindrop) -> None:
        search = client.search.get_results(
            request_id="request_id",
            page=0,
            page_size=0,
        )
        assert_matches_type(SearchResponse, search, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_get_results(self, client: Raindrop) -> None:
        response = client.search.with_raw_response.get_results(
            request_id="request_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        search = response.parse()
        assert_matches_type(SearchResponse, search, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_get_results(self, client: Raindrop) -> None:
        with client.search.with_streaming_response.get_results(
            request_id="request_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            search = response.parse()
            assert_matches_type(SearchResponse, search, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_perform(self, client: Raindrop) -> None:
        search = client.search.perform(
            input="input",
            request_id="request_id",
        )
        assert_matches_type(SearchResponse, search, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_perform_with_all_params(self, client: Raindrop) -> None:
        search = client.search.perform(
            input="input",
            request_id="request_id",
            bucket_ids=["string"],
        )
        assert_matches_type(SearchResponse, search, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_perform(self, client: Raindrop) -> None:
        response = client.search.with_raw_response.perform(
            input="input",
            request_id="request_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        search = response.parse()
        assert_matches_type(SearchResponse, search, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_perform(self, client: Raindrop) -> None:
        with client.search.with_streaming_response.perform(
            input="input",
            request_id="request_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            search = response.parse()
            assert_matches_type(SearchResponse, search, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncSearch:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_get_results(self, async_client: AsyncRaindrop) -> None:
        search = await async_client.search.get_results(
            request_id="request_id",
        )
        assert_matches_type(SearchResponse, search, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_get_results_with_all_params(self, async_client: AsyncRaindrop) -> None:
        search = await async_client.search.get_results(
            request_id="request_id",
            page=0,
            page_size=0,
        )
        assert_matches_type(SearchResponse, search, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_get_results(self, async_client: AsyncRaindrop) -> None:
        response = await async_client.search.with_raw_response.get_results(
            request_id="request_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        search = await response.parse()
        assert_matches_type(SearchResponse, search, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_get_results(self, async_client: AsyncRaindrop) -> None:
        async with async_client.search.with_streaming_response.get_results(
            request_id="request_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            search = await response.parse()
            assert_matches_type(SearchResponse, search, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_perform(self, async_client: AsyncRaindrop) -> None:
        search = await async_client.search.perform(
            input="input",
            request_id="request_id",
        )
        assert_matches_type(SearchResponse, search, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_perform_with_all_params(self, async_client: AsyncRaindrop) -> None:
        search = await async_client.search.perform(
            input="input",
            request_id="request_id",
            bucket_ids=["string"],
        )
        assert_matches_type(SearchResponse, search, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_perform(self, async_client: AsyncRaindrop) -> None:
        response = await async_client.search.with_raw_response.perform(
            input="input",
            request_id="request_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        search = await response.parse()
        assert_matches_type(SearchResponse, search, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_perform(self, async_client: AsyncRaindrop) -> None:
        async with async_client.search.with_streaming_response.perform(
            input="input",
            request_id="request_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            search = await response.parse()
            assert_matches_type(SearchResponse, search, path=["response"])

        assert cast(Any, response.is_closed) is True

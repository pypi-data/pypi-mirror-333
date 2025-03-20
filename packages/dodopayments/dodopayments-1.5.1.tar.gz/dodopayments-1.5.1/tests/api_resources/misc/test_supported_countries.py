# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from dodopayments import DodoPayments, AsyncDodoPayments
from dodopayments.types.misc import SupportedCountryListResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSupportedCountries:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_list(self, client: DodoPayments) -> None:
        supported_country = client.misc.supported_countries.list()
        assert_matches_type(SupportedCountryListResponse, supported_country, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: DodoPayments) -> None:
        response = client.misc.supported_countries.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        supported_country = response.parse()
        assert_matches_type(SupportedCountryListResponse, supported_country, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: DodoPayments) -> None:
        with client.misc.supported_countries.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            supported_country = response.parse()
            assert_matches_type(SupportedCountryListResponse, supported_country, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncSupportedCountries:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_list(self, async_client: AsyncDodoPayments) -> None:
        supported_country = await async_client.misc.supported_countries.list()
        assert_matches_type(SupportedCountryListResponse, supported_country, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncDodoPayments) -> None:
        response = await async_client.misc.supported_countries.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        supported_country = await response.parse()
        assert_matches_type(SupportedCountryListResponse, supported_country, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncDodoPayments) -> None:
        async with async_client.misc.supported_countries.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            supported_country = await response.parse()
            assert_matches_type(SupportedCountryListResponse, supported_country, path=["response"])

        assert cast(Any, response.is_closed) is True

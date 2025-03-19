# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from avido import Avido, AsyncAvido
from avido.types import IngestCreateResponse
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestIngest:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: Avido) -> None:
        ingest = client.ingest.create(
            events=[
                {
                    "timestamp": "2025-01-01T12:00:00Z",
                    "type": "trace",
                },
                {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "model_id": "gpt-4o-2024-08-06",
                    "timestamp": "2025-01-01T12:01:00Z",
                    "trace_id": "123e4567-e89b-12d3-a456-426614174000",
                    "type": "llm",
                },
            ],
        )
        assert_matches_type(IngestCreateResponse, ingest, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: Avido) -> None:
        response = client.ingest.with_raw_response.create(
            events=[
                {
                    "timestamp": "2025-01-01T12:00:00Z",
                    "type": "trace",
                },
                {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "model_id": "gpt-4o-2024-08-06",
                    "timestamp": "2025-01-01T12:01:00Z",
                    "trace_id": "123e4567-e89b-12d3-a456-426614174000",
                    "type": "llm",
                },
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        ingest = response.parse()
        assert_matches_type(IngestCreateResponse, ingest, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: Avido) -> None:
        with client.ingest.with_streaming_response.create(
            events=[
                {
                    "timestamp": "2025-01-01T12:00:00Z",
                    "type": "trace",
                },
                {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "model_id": "gpt-4o-2024-08-06",
                    "timestamp": "2025-01-01T12:01:00Z",
                    "trace_id": "123e4567-e89b-12d3-a456-426614174000",
                    "type": "llm",
                },
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            ingest = response.parse()
            assert_matches_type(IngestCreateResponse, ingest, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncIngest:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncAvido) -> None:
        ingest = await async_client.ingest.create(
            events=[
                {
                    "timestamp": "2025-01-01T12:00:00Z",
                    "type": "trace",
                },
                {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "model_id": "gpt-4o-2024-08-06",
                    "timestamp": "2025-01-01T12:01:00Z",
                    "trace_id": "123e4567-e89b-12d3-a456-426614174000",
                    "type": "llm",
                },
            ],
        )
        assert_matches_type(IngestCreateResponse, ingest, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncAvido) -> None:
        response = await async_client.ingest.with_raw_response.create(
            events=[
                {
                    "timestamp": "2025-01-01T12:00:00Z",
                    "type": "trace",
                },
                {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "model_id": "gpt-4o-2024-08-06",
                    "timestamp": "2025-01-01T12:01:00Z",
                    "trace_id": "123e4567-e89b-12d3-a456-426614174000",
                    "type": "llm",
                },
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        ingest = await response.parse()
        assert_matches_type(IngestCreateResponse, ingest, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncAvido) -> None:
        async with async_client.ingest.with_streaming_response.create(
            events=[
                {
                    "timestamp": "2025-01-01T12:00:00Z",
                    "type": "trace",
                },
                {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "model_id": "gpt-4o-2024-08-06",
                    "timestamp": "2025-01-01T12:01:00Z",
                    "trace_id": "123e4567-e89b-12d3-a456-426614174000",
                    "type": "llm",
                },
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            ingest = await response.parse()
            assert_matches_type(IngestCreateResponse, ingest, path=["response"])

        assert cast(Any, response.is_closed) is True

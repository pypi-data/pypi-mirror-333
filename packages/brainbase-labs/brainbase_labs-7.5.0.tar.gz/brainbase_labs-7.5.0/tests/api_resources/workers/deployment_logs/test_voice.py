# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from brainbase_labs import BrainbaseLabs, AsyncBrainbaseLabs
from brainbase_labs.types.shared import Log
from brainbase_labs.types.workers.deployment_logs import VoiceListResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestVoice:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: BrainbaseLabs) -> None:
        voice = client.workers.deployment_logs.voice.retrieve(
            log_id="logId",
            worker_id="workerId",
        )
        assert_matches_type(Log, voice, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: BrainbaseLabs) -> None:
        response = client.workers.deployment_logs.voice.with_raw_response.retrieve(
            log_id="logId",
            worker_id="workerId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        voice = response.parse()
        assert_matches_type(Log, voice, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: BrainbaseLabs) -> None:
        with client.workers.deployment_logs.voice.with_streaming_response.retrieve(
            log_id="logId",
            worker_id="workerId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            voice = response.parse()
            assert_matches_type(Log, voice, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: BrainbaseLabs) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `worker_id` but received ''"):
            client.workers.deployment_logs.voice.with_raw_response.retrieve(
                log_id="logId",
                worker_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `log_id` but received ''"):
            client.workers.deployment_logs.voice.with_raw_response.retrieve(
                log_id="",
                worker_id="workerId",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: BrainbaseLabs) -> None:
        voice = client.workers.deployment_logs.voice.list(
            worker_id="workerId",
        )
        assert_matches_type(VoiceListResponse, voice, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_with_all_params(self, client: BrainbaseLabs) -> None:
        voice = client.workers.deployment_logs.voice.list(
            worker_id="workerId",
            deployment_id="deploymentId",
            flow_id="flowId",
        )
        assert_matches_type(VoiceListResponse, voice, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: BrainbaseLabs) -> None:
        response = client.workers.deployment_logs.voice.with_raw_response.list(
            worker_id="workerId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        voice = response.parse()
        assert_matches_type(VoiceListResponse, voice, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: BrainbaseLabs) -> None:
        with client.workers.deployment_logs.voice.with_streaming_response.list(
            worker_id="workerId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            voice = response.parse()
            assert_matches_type(VoiceListResponse, voice, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_list(self, client: BrainbaseLabs) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `worker_id` but received ''"):
            client.workers.deployment_logs.voice.with_raw_response.list(
                worker_id="",
            )


class TestAsyncVoice:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncBrainbaseLabs) -> None:
        voice = await async_client.workers.deployment_logs.voice.retrieve(
            log_id="logId",
            worker_id="workerId",
        )
        assert_matches_type(Log, voice, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncBrainbaseLabs) -> None:
        response = await async_client.workers.deployment_logs.voice.with_raw_response.retrieve(
            log_id="logId",
            worker_id="workerId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        voice = await response.parse()
        assert_matches_type(Log, voice, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncBrainbaseLabs) -> None:
        async with async_client.workers.deployment_logs.voice.with_streaming_response.retrieve(
            log_id="logId",
            worker_id="workerId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            voice = await response.parse()
            assert_matches_type(Log, voice, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncBrainbaseLabs) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `worker_id` but received ''"):
            await async_client.workers.deployment_logs.voice.with_raw_response.retrieve(
                log_id="logId",
                worker_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `log_id` but received ''"):
            await async_client.workers.deployment_logs.voice.with_raw_response.retrieve(
                log_id="",
                worker_id="workerId",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncBrainbaseLabs) -> None:
        voice = await async_client.workers.deployment_logs.voice.list(
            worker_id="workerId",
        )
        assert_matches_type(VoiceListResponse, voice, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncBrainbaseLabs) -> None:
        voice = await async_client.workers.deployment_logs.voice.list(
            worker_id="workerId",
            deployment_id="deploymentId",
            flow_id="flowId",
        )
        assert_matches_type(VoiceListResponse, voice, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncBrainbaseLabs) -> None:
        response = await async_client.workers.deployment_logs.voice.with_raw_response.list(
            worker_id="workerId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        voice = await response.parse()
        assert_matches_type(VoiceListResponse, voice, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncBrainbaseLabs) -> None:
        async with async_client.workers.deployment_logs.voice.with_streaming_response.list(
            worker_id="workerId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            voice = await response.parse()
            assert_matches_type(VoiceListResponse, voice, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_list(self, async_client: AsyncBrainbaseLabs) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `worker_id` but received ''"):
            await async_client.workers.deployment_logs.voice.with_raw_response.list(
                worker_id="",
            )

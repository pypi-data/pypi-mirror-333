# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from openint import Openint, AsyncOpenint
from tests.utils import assert_matches_type
from openint.types import (
    CreateTokenResponse,
    GetConnectionResponse,
    GetCurrentUserResponse,
    CheckConnectionResponse,
    CreateMagicLinkResponse,
    ListConnectionsResponse,
    ListConnectionConfigsResponse,
)
from openint.pagination import SyncOffsetPagination, AsyncOffsetPagination

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestClient:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_check_connection(self, client: Openint) -> None:
        client_ = client.check_connection(
            "conn_",
        )
        assert_matches_type(CheckConnectionResponse, client_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_check_connection(self, client: Openint) -> None:
        response = client.with_raw_response.check_connection(
            "conn_",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client_ = response.parse()
        assert_matches_type(CheckConnectionResponse, client_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_check_connection(self, client: Openint) -> None:
        with client.with_streaming_response.check_connection(
            "conn_",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client_ = response.parse()
            assert_matches_type(CheckConnectionResponse, client_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_check_connection(self, client: Openint) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.with_raw_response.check_connection(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_create_magic_link(self, client: Openint) -> None:
        client_ = client.create_magic_link(
            customer_id="customer_id",
        )
        assert_matches_type(CreateMagicLinkResponse, client_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_magic_link_with_all_params(self, client: Openint) -> None:
        client_ = client.create_magic_link(
            customer_id="customer_id",
            connection_id="conn_",
            connector_names=["aircall"],
            redirect_url="redirect_url",
            theme="light",
            validity_in_seconds=0,
            view="manage",
        )
        assert_matches_type(CreateMagicLinkResponse, client_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create_magic_link(self, client: Openint) -> None:
        response = client.with_raw_response.create_magic_link(
            customer_id="customer_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client_ = response.parse()
        assert_matches_type(CreateMagicLinkResponse, client_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create_magic_link(self, client: Openint) -> None:
        with client.with_streaming_response.create_magic_link(
            customer_id="customer_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client_ = response.parse()
            assert_matches_type(CreateMagicLinkResponse, client_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_create_magic_link(self, client: Openint) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `customer_id` but received ''"):
            client.with_raw_response.create_magic_link(
                customer_id="",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_create_token(self, client: Openint) -> None:
        client_ = client.create_token(
            customer_id="customer_id",
        )
        assert_matches_type(CreateTokenResponse, client_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_token_with_all_params(self, client: Openint) -> None:
        client_ = client.create_token(
            customer_id="customer_id",
            validity_in_seconds=1,
        )
        assert_matches_type(CreateTokenResponse, client_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create_token(self, client: Openint) -> None:
        response = client.with_raw_response.create_token(
            customer_id="customer_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client_ = response.parse()
        assert_matches_type(CreateTokenResponse, client_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create_token(self, client: Openint) -> None:
        with client.with_streaming_response.create_token(
            customer_id="customer_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client_ = response.parse()
            assert_matches_type(CreateTokenResponse, client_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_create_token(self, client: Openint) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `customer_id` but received ''"):
            client.with_raw_response.create_token(
                customer_id="",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_get_connection(self, client: Openint) -> None:
        client_ = client.get_connection(
            id="conn_",
        )
        assert_matches_type(GetConnectionResponse, client_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_get_connection_with_all_params(self, client: Openint) -> None:
        client_ = client.get_connection(
            id="conn_",
            expand=["connector"],
            include_secrets="none",
            refresh_policy="none",
        )
        assert_matches_type(GetConnectionResponse, client_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_get_connection(self, client: Openint) -> None:
        response = client.with_raw_response.get_connection(
            id="conn_",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client_ = response.parse()
        assert_matches_type(GetConnectionResponse, client_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_get_connection(self, client: Openint) -> None:
        with client.with_streaming_response.get_connection(
            id="conn_",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client_ = response.parse()
            assert_matches_type(GetConnectionResponse, client_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_get_connection(self, client: Openint) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.with_raw_response.get_connection(
                id="",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_get_current_user(self, client: Openint) -> None:
        client_ = client.get_current_user()
        assert_matches_type(GetCurrentUserResponse, client_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_get_current_user(self, client: Openint) -> None:
        response = client.with_raw_response.get_current_user()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client_ = response.parse()
        assert_matches_type(GetCurrentUserResponse, client_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_get_current_user(self, client: Openint) -> None:
        with client.with_streaming_response.get_current_user() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client_ = response.parse()
            assert_matches_type(GetCurrentUserResponse, client_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_list_connection_configs(self, client: Openint) -> None:
        client_ = client.list_connection_configs()
        assert_matches_type(SyncOffsetPagination[ListConnectionConfigsResponse], client_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_connection_configs_with_all_params(self, client: Openint) -> None:
        client_ = client.list_connection_configs(
            connector_name="aircall",
            expand="expand",
            limit=0,
            offset=0,
        )
        assert_matches_type(SyncOffsetPagination[ListConnectionConfigsResponse], client_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list_connection_configs(self, client: Openint) -> None:
        response = client.with_raw_response.list_connection_configs()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client_ = response.parse()
        assert_matches_type(SyncOffsetPagination[ListConnectionConfigsResponse], client_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list_connection_configs(self, client: Openint) -> None:
        with client.with_streaming_response.list_connection_configs() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client_ = response.parse()
            assert_matches_type(SyncOffsetPagination[ListConnectionConfigsResponse], client_, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_list_connections(self, client: Openint) -> None:
        client_ = client.list_connections()
        assert_matches_type(SyncOffsetPagination[ListConnectionsResponse], client_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_connections_with_all_params(self, client: Openint) -> None:
        client_ = client.list_connections(
            connector_config_id="ccfg_",
            connector_name="aircall",
            customer_id="customer_id",
            expand=["connector"],
            include_secrets="none",
            limit=0,
            offset=0,
        )
        assert_matches_type(SyncOffsetPagination[ListConnectionsResponse], client_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list_connections(self, client: Openint) -> None:
        response = client.with_raw_response.list_connections()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client_ = response.parse()
        assert_matches_type(SyncOffsetPagination[ListConnectionsResponse], client_, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list_connections(self, client: Openint) -> None:
        with client.with_streaming_response.list_connections() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client_ = response.parse()
            assert_matches_type(SyncOffsetPagination[ListConnectionsResponse], client_, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncClient:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_check_connection(self, async_client: AsyncOpenint) -> None:
        client = await async_client.check_connection(
            "conn_",
        )
        assert_matches_type(CheckConnectionResponse, client, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_check_connection(self, async_client: AsyncOpenint) -> None:
        response = await async_client.with_raw_response.check_connection(
            "conn_",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client = await response.parse()
        assert_matches_type(CheckConnectionResponse, client, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_check_connection(self, async_client: AsyncOpenint) -> None:
        async with async_client.with_streaming_response.check_connection(
            "conn_",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client = await response.parse()
            assert_matches_type(CheckConnectionResponse, client, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_check_connection(self, async_client: AsyncOpenint) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.with_raw_response.check_connection(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_magic_link(self, async_client: AsyncOpenint) -> None:
        client = await async_client.create_magic_link(
            customer_id="customer_id",
        )
        assert_matches_type(CreateMagicLinkResponse, client, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_magic_link_with_all_params(self, async_client: AsyncOpenint) -> None:
        client = await async_client.create_magic_link(
            customer_id="customer_id",
            connection_id="conn_",
            connector_names=["aircall"],
            redirect_url="redirect_url",
            theme="light",
            validity_in_seconds=0,
            view="manage",
        )
        assert_matches_type(CreateMagicLinkResponse, client, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create_magic_link(self, async_client: AsyncOpenint) -> None:
        response = await async_client.with_raw_response.create_magic_link(
            customer_id="customer_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client = await response.parse()
        assert_matches_type(CreateMagicLinkResponse, client, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create_magic_link(self, async_client: AsyncOpenint) -> None:
        async with async_client.with_streaming_response.create_magic_link(
            customer_id="customer_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client = await response.parse()
            assert_matches_type(CreateMagicLinkResponse, client, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_create_magic_link(self, async_client: AsyncOpenint) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `customer_id` but received ''"):
            await async_client.with_raw_response.create_magic_link(
                customer_id="",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_token(self, async_client: AsyncOpenint) -> None:
        client = await async_client.create_token(
            customer_id="customer_id",
        )
        assert_matches_type(CreateTokenResponse, client, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_token_with_all_params(self, async_client: AsyncOpenint) -> None:
        client = await async_client.create_token(
            customer_id="customer_id",
            validity_in_seconds=1,
        )
        assert_matches_type(CreateTokenResponse, client, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create_token(self, async_client: AsyncOpenint) -> None:
        response = await async_client.with_raw_response.create_token(
            customer_id="customer_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client = await response.parse()
        assert_matches_type(CreateTokenResponse, client, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create_token(self, async_client: AsyncOpenint) -> None:
        async with async_client.with_streaming_response.create_token(
            customer_id="customer_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client = await response.parse()
            assert_matches_type(CreateTokenResponse, client, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_create_token(self, async_client: AsyncOpenint) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `customer_id` but received ''"):
            await async_client.with_raw_response.create_token(
                customer_id="",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_get_connection(self, async_client: AsyncOpenint) -> None:
        client = await async_client.get_connection(
            id="conn_",
        )
        assert_matches_type(GetConnectionResponse, client, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_get_connection_with_all_params(self, async_client: AsyncOpenint) -> None:
        client = await async_client.get_connection(
            id="conn_",
            expand=["connector"],
            include_secrets="none",
            refresh_policy="none",
        )
        assert_matches_type(GetConnectionResponse, client, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_get_connection(self, async_client: AsyncOpenint) -> None:
        response = await async_client.with_raw_response.get_connection(
            id="conn_",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client = await response.parse()
        assert_matches_type(GetConnectionResponse, client, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_get_connection(self, async_client: AsyncOpenint) -> None:
        async with async_client.with_streaming_response.get_connection(
            id="conn_",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client = await response.parse()
            assert_matches_type(GetConnectionResponse, client, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_get_connection(self, async_client: AsyncOpenint) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.with_raw_response.get_connection(
                id="",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_get_current_user(self, async_client: AsyncOpenint) -> None:
        client = await async_client.get_current_user()
        assert_matches_type(GetCurrentUserResponse, client, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_get_current_user(self, async_client: AsyncOpenint) -> None:
        response = await async_client.with_raw_response.get_current_user()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client = await response.parse()
        assert_matches_type(GetCurrentUserResponse, client, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_get_current_user(self, async_client: AsyncOpenint) -> None:
        async with async_client.with_streaming_response.get_current_user() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client = await response.parse()
            assert_matches_type(GetCurrentUserResponse, client, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_connection_configs(self, async_client: AsyncOpenint) -> None:
        client = await async_client.list_connection_configs()
        assert_matches_type(AsyncOffsetPagination[ListConnectionConfigsResponse], client, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_connection_configs_with_all_params(self, async_client: AsyncOpenint) -> None:
        client = await async_client.list_connection_configs(
            connector_name="aircall",
            expand="expand",
            limit=0,
            offset=0,
        )
        assert_matches_type(AsyncOffsetPagination[ListConnectionConfigsResponse], client, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list_connection_configs(self, async_client: AsyncOpenint) -> None:
        response = await async_client.with_raw_response.list_connection_configs()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client = await response.parse()
        assert_matches_type(AsyncOffsetPagination[ListConnectionConfigsResponse], client, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list_connection_configs(self, async_client: AsyncOpenint) -> None:
        async with async_client.with_streaming_response.list_connection_configs() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client = await response.parse()
            assert_matches_type(AsyncOffsetPagination[ListConnectionConfigsResponse], client, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_connections(self, async_client: AsyncOpenint) -> None:
        client = await async_client.list_connections()
        assert_matches_type(AsyncOffsetPagination[ListConnectionsResponse], client, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_connections_with_all_params(self, async_client: AsyncOpenint) -> None:
        client = await async_client.list_connections(
            connector_config_id="ccfg_",
            connector_name="aircall",
            customer_id="customer_id",
            expand=["connector"],
            include_secrets="none",
            limit=0,
            offset=0,
        )
        assert_matches_type(AsyncOffsetPagination[ListConnectionsResponse], client, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list_connections(self, async_client: AsyncOpenint) -> None:
        response = await async_client.with_raw_response.list_connections()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        client = await response.parse()
        assert_matches_type(AsyncOffsetPagination[ListConnectionsResponse], client, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list_connections(self, async_client: AsyncOpenint) -> None:
        async with async_client.with_streaming_response.list_connections() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            client = await response.parse()
            assert_matches_type(AsyncOffsetPagination[ListConnectionsResponse], client, path=["response"])

        assert cast(Any, response.is_closed) is True

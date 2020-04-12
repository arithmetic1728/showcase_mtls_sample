# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from unittest import mock

import grpc
import math
import pytest

from google import auth
from google.api_core import client_options
from google.api_core import future
from google.api_core import grpc_helpers
from google.api_core import operations_v1
from google.auth import credentials
from google.longrunning import operations_pb2
from google.oauth2 import service_account
from google.protobuf import any_pb2 as any  # type: ignore
from google.protobuf import duration_pb2 as duration  # type: ignore
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore
from google.rpc import status_pb2 as status  # type: ignore
from google.showcase_v1beta1.services.echo import EchoClient
from google.showcase_v1beta1.services.echo import pagers
from google.showcase_v1beta1.services.echo import transports
from google.showcase_v1beta1.types import echo as gs_echo


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert EchoClient._get_default_mtls_endpoint(None) == None
    assert EchoClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    assert EchoClient._get_default_mtls_endpoint(api_mtls_endpoint) == api_mtls_endpoint
    assert EchoClient._get_default_mtls_endpoint(sandbox_endpoint) == sandbox_mtls_endpoint
    assert EchoClient._get_default_mtls_endpoint(sandbox_mtls_endpoint) == sandbox_mtls_endpoint
    assert EchoClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


def test_echo_client_from_service_account_file():
    creds = credentials.AnonymousCredentials()
    with mock.patch.object(service_account.Credentials, 'from_service_account_file') as factory:
        factory.return_value = creds
        client = EchoClient.from_service_account_file("dummy/file/path.json")
        assert client._transport._credentials == creds

        client = EchoClient.from_service_account_json("dummy/file/path.json")
        assert client._transport._credentials == creds

        assert client._transport._host == 'localhost:7469'


def test_echo_client_client_options():
    # Check that if channel is provided we won't create a new one.
    with mock.patch('google.showcase_v1beta1.services.echo.EchoClient.get_transport_class') as gtc:
        transport = transports.EchoGrpcTransport(
            credentials=credentials.AnonymousCredentials()
        )
        client = EchoClient(transport=transport)
        gtc.assert_not_called()

    # Check mTLS is not triggered with empty client options.
    options = client_options.ClientOptions()
    with mock.patch('google.showcase_v1beta1.services.echo.EchoClient.get_transport_class') as gtc:
        transport = gtc.return_value = mock.MagicMock()
        client = EchoClient(client_options=options)
        transport.assert_called_once_with(
            credentials=None,
            host=client.DEFAULT_ENDPOINT,
        )

    # Check mTLS is not triggered if api_endpoint is provided but
    # client_cert_source is None.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch('google.showcase_v1beta1.services.echo.transports.EchoGrpcTransport.__init__') as grpc_transport:
        grpc_transport.return_value = None
        client = EchoClient(client_options=options)
        grpc_transport.assert_called_once_with(
            api_mtls_endpoint=None,
            client_cert_source=None,
            credentials=None,
            host="squid.clam.whelk",
        )

    # Check mTLS is triggered if client_cert_source is provided.
    options = client_options.ClientOptions(
        client_cert_source=client_cert_source_callback
    )
    with mock.patch('google.showcase_v1beta1.services.echo.transports.EchoGrpcTransport.__init__') as grpc_transport:
        grpc_transport.return_value = None
        client = EchoClient(client_options=options)
        grpc_transport.assert_called_once_with(
            api_mtls_endpoint=client.DEFAULT_MTLS_ENDPOINT,
            client_cert_source=client_cert_source_callback,
            credentials=None,
            host=client.DEFAULT_ENDPOINT,
        )

    # Check mTLS is triggered if api_endpoint and client_cert_source are provided.
    options = client_options.ClientOptions(
        api_endpoint="squid.clam.whelk",
        client_cert_source=client_cert_source_callback
    )
    with mock.patch('google.showcase_v1beta1.services.echo.transports.EchoGrpcTransport.__init__') as grpc_transport:
        grpc_transport.return_value = None
        client = EchoClient(client_options=options)
        grpc_transport.assert_called_once_with(
            api_mtls_endpoint="squid.clam.whelk",
            client_cert_source=client_cert_source_callback,
            credentials=None,
            host="squid.clam.whelk",
        )

def test_echo_client_client_options_from_dict():
    with mock.patch('google.showcase_v1beta1.services.echo.transports.EchoGrpcTransport.__init__') as grpc_transport:
        grpc_transport.return_value = None
        client = EchoClient(
            client_options={'api_endpoint': 'squid.clam.whelk'}
        )
        grpc_transport.assert_called_once_with(
            api_mtls_endpoint=None,
            client_cert_source=None,
            credentials=None,
            host="squid.clam.whelk",
        )


def test_echo(transport: str = 'grpc'):
    client = EchoClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = gs_echo.EchoRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.echo),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = gs_echo.EchoResponse(
            content='content_value',
        )

        response = client.echo(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, gs_echo.EchoResponse)
    assert response.content == 'content_value'


def test_expand(transport: str = 'grpc'):
    client = EchoClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = gs_echo.ExpandRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.expand),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = iter([gs_echo.EchoResponse()])

        response = client.expand(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    for message in response:
        assert isinstance(message, gs_echo.EchoResponse)


def test_expand_flattened():
    client = EchoClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.expand),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = iter([gs_echo.EchoResponse()])

        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = client.expand(
            content='content_value',
            error=status.Status(code=411),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0].content == 'content_value'
        assert args[0].error == status.Status(code=411)


def test_expand_flattened_error():
    client = EchoClient(
        credentials=credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.expand(
            gs_echo.ExpandRequest(),
            content='content_value',
            error=status.Status(code=411),
        )


def test_collect(transport: str = 'grpc'):
    client = EchoClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = gs_echo.EchoRequest()

    requests = [request]

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.collect),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = gs_echo.EchoResponse(
            content='content_value',
        )

        response = client.collect(iter(requests))

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert next(args[0]) == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, gs_echo.EchoResponse)
    assert response.content == 'content_value'


def test_chat(transport: str = 'grpc'):
    client = EchoClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = gs_echo.EchoRequest()

    requests = [request]

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.chat),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = iter([gs_echo.EchoResponse()])

        response = client.chat(iter(requests))

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert next(args[0]) == request

    # Establish that the response is the type that we expect.
    for message in response:
        assert isinstance(message, gs_echo.EchoResponse)


def test_paged_expand(transport: str = 'grpc'):
    client = EchoClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = gs_echo.PagedExpandRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.paged_expand),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = gs_echo.PagedExpandResponse(
            next_page_token='next_page_token_value',
        )

        response = client.paged_expand(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.PagedExpandPager)
    assert response.next_page_token == 'next_page_token_value'


def test_paged_expand_pager():
    client = EchoClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.paged_expand),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            gs_echo.PagedExpandResponse(
                responses=[
                    gs_echo.EchoResponse(),
                    gs_echo.EchoResponse(),
                    gs_echo.EchoResponse(),
                ],
                next_page_token='abc',
            ),
            gs_echo.PagedExpandResponse(
                responses=[],
                next_page_token='def',
            ),
            gs_echo.PagedExpandResponse(
                responses=[
                    gs_echo.EchoResponse(),
                ],
                next_page_token='ghi',
            ),
            gs_echo.PagedExpandResponse(
                responses=[
                    gs_echo.EchoResponse(),
                    gs_echo.EchoResponse(),
                ],
            ),
            RuntimeError,
        )
        results = [i for i in client.paged_expand(
            request={},
        )]
        assert len(results) == 6
        assert all(isinstance(i, gs_echo.EchoResponse)
                   for i in results)

def test_paged_expand_pages():
    client = EchoClient(
        credentials=credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.paged_expand),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            gs_echo.PagedExpandResponse(
                responses=[
                    gs_echo.EchoResponse(),
                    gs_echo.EchoResponse(),
                    gs_echo.EchoResponse(),
                ],
                next_page_token='abc',
            ),
            gs_echo.PagedExpandResponse(
                responses=[],
                next_page_token='def',
            ),
            gs_echo.PagedExpandResponse(
                responses=[
                    gs_echo.EchoResponse(),
                ],
                next_page_token='ghi',
            ),
            gs_echo.PagedExpandResponse(
                responses=[
                    gs_echo.EchoResponse(),
                    gs_echo.EchoResponse(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.paged_expand(request={}).pages)
        for page, token in zip(pages, ['abc','def','ghi', '']):
            assert page.raw_page.next_page_token == token


def test_wait(transport: str = 'grpc'):
    client = EchoClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = gs_echo.WaitRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.wait),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/spam')

        response = client.wait(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_block(transport: str = 'grpc'):
    client = EchoClient(
        credentials=credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = gs_echo.BlockRequest()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client._transport.block),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = gs_echo.BlockResponse(
            content='content_value',
        )

        response = client.block(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]

        assert args[0] == request

    # Establish that the response is the type that we expect.
    assert isinstance(response, gs_echo.BlockResponse)
    assert response.content == 'content_value'


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.EchoGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = EchoClient(
            credentials=credentials.AnonymousCredentials(),
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.EchoGrpcTransport(
        credentials=credentials.AnonymousCredentials(),
    )
    client = EchoClient(transport=transport)
    assert client._transport is transport


def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = EchoClient(
        credentials=credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client._transport,
        transports.EchoGrpcTransport,
    )


def test_echo_base_transport():
    # Instantiate the base transport.
    transport = transports.EchoTransport(
        credentials=credentials.AnonymousCredentials(),
    )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        'echo',
        'expand',
        'collect',
        'chat',
        'paged_expand',
        'wait',
        'block',
        )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    # Additionally, the LRO client (a property) should
    # also raise NotImplementedError
    with pytest.raises(NotImplementedError):
        transport.operations_client


def test_echo_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(auth, 'default') as adc:
        adc.return_value = (credentials.AnonymousCredentials(), None)
        EchoClient()
        adc.assert_called_once_with(scopes=(
        ))


def test_echo_host_no_port():
    client = EchoClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(api_endpoint='localhost'),
        transport='grpc',
    )
    assert client._transport._host == 'localhost:443'


def test_echo_host_with_port():
    client = EchoClient(
        credentials=credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(api_endpoint='localhost:8000'),
        transport='grpc',
    )
    assert client._transport._host == 'localhost:8000'


def test_echo_grpc_transport_channel():
    channel = grpc.insecure_channel('http://localhost/')

    # Check that if channel is provided, mtls endpoint and client_cert_source
    # won't be used.
    callback = mock.MagicMock()
    transport = transports.EchoGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
        api_mtls_endpoint="mtls.squid.clam.whelk",
        client_cert_source=callback,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert not callback.called


@mock.patch("grpc.ssl_channel_credentials", autospec=True)
@mock.patch("google.api_core.grpc_helpers.create_channel", autospec=True)
def test_echo_grpc_transport_channel_mtls_with_client_cert_source(
    grpc_create_channel, grpc_ssl_channel_cred
):
    # Check that if channel is None, but api_mtls_endpoint and client_cert_source
    # are provided, then a mTLS channel will be created.
    mock_cred = mock.Mock()

    mock_ssl_cred = mock.Mock()
    grpc_ssl_channel_cred.return_value = mock_ssl_cred

    mock_grpc_channel = mock.Mock()
    grpc_create_channel.return_value = mock_grpc_channel

    transport = transports.EchoGrpcTransport(
        host="squid.clam.whelk",
        credentials=mock_cred,
        api_mtls_endpoint="mtls.squid.clam.whelk",
        client_cert_source=client_cert_source_callback,
    )
    grpc_ssl_channel_cred.assert_called_once_with(
        certificate_chain=b"cert bytes", private_key=b"key bytes"
    )
    grpc_create_channel.assert_called_once_with(
        "mtls.squid.clam.whelk:443",
        credentials=mock_cred,
        ssl_credentials=mock_ssl_cred,
        scopes=(
        ),
    )
    assert transport.grpc_channel == mock_grpc_channel


@pytest.mark.parametrize(
    "api_mtls_endpoint", ["mtls.squid.clam.whelk", "mtls.squid.clam.whelk:443"]
)
@mock.patch("google.api_core.grpc_helpers.create_channel", autospec=True)
def test_echo_grpc_transport_channel_mtls_with_adc(
    grpc_create_channel, api_mtls_endpoint
):
    # Check that if channel and client_cert_source are None, but api_mtls_endpoint
    # is provided, then a mTLS channel will be created with SSL ADC.
    mock_grpc_channel = mock.Mock()
    grpc_create_channel.return_value = mock_grpc_channel

    # Mock google.auth.transport.grpc.SslCredentials class.
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        mock_cred = mock.Mock()
        transport = transports.EchoGrpcTransport(
            host="squid.clam.whelk",
            credentials=mock_cred,
            api_mtls_endpoint=api_mtls_endpoint,
            client_cert_source=None,
        )
        grpc_create_channel.assert_called_once_with(
            "mtls.squid.clam.whelk:443",
            credentials=mock_cred,
            ssl_credentials=mock_ssl_cred,
            scopes=(
            ),
        )
        assert transport.grpc_channel == mock_grpc_channel


def test_echo_grpc_lro_client():
    client = EchoClient(
        credentials=credentials.AnonymousCredentials(),
        transport='grpc',
    )
    transport = client._transport

    # Ensure that we have a api-core operations client.
    assert isinstance(
        transport.operations_client,
        operations_v1.OperationsClient,
    )

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client

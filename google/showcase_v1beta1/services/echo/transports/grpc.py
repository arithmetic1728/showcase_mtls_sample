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

from typing import Callable, Dict, Tuple

from google.api_core import grpc_helpers   # type: ignore
from google.api_core import operations_v1  # type: ignore
from google.auth import credentials        # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore


import grpc  # type: ignore

from google.longrunning import operations_pb2 as operations  # type: ignore
from google.showcase_v1beta1.types import echo as gs_echo

from .base import EchoTransport


class EchoGrpcTransport(EchoTransport):
    """gRPC backend transport for Echo.

    This service is used showcase the four main types of rpcs -
    unary, server side streaming, client side streaming, and
    bidirectional streaming. This service also exposes methods that
    explicitly implement server delay, and paginated calls. Set the
    'showcase-trailer' metadata key on any method to have the values
    echoed in the response trailers.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """
    def __init__(self, *,
            host: str = 'localhost:7469',
            credentials: credentials.Credentials = None,
            channel: grpc.Channel = None,
            api_mtls_endpoint: str = None,
            client_cert_source: Callable[[], Tuple[bytes, bytes]] = None) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]): The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if ``channel`` is provided.
            channel (Optional[grpc.Channel]): A ``Channel`` instance through
                which to make calls.
            api_mtls_endpoint (Optional[str]): The mutual TLS endpoint. If
                provided, it overrides the ``host`` argument and tries to create
                a mutual TLS channel with client SSL credentials from
                ``client_cert_source`` or applicatin default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]): A
                callback to provide client SSL certificate bytes and private key
                bytes, both in PEM format. It is ignored if ``api_mtls_endpoint``
                is None.

        Raises:
          google.auth.exceptions.MutualTlsChannelError: If mutual TLS transport
              creation failed for any reason.
        """
        if channel:
            # Sanity check: Ensure that channel and credentials are not both
            # provided.
            credentials = False

            # If a channel was explicitly provided, set it.
            self._grpc_channel = channel
        elif api_mtls_endpoint:
            host = api_mtls_endpoint if ":" in api_mtls_endpoint else api_mtls_endpoint + ":443"

            # Create SSL credentials with client_cert_source or application
            # default SSL credentials.
            if client_cert_source:
                cert, key = client_cert_source()
                ssl_credentials = grpc.ssl_channel_credentials(
                    certificate_chain=cert, private_key=key
                )
            else:
                ssl_credentials = SslCredentials().ssl_credentials

            # create a new channel. The provided one is ignored.
            self._grpc_channel = grpc_helpers.create_channel(
                host,
                credentials=credentials,
                ssl_credentials=ssl_credentials,
                scopes=self.AUTH_SCOPES,
            )

        # Run the base constructor.
        super().__init__(host=host, credentials=credentials)
        self._stubs = {}  # type: Dict[str, Callable]

    @classmethod
    def create_channel(cls,
                       host: str = 'localhost:7469',
                       credentials: credentials.Credentials = None,
                       **kwargs) -> grpc.Channel:
        """Create and return a gRPC channel object.
        Args:
            address (Optionsl[str]): The host for the channel to use.
            credentials (Optional[~.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            kwargs (Optional[dict]): Keyword arguments, which are passed to the
                channel creation.
        Returns:
            grpc.Channel: A gRPC channel object.
        """
        return grpc_helpers.create_channel(
            host,
            credentials=credentials,
            scopes=cls.AUTH_SCOPES,
            **kwargs
        )

    @property
    def grpc_channel(self) -> grpc.Channel:
        """Create the channel designed to connect to this service.

        This property caches on the instance; repeated calls return
        the same channel.
        """
        # Sanity check: Only create a new channel if we do not already
        # have one.
        if not hasattr(self, '_grpc_channel'):
            self._grpc_channel = self.create_channel(
                self._host,
                credentials=self._credentials,
            )

        # Return the channel from cache.
        return self._grpc_channel

    @property
    def operations_client(self) -> operations_v1.OperationsClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Sanity check: Only create a new client if we do not already have one.
        if 'operations_client' not in self.__dict__:
            self.__dict__['operations_client'] = operations_v1.OperationsClient(
                self.grpc_channel
            )

        # Return the client from cache.
        return self.__dict__['operations_client']

    @property
    def echo(self) -> Callable[
            [gs_echo.EchoRequest],
            gs_echo.EchoResponse]:
        r"""Return a callable for the echo method over gRPC.

        This method simply echos the request. This method is
        showcases unary rpcs.

        Returns:
            Callable[[~.EchoRequest],
                    ~.EchoResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'echo' not in self._stubs:
            self._stubs['echo'] = self.grpc_channel.unary_unary(
                '/google.showcase.v1beta1.Echo/Echo',
                request_serializer=gs_echo.EchoRequest.serialize,
                response_deserializer=gs_echo.EchoResponse.deserialize,
            )
        return self._stubs['echo']

    @property
    def expand(self) -> Callable[
            [gs_echo.ExpandRequest],
            gs_echo.EchoResponse]:
        r"""Return a callable for the expand method over gRPC.

        This method split the given content into words and
        will pass each word back through the stream. This method
        showcases server-side streaming rpcs.

        Returns:
            Callable[[~.ExpandRequest],
                    ~.EchoResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'expand' not in self._stubs:
            self._stubs['expand'] = self.grpc_channel.unary_stream(
                '/google.showcase.v1beta1.Echo/Expand',
                request_serializer=gs_echo.ExpandRequest.serialize,
                response_deserializer=gs_echo.EchoResponse.deserialize,
            )
        return self._stubs['expand']

    @property
    def collect(self) -> Callable[
            [gs_echo.EchoRequest],
            gs_echo.EchoResponse]:
        r"""Return a callable for the collect method over gRPC.

        This method will collect the words given to it. When
        the stream is closed by the client, this method will
        return the a concatenation of the strings passed to it.
        This method showcases client-side streaming rpcs.

        Returns:
            Callable[[~.EchoRequest],
                    ~.EchoResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'collect' not in self._stubs:
            self._stubs['collect'] = self.grpc_channel.stream_unary(
                '/google.showcase.v1beta1.Echo/Collect',
                request_serializer=gs_echo.EchoRequest.serialize,
                response_deserializer=gs_echo.EchoResponse.deserialize,
            )
        return self._stubs['collect']

    @property
    def chat(self) -> Callable[
            [gs_echo.EchoRequest],
            gs_echo.EchoResponse]:
        r"""Return a callable for the chat method over gRPC.

        This method, upon receiving a request on the stream,
        the same content will be passed  back on the stream.
        This method showcases bidirectional streaming rpcs.

        Returns:
            Callable[[~.EchoRequest],
                    ~.EchoResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'chat' not in self._stubs:
            self._stubs['chat'] = self.grpc_channel.stream_stream(
                '/google.showcase.v1beta1.Echo/Chat',
                request_serializer=gs_echo.EchoRequest.serialize,
                response_deserializer=gs_echo.EchoResponse.deserialize,
            )
        return self._stubs['chat']

    @property
    def paged_expand(self) -> Callable[
            [gs_echo.PagedExpandRequest],
            gs_echo.PagedExpandResponse]:
        r"""Return a callable for the paged expand method over gRPC.

        This is similar to the Expand method but instead of
        returning a stream of expanded words, this method
        returns a paged list of expanded words.

        Returns:
            Callable[[~.PagedExpandRequest],
                    ~.PagedExpandResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'paged_expand' not in self._stubs:
            self._stubs['paged_expand'] = self.grpc_channel.unary_unary(
                '/google.showcase.v1beta1.Echo/PagedExpand',
                request_serializer=gs_echo.PagedExpandRequest.serialize,
                response_deserializer=gs_echo.PagedExpandResponse.deserialize,
            )
        return self._stubs['paged_expand']

    @property
    def wait(self) -> Callable[
            [gs_echo.WaitRequest],
            operations.Operation]:
        r"""Return a callable for the wait method over gRPC.

        This method will wait the requested amount of and
        then return. This method showcases how a client handles
        a request timing out.

        Returns:
            Callable[[~.WaitRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'wait' not in self._stubs:
            self._stubs['wait'] = self.grpc_channel.unary_unary(
                '/google.showcase.v1beta1.Echo/Wait',
                request_serializer=gs_echo.WaitRequest.serialize,
                response_deserializer=operations.Operation.FromString,
            )
        return self._stubs['wait']

    @property
    def block(self) -> Callable[
            [gs_echo.BlockRequest],
            gs_echo.BlockResponse]:
        r"""Return a callable for the block method over gRPC.

        This method will block (wait) for the requested
        amount of time  and then return the response or error.
        This method showcases how a client handles delays or
        retries.

        Returns:
            Callable[[~.BlockRequest],
                    ~.BlockResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'block' not in self._stubs:
            self._stubs['block'] = self.grpc_channel.unary_unary(
                '/google.showcase.v1beta1.Echo/Block',
                request_serializer=gs_echo.BlockRequest.serialize,
                response_deserializer=gs_echo.BlockResponse.deserialize,
            )
        return self._stubs['block']


__all__ = (
    'EchoGrpcTransport',
)

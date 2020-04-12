import os

import pytest
import mock

import google.api_core.client_options as ClientOptions
from google import showcase
from google.auth import credentials
from google.showcase import EchoClient
from google.showcase import IdentityClient

import grpc

dir = os.path.dirname(__file__)
with open(os.path.join(dir, "server.crt"), "rb") as fh:
    cert = fh.read()
with open(os.path.join(dir, "server.key"), "rb") as fh:
    key = fh.read()


def callback():
    return cert, key


client_options = ClientOptions.ClientOptions()
client_options.client_cert_source = callback


def test_sample():
    ssl_credentials = grpc.ssl_channel_credentials(
        root_certificates=cert, certificate_chain=cert, private_key=key
    )

    with mock.patch("grpc.ssl_channel_credentials", autospec=True) as mock_ssl_cred:
        mock_ssl_cred.return_value = ssl_credentials
        client = EchoClient(
            credentials=credentials.AnonymousCredentials(),
            client_options=client_options,
        )
        mock_ssl_cred.assert_called_once_with(certificate_chain=cert, private_key=key)

        response = client.echo(
            showcase.EchoRequest(
                content="The hail in Wales falls mainly on the snails."
            )
        )
        assert response.content == "The hail in Wales falls mainly on the snails."

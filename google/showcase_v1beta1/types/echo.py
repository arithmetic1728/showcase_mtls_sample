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

import proto  # type: ignore


from google.protobuf import duration_pb2 as duration  # type: ignore
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore
from google.rpc import status_pb2 as status  # type: ignore


__protobuf__ = proto.module(
    package='google.showcase.v1beta1',
    manifest={
        'EchoRequest',
        'EchoResponse',
        'ExpandRequest',
        'PagedExpandRequest',
        'PagedExpandResponse',
        'WaitRequest',
        'WaitResponse',
        'WaitMetadata',
        'BlockRequest',
        'BlockResponse',
    },
)


class EchoRequest(proto.Message):
    r"""The request message used for the Echo, Collect and Chat
    methods. If content is set in this message then the request will
    succeed. If status is set in  this message then the status will
    be returned as an error.

    Attributes:
        content (str):
            The content to be echoed by the server.
        error (~.status.Status):
            The error to be thrown by the server.
    """

    content = proto.Field(proto.STRING, number=1)
    error = proto.Field(proto.MESSAGE, number=2,
        message=status.Status,
    )


class EchoResponse(proto.Message):
    r"""The response message for the Echo methods.

    Attributes:
        content (str):
            The content specified in the request.
    """

    content = proto.Field(proto.STRING, number=1)


class ExpandRequest(proto.Message):
    r"""The request message for the Expand method.

    Attributes:
        content (str):
            The content that will be split into words and
            returned on the stream.
        error (~.status.Status):
            The error that is thrown after all words are
            sent on the stream.
    """

    content = proto.Field(proto.STRING, number=1)
    error = proto.Field(proto.MESSAGE, number=2,
        message=status.Status,
    )


class PagedExpandRequest(proto.Message):
    r"""The request for the PagedExpand method.

    Attributes:
        content (str):
            The string to expand.
        page_size (int):
            The amount of words to returned in each page.
        page_token (str):
            The position of the page to be returned.
    """

    content = proto.Field(proto.STRING, number=1)
    page_size = proto.Field(proto.INT32, number=2)
    page_token = proto.Field(proto.STRING, number=3)


class PagedExpandResponse(proto.Message):
    r"""The response for the PagedExpand method.

    Attributes:
        responses (Sequence[~.echo.EchoResponse]):
            The words that were expanded.
        next_page_token (str):
            The next page token.
    """

    @property
    def raw_page(self):
        return self

    responses = proto.RepeatedField(proto.MESSAGE, number=1,
        message=EchoResponse,
    )
    next_page_token = proto.Field(proto.STRING, number=2)


class WaitRequest(proto.Message):
    r"""The request for Wait method.

    Attributes:
        end_time (~.timestamp.Timestamp):
            The time that this operation will complete.
        ttl (~.duration.Duration):
            The duration of this operation.
        error (~.status.Status):
            The error that will be returned by the
            server. If this code is specified to be the OK
            rpc code, an empty response will be returned.
        success (~.echo.WaitResponse):
            The response to be returned on operation
            completion.
    """

    end_time = proto.Field(proto.MESSAGE, number=1,
        message=timestamp.Timestamp,
    )
    ttl = proto.Field(proto.MESSAGE, number=4,
        message=duration.Duration,
    )
    error = proto.Field(proto.MESSAGE, number=2,
        message=status.Status,
    )
    success = proto.Field(proto.MESSAGE, number=3,
        message='WaitResponse',
    )


class WaitResponse(proto.Message):
    r"""The result of the Wait operation.

    Attributes:
        content (str):
            This content of the result.
    """

    content = proto.Field(proto.STRING, number=1)


class WaitMetadata(proto.Message):
    r"""The metadata for Wait operation.

    Attributes:
        end_time (~.timestamp.Timestamp):
            The time that this operation will complete.
    """

    end_time = proto.Field(proto.MESSAGE, number=1,
        message=timestamp.Timestamp,
    )


class BlockRequest(proto.Message):
    r"""The request for Block method.

    Attributes:
        response_delay (~.duration.Duration):
            The amount of time to block before returning
            a response.
        error (~.status.Status):
            The error that will be returned by the
            server. If this code is specified to be the OK
            rpc code, an empty response will be returned.
        success (~.echo.BlockResponse):
            The response to be returned that will signify
            successful method call.
    """

    response_delay = proto.Field(proto.MESSAGE, number=1,
        message=duration.Duration,
    )
    error = proto.Field(proto.MESSAGE, number=2,
        message=status.Status,
    )
    success = proto.Field(proto.MESSAGE, number=3,
        message='BlockResponse',
    )


class BlockResponse(proto.Message):
    r"""The response for Block method.

    Attributes:
        content (str):
            This content can contain anything, the server
            will not depend on a value here.
    """

    content = proto.Field(proto.STRING, number=1)


__all__ = tuple(sorted(__protobuf__.manifest))

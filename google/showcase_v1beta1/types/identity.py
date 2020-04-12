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


from google.protobuf import field_mask_pb2 as field_mask  # type: ignore
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore


__protobuf__ = proto.module(
    package='google.showcase.v1beta1',
    manifest={
        'User',
        'CreateUserRequest',
        'GetUserRequest',
        'UpdateUserRequest',
        'DeleteUserRequest',
        'ListUsersRequest',
        'ListUsersResponse',
    },
)


class User(proto.Message):
    r"""A user.

    Attributes:
        name (str):
            The resource name of the user.
        display_name (str):
            The display\_name of the user.
        email (str):
            The email address of the user.
        create_time (~.timestamp.Timestamp):
            The timestamp at which the user was created.
        update_time (~.timestamp.Timestamp):
            The latest timestamp at which the user was
            updated.
    """

    name = proto.Field(proto.STRING, number=1)
    display_name = proto.Field(proto.STRING, number=2)
    email = proto.Field(proto.STRING, number=3)
    create_time = proto.Field(proto.MESSAGE, number=4,
        message=timestamp.Timestamp,
    )
    update_time = proto.Field(proto.MESSAGE, number=5,
        message=timestamp.Timestamp,
    )


class CreateUserRequest(proto.Message):
    r"""The request message for the
    google.showcase.v1beta1.Identity\CreateUser method.

    Attributes:
        user (~.identity.User):
            The user to create.
    """

    user = proto.Field(proto.MESSAGE, number=1,
        message=User,
    )


class GetUserRequest(proto.Message):
    r"""The request message for the
    google.showcase.v1beta1.Identity\GetUser method.

    Attributes:
        name (str):
            The resource name of the requested user.
    """

    name = proto.Field(proto.STRING, number=1)


class UpdateUserRequest(proto.Message):
    r"""The request message for the
    google.showcase.v1beta1.Identity\UpdateUser method.

    Attributes:
        user (~.identity.User):
            The user to update.
        update_mask (~.field_mask.FieldMask):
            The field mask to determine wich fields are
            to be updated. If empty, the server will assume
            all fields are to be updated.
    """

    user = proto.Field(proto.MESSAGE, number=1,
        message=User,
    )
    update_mask = proto.Field(proto.MESSAGE, number=2,
        message=field_mask.FieldMask,
    )


class DeleteUserRequest(proto.Message):
    r"""The request message for the
    google.showcase.v1beta1.Identity\DeleteUser method.

    Attributes:
        name (str):
            The resource name of the user to delete.
    """

    name = proto.Field(proto.STRING, number=1)


class ListUsersRequest(proto.Message):
    r"""The request message for the
    google.showcase.v1beta1.Identity\ListUsers method.

    Attributes:
        page_size (int):
            The maximum number of users to return. Server
            may return fewer users than requested. If
            unspecified, server will pick an appropriate
            default.
        page_token (str):
            The value of
            google.showcase.v1beta1.ListUsersResponse.next\_page\_token
            returned from the previous call to
            ``google.showcase.v1beta1.Identity\ListUsers`` method.
    """

    page_size = proto.Field(proto.INT32, number=1)
    page_token = proto.Field(proto.STRING, number=2)


class ListUsersResponse(proto.Message):
    r"""The response message for the
    google.showcase.v1beta1.Identity\ListUsers method.

    Attributes:
        users (Sequence[~.identity.User]):
            The list of users.
        next_page_token (str):
            A token to retrieve next page of results. Pass this value in
            ListUsersRequest.page\_token field in the subsequent call to
            ``google.showcase.v1beta1.Message\ListUsers`` method to
            retrieve the next page of results.
    """

    @property
    def raw_page(self):
        return self

    users = proto.RepeatedField(proto.MESSAGE, number=1,
        message=User,
    )
    next_page_token = proto.Field(proto.STRING, number=2)


__all__ = tuple(sorted(__protobuf__.manifest))

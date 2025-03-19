"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.message
import google.protobuf.timestamp_pb2
import sys
import typing

if sys.version_info >= (3, 8):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing_extensions.final
class Object(google.protobuf.message.Message):
    """Object"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    UID_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    SIZE_FIELD_NUMBER: builtins.int
    CONTENT_TYPE_FIELD_NUMBER: builtins.int
    NAMESPACE_UID_FIELD_NUMBER: builtins.int
    CREATOR_FIELD_NUMBER: builtins.int
    IS_UPLOADED_FIELD_NUMBER: builtins.int
    PATH_FIELD_NUMBER: builtins.int
    OBJECT_EXPIRE_DAYS_FIELD_NUMBER: builtins.int
    LAST_MODIFIED_TIME_FIELD_NUMBER: builtins.int
    CREATED_TIME_FIELD_NUMBER: builtins.int
    UPDATED_TIME_FIELD_NUMBER: builtins.int
    uid: builtins.str
    """uid"""
    name: builtins.str
    """name of the object"""
    size: builtins.int
    """size in bytes"""
    content_type: builtins.str
    """content type
    this is mime type from content-type header of http request or from file extension
    """
    namespace_uid: builtins.str
    """namespace uid"""
    creator: builtins.str
    """creator"""
    is_uploaded: builtins.bool
    """if file is uploaded"""
    path: builtins.str
    """object path(optional)"""
    object_expire_days: builtins.int
    """object live time in days
    if set to 0, the object will not be deleted automatically
    """
    @property
    def last_modified_time(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """last modified time"""
    @property
    def created_time(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """created time"""
    @property
    def updated_time(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """updated time"""
    def __init__(
        self,
        *,
        uid: builtins.str = ...,
        name: builtins.str = ...,
        size: builtins.int = ...,
        content_type: builtins.str = ...,
        namespace_uid: builtins.str = ...,
        creator: builtins.str = ...,
        is_uploaded: builtins.bool = ...,
        path: builtins.str | None = ...,
        object_expire_days: builtins.int = ...,
        last_modified_time: google.protobuf.timestamp_pb2.Timestamp | None = ...,
        created_time: google.protobuf.timestamp_pb2.Timestamp | None = ...,
        updated_time: google.protobuf.timestamp_pb2.Timestamp | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["_last_modified_time", b"_last_modified_time", "_path", b"_path", "created_time", b"created_time", "last_modified_time", b"last_modified_time", "path", b"path", "updated_time", b"updated_time"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["_last_modified_time", b"_last_modified_time", "_path", b"_path", "content_type", b"content_type", "created_time", b"created_time", "creator", b"creator", "is_uploaded", b"is_uploaded", "last_modified_time", b"last_modified_time", "name", b"name", "namespace_uid", b"namespace_uid", "object_expire_days", b"object_expire_days", "path", b"path", "size", b"size", "uid", b"uid", "updated_time", b"updated_time"]) -> None: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_last_modified_time", b"_last_modified_time"]) -> typing_extensions.Literal["last_modified_time"] | None: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_path", b"_path"]) -> typing_extensions.Literal["path"] | None: ...

global___Object = Object

@typing_extensions.final
class GetObjectUploadURLRequest(google.protobuf.message.Message):
    """GetObjectUploadURLRequest"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NAMESPACE_ID_FIELD_NUMBER: builtins.int
    OBJECT_NAME_FIELD_NUMBER: builtins.int
    URL_EXPIRE_DAYS_FIELD_NUMBER: builtins.int
    LAST_MODIFIED_TIME_FIELD_NUMBER: builtins.int
    OBJECT_EXPIRE_DAYS_FIELD_NUMBER: builtins.int
    namespace_id: builtins.str
    """id of the namespace"""
    object_name: builtins.str
    """name of the object with length limit to 1024 characters.
    this is the unique identifier of the object in the namespace
    """
    url_expire_days: builtins.int
    """expiration time in days for the URL.
    maximum is 7 days. if set to 0, URL will not expire.
    """
    @property
    def last_modified_time(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """last modified time this value is provided by the client when the object url is created
        it must be in RFC3339 formatted date-time string
        """
    object_expire_days: builtins.int
    """object live time in days
    minimum is 1 day. if set to 0, the object will not be deleted automatically
    """
    def __init__(
        self,
        *,
        namespace_id: builtins.str = ...,
        object_name: builtins.str = ...,
        url_expire_days: builtins.int = ...,
        last_modified_time: google.protobuf.timestamp_pb2.Timestamp | None = ...,
        object_expire_days: builtins.int = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["last_modified_time", b"last_modified_time"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["last_modified_time", b"last_modified_time", "namespace_id", b"namespace_id", "object_expire_days", b"object_expire_days", "object_name", b"object_name", "url_expire_days", b"url_expire_days"]) -> None: ...

global___GetObjectUploadURLRequest = GetObjectUploadURLRequest

@typing_extensions.final
class GetObjectUploadURLResponse(google.protobuf.message.Message):
    """GetObjectUploadURLResponse"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    UPLOAD_URL_FIELD_NUMBER: builtins.int
    URL_EXPIRE_AT_FIELD_NUMBER: builtins.int
    OBJECT_FIELD_NUMBER: builtins.int
    upload_url: builtins.str
    """upload url"""
    @property
    def url_expire_at(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """expire at in UTC (UTC+0)"""
    @property
    def object(self) -> global___Object:
        """object"""
    def __init__(
        self,
        *,
        upload_url: builtins.str = ...,
        url_expire_at: google.protobuf.timestamp_pb2.Timestamp | None = ...,
        object: global___Object | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["object", b"object", "url_expire_at", b"url_expire_at"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["object", b"object", "upload_url", b"upload_url", "url_expire_at", b"url_expire_at"]) -> None: ...

global___GetObjectUploadURLResponse = GetObjectUploadURLResponse

@typing_extensions.final
class GetObjectDownloadURLRequest(google.protobuf.message.Message):
    """GetObjectDownloadURLRequest"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NAMESPACE_ID_FIELD_NUMBER: builtins.int
    OBJECT_UID_FIELD_NUMBER: builtins.int
    URL_EXPIRE_DAYS_FIELD_NUMBER: builtins.int
    namespace_id: builtins.str
    """id of the namespace"""
    object_uid: builtins.str
    """uid of the object"""
    url_expire_days: builtins.int
    """expiration time in days for the URL.
    maximum is 7 days. if set to 0, URL will not expire.
    """
    def __init__(
        self,
        *,
        namespace_id: builtins.str = ...,
        object_uid: builtins.str = ...,
        url_expire_days: builtins.int = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["namespace_id", b"namespace_id", "object_uid", b"object_uid", "url_expire_days", b"url_expire_days"]) -> None: ...

global___GetObjectDownloadURLRequest = GetObjectDownloadURLRequest

@typing_extensions.final
class GetObjectDownloadURLResponse(google.protobuf.message.Message):
    """GetObjectDownloadURLResponse"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    DOWNLOAD_URL_FIELD_NUMBER: builtins.int
    URL_EXPIRE_AT_FIELD_NUMBER: builtins.int
    OBJECT_FIELD_NUMBER: builtins.int
    download_url: builtins.str
    """download url"""
    @property
    def url_expire_at(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """expire at in UTC (UTC+0)"""
    @property
    def object(self) -> global___Object:
        """object"""
    def __init__(
        self,
        *,
        download_url: builtins.str = ...,
        url_expire_at: google.protobuf.timestamp_pb2.Timestamp | None = ...,
        object: global___Object | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["object", b"object", "url_expire_at", b"url_expire_at"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["download_url", b"download_url", "object", b"object", "url_expire_at", b"url_expire_at"]) -> None: ...

global___GetObjectDownloadURLResponse = GetObjectDownloadURLResponse

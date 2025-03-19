"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import app.app.v1alpha.conversation_pb2
import builtins
import collections.abc
import common.healthcheck.v1beta.healthcheck_pb2
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import google.protobuf.timestamp_pb2
import sys
import typing

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class _AppType:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _AppTypeEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_AppType.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    APP_TYPE_UNSPECIFIED: _AppType.ValueType  # 0
    """AppType is not specified."""
    APP_TYPE_AI_ASSISTANT: _AppType.ValueType  # 1
    """AppType is a AI assistant app."""

class AppType(_AppType, metaclass=_AppTypeEnumTypeWrapper):
    """AppType represents the type of the app."""

APP_TYPE_UNSPECIFIED: AppType.ValueType  # 0
"""AppType is not specified."""
APP_TYPE_AI_ASSISTANT: AppType.ValueType  # 1
"""AppType is a AI assistant app."""
global___AppType = AppType

@typing_extensions.final
class LivenessRequest(google.protobuf.message.Message):
    """LivenessRequest represents a request to check a service liveness status"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    HEALTH_CHECK_REQUEST_FIELD_NUMBER: builtins.int
    @property
    def health_check_request(self) -> common.healthcheck.v1beta.healthcheck_pb2.HealthCheckRequest:
        """HealthCheckRequest message"""
    def __init__(
        self,
        *,
        health_check_request: common.healthcheck.v1beta.healthcheck_pb2.HealthCheckRequest | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["_health_check_request", b"_health_check_request", "health_check_request", b"health_check_request"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["_health_check_request", b"_health_check_request", "health_check_request", b"health_check_request"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_health_check_request", b"_health_check_request"]) -> typing_extensions.Literal["health_check_request"] | None: ...

global___LivenessRequest = LivenessRequest

@typing_extensions.final
class LivenessResponse(google.protobuf.message.Message):
    """LivenessResponse represents a response for a service liveness status"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    HEALTH_CHECK_RESPONSE_FIELD_NUMBER: builtins.int
    @property
    def health_check_response(self) -> common.healthcheck.v1beta.healthcheck_pb2.HealthCheckResponse:
        """HealthCheckResponse message"""
    def __init__(
        self,
        *,
        health_check_response: common.healthcheck.v1beta.healthcheck_pb2.HealthCheckResponse | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["health_check_response", b"health_check_response"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["health_check_response", b"health_check_response"]) -> None: ...

global___LivenessResponse = LivenessResponse

@typing_extensions.final
class ReadinessRequest(google.protobuf.message.Message):
    """ReadinessRequest represents a request to check a service readiness status"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    HEALTH_CHECK_REQUEST_FIELD_NUMBER: builtins.int
    @property
    def health_check_request(self) -> common.healthcheck.v1beta.healthcheck_pb2.HealthCheckRequest:
        """HealthCheckRequest message"""
    def __init__(
        self,
        *,
        health_check_request: common.healthcheck.v1beta.healthcheck_pb2.HealthCheckRequest | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["_health_check_request", b"_health_check_request", "health_check_request", b"health_check_request"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["_health_check_request", b"_health_check_request", "health_check_request", b"health_check_request"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_health_check_request", b"_health_check_request"]) -> typing_extensions.Literal["health_check_request"] | None: ...

global___ReadinessRequest = ReadinessRequest

@typing_extensions.final
class ReadinessResponse(google.protobuf.message.Message):
    """ReadinessResponse represents a response for a service readiness status"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    HEALTH_CHECK_RESPONSE_FIELD_NUMBER: builtins.int
    @property
    def health_check_response(self) -> common.healthcheck.v1beta.healthcheck_pb2.HealthCheckResponse:
        """HealthCheckResponse message"""
    def __init__(
        self,
        *,
        health_check_response: common.healthcheck.v1beta.healthcheck_pb2.HealthCheckResponse | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["health_check_response", b"health_check_response"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["health_check_response", b"health_check_response"]) -> None: ...

global___ReadinessResponse = ReadinessResponse

@typing_extensions.final
class App(google.protobuf.message.Message):
    """
    This API is under development and, therefore, some of its entities and
    endpoints are not implemented yet. This section aims to give context about
    the current interface and how it fits in the App vision.

    # App

    The App domain is responsible of ready-to-use AI applications.

    App represents a app.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    APP_ID_FIELD_NUMBER: builtins.int
    DESCRIPTION_FIELD_NUMBER: builtins.int
    CREATE_TIME_FIELD_NUMBER: builtins.int
    UPDATE_TIME_FIELD_NUMBER: builtins.int
    OWNER_UID_FIELD_NUMBER: builtins.int
    TAGS_FIELD_NUMBER: builtins.int
    AI_ASSISTANT_APP_FIELD_NUMBER: builtins.int
    APP_TYPE_FIELD_NUMBER: builtins.int
    APP_UID_FIELD_NUMBER: builtins.int
    CREATOR_UID_FIELD_NUMBER: builtins.int
    app_id: builtins.str
    """The app id."""
    description: builtins.str
    """The app description."""
    @property
    def create_time(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """The creation time of the app."""
    @property
    def update_time(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """The last update time of the app."""
    owner_uid: builtins.str
    """The owner/namespace of the app."""
    @property
    def tags(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]:
        """The app tags."""
    @property
    def ai_assistant_app(self) -> global___AIAssistantAppMetadata:
        """The AI assistant app metadata."""
    app_type: global___AppType.ValueType
    """The app type."""
    app_uid: builtins.str
    """app uid"""
    creator_uid: builtins.str
    """creator uid"""
    def __init__(
        self,
        *,
        app_id: builtins.str = ...,
        description: builtins.str = ...,
        create_time: google.protobuf.timestamp_pb2.Timestamp | None = ...,
        update_time: google.protobuf.timestamp_pb2.Timestamp | None = ...,
        owner_uid: builtins.str = ...,
        tags: collections.abc.Iterable[builtins.str] | None = ...,
        ai_assistant_app: global___AIAssistantAppMetadata | None = ...,
        app_type: global___AppType.ValueType = ...,
        app_uid: builtins.str = ...,
        creator_uid: builtins.str = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["ai_assistant_app", b"ai_assistant_app", "create_time", b"create_time", "metadata", b"metadata", "update_time", b"update_time"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["ai_assistant_app", b"ai_assistant_app", "app_id", b"app_id", "app_type", b"app_type", "app_uid", b"app_uid", "create_time", b"create_time", "creator_uid", b"creator_uid", "description", b"description", "metadata", b"metadata", "owner_uid", b"owner_uid", "tags", b"tags", "update_time", b"update_time"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["metadata", b"metadata"]) -> typing_extensions.Literal["ai_assistant_app"] | None: ...

global___App = App

@typing_extensions.final
class AIAssistantAppMetadata(google.protobuf.message.Message):
    """AIAssistantAppMetadata represents the metadata for the AI assistant app."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CATALOG_UID_FIELD_NUMBER: builtins.int
    TOP_K_FIELD_NUMBER: builtins.int
    catalog_uid: builtins.str
    """The AI assistant app catalog uid."""
    top_k: builtins.int
    """The AI assistant app top k."""
    def __init__(
        self,
        *,
        catalog_uid: builtins.str = ...,
        top_k: builtins.int = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["catalog_uid", b"catalog_uid", "top_k", b"top_k"]) -> None: ...

global___AIAssistantAppMetadata = AIAssistantAppMetadata

@typing_extensions.final
class CreateAppRequest(google.protobuf.message.Message):
    """CreateAppRequest represents a request to create a app."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NAMESPACE_ID_FIELD_NUMBER: builtins.int
    ID_FIELD_NUMBER: builtins.int
    DESCRIPTION_FIELD_NUMBER: builtins.int
    TAGS_FIELD_NUMBER: builtins.int
    namespace_id: builtins.str
    """The app's owner(namespaces)."""
    id: builtins.str
    """The app id.
    the app id should be lowercase without any space or special character besides the hyphen,
    it can not start with number or hyphen, and should be less than 32 characters.
    """
    description: builtins.str
    """The app description."""
    @property
    def tags(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]:
        """The app tags."""
    def __init__(
        self,
        *,
        namespace_id: builtins.str = ...,
        id: builtins.str = ...,
        description: builtins.str = ...,
        tags: collections.abc.Iterable[builtins.str] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["description", b"description", "id", b"id", "namespace_id", b"namespace_id", "tags", b"tags"]) -> None: ...

global___CreateAppRequest = CreateAppRequest

@typing_extensions.final
class CreateAppResponse(google.protobuf.message.Message):
    """CreateAppResponse represents a response for creating a app."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    APP_FIELD_NUMBER: builtins.int
    @property
    def app(self) -> global___App:
        """The created app."""
    def __init__(
        self,
        *,
        app: global___App | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["app", b"app"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["app", b"app"]) -> None: ...

global___CreateAppResponse = CreateAppResponse

@typing_extensions.final
class ListAppsRequest(google.protobuf.message.Message):
    """Request message for ListApps"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NAMESPACE_ID_FIELD_NUMBER: builtins.int
    namespace_id: builtins.str
    """User ID for which to list the apps"""
    def __init__(
        self,
        *,
        namespace_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["namespace_id", b"namespace_id"]) -> None: ...

global___ListAppsRequest = ListAppsRequest

@typing_extensions.final
class ListAppsResponse(google.protobuf.message.Message):
    """GetAppsResponse represents a response for getting all apps from users."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    APPS_FIELD_NUMBER: builtins.int
    @property
    def apps(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___App]:
        """The apps container."""
    def __init__(
        self,
        *,
        apps: collections.abc.Iterable[global___App] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["apps", b"apps"]) -> None: ...

global___ListAppsResponse = ListAppsResponse

@typing_extensions.final
class UpdateAppRequest(google.protobuf.message.Message):
    """UpdateAppRequest represents a request to update a app."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NAMESPACE_ID_FIELD_NUMBER: builtins.int
    APP_ID_FIELD_NUMBER: builtins.int
    NEW_APP_ID_FIELD_NUMBER: builtins.int
    NEW_DESCRIPTION_FIELD_NUMBER: builtins.int
    NEW_TAGS_FIELD_NUMBER: builtins.int
    LAST_AI_ASSISTANT_APP_CATALOG_UID_FIELD_NUMBER: builtins.int
    LAST_AI_ASSISTANT_APP_TOP_K_FIELD_NUMBER: builtins.int
    namespace_id: builtins.str
    """Namespace id."""
    app_id: builtins.str
    """App id."""
    new_app_id: builtins.str
    """The app id needs to follow the kebab case format.
    if the new app id is not provided, the app id will not be updated.
    """
    new_description: builtins.str
    """The app description.
    If the new description is empty, the description will be set to empty.
    """
    @property
    def new_tags(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]:
        """The app tags.
        If the new tags is empty, the tags will be set to empty.
        """
    last_ai_assistant_app_catalog_uid: builtins.str
    """last AI assistant app catalog uid
    If the last AI assistant app catalog uid is empty, the last AI assistant app catalog uid will be set to empty.
    """
    last_ai_assistant_app_top_k: builtins.int
    """last AI assistant app top k
    If the last AI assistant app top k is empty, the last AI assistant app top k will be set to empty.
    """
    def __init__(
        self,
        *,
        namespace_id: builtins.str = ...,
        app_id: builtins.str = ...,
        new_app_id: builtins.str = ...,
        new_description: builtins.str = ...,
        new_tags: collections.abc.Iterable[builtins.str] | None = ...,
        last_ai_assistant_app_catalog_uid: builtins.str = ...,
        last_ai_assistant_app_top_k: builtins.int = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["app_id", b"app_id", "last_ai_assistant_app_catalog_uid", b"last_ai_assistant_app_catalog_uid", "last_ai_assistant_app_top_k", b"last_ai_assistant_app_top_k", "namespace_id", b"namespace_id", "new_app_id", b"new_app_id", "new_description", b"new_description", "new_tags", b"new_tags"]) -> None: ...

global___UpdateAppRequest = UpdateAppRequest

@typing_extensions.final
class UpdateAppResponse(google.protobuf.message.Message):
    """UpdateAppResponse represents a response for updating a app."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    APP_FIELD_NUMBER: builtins.int
    @property
    def app(self) -> global___App:
        """The updated app."""
    def __init__(
        self,
        *,
        app: global___App | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["app", b"app"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["app", b"app"]) -> None: ...

global___UpdateAppResponse = UpdateAppResponse

@typing_extensions.final
class DeleteAppRequest(google.protobuf.message.Message):
    """DeleteAppRequest represents a request to delete a app."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NAMESPACE_ID_FIELD_NUMBER: builtins.int
    APP_ID_FIELD_NUMBER: builtins.int
    namespace_id: builtins.str
    """The owner's id. i.e. namespace."""
    app_id: builtins.str
    """The app id."""
    def __init__(
        self,
        *,
        namespace_id: builtins.str = ...,
        app_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["app_id", b"app_id", "namespace_id", b"namespace_id"]) -> None: ...

global___DeleteAppRequest = DeleteAppRequest

@typing_extensions.final
class DeleteAppResponse(google.protobuf.message.Message):
    """DeleteAppResponse represents a response for deleting a app."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___DeleteAppResponse = DeleteAppResponse

@typing_extensions.final
class RestartPlaygroundConversationRequest(google.protobuf.message.Message):
    """RestartPlaygroundConversationRequest represents a request to restart a playground conversation."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NAMESPACE_ID_FIELD_NUMBER: builtins.int
    APP_ID_FIELD_NUMBER: builtins.int
    namespace_id: builtins.str
    """The namespace id."""
    app_id: builtins.str
    """The app id."""
    def __init__(
        self,
        *,
        namespace_id: builtins.str = ...,
        app_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["app_id", b"app_id", "namespace_id", b"namespace_id"]) -> None: ...

global___RestartPlaygroundConversationRequest = RestartPlaygroundConversationRequest

@typing_extensions.final
class RestartPlaygroundConversationResponse(google.protobuf.message.Message):
    """RestartPlaygroundConversationResponse represents a response for restarting a playground conversation."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CONVERSATION_FIELD_NUMBER: builtins.int
    @property
    def conversation(self) -> app.app.v1alpha.conversation_pb2.Conversation:
        """conversation"""
    def __init__(
        self,
        *,
        conversation: app.app.v1alpha.conversation_pb2.Conversation | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["conversation", b"conversation"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["conversation", b"conversation"]) -> None: ...

global___RestartPlaygroundConversationResponse = RestartPlaygroundConversationResponse

@typing_extensions.final
class GetPlaygroundConversationRequest(google.protobuf.message.Message):
    """GetPlaygroundConversationRequest represents a request to get a playground conversation."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NAMESPACE_ID_FIELD_NUMBER: builtins.int
    APP_ID_FIELD_NUMBER: builtins.int
    namespace_id: builtins.str
    """The namespace id."""
    app_id: builtins.str
    """The app id."""
    def __init__(
        self,
        *,
        namespace_id: builtins.str = ...,
        app_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["app_id", b"app_id", "namespace_id", b"namespace_id"]) -> None: ...

global___GetPlaygroundConversationRequest = GetPlaygroundConversationRequest

@typing_extensions.final
class GetPlaygroundConversationResponse(google.protobuf.message.Message):
    """GetPlaygroundConversationResponse represents a response for getting a playground conversation."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CONVERSATION_FIELD_NUMBER: builtins.int
    @property
    def conversation(self) -> app.app.v1alpha.conversation_pb2.Conversation:
        """conversation"""
    def __init__(
        self,
        *,
        conversation: app.app.v1alpha.conversation_pb2.Conversation | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["conversation", b"conversation"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["conversation", b"conversation"]) -> None: ...

global___GetPlaygroundConversationResponse = GetPlaygroundConversationResponse

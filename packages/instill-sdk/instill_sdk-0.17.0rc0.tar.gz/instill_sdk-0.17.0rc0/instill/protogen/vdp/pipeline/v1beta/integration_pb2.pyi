"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.field_mask_pb2
import google.protobuf.internal.containers
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import google.protobuf.struct_pb2
import google.protobuf.timestamp_pb2
import sys
import typing
import vdp.pipeline.v1beta.common_pb2

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing_extensions.final
class Connection(google.protobuf.message.Message):
    """Connection contains the parameters to communicate with a 3rd party app. A
    component may reference a connection in their setup. One connection may be
    used by several components and pipelines.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    class _Method:
        ValueType = typing.NewType("ValueType", builtins.int)
        V: typing_extensions.TypeAlias = ValueType

    class _MethodEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[Connection._Method.ValueType], builtins.type):
        DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
        METHOD_UNSPECIFIED: Connection._Method.ValueType  # 0
        """Unspecified."""
        METHOD_DICTIONARY: Connection._Method.ValueType  # 1
        """Key-value collection. The user is responsible of fetching the connection
        details from the 3rd party service.
        """
        METHOD_OAUTH: Connection._Method.ValueType  # 2
        """Access token created via OAuth 2.0 authorization."""

    class Method(_Method, metaclass=_MethodEnumTypeWrapper):
        """Method defines how the connection is set up."""

    METHOD_UNSPECIFIED: Connection.Method.ValueType  # 0
    """Unspecified."""
    METHOD_DICTIONARY: Connection.Method.ValueType  # 1
    """Key-value collection. The user is responsible of fetching the connection
    details from the 3rd party service.
    """
    METHOD_OAUTH: Connection.Method.ValueType  # 2
    """Access token created via OAuth 2.0 authorization."""

    UID_FIELD_NUMBER: builtins.int
    ID_FIELD_NUMBER: builtins.int
    NAMESPACE_ID_FIELD_NUMBER: builtins.int
    INTEGRATION_ID_FIELD_NUMBER: builtins.int
    INTEGRATION_TITLE_FIELD_NUMBER: builtins.int
    METHOD_FIELD_NUMBER: builtins.int
    SETUP_FIELD_NUMBER: builtins.int
    SCOPES_FIELD_NUMBER: builtins.int
    IDENTITY_FIELD_NUMBER: builtins.int
    O_AUTH_ACCESS_DETAILS_FIELD_NUMBER: builtins.int
    VIEW_FIELD_NUMBER: builtins.int
    CREATE_TIME_FIELD_NUMBER: builtins.int
    UPDATE_TIME_FIELD_NUMBER: builtins.int
    uid: builtins.str
    """UUID-formatted unique identifier."""
    id: builtins.str
    """ID."""
    namespace_id: builtins.str
    """ID of the namespace owning the connection."""
    integration_id: builtins.str
    """Integration ID. It determines for which type of components can reference
    this connection.
    """
    integration_title: builtins.str
    """Integration title. This helps the console display the results grouped by
    integration ID without needing an extra call to fetch title by integration
    ID.
    """
    method: global___Connection.Method.ValueType
    """Connection method. It references the setup schema provided by the
    integration.
    """
    @property
    def setup(self) -> google.protobuf.struct_pb2.Struct:
        """Connection details. This field is required on creation, optional on view.
        When viewing the connection details, the setup values will be redacted.
        """
    @property
    def scopes(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]:
        """A list of scopes that identify the resources that the connection will be
        able to access on the user's behalf. This is typically passed on creation
        when the setup has been generated through an OAuth flow with a limited set
        of scopes.
        """
    identity: builtins.str
    """When the connection method is METHOD_OAUTH, this field will hold the
    identity (e.g., email, username) with which the access token has been
    generated.
    """
    @property
    def o_auth_access_details(self) -> google.protobuf.struct_pb2.Struct:
        """When the connection method is METHOD_OAUTH, the access token might come
        with some extra information that might vary across vendors. This
        information is passed as connection metadata.
        """
    view: vdp.pipeline.v1beta.common_pb2.View.ValueType
    """View defines how the connection is presented. The following fields are
    only shown in the FULL view:
    - setup
    - scopes
    - oAuthAccessDetails
    """
    @property
    def create_time(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """Creation timestamp."""
    @property
    def update_time(self) -> google.protobuf.timestamp_pb2.Timestamp:
        """Last update timestamp."""
    def __init__(
        self,
        *,
        uid: builtins.str = ...,
        id: builtins.str = ...,
        namespace_id: builtins.str = ...,
        integration_id: builtins.str = ...,
        integration_title: builtins.str = ...,
        method: global___Connection.Method.ValueType = ...,
        setup: google.protobuf.struct_pb2.Struct | None = ...,
        scopes: collections.abc.Iterable[builtins.str] | None = ...,
        identity: builtins.str | None = ...,
        o_auth_access_details: google.protobuf.struct_pb2.Struct | None = ...,
        view: vdp.pipeline.v1beta.common_pb2.View.ValueType = ...,
        create_time: google.protobuf.timestamp_pb2.Timestamp | None = ...,
        update_time: google.protobuf.timestamp_pb2.Timestamp | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["_identity", b"_identity", "_o_auth_access_details", b"_o_auth_access_details", "create_time", b"create_time", "identity", b"identity", "o_auth_access_details", b"o_auth_access_details", "setup", b"setup", "update_time", b"update_time"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["_identity", b"_identity", "_o_auth_access_details", b"_o_auth_access_details", "create_time", b"create_time", "id", b"id", "identity", b"identity", "integration_id", b"integration_id", "integration_title", b"integration_title", "method", b"method", "namespace_id", b"namespace_id", "o_auth_access_details", b"o_auth_access_details", "scopes", b"scopes", "setup", b"setup", "uid", b"uid", "update_time", b"update_time", "view", b"view"]) -> None: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_identity", b"_identity"]) -> typing_extensions.Literal["identity"] | None: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_o_auth_access_details", b"_o_auth_access_details"]) -> typing_extensions.Literal["o_auth_access_details"] | None: ...

global___Connection = Connection

@typing_extensions.final
class ListNamespaceConnectionsRequest(google.protobuf.message.Message):
    """ListNamespaceConnectionsRequest represents a request to list the connections
    created by a namespace.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NAMESPACE_ID_FIELD_NUMBER: builtins.int
    PAGE_SIZE_FIELD_NUMBER: builtins.int
    PAGE_TOKEN_FIELD_NUMBER: builtins.int
    FILTER_FIELD_NUMBER: builtins.int
    namespace_id: builtins.str
    """Namespace ID."""
    page_size: builtins.int
    """The maximum number of items to return. The default and cap values are 10 and 100, respectively."""
    page_token: builtins.str
    """Page token. By default, the first page will be returned."""
    filter: builtins.str
    """Filter can hold an [AIP-160](https://google.aip.dev/160)-compliant filter expression.
    The following filters are supported:
    - `integrationId`
    - `qConnection` (fuzzy search on connection ID, integration title or vendor)

    **Examples**:
    - List connections where app name, vendor or connection ID match `googl`: `q="googl"`.
    - List connections where the component type is `openai` (e.g. to setup a connector within a pipeline): `integrationId="openai"`.
    """
    def __init__(
        self,
        *,
        namespace_id: builtins.str = ...,
        page_size: builtins.int | None = ...,
        page_token: builtins.str | None = ...,
        filter: builtins.str | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["_filter", b"_filter", "_page_size", b"_page_size", "_page_token", b"_page_token", "filter", b"filter", "page_size", b"page_size", "page_token", b"page_token"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["_filter", b"_filter", "_page_size", b"_page_size", "_page_token", b"_page_token", "filter", b"filter", "namespace_id", b"namespace_id", "page_size", b"page_size", "page_token", b"page_token"]) -> None: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_filter", b"_filter"]) -> typing_extensions.Literal["filter"] | None: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_page_size", b"_page_size"]) -> typing_extensions.Literal["page_size"] | None: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_page_token", b"_page_token"]) -> typing_extensions.Literal["page_token"] | None: ...

global___ListNamespaceConnectionsRequest = ListNamespaceConnectionsRequest

@typing_extensions.final
class ListNamespaceConnectionsResponse(google.protobuf.message.Message):
    """ListNamespaceConnectionsResponse contains a paginated list of connections."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CONNECTIONS_FIELD_NUMBER: builtins.int
    NEXT_PAGE_TOKEN_FIELD_NUMBER: builtins.int
    TOTAL_SIZE_FIELD_NUMBER: builtins.int
    @property
    def connections(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___Connection]:
        """A list of connections matching the request parameters."""
    next_page_token: builtins.str
    """Next page token."""
    total_size: builtins.int
    """Total number of items."""
    def __init__(
        self,
        *,
        connections: collections.abc.Iterable[global___Connection] | None = ...,
        next_page_token: builtins.str = ...,
        total_size: builtins.int = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["connections", b"connections", "next_page_token", b"next_page_token", "total_size", b"total_size"]) -> None: ...

global___ListNamespaceConnectionsResponse = ListNamespaceConnectionsResponse

@typing_extensions.final
class GetNamespaceConnectionRequest(google.protobuf.message.Message):
    """GetNamespaceConnectionRequest represents a request to view the details of a
    connection.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NAMESPACE_ID_FIELD_NUMBER: builtins.int
    CONNECTION_ID_FIELD_NUMBER: builtins.int
    VIEW_FIELD_NUMBER: builtins.int
    namespace_id: builtins.str
    """Namespace ID."""
    connection_id: builtins.str
    """Connection ID."""
    view: vdp.pipeline.v1beta.common_pb2.View.ValueType
    """View allows clients to specify the desired view in the response."""
    def __init__(
        self,
        *,
        namespace_id: builtins.str = ...,
        connection_id: builtins.str = ...,
        view: vdp.pipeline.v1beta.common_pb2.View.ValueType | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["_view", b"_view", "view", b"view"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["_view", b"_view", "connection_id", b"connection_id", "namespace_id", b"namespace_id", "view", b"view"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_view", b"_view"]) -> typing_extensions.Literal["view"] | None: ...

global___GetNamespaceConnectionRequest = GetNamespaceConnectionRequest

@typing_extensions.final
class GetNamespaceConnectionResponse(google.protobuf.message.Message):
    """GetNamespaceConnectionResponse contains the requested connection."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CONNECTION_FIELD_NUMBER: builtins.int
    @property
    def connection(self) -> global___Connection:
        """The requested connection."""
    def __init__(
        self,
        *,
        connection: global___Connection | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["connection", b"connection"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["connection", b"connection"]) -> None: ...

global___GetNamespaceConnectionResponse = GetNamespaceConnectionResponse

@typing_extensions.final
class CreateNamespaceConnectionRequest(google.protobuf.message.Message):
    """CreateNamespaceConnectionRequest represents a request to create a
    connection.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NAMESPACE_ID_FIELD_NUMBER: builtins.int
    CONNECTION_FIELD_NUMBER: builtins.int
    namespace_id: builtins.str
    """ID of the namespace that owns the connection."""
    @property
    def connection(self) -> global___Connection:
        """Properties of the connection to be created."""
    def __init__(
        self,
        *,
        namespace_id: builtins.str = ...,
        connection: global___Connection | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["connection", b"connection"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["connection", b"connection", "namespace_id", b"namespace_id"]) -> None: ...

global___CreateNamespaceConnectionRequest = CreateNamespaceConnectionRequest

@typing_extensions.final
class CreateNamespaceConnectionResponse(google.protobuf.message.Message):
    """CreateNamespaceConnectionResponse contains the created connection."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CONNECTION_FIELD_NUMBER: builtins.int
    @property
    def connection(self) -> global___Connection:
        """The created connection."""
    def __init__(
        self,
        *,
        connection: global___Connection | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["connection", b"connection"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["connection", b"connection"]) -> None: ...

global___CreateNamespaceConnectionResponse = CreateNamespaceConnectionResponse

@typing_extensions.final
class UpdateNamespaceConnectionRequest(google.protobuf.message.Message):
    """UpdateNamespaceConnectionRequest represents a request to update a
    connection.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CONNECTION_ID_FIELD_NUMBER: builtins.int
    NAMESPACE_ID_FIELD_NUMBER: builtins.int
    CONNECTION_FIELD_NUMBER: builtins.int
    UPDATE_MASK_FIELD_NUMBER: builtins.int
    connection_id: builtins.str
    """ID of the connection to be updated, as present in the database."""
    namespace_id: builtins.str
    """ID of the namespace that owns the connection."""
    @property
    def connection(self) -> global___Connection:
        """Connection object with the new properties to be updated. Immutable and
        output-only fields will be ignored. The Setup property must be updated
        in block (no partial update is supported).
        """
    @property
    def update_mask(self) -> google.protobuf.field_mask_pb2.FieldMask:
        """The update mask specifies the subset of fields that should be modified.

        For more information about this field, see
        https://developers.google.com/protocol-buffers/docs/reference/google.protobuf#field-mask.
        """
    def __init__(
        self,
        *,
        connection_id: builtins.str = ...,
        namespace_id: builtins.str = ...,
        connection: global___Connection | None = ...,
        update_mask: google.protobuf.field_mask_pb2.FieldMask | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["connection", b"connection", "update_mask", b"update_mask"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["connection", b"connection", "connection_id", b"connection_id", "namespace_id", b"namespace_id", "update_mask", b"update_mask"]) -> None: ...

global___UpdateNamespaceConnectionRequest = UpdateNamespaceConnectionRequest

@typing_extensions.final
class UpdateNamespaceConnectionResponse(google.protobuf.message.Message):
    """UpdateNamespaceConnectionResponse contains the updated connection."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CONNECTION_FIELD_NUMBER: builtins.int
    @property
    def connection(self) -> global___Connection:
        """The created connection."""
    def __init__(
        self,
        *,
        connection: global___Connection | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["connection", b"connection"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["connection", b"connection"]) -> None: ...

global___UpdateNamespaceConnectionResponse = UpdateNamespaceConnectionResponse

@typing_extensions.final
class DeleteNamespaceConnectionRequest(google.protobuf.message.Message):
    """DeleteNamespaceConnectionRequest represents a request to delete a
    connection.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NAMESPACE_ID_FIELD_NUMBER: builtins.int
    CONNECTION_ID_FIELD_NUMBER: builtins.int
    namespace_id: builtins.str
    """Namespace ID."""
    connection_id: builtins.str
    """Connection ID."""
    def __init__(
        self,
        *,
        namespace_id: builtins.str = ...,
        connection_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["connection_id", b"connection_id", "namespace_id", b"namespace_id"]) -> None: ...

global___DeleteNamespaceConnectionRequest = DeleteNamespaceConnectionRequest

@typing_extensions.final
class DeleteNamespaceConnectionResponse(google.protobuf.message.Message):
    """DeleteNamespaceConnectionResponse is an empty response."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___DeleteNamespaceConnectionResponse = DeleteNamespaceConnectionResponse

@typing_extensions.final
class TestNamespaceConnectionRequest(google.protobuf.message.Message):
    """TestNamespaceConnectionRequest represents a request to test a connection."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NAMESPACE_ID_FIELD_NUMBER: builtins.int
    CONNECTION_ID_FIELD_NUMBER: builtins.int
    namespace_id: builtins.str
    """Namespace ID."""
    connection_id: builtins.str
    """Connection ID."""
    def __init__(
        self,
        *,
        namespace_id: builtins.str = ...,
        connection_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["connection_id", b"connection_id", "namespace_id", b"namespace_id"]) -> None: ...

global___TestNamespaceConnectionRequest = TestNamespaceConnectionRequest

@typing_extensions.final
class TestNamespaceConnectionResponse(google.protobuf.message.Message):
    """TestNamespaceConnectionResponse is an empty response."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___TestNamespaceConnectionResponse = TestNamespaceConnectionResponse

@typing_extensions.final
class Integration(google.protobuf.message.Message):
    """Integration contains the parameters to create a connection between
    components and 3rd party apps.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing_extensions.final
    class Link(google.protobuf.message.Message):
        """Link contains the information to display an reference to an external URL."""

        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        TEXT_FIELD_NUMBER: builtins.int
        URL_FIELD_NUMBER: builtins.int
        text: builtins.str
        """Text contains the message to display."""
        url: builtins.str
        """URL contains the reference the link will redirect to."""
        def __init__(
            self,
            *,
            text: builtins.str = ...,
            url: builtins.str = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["text", b"text", "url", b"url"]) -> None: ...

    @typing_extensions.final
    class OAuthConfig(google.protobuf.message.Message):
        """OAuthConfig contains the configuration parameters for fetching an access
        token via an OAuth 2.0 flow.
        """

        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        AUTH_URL_FIELD_NUMBER: builtins.int
        ACCESS_URL_FIELD_NUMBER: builtins.int
        SCOPES_FIELD_NUMBER: builtins.int
        auth_url: builtins.str
        """The URL of the OAuth server to initiate the authentication and
        authorization process.
        """
        access_url: builtins.str
        """The URL of the OAuth server to exchange the authorization code for an
        access token.
        """
        @property
        def scopes(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]:
            """A list of scopes that identify the resources that the connection will be
            able to access on the user's behalf.
            """
        def __init__(
            self,
            *,
            auth_url: builtins.str = ...,
            access_url: builtins.str = ...,
            scopes: collections.abc.Iterable[builtins.str] | None = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["access_url", b"access_url", "auth_url", b"auth_url", "scopes", b"scopes"]) -> None: ...

    @typing_extensions.final
    class SetupSchema(google.protobuf.message.Message):
        """SetupSchema defines the schema for a connection setup.
        This message is deprecated.
        """

        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        METHOD_FIELD_NUMBER: builtins.int
        SCHEMA_FIELD_NUMBER: builtins.int
        method: global___Connection.Method.ValueType
        """The connection method, which will define the fields in the schema."""
        @property
        def schema(self) -> google.protobuf.struct_pb2.Struct:
            """The connection setup field definitions. Each integration will require
            different data to connect to the 3rd party app.
            """
        def __init__(
            self,
            *,
            method: global___Connection.Method.ValueType = ...,
            schema: google.protobuf.struct_pb2.Struct | None = ...,
        ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal["schema", b"schema"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal["method", b"method", "schema", b"schema"]) -> None: ...

    UID_FIELD_NUMBER: builtins.int
    ID_FIELD_NUMBER: builtins.int
    TITLE_FIELD_NUMBER: builtins.int
    DESCRIPTION_FIELD_NUMBER: builtins.int
    VENDOR_FIELD_NUMBER: builtins.int
    ICON_FIELD_NUMBER: builtins.int
    HELP_LINK_FIELD_NUMBER: builtins.int
    SETUP_SCHEMA_FIELD_NUMBER: builtins.int
    O_AUTH_CONFIG_FIELD_NUMBER: builtins.int
    VIEW_FIELD_NUMBER: builtins.int
    SCHEMAS_FIELD_NUMBER: builtins.int
    uid: builtins.str
    """UUID-formatted unique identifier. It references a component definition."""
    id: builtins.str
    """Identifier of the integration, which references a component definition.
    Components with that definition ID will be able to use the connections
    produced by this integration.
    """
    title: builtins.str
    """Title, reflects the app name."""
    description: builtins.str
    """Short description of the integrated app."""
    vendor: builtins.str
    """Integrated app vendor name."""
    icon: builtins.str
    """Integration icon. This is a path that's relative to the root of
    the component implementation and that allows frontend applications to pull
    and locate the icons.
    See the `icon` field in the `ComponentDefinition` entity for more
    information.
    """
    @property
    def help_link(self) -> global___Integration.Link:
        """Reference to the vendor's documentation to expand the integration details."""
    @property
    def setup_schema(self) -> google.protobuf.struct_pb2.Struct:
        """The connection setup field definitions. Each integration will require
        different data to connect to the 3rd party app.
        """
    @property
    def o_auth_config(self) -> global___Integration.OAuthConfig:
        """Configuration parameters required for the OAuth setup flow. This field
        will be present only if the integration supports OAuth 2.0.
        """
    view: vdp.pipeline.v1beta.common_pb2.View.ValueType
    """View defines how the integration is presented. The following fields are
    only shown in the FULL view:
    - schemas
    - setupSchema
    - oAuthConfig
    """
    @property
    def schemas(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___Integration.SetupSchema]:
        """Schemas defines the supported schemas for the connection setup.
        We haven't found a case for a schema that changes on the connection method
        (components don't care about how the connection was built), so the schema
        will be provided in the setupSchema field and the OAuth support and
        configuration will be provided in oAuthConfig.
        """
    def __init__(
        self,
        *,
        uid: builtins.str = ...,
        id: builtins.str = ...,
        title: builtins.str = ...,
        description: builtins.str = ...,
        vendor: builtins.str = ...,
        icon: builtins.str = ...,
        help_link: global___Integration.Link | None = ...,
        setup_schema: google.protobuf.struct_pb2.Struct | None = ...,
        o_auth_config: global___Integration.OAuthConfig | None = ...,
        view: vdp.pipeline.v1beta.common_pb2.View.ValueType = ...,
        schemas: collections.abc.Iterable[global___Integration.SetupSchema] | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["_help_link", b"_help_link", "_o_auth_config", b"_o_auth_config", "help_link", b"help_link", "o_auth_config", b"o_auth_config", "setup_schema", b"setup_schema"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["_help_link", b"_help_link", "_o_auth_config", b"_o_auth_config", "description", b"description", "help_link", b"help_link", "icon", b"icon", "id", b"id", "o_auth_config", b"o_auth_config", "schemas", b"schemas", "setup_schema", b"setup_schema", "title", b"title", "uid", b"uid", "vendor", b"vendor", "view", b"view"]) -> None: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_help_link", b"_help_link"]) -> typing_extensions.Literal["help_link"] | None: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_o_auth_config", b"_o_auth_config"]) -> typing_extensions.Literal["o_auth_config"] | None: ...

global___Integration = Integration

@typing_extensions.final
class ListPipelineIDsByConnectionIDRequest(google.protobuf.message.Message):
    """ListPipelineIDsByConnectionIDRequest represents a request to list the
    pipelines that reference a connection.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NAMESPACE_ID_FIELD_NUMBER: builtins.int
    CONNECTION_ID_FIELD_NUMBER: builtins.int
    PAGE_SIZE_FIELD_NUMBER: builtins.int
    PAGE_TOKEN_FIELD_NUMBER: builtins.int
    FILTER_FIELD_NUMBER: builtins.int
    namespace_id: builtins.str
    """Namespace ID."""
    connection_id: builtins.str
    """Connection ID."""
    page_size: builtins.int
    """The maximum number of items to return. The default and cap values are 10 and 100, respectively."""
    page_token: builtins.str
    """Page token. By default, the first page will be returned."""
    filter: builtins.str
    """Filter can hold an [AIP-160](https://google.aip.dev/160)-compliant filter expression.
    The following filters are supported:
    - `q` (fuzzy search on pipeline ID)
    """
    def __init__(
        self,
        *,
        namespace_id: builtins.str = ...,
        connection_id: builtins.str = ...,
        page_size: builtins.int | None = ...,
        page_token: builtins.str | None = ...,
        filter: builtins.str | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["_filter", b"_filter", "_page_size", b"_page_size", "_page_token", b"_page_token", "filter", b"filter", "page_size", b"page_size", "page_token", b"page_token"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["_filter", b"_filter", "_page_size", b"_page_size", "_page_token", b"_page_token", "connection_id", b"connection_id", "filter", b"filter", "namespace_id", b"namespace_id", "page_size", b"page_size", "page_token", b"page_token"]) -> None: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_filter", b"_filter"]) -> typing_extensions.Literal["filter"] | None: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_page_size", b"_page_size"]) -> typing_extensions.Literal["page_size"] | None: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_page_token", b"_page_token"]) -> typing_extensions.Literal["page_token"] | None: ...

global___ListPipelineIDsByConnectionIDRequest = ListPipelineIDsByConnectionIDRequest

@typing_extensions.final
class ListPipelineIDsByConnectionIDResponse(google.protobuf.message.Message):
    """ListPipelineIDsByConnectionIDResponse contains a paginated list of integrations."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    PIPELINE_IDS_FIELD_NUMBER: builtins.int
    NEXT_PAGE_TOKEN_FIELD_NUMBER: builtins.int
    TOTAL_SIZE_FIELD_NUMBER: builtins.int
    @property
    def pipeline_ids(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]:
        """A list of pipeline IDs matching the request parameters."""
    next_page_token: builtins.str
    """Next page token."""
    total_size: builtins.int
    """Total number of items."""
    def __init__(
        self,
        *,
        pipeline_ids: collections.abc.Iterable[builtins.str] | None = ...,
        next_page_token: builtins.str = ...,
        total_size: builtins.int = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["next_page_token", b"next_page_token", "pipeline_ids", b"pipeline_ids", "total_size", b"total_size"]) -> None: ...

global___ListPipelineIDsByConnectionIDResponse = ListPipelineIDsByConnectionIDResponse

@typing_extensions.final
class ListIntegrationsRequest(google.protobuf.message.Message):
    """ListIntegrationsRequest represents a request to list the available
    integrations.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    PAGE_SIZE_FIELD_NUMBER: builtins.int
    PAGE_TOKEN_FIELD_NUMBER: builtins.int
    FILTER_FIELD_NUMBER: builtins.int
    page_size: builtins.int
    """The maximum number of items to return. The default and cap values are 10 and 100, respectively."""
    page_token: builtins.str
    """Page token. By default, the first page will be returned."""
    filter: builtins.str
    """Filter can hold an [AIP-160](https://google.aip.dev/160)-compliant filter expression.
    The following filters are supported:
    - `qIntegration` (fuzzy search on title or vendor)

    **Examples**:
    - List integrations where app name or vendor match `googl`: `q="googl"`.
    """
    def __init__(
        self,
        *,
        page_size: builtins.int | None = ...,
        page_token: builtins.str | None = ...,
        filter: builtins.str | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["_filter", b"_filter", "_page_size", b"_page_size", "_page_token", b"_page_token", "filter", b"filter", "page_size", b"page_size", "page_token", b"page_token"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["_filter", b"_filter", "_page_size", b"_page_size", "_page_token", b"_page_token", "filter", b"filter", "page_size", b"page_size", "page_token", b"page_token"]) -> None: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_filter", b"_filter"]) -> typing_extensions.Literal["filter"] | None: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_page_size", b"_page_size"]) -> typing_extensions.Literal["page_size"] | None: ...
    @typing.overload
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_page_token", b"_page_token"]) -> typing_extensions.Literal["page_token"] | None: ...

global___ListIntegrationsRequest = ListIntegrationsRequest

@typing_extensions.final
class ListIntegrationsResponse(google.protobuf.message.Message):
    """ListIntegrationsResponse contains a paginated list of integrations."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    INTEGRATIONS_FIELD_NUMBER: builtins.int
    NEXT_PAGE_TOKEN_FIELD_NUMBER: builtins.int
    TOTAL_SIZE_FIELD_NUMBER: builtins.int
    @property
    def integrations(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___Integration]:
        """A list of integrations matching the request parameters."""
    next_page_token: builtins.str
    """Next page token."""
    total_size: builtins.int
    """Total number of items."""
    def __init__(
        self,
        *,
        integrations: collections.abc.Iterable[global___Integration] | None = ...,
        next_page_token: builtins.str = ...,
        total_size: builtins.int = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["integrations", b"integrations", "next_page_token", b"next_page_token", "total_size", b"total_size"]) -> None: ...

global___ListIntegrationsResponse = ListIntegrationsResponse

@typing_extensions.final
class GetIntegrationRequest(google.protobuf.message.Message):
    """GetIntegrationRequest represents a request to view the details of an
    integration.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    INTEGRATION_ID_FIELD_NUMBER: builtins.int
    VIEW_FIELD_NUMBER: builtins.int
    integration_id: builtins.str
    """Integration ID."""
    view: vdp.pipeline.v1beta.common_pb2.View.ValueType
    """View allows clients to specify the desired view in the response."""
    def __init__(
        self,
        *,
        integration_id: builtins.str = ...,
        view: vdp.pipeline.v1beta.common_pb2.View.ValueType | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["_view", b"_view", "view", b"view"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["_view", b"_view", "integration_id", b"integration_id", "view", b"view"]) -> None: ...
    def WhichOneof(self, oneof_group: typing_extensions.Literal["_view", b"_view"]) -> typing_extensions.Literal["view"] | None: ...

global___GetIntegrationRequest = GetIntegrationRequest

@typing_extensions.final
class GetIntegrationResponse(google.protobuf.message.Message):
    """GetIntegrationResponse contains the requested integration."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    INTEGRATION_FIELD_NUMBER: builtins.int
    @property
    def integration(self) -> global___Integration:
        """The requested integration."""
    def __init__(
        self,
        *,
        integration: global___Integration | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["integration", b"integration"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["integration", b"integration"]) -> None: ...

global___GetIntegrationResponse = GetIntegrationResponse

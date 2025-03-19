"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
UPDATE NOTICE

If you make changes to the proto definitions (add, update, delete)s, please
also update VersionUtil.java and apiversion.properties as described in the
projects README.md
"""

import builtins
import collections.abc
import google.protobuf.any_pb2
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import hansken_extraction_plugin.framework.DataMessages_pb2
import sys
import typing

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class _RpcSearchScope:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _RpcSearchScopeEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_RpcSearchScope.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    Project: _RpcSearchScope.ValueType  # 0
    """default if not set in older plugin versions"""
    Image: _RpcSearchScope.ValueType  # 1

class RpcSearchScope(_RpcSearchScope, metaclass=_RpcSearchScopeEnumTypeWrapper):
    """*
    RpcSearchRequest search scope options.
    """

Project: RpcSearchScope.ValueType  # 0
"""default if not set in older plugin versions"""
Image: RpcSearchScope.ValueType  # 1
global___RpcSearchScope = RpcSearchScope

@typing.final
class RpcSync(google.protobuf.message.Message):
    """*
    This proto file contains message definitions which represent method calls, such as reading
    a certain amount of bytes from the processed data sequence. As seen in ExtractionPluginService,
    we have a single stream between client and server when processing a trace. These messages are
    sent through this stream in order to invoke a method on the other side.

    *
    Synchronization request.
    Can be used to control message flow. The plugin server can send this message to
    the plugin client. The server can then block until the client has acknowledged the
    sync-request.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___RpcSync = RpcSync

@typing.final
class RpcSyncAck(google.protobuf.message.Message):
    """*
    Acknowledges a synchronization request.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    INPROGRESSTRACES_FIELD_NUMBER: builtins.int
    inProgressTraces: builtins.int
    def __init__(
        self,
        *,
        inProgressTraces: builtins.int = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["inProgressTraces", b"inProgressTraces"]) -> None: ...

global___RpcSyncAck = RpcSyncAck

@typing.final
class RpcStart(google.protobuf.message.Message):
    """*
    Start is the first message from the plugin client to the plugin server.

    After receiving this message, the extraction plugin starts processing a
    trace. The start message already contains information of the trace to
    process.

    The client should send as much of the required information to the server for
    performance reasons: there are no additional round-trips required to get
    information from server to client.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    TRACE_FIELD_NUMBER: builtins.int
    DATACONTEXT_FIELD_NUMBER: builtins.int
    @property
    def trace(self) -> hansken_extraction_plugin.framework.DataMessages_pb2.RpcTrace: ...
    @property
    def dataContext(self) -> hansken_extraction_plugin.framework.DataMessages_pb2.RpcDataContext: ...
    def __init__(
        self,
        *,
        trace: hansken_extraction_plugin.framework.DataMessages_pb2.RpcTrace | None = ...,
        dataContext: hansken_extraction_plugin.framework.DataMessages_pb2.RpcDataContext | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["dataContext", b"dataContext", "trace", b"trace"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["dataContext", b"dataContext", "trace", b"trace"]) -> None: ...

global___RpcStart = RpcStart

@typing.final
class RpcBatchUpdate(google.protobuf.message.Message):
    """*
    Update which contains actions to execute while the processing of the plugin
    is still running (e.g. due to buffered updates being flushed). They can contain
    for example a batch of child traces to add to the result.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ACTIONS_FIELD_NUMBER: builtins.int
    @property
    def actions(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[google.protobuf.any_pb2.Any]: ...
    def __init__(
        self,
        *,
        actions: collections.abc.Iterable[google.protobuf.any_pb2.Any] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["actions", b"actions"]) -> None: ...

global___RpcBatchUpdate = RpcBatchUpdate

@typing.final
class RpcProfile(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    @typing.final
    class ProfileInt64sEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: builtins.str
        value: builtins.int
        def __init__(
            self,
            *,
            key: builtins.str = ...,
            value: builtins.int = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing.Literal["key", b"key", "value", b"value"]) -> None: ...

    @typing.final
    class ProfileDoublesEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor

        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: builtins.str
        value: builtins.float
        def __init__(
            self,
            *,
            key: builtins.str = ...,
            value: builtins.float = ...,
        ) -> None: ...
        def ClearField(self, field_name: typing.Literal["key", b"key", "value", b"value"]) -> None: ...

    PROFILE_INT64S_FIELD_NUMBER: builtins.int
    PROFILE_DOUBLES_FIELD_NUMBER: builtins.int
    @property
    def profile_int64s(self) -> google.protobuf.internal.containers.ScalarMap[builtins.str, builtins.int]: ...
    @property
    def profile_doubles(self) -> google.protobuf.internal.containers.ScalarMap[builtins.str, builtins.float]: ...
    def __init__(
        self,
        *,
        profile_int64s: collections.abc.Mapping[builtins.str, builtins.int] | None = ...,
        profile_doubles: collections.abc.Mapping[builtins.str, builtins.float] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["profile_doubles", b"profile_doubles", "profile_int64s", b"profile_int64s"]) -> None: ...

global___RpcProfile = RpcProfile

@typing.final
class RpcFinish(google.protobuf.message.Message):
    """*
    Signal from server to client that processing the trace is finished.
    The message may contain a (final) set of trace update actions.
    When receiving this request, the client should close the communication
    channel.

    The server closes the gRPC stream directly after sending the Finish message.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    UPDATE_FIELD_NUMBER: builtins.int
    PROFILE_FIELD_NUMBER: builtins.int
    @property
    def update(self) -> global___RpcBatchUpdate: ...
    @property
    def profile(self) -> global___RpcProfile: ...
    def __init__(
        self,
        *,
        update: global___RpcBatchUpdate | None = ...,
        profile: global___RpcProfile | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["profile", b"profile", "update", b"update"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["profile", b"profile", "update", b"update"]) -> None: ...

global___RpcFinish = RpcFinish

@typing.final
class RpcPartialFinishWithError(google.protobuf.message.Message):
    """*
    This response behaves the same as {@link org.hansken.extraction.plugin.grpc.RpcFinish}, with the exception
    that it is only used when an error occurs during the processing of a trace.

    The response contains a partial list of actions, a (error)statusCode and an errorDescription.

    The server processes the partial results towards the client, and throws an exception with the
    statusCode & errorDescription which should be handled client-side.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ACTIONS_FIELD_NUMBER: builtins.int
    STATUSCODE_FIELD_NUMBER: builtins.int
    ERRORDESCRIPTION_FIELD_NUMBER: builtins.int
    PROFILE_FIELD_NUMBER: builtins.int
    statusCode: builtins.str
    errorDescription: builtins.str
    @property
    def actions(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[google.protobuf.any_pb2.Any]: ...
    @property
    def profile(self) -> global___RpcProfile: ...
    def __init__(
        self,
        *,
        actions: collections.abc.Iterable[google.protobuf.any_pb2.Any] | None = ...,
        statusCode: builtins.str = ...,
        errorDescription: builtins.str = ...,
        profile: global___RpcProfile | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["profile", b"profile"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["actions", b"actions", "errorDescription", b"errorDescription", "profile", b"profile", "statusCode", b"statusCode"]) -> None: ...

global___RpcPartialFinishWithError = RpcPartialFinishWithError

@typing.final
class RpcEnrichTrace(google.protobuf.message.Message):
    """*
    The following messages are used to create new child traces and updating
    existing traces. For example, say we create a simple trace tree as follows
    (each node is represented by its id and the given name):

      0 (folder.name = root)
      |____ 0-0 (folder.name = folder0)
    |     |____ 0-0-0 (file.name = file0)
      |
      |____ 0-1 (file.name = file1)

    Then the flow of the messages could be:
    Hansken <<-  ExtractionPlugin : enrichTrace (0, {'folder.name', 'root'})
    Hansken <<-  ExtractionPlugin : beginChild  (0-0)
    Hansken <<-  ExtractionPlugin : enrichTrace (0-0, {'folder.name', 'folder0'})
    Hansken <<-  ExtractionPlugin : beginChild  (0-0-0)
    Hansken <<-  ExtractionPlugin : enrichTrace (0-0-0, {'file.name', 'file0'})
    Hansken <<-  ExtractionPlugin : finishChild (0-0-0)
    Hansken <<-  ExtractionPlugin : finishChild (0-0)
    Hansken <<-  ExtractionPlugin : beginChild  (0-1)
    Hansken <<-  ExtractionPlugin : enrichTrace (0-1, {'file.name', 'file1'})
    Hansken <<-  ExtractionPlugin : finishChild (0-1)

    Note that setting the name on the root trace could also be sent as the last request,
    because we would again be in scope of the root trace.

    Also note that the plugin will wait for acknowledgement of Hansken (or any other client).
    These requests can (and will) be batched.

    *
    Update the trace currently being processed with the information in the given trace. Note that
    this trace only contains new properties not already set on the trace being processed (i.e. the
    properties which were already set on the trace in RpcStart).
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    TRACE_FIELD_NUMBER: builtins.int
    @property
    def trace(self) -> hansken_extraction_plugin.framework.DataMessages_pb2.RpcTrace: ...
    def __init__(
        self,
        *,
        trace: hansken_extraction_plugin.framework.DataMessages_pb2.RpcTrace | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["trace", b"trace"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["trace", b"trace"]) -> None: ...

global___RpcEnrichTrace = RpcEnrichTrace

@typing.final
class RpcBeginChild(google.protobuf.message.Message):
    """*
    Signal that we are in the scope of a newly created child.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ID_FIELD_NUMBER: builtins.int
    NAME_FIELD_NUMBER: builtins.int
    id: builtins.str
    name: builtins.str
    def __init__(
        self,
        *,
        id: builtins.str = ...,
        name: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["id", b"id", "name", b"name"]) -> None: ...

global___RpcBeginChild = RpcBeginChild

@typing.final
class RpcFinishChild(google.protobuf.message.Message):
    """
    Signal that we exited the last created child scope.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ID_FIELD_NUMBER: builtins.int
    id: builtins.str
    def __init__(
        self,
        *,
        id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["id", b"id"]) -> None: ...

global___RpcFinishChild = RpcFinishChild

@typing.final
class RpcRead(google.protobuf.message.Message):
    """*
    Read data from the data sequence which answers to the traceUid with the specified dataType.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    POSITION_FIELD_NUMBER: builtins.int
    COUNT_FIELD_NUMBER: builtins.int
    TRACEID_FIELD_NUMBER: builtins.int
    DATATYPE_FIELD_NUMBER: builtins.int
    TRACEUID_FIELD_NUMBER: builtins.int
    position: builtins.int
    count: builtins.int
    traceId: builtins.str
    """*
    The id of the trace.
    @deprecated since version 0.4.9: use traceUid instead. Different traces from different images may use the same traceId,
    so using the traceId to identify data may cause wrong data to return.
    """
    dataType: builtins.str
    traceUid: builtins.str
    def __init__(
        self,
        *,
        position: builtins.int = ...,
        count: builtins.int = ...,
        traceId: builtins.str = ...,
        dataType: builtins.str = ...,
        traceUid: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["count", b"count", "dataType", b"dataType", "position", b"position", "traceId", b"traceId", "traceUid", b"traceUid"]) -> None: ...

global___RpcRead = RpcRead

@typing.final
class RpcBeginDataStream(google.protobuf.message.Message):
    """*
    Signal that we are starting to write a data stream of given type.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    TRACEID_FIELD_NUMBER: builtins.int
    DATATYPE_FIELD_NUMBER: builtins.int
    ENCODING_FIELD_NUMBER: builtins.int
    traceId: builtins.str
    dataType: builtins.str
    encoding: builtins.str
    """*
    Optional encoding of the data, if set, the receiver can assume that
    the bytes are encoded text, encoded with with given encoding.
    """
    def __init__(
        self,
        *,
        traceId: builtins.str = ...,
        dataType: builtins.str = ...,
        encoding: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["dataType", b"dataType", "encoding", b"encoding", "traceId", b"traceId"]) -> None: ...

global___RpcBeginDataStream = RpcBeginDataStream

@typing.final
class RpcWriteDataStream(google.protobuf.message.Message):
    """*
    Message containing a chunk of data from the currently written data stream.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    TRACEID_FIELD_NUMBER: builtins.int
    DATATYPE_FIELD_NUMBER: builtins.int
    DATA_FIELD_NUMBER: builtins.int
    traceId: builtins.str
    dataType: builtins.str
    data: builtins.bytes
    def __init__(
        self,
        *,
        traceId: builtins.str = ...,
        dataType: builtins.str = ...,
        data: builtins.bytes = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["data", b"data", "dataType", b"dataType", "traceId", b"traceId"]) -> None: ...

global___RpcWriteDataStream = RpcWriteDataStream

@typing.final
class RpcFinishDataStream(google.protobuf.message.Message):
    """*
    Signal that we finished writing the data stream of given type.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    TRACEID_FIELD_NUMBER: builtins.int
    DATATYPE_FIELD_NUMBER: builtins.int
    traceId: builtins.str
    dataType: builtins.str
    def __init__(
        self,
        *,
        traceId: builtins.str = ...,
        dataType: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["dataType", b"dataType", "traceId", b"traceId"]) -> None: ...

global___RpcFinishDataStream = RpcFinishDataStream

@typing.final
class RpcSearchRequest(google.protobuf.message.Message):
    """*
    A search request to retrieve traces. The count is an integer representing the number of traces to return and the query is
    a HQL query used to find matching traces.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    COUNT_FIELD_NUMBER: builtins.int
    QUERY_FIELD_NUMBER: builtins.int
    SCOPE_FIELD_NUMBER: builtins.int
    count: builtins.int
    query: builtins.str
    scope: global___RpcSearchScope.ValueType
    def __init__(
        self,
        *,
        count: builtins.int = ...,
        query: builtins.str = ...,
        scope: global___RpcSearchScope.ValueType = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["count", b"count", "query", b"query", "scope", b"scope"]) -> None: ...

global___RpcSearchRequest = RpcSearchRequest

@typing.final
class RpcSearchResult(google.protobuf.message.Message):
    """*
    Search response containing the queried traces and the total number of found traces. This number
    may be higher than the count provided with the RpcSearchRequest.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    TOTALRESULTS_FIELD_NUMBER: builtins.int
    TRACES_FIELD_NUMBER: builtins.int
    totalResults: builtins.int
    @property
    def traces(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[hansken_extraction_plugin.framework.DataMessages_pb2.RpcSearchTrace]: ...
    def __init__(
        self,
        *,
        totalResults: builtins.int = ...,
        traces: collections.abc.Iterable[hansken_extraction_plugin.framework.DataMessages_pb2.RpcSearchTrace] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["totalResults", b"totalResults", "traces", b"traces"]) -> None: ...

global___RpcSearchResult = RpcSearchResult

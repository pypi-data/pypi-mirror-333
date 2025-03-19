"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import artifact.artifact.v1alpha.chunk_pb2
import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import sys

if sys.version_info >= (3, 8):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing_extensions.final
class QuestionAnsweringRequest(google.protobuf.message.Message):
    """QuestionAnsweringRequest"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    NAMESPACE_ID_FIELD_NUMBER: builtins.int
    CATALOG_ID_FIELD_NUMBER: builtins.int
    QUESTION_FIELD_NUMBER: builtins.int
    TOP_K_FIELD_NUMBER: builtins.int
    namespace_id: builtins.str
    """id of the namespace"""
    catalog_id: builtins.str
    """id of the catalog"""
    question: builtins.str
    """question to be answered"""
    top_k: builtins.int
    """top k default to 5"""
    def __init__(
        self,
        *,
        namespace_id: builtins.str = ...,
        catalog_id: builtins.str = ...,
        question: builtins.str = ...,
        top_k: builtins.int = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["catalog_id", b"catalog_id", "namespace_id", b"namespace_id", "question", b"question", "top_k", b"top_k"]) -> None: ...

global___QuestionAnsweringRequest = QuestionAnsweringRequest

@typing_extensions.final
class QuestionAnsweringResponse(google.protobuf.message.Message):
    """QuestionAnsweringResponse"""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ANSWER_FIELD_NUMBER: builtins.int
    SIMILAR_CHUNKS_FIELD_NUMBER: builtins.int
    answer: builtins.str
    """answer to the question"""
    @property
    def similar_chunks(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[artifact.artifact.v1alpha.chunk_pb2.SimilarityChunk]:
        """chunks"""
    def __init__(
        self,
        *,
        answer: builtins.str = ...,
        similar_chunks: collections.abc.Iterable[artifact.artifact.v1alpha.chunk_pb2.SimilarityChunk] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["answer", b"answer", "similar_chunks", b"similar_chunks"]) -> None: ...

global___QuestionAnsweringResponse = QuestionAnsweringResponse

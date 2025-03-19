"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.internal.enum_type_wrapper
import sys
import typing

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class _Task:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _TaskEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_Task.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    TASK_UNSPECIFIED: _Task.ValueType  # 0
    """Unspecified."""
    TASK_CLASSIFICATION: _Task.ValueType  # 1
    """Image Classification - classify images into predefined categories."""
    TASK_DETECTION: _Task.ValueType  # 2
    """Object Detection - detect and localize multiple objects in images."""
    TASK_KEYPOINT: _Task.ValueType  # 3
    """Keypoint Detection - detect and localize multiple keypoints of objects in images."""
    TASK_OCR: _Task.ValueType  # 4
    """OCR (Optical Character Recognition) - detect and recognize text in images."""
    TASK_INSTANCE_SEGMENTATION: _Task.ValueType  # 5
    """Instance Segmentation - detect, localize and delineate multiple objects in images."""
    TASK_SEMANTIC_SEGMENTATION: _Task.ValueType  # 6
    """Semantic Segmentation - classify image pixels into predefined categories."""
    TASK_TEXT_TO_IMAGE: _Task.ValueType  # 7
    """Text to Image - generate images from input text prompts."""
    TASK_IMAGE_TO_IMAGE: _Task.ValueType  # 11
    """Image to Image - generate an image from another image."""
    TASK_EMBEDDING: _Task.ValueType  # 12
    """Embedding - generate an embedding (a representation as coordinates) from a multimodal input."""
    TASK_SPEECH_RECOGNITION: _Task.ValueType  # 13
    """Speech Recognition - transcribe the words in an audio input."""
    TASK_CHAT: _Task.ValueType  # 14
    """Conversational Text Generation - generate text as responses to a dialog input."""
    TASK_COMPLETION: _Task.ValueType  # 15
    """Completion Text Generation - generate text following the input prompt."""
    TASK_CUSTOM: _Task.ValueType  # 16
    """Custom - custom task type for free form input/output."""

class Task(_Task, metaclass=_TaskEnumTypeWrapper):
    """Task enumerates the AI task that a model is designed to solve."""

TASK_UNSPECIFIED: Task.ValueType  # 0
"""Unspecified."""
TASK_CLASSIFICATION: Task.ValueType  # 1
"""Image Classification - classify images into predefined categories."""
TASK_DETECTION: Task.ValueType  # 2
"""Object Detection - detect and localize multiple objects in images."""
TASK_KEYPOINT: Task.ValueType  # 3
"""Keypoint Detection - detect and localize multiple keypoints of objects in images."""
TASK_OCR: Task.ValueType  # 4
"""OCR (Optical Character Recognition) - detect and recognize text in images."""
TASK_INSTANCE_SEGMENTATION: Task.ValueType  # 5
"""Instance Segmentation - detect, localize and delineate multiple objects in images."""
TASK_SEMANTIC_SEGMENTATION: Task.ValueType  # 6
"""Semantic Segmentation - classify image pixels into predefined categories."""
TASK_TEXT_TO_IMAGE: Task.ValueType  # 7
"""Text to Image - generate images from input text prompts."""
TASK_IMAGE_TO_IMAGE: Task.ValueType  # 11
"""Image to Image - generate an image from another image."""
TASK_EMBEDDING: Task.ValueType  # 12
"""Embedding - generate an embedding (a representation as coordinates) from a multimodal input."""
TASK_SPEECH_RECOGNITION: Task.ValueType  # 13
"""Speech Recognition - transcribe the words in an audio input."""
TASK_CHAT: Task.ValueType  # 14
"""Conversational Text Generation - generate text as responses to a dialog input."""
TASK_COMPLETION: Task.ValueType  # 15
"""Completion Text Generation - generate text following the input prompt."""
TASK_CUSTOM: Task.ValueType  # 16
"""Custom - custom task type for free form input/output."""
global___Task = Task

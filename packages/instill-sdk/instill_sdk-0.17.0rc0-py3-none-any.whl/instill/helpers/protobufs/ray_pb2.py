# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ray.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\tray.proto\x12\x06ray.v1\x1a\x1cgoogle/protobuf/struct.proto\";\n\x0b\x43\x61llRequest\x12,\n\x0btask_inputs\x18\x01 \x03(\x0b\x32\x17.google.protobuf.Struct\"=\n\x0c\x43\x61llResponse\x12-\n\x0ctask_outputs\x18\x01 \x03(\x0b\x32\x17.google.protobuf.Struct2C\n\nRayService\x12\x35\n\x08__call__\x12\x13.ray.v1.CallRequest\x1a\x14.ray.v1.CallResponseB\rZ\x0b./rayserverb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'ray_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z\013./rayserver'
  _globals['_CALLREQUEST']._serialized_start=51
  _globals['_CALLREQUEST']._serialized_end=110
  _globals['_CALLRESPONSE']._serialized_start=112
  _globals['_CALLRESPONSE']._serialized_end=173
  _globals['_RAYSERVICE']._serialized_start=175
  _globals['_RAYSERVICE']._serialized_end=242
# @@protoc_insertion_point(module_scope)

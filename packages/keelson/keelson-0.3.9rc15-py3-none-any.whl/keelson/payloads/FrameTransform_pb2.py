# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: FrameTransform.proto
# Protobuf Python Version: 5.27.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    0,
    '',
    'FrameTransform.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import Quaternion_pb2 as Quaternion__pb2
from . import Vector_pb2 as Vector__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x14\x46rameTransform.proto\x12\x08\x66oxglove\x1a\x10Quaternion.proto\x1a\x0cVector.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"?\n\x0f\x46rameTransforms\x12,\n\ntransforms\x18\x01 \x03(\x0b\x32\x18.foxglove.FrameTransform\"\xc0\x01\n\x0e\x46rameTransform\x12-\n\ttimestamp\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x17\n\x0fparent_frame_id\x18\x02 \x01(\t\x12\x16\n\x0e\x63hild_frame_id\x18\x03 \x01(\t\x12&\n\x0btranslation\x18\x04 \x01(\x0b\x32\x11.foxglove.Vector3\x12&\n\x08rotation\x18\x05 \x01(\x0b\x32\x14.foxglove.Quaternionb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'FrameTransform_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_FRAMETRANSFORMS']._serialized_start=99
  _globals['_FRAMETRANSFORMS']._serialized_end=162
  _globals['_FRAMETRANSFORM']._serialized_start=165
  _globals['_FRAMETRANSFORM']._serialized_end=357
# @@protoc_insertion_point(module_scope)

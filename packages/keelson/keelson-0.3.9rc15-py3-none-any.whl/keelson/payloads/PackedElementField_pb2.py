# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: PackedElementField.proto
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
    'PackedElementField.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x18PackedElementField.proto\x12\x08\x66oxglove\"\xe3\x01\n\x12PackedElementField\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0e\n\x06offset\x18\x02 \x01(\x07\x12\x36\n\x04type\x18\x03 \x01(\x0e\x32(.foxglove.PackedElementField.NumericType\"w\n\x0bNumericType\x12\x0b\n\x07UNKNOWN\x10\x00\x12\t\n\x05UINT8\x10\x01\x12\x08\n\x04INT8\x10\x02\x12\n\n\x06UINT16\x10\x03\x12\t\n\x05INT16\x10\x04\x12\n\n\x06UINT32\x10\x05\x12\t\n\x05INT32\x10\x06\x12\x0b\n\x07\x46LOAT32\x10\x07\x12\x0b\n\x07\x46LOAT64\x10\x08\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'PackedElementField_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_PACKEDELEMENTFIELD']._serialized_start=39
  _globals['_PACKEDELEMENTFIELD']._serialized_end=266
  _globals['_PACKEDELEMENTFIELD_NUMERICTYPE']._serialized_start=147
  _globals['_PACKEDELEMENTFIELD_NUMERICTYPE']._serialized_end=266
# @@protoc_insertion_point(module_scope)

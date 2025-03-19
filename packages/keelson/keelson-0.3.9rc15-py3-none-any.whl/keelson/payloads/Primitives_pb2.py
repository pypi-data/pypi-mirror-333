# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: Primitives.proto
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
    'Primitives.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10Primitives.proto\x12\x12keelson.primitives\x1a\x1fgoogle/protobuf/timestamp.proto\"P\n\x10TimestampedBytes\x12-\n\ttimestamp\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\r\n\x05value\x18\x02 \x01(\x0c\"\x84\x01\n\x11TimestampedDouble\x12-\n\ttimestamp\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\r\n\x05value\x18\x02 \x01(\x01\x12\x31\n\x04unit\x18\x03 \x01(\x0b\x32#.keelson.primitives.MeasurementUnit\"\x83\x01\n\x10TimestampedFloat\x12-\n\ttimestamp\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\r\n\x05value\x18\x02 \x01(\x02\x12\x31\n\x04unit\x18\x03 \x01(\x0b\x32#.keelson.primitives.MeasurementUnit\"\x81\x01\n\x0eTimestampedInt\x12-\n\ttimestamp\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\r\n\x05value\x18\x02 \x01(\x05\x12\x31\n\x04unit\x18\x03 \x01(\x0b\x32#.keelson.primitives.MeasurementUnit\"\x84\x01\n\x11TimestampedString\x12-\n\ttimestamp\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\r\n\x05value\x18\x02 \x01(\t\x12\x31\n\x04unit\x18\x03 \x01(\x0b\x32#.keelson.primitives.MeasurementUnit\"\xbb\x04\n\x0fMeasurementUnit\x12\x36\n\x04unit\x18\x02 \x01(\x0e\x32(.keelson.primitives.MeasurementUnit.Unit\"\xef\x03\n\x04Unit\x12\x0b\n\x07UNKNOWN\x10\x00\x12\x0b\n\x07\x44\x45GREES\x10\x01\x12\x08\n\x04\x46\x45\x45T\x10\x02\x12\x0e\n\nKILOMETERS\x10\x03\x12\n\n\x06METERS\x10\x04\x12\t\n\x05MILES\x10\x05\x12\x12\n\x0eNAUTICAL_MILES\x10\x06\x12\t\n\x05YARDS\x10\x07\x12\x0b\n\x07\x41MPERES\x10\x08\x12\n\n\x06JOULES\x10\t\x12\n\n\x06LUMENS\x10\n\x12\x07\n\x03LUX\x10\x0b\x12\x0b\n\x07NEWTONS\x10\x0c\x12\x08\n\x04OHMS\x10\r\x12\t\n\x05VOLTS\x10\x0e\x12\t\n\x05WATTS\x10\x0f\x12\t\n\x05HERTZ\x10\x10\x12\t\n\x05GRAMS\x10\x11\x12\n\n\x06OUNCES\x10\x12\x12\n\n\x06POUNDS\x10\x13\x12\x10\n\x0cHECTOPASCALS\x10\x14\x12\x15\n\x11INCHES_OF_MERCURY\x10\x15\x12\r\n\tMILLIBARS\x10\x16\x12\x0b\n\x07PASCALS\x10\x17\x12\x17\n\x13KILOMETERS_PER_HOUR\x10\x18\x12\t\n\x05KNOTS\x10\x19\x12\x15\n\x11METERS_PER_SECOND\x10\x1a\x12\x0b\n\x07\x43\x45LSIUS\x10\x1b\x12\x0e\n\nFAHRENHEIT\x10\x1c\x12\n\n\x06KELVIN\x10\x1d\x12\x0b\n\x07GALLONS\x10\x1e\x12\n\n\x06LITERS\x10\x1f\x12\x0b\n\x07\x43\x41NDELA\x10 \x12\x0c\n\x08\x44\x45\x43IBELS\x10!\x12\x0e\n\nPERCENTAGE\x10\"\x12\x07\n\x03RPM\x10#b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'Primitives_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_TIMESTAMPEDBYTES']._serialized_start=73
  _globals['_TIMESTAMPEDBYTES']._serialized_end=153
  _globals['_TIMESTAMPEDDOUBLE']._serialized_start=156
  _globals['_TIMESTAMPEDDOUBLE']._serialized_end=288
  _globals['_TIMESTAMPEDFLOAT']._serialized_start=291
  _globals['_TIMESTAMPEDFLOAT']._serialized_end=422
  _globals['_TIMESTAMPEDINT']._serialized_start=425
  _globals['_TIMESTAMPEDINT']._serialized_end=554
  _globals['_TIMESTAMPEDSTRING']._serialized_start=557
  _globals['_TIMESTAMPEDSTRING']._serialized_end=689
  _globals['_MEASUREMENTUNIT']._serialized_start=692
  _globals['_MEASUREMENTUNIT']._serialized_end=1263
  _globals['_MEASUREMENTUNIT_UNIT']._serialized_start=768
  _globals['_MEASUREMENTUNIT_UNIT']._serialized_end=1263
# @@protoc_insertion_point(module_scope)

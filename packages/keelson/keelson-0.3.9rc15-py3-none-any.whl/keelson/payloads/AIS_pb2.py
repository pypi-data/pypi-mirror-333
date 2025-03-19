# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: AIS.proto
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
    'AIS.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\tAIS.proto\x12\x0bkeelson.ais\x1a\x1fgoogle/protobuf/timestamp.proto\"j\n\x0b\x41ISMessages\x12-\n\ttimestamp\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12,\n\x0b\x41ISMessages\x18\x02 \x03(\x0b\x32\x17.keelson.ais.AISMessage\"g\n\nAISMessage\x12-\n\ttimestamp\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12*\n\nais_vessel\x18\x02 \x01(\x0b\x32\x16.keelson.ais.AISVessel\"\xb0\x03\n\tAISVessel\x12-\n\ttimestamp\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x0c\n\x04mmsi\x18\x02 \x01(\x03\x12\x0f\n\x07\x63lass_a\x18\x03 \x01(\x08\x12\x15\n\rstatics_valid\x18\x04 \x01(\x08\x12\x11\n\tsog_knots\x18\x05 \x01(\x02\x12\x19\n\x11position_accuracy\x18\x06 \x01(\x05\x12\x17\n\x0flatitude_degree\x18\x07 \x01(\x01\x12\x18\n\x10longitude_degree\x18\x08 \x01(\x01\x12\x12\n\ncog_degree\x18\t \x01(\x02\x12\x1b\n\x13true_heading_degree\x18\n \x01(\x05\x12.\n\x07statics\x18\x0b \x01(\x0b\x32\x1d.keelson.ais.AISVesselStatics\x12>\n\x10position_class_a\x18\x0c \x01(\x0b\x32$.keelson.ais.AISVesselPositionClassA\x12<\n\x0fstatics_class_a\x18\r \x01(\x0b\x32#.keelson.ais.AISVesselStaticsClassA\"\xd1\x01\n\x10\x41ISVesselStatics\x12-\n\ttimestamp\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x10\n\x08\x63\x61llsign\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x16\n\x0etype_and_cargo\x18\x04 \x01(\x05\x12\x14\n\x0c\x64im_a_meters\x18\x05 \x01(\x05\x12\x14\n\x0c\x64im_b_meters\x18\x06 \x01(\x05\x12\x14\n\x0c\x64im_c_meters\x18\x07 \x01(\x05\x12\x14\n\x0c\x64im_d_meters\x18\x08 \x01(\x05\"\xf1\x01\n\x16\x41ISVesselStaticsClassA\x12-\n\ttimestamp\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x13\n\x0b\x61is_version\x18\x02 \x01(\x05\x12\x0b\n\x03imo\x18\x03 \x01(\x05\x12\x10\n\x08\x66ix_type\x18\x04 \x01(\x05\x12\x11\n\teta_month\x18\x05 \x01(\x05\x12\x0f\n\x07\x65ta_day\x18\x06 \x01(\x05\x12\x10\n\x08\x65ta_hour\x18\x07 \x01(\x05\x12\x12\n\neta_minute\x18\x08 \x01(\x05\x12\x15\n\rdraught_meter\x18\t \x01(\x02\x12\x13\n\x0b\x64\x65stination\x18\n \x01(\t\"\xad\x01\n\x17\x41ISVesselPositionClassA\x12-\n\ttimestamp\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x12\n\nnav_status\x18\x02 \x01(\x05\x12\x16\n\x0erot_over_range\x18\x03 \x01(\x08\x12\x0f\n\x07rot_raw\x18\x04 \x01(\x05\x12\x0b\n\x03rot\x18\x05 \x01(\x02\x12\x19\n\x11special_manoeuver\x18\x06 \x01(\x05\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'AIS_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_AISMESSAGES']._serialized_start=59
  _globals['_AISMESSAGES']._serialized_end=165
  _globals['_AISMESSAGE']._serialized_start=167
  _globals['_AISMESSAGE']._serialized_end=270
  _globals['_AISVESSEL']._serialized_start=273
  _globals['_AISVESSEL']._serialized_end=705
  _globals['_AISVESSELSTATICS']._serialized_start=708
  _globals['_AISVESSELSTATICS']._serialized_end=917
  _globals['_AISVESSELSTATICSCLASSA']._serialized_start=920
  _globals['_AISVESSELSTATICSCLASSA']._serialized_end=1161
  _globals['_AISVESSELPOSITIONCLASSA']._serialized_start=1164
  _globals['_AISVESSELPOSITIONCLASSA']._serialized_end=1337
# @@protoc_insertion_point(module_scope)

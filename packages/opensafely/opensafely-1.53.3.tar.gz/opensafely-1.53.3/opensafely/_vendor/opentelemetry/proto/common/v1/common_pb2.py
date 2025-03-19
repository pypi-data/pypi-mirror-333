# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: opentelemetry/proto/common/v1/common.proto
"""Generated protocol buffer code."""
from opensafely._vendor.google.protobuf import descriptor as _descriptor
from opensafely._vendor.google.protobuf import message as _message
from opensafely._vendor.google.protobuf import reflection as _reflection
from opensafely._vendor.google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='opentelemetry/proto/common/v1/common.proto',
  package='opentelemetry.proto.common.v1',
  syntax='proto3',
  serialized_options=b'\n io.opentelemetry.proto.common.v1B\013CommonProtoP\001Z(go.opentelemetry.io/proto/otlp/common/v1',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n*opentelemetry/proto/common/v1/common.proto\x12\x1dopentelemetry.proto.common.v1\"\x8c\x02\n\x08\x41nyValue\x12\x16\n\x0cstring_value\x18\x01 \x01(\tH\x00\x12\x14\n\nbool_value\x18\x02 \x01(\x08H\x00\x12\x13\n\tint_value\x18\x03 \x01(\x03H\x00\x12\x16\n\x0c\x64ouble_value\x18\x04 \x01(\x01H\x00\x12@\n\x0b\x61rray_value\x18\x05 \x01(\x0b\x32).opentelemetry.proto.common.v1.ArrayValueH\x00\x12\x43\n\x0ckvlist_value\x18\x06 \x01(\x0b\x32+.opentelemetry.proto.common.v1.KeyValueListH\x00\x12\x15\n\x0b\x62ytes_value\x18\x07 \x01(\x0cH\x00\x42\x07\n\x05value\"E\n\nArrayValue\x12\x37\n\x06values\x18\x01 \x03(\x0b\x32\'.opentelemetry.proto.common.v1.AnyValue\"G\n\x0cKeyValueList\x12\x37\n\x06values\x18\x01 \x03(\x0b\x32\'.opentelemetry.proto.common.v1.KeyValue\"O\n\x08KeyValue\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x36\n\x05value\x18\x02 \x01(\x0b\x32\'.opentelemetry.proto.common.v1.AnyValue\";\n\x16InstrumentationLibrary\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0f\n\x07version\x18\x02 \x01(\t:\x02\x18\x01\"5\n\x14InstrumentationScope\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0f\n\x07version\x18\x02 \x01(\tB[\n io.opentelemetry.proto.common.v1B\x0b\x43ommonProtoP\x01Z(go.opentelemetry.io/proto/otlp/common/v1b\x06proto3'
)




_ANYVALUE = _descriptor.Descriptor(
  name='AnyValue',
  full_name='opentelemetry.proto.common.v1.AnyValue',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='string_value', full_name='opentelemetry.proto.common.v1.AnyValue.string_value', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='bool_value', full_name='opentelemetry.proto.common.v1.AnyValue.bool_value', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='int_value', full_name='opentelemetry.proto.common.v1.AnyValue.int_value', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='double_value', full_name='opentelemetry.proto.common.v1.AnyValue.double_value', index=3,
      number=4, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='array_value', full_name='opentelemetry.proto.common.v1.AnyValue.array_value', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='kvlist_value', full_name='opentelemetry.proto.common.v1.AnyValue.kvlist_value', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='bytes_value', full_name='opentelemetry.proto.common.v1.AnyValue.bytes_value', index=6,
      number=7, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='value', full_name='opentelemetry.proto.common.v1.AnyValue.value',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=78,
  serialized_end=346,
)


_ARRAYVALUE = _descriptor.Descriptor(
  name='ArrayValue',
  full_name='opentelemetry.proto.common.v1.ArrayValue',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='values', full_name='opentelemetry.proto.common.v1.ArrayValue.values', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=348,
  serialized_end=417,
)


_KEYVALUELIST = _descriptor.Descriptor(
  name='KeyValueList',
  full_name='opentelemetry.proto.common.v1.KeyValueList',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='values', full_name='opentelemetry.proto.common.v1.KeyValueList.values', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=419,
  serialized_end=490,
)


_KEYVALUE = _descriptor.Descriptor(
  name='KeyValue',
  full_name='opentelemetry.proto.common.v1.KeyValue',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='opentelemetry.proto.common.v1.KeyValue.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='opentelemetry.proto.common.v1.KeyValue.value', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=492,
  serialized_end=571,
)


_INSTRUMENTATIONLIBRARY = _descriptor.Descriptor(
  name='InstrumentationLibrary',
  full_name='opentelemetry.proto.common.v1.InstrumentationLibrary',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='opentelemetry.proto.common.v1.InstrumentationLibrary.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='version', full_name='opentelemetry.proto.common.v1.InstrumentationLibrary.version', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=b'\030\001',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=573,
  serialized_end=632,
)


_INSTRUMENTATIONSCOPE = _descriptor.Descriptor(
  name='InstrumentationScope',
  full_name='opentelemetry.proto.common.v1.InstrumentationScope',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='opentelemetry.proto.common.v1.InstrumentationScope.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='version', full_name='opentelemetry.proto.common.v1.InstrumentationScope.version', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=634,
  serialized_end=687,
)

_ANYVALUE.fields_by_name['array_value'].message_type = _ARRAYVALUE
_ANYVALUE.fields_by_name['kvlist_value'].message_type = _KEYVALUELIST
_ANYVALUE.oneofs_by_name['value'].fields.append(
  _ANYVALUE.fields_by_name['string_value'])
_ANYVALUE.fields_by_name['string_value'].containing_oneof = _ANYVALUE.oneofs_by_name['value']
_ANYVALUE.oneofs_by_name['value'].fields.append(
  _ANYVALUE.fields_by_name['bool_value'])
_ANYVALUE.fields_by_name['bool_value'].containing_oneof = _ANYVALUE.oneofs_by_name['value']
_ANYVALUE.oneofs_by_name['value'].fields.append(
  _ANYVALUE.fields_by_name['int_value'])
_ANYVALUE.fields_by_name['int_value'].containing_oneof = _ANYVALUE.oneofs_by_name['value']
_ANYVALUE.oneofs_by_name['value'].fields.append(
  _ANYVALUE.fields_by_name['double_value'])
_ANYVALUE.fields_by_name['double_value'].containing_oneof = _ANYVALUE.oneofs_by_name['value']
_ANYVALUE.oneofs_by_name['value'].fields.append(
  _ANYVALUE.fields_by_name['array_value'])
_ANYVALUE.fields_by_name['array_value'].containing_oneof = _ANYVALUE.oneofs_by_name['value']
_ANYVALUE.oneofs_by_name['value'].fields.append(
  _ANYVALUE.fields_by_name['kvlist_value'])
_ANYVALUE.fields_by_name['kvlist_value'].containing_oneof = _ANYVALUE.oneofs_by_name['value']
_ANYVALUE.oneofs_by_name['value'].fields.append(
  _ANYVALUE.fields_by_name['bytes_value'])
_ANYVALUE.fields_by_name['bytes_value'].containing_oneof = _ANYVALUE.oneofs_by_name['value']
_ARRAYVALUE.fields_by_name['values'].message_type = _ANYVALUE
_KEYVALUELIST.fields_by_name['values'].message_type = _KEYVALUE
_KEYVALUE.fields_by_name['value'].message_type = _ANYVALUE
DESCRIPTOR.message_types_by_name['AnyValue'] = _ANYVALUE
DESCRIPTOR.message_types_by_name['ArrayValue'] = _ARRAYVALUE
DESCRIPTOR.message_types_by_name['KeyValueList'] = _KEYVALUELIST
DESCRIPTOR.message_types_by_name['KeyValue'] = _KEYVALUE
DESCRIPTOR.message_types_by_name['InstrumentationLibrary'] = _INSTRUMENTATIONLIBRARY
DESCRIPTOR.message_types_by_name['InstrumentationScope'] = _INSTRUMENTATIONSCOPE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

AnyValue = _reflection.GeneratedProtocolMessageType('AnyValue', (_message.Message,), {
  'DESCRIPTOR' : _ANYVALUE,
  '__module__' : 'opentelemetry.proto.common.v1.common_pb2'
  # @@protoc_insertion_point(class_scope:opentelemetry.proto.common.v1.AnyValue)
  })
_sym_db.RegisterMessage(AnyValue)

ArrayValue = _reflection.GeneratedProtocolMessageType('ArrayValue', (_message.Message,), {
  'DESCRIPTOR' : _ARRAYVALUE,
  '__module__' : 'opentelemetry.proto.common.v1.common_pb2'
  # @@protoc_insertion_point(class_scope:opentelemetry.proto.common.v1.ArrayValue)
  })
_sym_db.RegisterMessage(ArrayValue)

KeyValueList = _reflection.GeneratedProtocolMessageType('KeyValueList', (_message.Message,), {
  'DESCRIPTOR' : _KEYVALUELIST,
  '__module__' : 'opentelemetry.proto.common.v1.common_pb2'
  # @@protoc_insertion_point(class_scope:opentelemetry.proto.common.v1.KeyValueList)
  })
_sym_db.RegisterMessage(KeyValueList)

KeyValue = _reflection.GeneratedProtocolMessageType('KeyValue', (_message.Message,), {
  'DESCRIPTOR' : _KEYVALUE,
  '__module__' : 'opentelemetry.proto.common.v1.common_pb2'
  # @@protoc_insertion_point(class_scope:opentelemetry.proto.common.v1.KeyValue)
  })
_sym_db.RegisterMessage(KeyValue)

InstrumentationLibrary = _reflection.GeneratedProtocolMessageType('InstrumentationLibrary', (_message.Message,), {
  'DESCRIPTOR' : _INSTRUMENTATIONLIBRARY,
  '__module__' : 'opentelemetry.proto.common.v1.common_pb2'
  # @@protoc_insertion_point(class_scope:opentelemetry.proto.common.v1.InstrumentationLibrary)
  })
_sym_db.RegisterMessage(InstrumentationLibrary)

InstrumentationScope = _reflection.GeneratedProtocolMessageType('InstrumentationScope', (_message.Message,), {
  'DESCRIPTOR' : _INSTRUMENTATIONSCOPE,
  '__module__' : 'opentelemetry.proto.common.v1.common_pb2'
  # @@protoc_insertion_point(class_scope:opentelemetry.proto.common.v1.InstrumentationScope)
  })
_sym_db.RegisterMessage(InstrumentationScope)


DESCRIPTOR._options = None
_INSTRUMENTATIONLIBRARY._options = None
# @@protoc_insertion_point(module_scope)

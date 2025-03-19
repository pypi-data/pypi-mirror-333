# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tensorboard/compat/proto/function.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from tensorboard.compat.proto import attr_value_pb2 as tensorboard_dot_compat_dot_proto_dot_attr__value__pb2
from tensorboard.compat.proto import node_def_pb2 as tensorboard_dot_compat_dot_proto_dot_node__def__pb2
from tensorboard.compat.proto import op_def_pb2 as tensorboard_dot_compat_dot_proto_dot_op__def__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\'tensorboard/compat/proto/function.proto\x12\x0btensorboard\x1a)tensorboard/compat/proto/attr_value.proto\x1a\'tensorboard/compat/proto/node_def.proto\x1a%tensorboard/compat/proto/op_def.proto\"\xab\x01\n\x12\x46unctionDefLibrary\x12*\n\x08\x66unction\x18\x01 \x03(\x0b\x32\x18.tensorboard.FunctionDef\x12*\n\x08gradient\x18\x02 \x03(\x0b\x32\x18.tensorboard.GradientDef\x12=\n\x14registered_gradients\x18\x03 \x03(\x0b\x32\x1f.tensorboard.RegisteredGradient\"\xcf\x06\n\x0b\x46unctionDef\x12%\n\tsignature\x18\x01 \x01(\x0b\x32\x12.tensorboard.OpDef\x12\x30\n\x04\x61ttr\x18\x05 \x03(\x0b\x32\".tensorboard.FunctionDef.AttrEntry\x12\x37\n\x08\x61rg_attr\x18\x07 \x03(\x0b\x32%.tensorboard.FunctionDef.ArgAttrEntry\x12Q\n\x16resource_arg_unique_id\x18\x08 \x03(\x0b\x32\x31.tensorboard.FunctionDef.ResourceArgUniqueIdEntry\x12&\n\x08node_def\x18\x03 \x03(\x0b\x32\x14.tensorboard.NodeDef\x12.\n\x03ret\x18\x04 \x03(\x0b\x32!.tensorboard.FunctionDef.RetEntry\x12=\n\x0b\x63ontrol_ret\x18\x06 \x03(\x0b\x32(.tensorboard.FunctionDef.ControlRetEntry\x1a\x43\n\tAttrEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12%\n\x05value\x18\x02 \x01(\x0b\x32\x16.tensorboard.AttrValue:\x02\x38\x01\x1a\x8a\x01\n\x08\x41rgAttrs\x12\x39\n\x04\x61ttr\x18\x01 \x03(\x0b\x32+.tensorboard.FunctionDef.ArgAttrs.AttrEntry\x1a\x43\n\tAttrEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12%\n\x05value\x18\x02 \x01(\x0b\x32\x16.tensorboard.AttrValue:\x02\x38\x01\x1aQ\n\x0c\x41rgAttrEntry\x12\x0b\n\x03key\x18\x01 \x01(\r\x12\x30\n\x05value\x18\x02 \x01(\x0b\x32!.tensorboard.FunctionDef.ArgAttrs:\x02\x38\x01\x1a:\n\x18ResourceArgUniqueIdEntry\x12\x0b\n\x03key\x18\x01 \x01(\r\x12\r\n\x05value\x18\x02 \x01(\r:\x02\x38\x01\x1a*\n\x08RetEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x1a\x31\n\x0f\x43ontrolRetEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01J\x04\x08\x02\x10\x03\";\n\x0bGradientDef\x12\x15\n\rfunction_name\x18\x01 \x01(\t\x12\x15\n\rgradient_func\x18\x02 \x01(\t\"G\n\x12RegisteredGradient\x12\x15\n\rgradient_func\x18\x01 \x01(\t\x12\x1a\n\x12registered_op_type\x18\x02 \x01(\tB\x80\x01\n\x18org.tensorflow.frameworkB\x0e\x46unctionProtosP\x01ZOgithub.com/tensorflow/tensorflow/tensorflow/go/core/framework/function_go_proto\xf8\x01\x01\x62\x06proto3')



_FUNCTIONDEFLIBRARY = DESCRIPTOR.message_types_by_name['FunctionDefLibrary']
_FUNCTIONDEF = DESCRIPTOR.message_types_by_name['FunctionDef']
_FUNCTIONDEF_ATTRENTRY = _FUNCTIONDEF.nested_types_by_name['AttrEntry']
_FUNCTIONDEF_ARGATTRS = _FUNCTIONDEF.nested_types_by_name['ArgAttrs']
_FUNCTIONDEF_ARGATTRS_ATTRENTRY = _FUNCTIONDEF_ARGATTRS.nested_types_by_name['AttrEntry']
_FUNCTIONDEF_ARGATTRENTRY = _FUNCTIONDEF.nested_types_by_name['ArgAttrEntry']
_FUNCTIONDEF_RESOURCEARGUNIQUEIDENTRY = _FUNCTIONDEF.nested_types_by_name['ResourceArgUniqueIdEntry']
_FUNCTIONDEF_RETENTRY = _FUNCTIONDEF.nested_types_by_name['RetEntry']
_FUNCTIONDEF_CONTROLRETENTRY = _FUNCTIONDEF.nested_types_by_name['ControlRetEntry']
_GRADIENTDEF = DESCRIPTOR.message_types_by_name['GradientDef']
_REGISTEREDGRADIENT = DESCRIPTOR.message_types_by_name['RegisteredGradient']
FunctionDefLibrary = _reflection.GeneratedProtocolMessageType('FunctionDefLibrary', (_message.Message,), {
  'DESCRIPTOR' : _FUNCTIONDEFLIBRARY,
  '__module__' : 'tensorboard.compat.proto.function_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.FunctionDefLibrary)
  })
_sym_db.RegisterMessage(FunctionDefLibrary)

FunctionDef = _reflection.GeneratedProtocolMessageType('FunctionDef', (_message.Message,), {

  'AttrEntry' : _reflection.GeneratedProtocolMessageType('AttrEntry', (_message.Message,), {
    'DESCRIPTOR' : _FUNCTIONDEF_ATTRENTRY,
    '__module__' : 'tensorboard.compat.proto.function_pb2'
    # @@protoc_insertion_point(class_scope:tensorboard.FunctionDef.AttrEntry)
    })
  ,

  'ArgAttrs' : _reflection.GeneratedProtocolMessageType('ArgAttrs', (_message.Message,), {

    'AttrEntry' : _reflection.GeneratedProtocolMessageType('AttrEntry', (_message.Message,), {
      'DESCRIPTOR' : _FUNCTIONDEF_ARGATTRS_ATTRENTRY,
      '__module__' : 'tensorboard.compat.proto.function_pb2'
      # @@protoc_insertion_point(class_scope:tensorboard.FunctionDef.ArgAttrs.AttrEntry)
      })
    ,
    'DESCRIPTOR' : _FUNCTIONDEF_ARGATTRS,
    '__module__' : 'tensorboard.compat.proto.function_pb2'
    # @@protoc_insertion_point(class_scope:tensorboard.FunctionDef.ArgAttrs)
    })
  ,

  'ArgAttrEntry' : _reflection.GeneratedProtocolMessageType('ArgAttrEntry', (_message.Message,), {
    'DESCRIPTOR' : _FUNCTIONDEF_ARGATTRENTRY,
    '__module__' : 'tensorboard.compat.proto.function_pb2'
    # @@protoc_insertion_point(class_scope:tensorboard.FunctionDef.ArgAttrEntry)
    })
  ,

  'ResourceArgUniqueIdEntry' : _reflection.GeneratedProtocolMessageType('ResourceArgUniqueIdEntry', (_message.Message,), {
    'DESCRIPTOR' : _FUNCTIONDEF_RESOURCEARGUNIQUEIDENTRY,
    '__module__' : 'tensorboard.compat.proto.function_pb2'
    # @@protoc_insertion_point(class_scope:tensorboard.FunctionDef.ResourceArgUniqueIdEntry)
    })
  ,

  'RetEntry' : _reflection.GeneratedProtocolMessageType('RetEntry', (_message.Message,), {
    'DESCRIPTOR' : _FUNCTIONDEF_RETENTRY,
    '__module__' : 'tensorboard.compat.proto.function_pb2'
    # @@protoc_insertion_point(class_scope:tensorboard.FunctionDef.RetEntry)
    })
  ,

  'ControlRetEntry' : _reflection.GeneratedProtocolMessageType('ControlRetEntry', (_message.Message,), {
    'DESCRIPTOR' : _FUNCTIONDEF_CONTROLRETENTRY,
    '__module__' : 'tensorboard.compat.proto.function_pb2'
    # @@protoc_insertion_point(class_scope:tensorboard.FunctionDef.ControlRetEntry)
    })
  ,
  'DESCRIPTOR' : _FUNCTIONDEF,
  '__module__' : 'tensorboard.compat.proto.function_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.FunctionDef)
  })
_sym_db.RegisterMessage(FunctionDef)
_sym_db.RegisterMessage(FunctionDef.AttrEntry)
_sym_db.RegisterMessage(FunctionDef.ArgAttrs)
_sym_db.RegisterMessage(FunctionDef.ArgAttrs.AttrEntry)
_sym_db.RegisterMessage(FunctionDef.ArgAttrEntry)
_sym_db.RegisterMessage(FunctionDef.ResourceArgUniqueIdEntry)
_sym_db.RegisterMessage(FunctionDef.RetEntry)
_sym_db.RegisterMessage(FunctionDef.ControlRetEntry)

GradientDef = _reflection.GeneratedProtocolMessageType('GradientDef', (_message.Message,), {
  'DESCRIPTOR' : _GRADIENTDEF,
  '__module__' : 'tensorboard.compat.proto.function_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.GradientDef)
  })
_sym_db.RegisterMessage(GradientDef)

RegisteredGradient = _reflection.GeneratedProtocolMessageType('RegisteredGradient', (_message.Message,), {
  'DESCRIPTOR' : _REGISTEREDGRADIENT,
  '__module__' : 'tensorboard.compat.proto.function_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.RegisteredGradient)
  })
_sym_db.RegisterMessage(RegisteredGradient)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\030org.tensorflow.frameworkB\016FunctionProtosP\001ZOgithub.com/tensorflow/tensorflow/tensorflow/go/core/framework/function_go_proto\370\001\001'
  _FUNCTIONDEF_ATTRENTRY._options = None
  _FUNCTIONDEF_ATTRENTRY._serialized_options = b'8\001'
  _FUNCTIONDEF_ARGATTRS_ATTRENTRY._options = None
  _FUNCTIONDEF_ARGATTRS_ATTRENTRY._serialized_options = b'8\001'
  _FUNCTIONDEF_ARGATTRENTRY._options = None
  _FUNCTIONDEF_ARGATTRENTRY._serialized_options = b'8\001'
  _FUNCTIONDEF_RESOURCEARGUNIQUEIDENTRY._options = None
  _FUNCTIONDEF_RESOURCEARGUNIQUEIDENTRY._serialized_options = b'8\001'
  _FUNCTIONDEF_RETENTRY._options = None
  _FUNCTIONDEF_RETENTRY._serialized_options = b'8\001'
  _FUNCTIONDEF_CONTROLRETENTRY._options = None
  _FUNCTIONDEF_CONTROLRETENTRY._serialized_options = b'8\001'
  _FUNCTIONDEFLIBRARY._serialized_start=180
  _FUNCTIONDEFLIBRARY._serialized_end=351
  _FUNCTIONDEF._serialized_start=354
  _FUNCTIONDEF._serialized_end=1201
  _FUNCTIONDEF_ATTRENTRY._serialized_start=749
  _FUNCTIONDEF_ATTRENTRY._serialized_end=816
  _FUNCTIONDEF_ARGATTRS._serialized_start=819
  _FUNCTIONDEF_ARGATTRS._serialized_end=957
  _FUNCTIONDEF_ARGATTRS_ATTRENTRY._serialized_start=749
  _FUNCTIONDEF_ARGATTRS_ATTRENTRY._serialized_end=816
  _FUNCTIONDEF_ARGATTRENTRY._serialized_start=959
  _FUNCTIONDEF_ARGATTRENTRY._serialized_end=1040
  _FUNCTIONDEF_RESOURCEARGUNIQUEIDENTRY._serialized_start=1042
  _FUNCTIONDEF_RESOURCEARGUNIQUEIDENTRY._serialized_end=1100
  _FUNCTIONDEF_RETENTRY._serialized_start=1102
  _FUNCTIONDEF_RETENTRY._serialized_end=1144
  _FUNCTIONDEF_CONTROLRETENTRY._serialized_start=1146
  _FUNCTIONDEF_CONTROLRETENTRY._serialized_end=1195
  _GRADIENTDEF._serialized_start=1203
  _GRADIENTDEF._serialized_end=1262
  _REGISTEREDGRADIENT._serialized_start=1264
  _REGISTEREDGRADIENT._serialized_end=1335
# @@protoc_insertion_point(module_scope)

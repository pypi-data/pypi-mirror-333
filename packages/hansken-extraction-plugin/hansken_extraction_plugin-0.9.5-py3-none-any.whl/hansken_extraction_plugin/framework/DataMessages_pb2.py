# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: hansken_extraction_plugin/framework/DataMessages.proto
# Protobuf Python Version: 5.28.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    28,
    1,
    '',
    'hansken_extraction_plugin/framework/DataMessages.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from hansken_extraction_plugin.framework import PrimitiveMessages_pb2 as hansken__extraction__plugin_dot_framework_dot_PrimitiveMessages__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n6hansken_extraction_plugin/framework/DataMessages.proto\x12\"org.hansken.extraction.plugin.grpc\x1a\x19google/protobuf/any.proto\x1a;hansken_extraction_plugin/framework/PrimitiveMessages.proto\"\xd9\x04\n\rRpcPluginInfo\x12?\n\x04type\x18\x01 \x01(\x0e\x32\x31.org.hansken.extraction.plugin.grpc.RpcPluginType\x12\x12\n\napiVersion\x18\x02 \x01(\t\x12\x10\n\x04name\x18\x03 \x01(\tB\x02\x18\x01\x12\x0f\n\x07version\x18\x04 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x05 \x01(\t\x12=\n\x06\x61uthor\x18\x06 \x01(\x0b\x32-.org.hansken.extraction.plugin.grpc.RpcAuthor\x12\x41\n\x08maturity\x18\x07 \x01(\x0e\x32/.org.hansken.extraction.plugin.grpc.RpcMaturity\x12\x0f\n\x07matcher\x18\x08 \x01(\t\x12\x12\n\nwebpageUrl\x18\t \x01(\t\x12\x1a\n\x12\x64\x65\x66\x65rredIterations\x18\n \x01(\x05\x12\x43\n\x02id\x18\x0b \x01(\x0b\x32\x37.org.hansken.extraction.plugin.grpc.RpcPluginIdentifier\x12\x0f\n\x07license\x18\r \x01(\t\x12I\n\tresources\x18\x0e \x01(\x0b\x32\x36.org.hansken.extraction.plugin.grpc.RpcPluginResources\x12H\n\x0ctransformers\x18\x0f \x03(\x0b\x32\x32.org.hansken.extraction.plugin.grpc.RpcTransformer\x12\r\n\x05model\x18\x10 \x01(\t\"E\n\x13RpcPluginIdentifier\x12\x0e\n\x06\x64omain\x18\x01 \x01(\t\x12\x10\n\x08\x63\x61tegory\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\">\n\tRpcAuthor\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05\x65mail\x18\x02 \x01(\t\x12\x14\n\x0corganisation\x18\x03 \x01(\t\"K\n\x12RpcPluginResources\x12\x0e\n\x06maxCpu\x18\x01 \x01(\x02\x12\x11\n\tmaxMemory\x18\x02 \x01(\r\x12\x12\n\nmaxWorkers\x18\x03 \x01(\r\"E\n\x10RpcTraceProperty\x12\x0c\n\x04name\x18\x01 \x01(\t\x12#\n\x05value\x18\x02 \x01(\x0b\x32\x14.google.protobuf.Any\"e\n\x0bRpcTracelet\x12\x0c\n\x04name\x18\x01 \x01(\t\x12H\n\nproperties\x18\x02 \x03(\x0b\x32\x34.org.hansken.extraction.plugin.grpc.RpcTraceProperty\"\x8d\x02\n\x08RpcTrace\x12\n\n\x02id\x18\x01 \x01(\t\x12\r\n\x05types\x18\x02 \x03(\t\x12H\n\nproperties\x18\x03 \x03(\x0b\x32\x34.org.hansken.extraction.plugin.grpc.RpcTraceProperty\x12\x42\n\ttracelets\x18\x04 \x03(\x0b\x32/.org.hansken.extraction.plugin.grpc.RpcTracelet\x12X\n\x0ftransformations\x18\x05 \x03(\x0b\x32?.org.hansken.extraction.plugin.grpc.RpcDataStreamTransformation\"\x7f\n\x1bRpcDataStreamTransformation\x12\x10\n\x08\x64\x61taType\x18\x01 \x01(\t\x12N\n\x0ftransformations\x18\x02 \x03(\x0b\x32\x35.org.hansken.extraction.plugin.grpc.RpcTransformation\"\xc0\x01\n\x0eRpcSearchTrace\x12\n\n\x02id\x18\x01 \x01(\t\x12\r\n\x05types\x18\x02 \x03(\t\x12H\n\nproperties\x18\x03 \x03(\x0b\x32\x34.org.hansken.extraction.plugin.grpc.RpcTraceProperty\x12I\n\x04\x64\x61ta\x18\x04 \x03(\x0b\x32;.org.hansken.extraction.plugin.grpc.RpcRandomAccessDataMeta\"m\n\x0eRpcDataContext\x12\x10\n\x08\x64\x61taType\x18\x01 \x01(\t\x12I\n\x04\x64\x61ta\x18\x02 \x01(\x0b\x32;.org.hansken.extraction.plugin.grpc.RpcRandomAccessDataMeta\"I\n\x17RpcRandomAccessDataMeta\x12\x0c\n\x04type\x18\x01 \x01(\t\x12\x0c\n\x04size\x18\x02 \x01(\x03\x12\x12\n\nfirstBytes\x18\x03 \x01(\x0c\"y\n\x11RpcTransformation\x12[\n\x14rangedTransformation\x18\x01 \x01(\x0b\x32;.org.hansken.extraction.plugin.grpc.RpcRangedTransformationH\x00\x42\x07\n\x05value\"W\n\x17RpcRangedTransformation\x12<\n\x06ranges\x18\x01 \x03(\x0b\x32,.org.hansken.extraction.plugin.grpc.RpcRange\"*\n\x08RpcRange\x12\x0e\n\x06offset\x18\x01 \x01(\x03\x12\x0e\n\x06length\x18\x02 \x01(\x03\"\xa8\x05\n\x16RpcTransformerArgument\x12\x41\n\x07\x62oolean\x18\x02 \x01(\x0b\x32..org.hansken.extraction.plugin.grpc.RpcBooleanH\x00\x12=\n\x05\x62ytes\x18\x03 \x01(\x0b\x32,.org.hansken.extraction.plugin.grpc.RpcBytesH\x00\x12>\n\x07integer\x18\x04 \x01(\x0b\x32+.org.hansken.extraction.plugin.grpc.RpcLongH\x00\x12=\n\x04real\x18\x05 \x01(\x0b\x32-.org.hansken.extraction.plugin.grpc.RpcDoubleH\x00\x12?\n\x06string\x18\x06 \x01(\x0b\x32-.org.hansken.extraction.plugin.grpc.RpcStringH\x00\x12?\n\x06vector\x18\x07 \x01(\x0b\x32-.org.hansken.extraction.plugin.grpc.RpcVectorH\x00\x12\x41\n\x07latLong\x18\x08 \x01(\x0b\x32..org.hansken.extraction.plugin.grpc.RpcLatLongH\x00\x12H\n\x08\x64\x61tetime\x18\t \x01(\x0b\x32\x34.org.hansken.extraction.plugin.grpc.RpcZonedDateTimeH\x00\x12;\n\x04list\x18\n \x01(\x0b\x32+.org.hansken.extraction.plugin.grpc.RpcListH\x00\x12\x39\n\x03map\x18\x0b \x01(\x0b\x32*.org.hansken.extraction.plugin.grpc.RpcMapH\x00\x42\x06\n\x04type\"\xc3\x01\n\x0eRpcTransformer\x12\x12\n\nmethodName\x18\x01 \x01(\t\x12V\n\nparameters\x18\x02 \x03(\x0b\x32\x42.org.hansken.extraction.plugin.grpc.RpcTransformer.ParametersEntry\x12\x12\n\nreturnType\x18\x03 \x01(\t\x1a\x31\n\x0fParametersEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\x85\x02\n\x15RpcTransformerRequest\x12\x12\n\nmethodName\x18\x01 \x01(\t\x12\x65\n\x0enamedArguments\x18\x02 \x03(\x0b\x32M.org.hansken.extraction.plugin.grpc.RpcTransformerRequest.NamedArgumentsEntry\x1aq\n\x13NamedArgumentsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12I\n\x05value\x18\x02 \x01(\x0b\x32:.org.hansken.extraction.plugin.grpc.RpcTransformerArgument:\x02\x38\x01\"f\n\x16RpcTransformerResponse\x12L\n\x08response\x18\x01 \x01(\x0b\x32:.org.hansken.extraction.plugin.grpc.RpcTransformerArgument*]\n\rRpcPluginType\x12\x14\n\x10\x45xtractionPlugin\x10\x00\x12\x18\n\x14MetaExtractionPlugin\x10\x01\x12\x1c\n\x18\x44\x65\x66\x65rredExtractionPlugin\x10\x02*H\n\x0bRpcMaturity\x12\x12\n\x0eProofOfConcept\x10\x00\x12\x10\n\x0cReadyForTest\x10\x01\x12\x13\n\x0fProductionReady\x10\x02\x42&\n\"org.hansken.extraction.plugin.grpcP\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'hansken_extraction_plugin.framework.DataMessages_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\"org.hansken.extraction.plugin.grpcP\001'
  _globals['_RPCPLUGININFO'].fields_by_name['name']._loaded_options = None
  _globals['_RPCPLUGININFO'].fields_by_name['name']._serialized_options = b'\030\001'
  _globals['_RPCTRANSFORMER_PARAMETERSENTRY']._loaded_options = None
  _globals['_RPCTRANSFORMER_PARAMETERSENTRY']._serialized_options = b'8\001'
  _globals['_RPCTRANSFORMERREQUEST_NAMEDARGUMENTSENTRY']._loaded_options = None
  _globals['_RPCTRANSFORMERREQUEST_NAMEDARGUMENTSENTRY']._serialized_options = b'8\001'
  _globals['_RPCPLUGINTYPE']._serialized_start=3459
  _globals['_RPCPLUGINTYPE']._serialized_end=3552
  _globals['_RPCMATURITY']._serialized_start=3554
  _globals['_RPCMATURITY']._serialized_end=3626
  _globals['_RPCPLUGININFO']._serialized_start=183
  _globals['_RPCPLUGININFO']._serialized_end=784
  _globals['_RPCPLUGINIDENTIFIER']._serialized_start=786
  _globals['_RPCPLUGINIDENTIFIER']._serialized_end=855
  _globals['_RPCAUTHOR']._serialized_start=857
  _globals['_RPCAUTHOR']._serialized_end=919
  _globals['_RPCPLUGINRESOURCES']._serialized_start=921
  _globals['_RPCPLUGINRESOURCES']._serialized_end=996
  _globals['_RPCTRACEPROPERTY']._serialized_start=998
  _globals['_RPCTRACEPROPERTY']._serialized_end=1067
  _globals['_RPCTRACELET']._serialized_start=1069
  _globals['_RPCTRACELET']._serialized_end=1170
  _globals['_RPCTRACE']._serialized_start=1173
  _globals['_RPCTRACE']._serialized_end=1442
  _globals['_RPCDATASTREAMTRANSFORMATION']._serialized_start=1444
  _globals['_RPCDATASTREAMTRANSFORMATION']._serialized_end=1571
  _globals['_RPCSEARCHTRACE']._serialized_start=1574
  _globals['_RPCSEARCHTRACE']._serialized_end=1766
  _globals['_RPCDATACONTEXT']._serialized_start=1768
  _globals['_RPCDATACONTEXT']._serialized_end=1877
  _globals['_RPCRANDOMACCESSDATAMETA']._serialized_start=1879
  _globals['_RPCRANDOMACCESSDATAMETA']._serialized_end=1952
  _globals['_RPCTRANSFORMATION']._serialized_start=1954
  _globals['_RPCTRANSFORMATION']._serialized_end=2075
  _globals['_RPCRANGEDTRANSFORMATION']._serialized_start=2077
  _globals['_RPCRANGEDTRANSFORMATION']._serialized_end=2164
  _globals['_RPCRANGE']._serialized_start=2166
  _globals['_RPCRANGE']._serialized_end=2208
  _globals['_RPCTRANSFORMERARGUMENT']._serialized_start=2211
  _globals['_RPCTRANSFORMERARGUMENT']._serialized_end=2891
  _globals['_RPCTRANSFORMER']._serialized_start=2894
  _globals['_RPCTRANSFORMER']._serialized_end=3089
  _globals['_RPCTRANSFORMER_PARAMETERSENTRY']._serialized_start=3040
  _globals['_RPCTRANSFORMER_PARAMETERSENTRY']._serialized_end=3089
  _globals['_RPCTRANSFORMERREQUEST']._serialized_start=3092
  _globals['_RPCTRANSFORMERREQUEST']._serialized_end=3353
  _globals['_RPCTRANSFORMERREQUEST_NAMEDARGUMENTSENTRY']._serialized_start=3240
  _globals['_RPCTRANSFORMERREQUEST_NAMEDARGUMENTSENTRY']._serialized_end=3353
  _globals['_RPCTRANSFORMERRESPONSE']._serialized_start=3355
  _globals['_RPCTRANSFORMERRESPONSE']._serialized_end=3457
# @@protoc_insertion_point(module_scope)

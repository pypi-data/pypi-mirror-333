# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: datasets/v1/well_known_types.proto
# Protobuf Python Version: 5.29.3
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    3,
    '',
    'datasets/v1/well_known_types.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\"datasets/v1/well_known_types.proto\x12\x0b\x64\x61tasets.v1\x1a\x1egoogle/protobuf/duration.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"\x1a\n\x04UUID\x12\x12\n\x04uuid\x18\x01 \x01(\x0cR\x04uuid\"0\n\x04Vec3\x12\x0c\n\x01x\x18\x01 \x01(\x01R\x01x\x12\x0c\n\x01y\x18\x02 \x01(\x01R\x01y\x12\x0c\n\x01z\x18\x03 \x01(\x01R\x01z\"L\n\nQuaternion\x12\x0e\n\x02q1\x18\x01 \x01(\x01R\x02q1\x12\x0e\n\x02q2\x18\x02 \x01(\x01R\x02q2\x12\x0e\n\x02q3\x18\x03 \x01(\x01R\x02q3\x12\x0e\n\x02q4\x18\x04 \x01(\x01R\x02q4\"B\n\x06LatLon\x12\x1a\n\x08latitude\x18\x01 \x01(\x01R\x08latitude\x12\x1c\n\tlongitude\x18\x02 \x01(\x01R\tlongitude\"a\n\tLatLonAlt\x12\x1a\n\x08latitude\x18\x01 \x01(\x01R\x08latitude\x12\x1c\n\tlongitude\x18\x02 \x01(\x01R\tlongitude\x12\x1a\n\x08\x61ltitude\x18\x03 \x01(\x01R\x08\x61ltitude\"\xc2\x0b\n\nGeobufData\x12\x12\n\x04keys\x18\x01 \x03(\tR\x04keys\x12\x1e\n\ndimensions\x18\x02 \x01(\rR\ndimensions\x12\x1c\n\tprecision\x18\x03 \x01(\rR\tprecision\x12Z\n\x12\x66\x65\x61ture_collection\x18\x04 \x01(\x0b\x32).datasets.v1.GeobufData.FeatureCollectionH\x00R\x11\x66\x65\x61tureCollection\x12;\n\x07\x66\x65\x61ture\x18\x05 \x01(\x0b\x32\x1f.datasets.v1.GeobufData.FeatureH\x00R\x07\x66\x65\x61ture\x12>\n\x08geometry\x18\x06 \x01(\x0b\x32 .datasets.v1.GeobufData.GeometryH\x00R\x08geometry\x1a\x81\x02\n\x07\x46\x65\x61ture\x12<\n\x08geometry\x18\x01 \x01(\x0b\x32 .datasets.v1.GeobufData.GeometryR\x08geometry\x12\x10\n\x02id\x18\x0b \x01(\tH\x00R\x02id\x12\x17\n\x06int_id\x18\x0c \x01(\x12H\x00R\x05intId\x12\x35\n\x06values\x18\r \x03(\x0b\x32\x1d.datasets.v1.GeobufData.ValueR\x06values\x12\x1e\n\nproperties\x18\x0e \x03(\rR\nproperties\x12+\n\x11\x63ustom_properties\x18\x0f \x03(\rR\x10\x63ustomPropertiesB\t\n\x07id_type\x1a\xd0\x03\n\x08Geometry\x12\x39\n\x04type\x18\x01 \x01(\x0e\x32%.datasets.v1.GeobufData.Geometry.TypeR\x04type\x12\x18\n\x07lengths\x18\x02 \x03(\rR\x07lengths\x12\x16\n\x06\x63oords\x18\x03 \x03(\x12R\x06\x63oords\x12@\n\ngeometries\x18\x04 \x03(\x0b\x32 .datasets.v1.GeobufData.GeometryR\ngeometries\x12\x35\n\x06values\x18\r \x03(\x0b\x32\x1d.datasets.v1.GeobufData.ValueR\x06values\x12+\n\x11\x63ustom_properties\x18\x0f \x03(\rR\x10\x63ustomProperties\"\xb0\x01\n\x04Type\x12\x0e\n\nTYPE_EMPTY\x10\x00\x12\x0e\n\nTYPE_POINT\x10\x01\x12\x13\n\x0fTYPE_MULTIPOINT\x10\x02\x12\x13\n\x0fTYPE_LINESTRING\x10\x03\x12\x18\n\x14TYPE_MULTILINESTRING\x10\x04\x12\x10\n\x0cTYPE_POLYGON\x10\x05\x12\x15\n\x11TYPE_MULTIPOLYGON\x10\x06\x12\x1b\n\x17TYPE_GEOMETRYCOLLECTION\x10\x07\x1a\xb4\x01\n\x11\x46\x65\x61tureCollection\x12;\n\x08\x66\x65\x61tures\x18\x01 \x03(\x0b\x32\x1f.datasets.v1.GeobufData.FeatureR\x08\x66\x65\x61tures\x12\x35\n\x06values\x18\r \x03(\x0b\x32\x1d.datasets.v1.GeobufData.ValueR\x06values\x12+\n\x11\x63ustom_properties\x18\x0f \x03(\rR\x10\x63ustomProperties\x1a\xed\x01\n\x05Value\x12#\n\x0cstring_value\x18\x01 \x01(\tH\x00R\x0bstringValue\x12#\n\x0c\x64ouble_value\x18\x02 \x01(\x01H\x00R\x0b\x64oubleValue\x12$\n\rpos_int_value\x18\x03 \x01(\x04H\x00R\x0bposIntValue\x12$\n\rneg_int_value\x18\x04 \x01(\x04H\x00R\x0bnegIntValue\x12\x1f\n\nbool_value\x18\x05 \x01(\x08H\x00R\tboolValue\x12\x1f\n\njson_value\x18\x06 \x01(\x0cH\x00R\tjsonValueB\x0c\n\nvalue_typeB\x0b\n\tdata_type*t\n\x0f\x46lightDirection\x12 \n\x1c\x46LIGHT_DIRECTION_UNSPECIFIED\x10\x00\x12\x1e\n\x1a\x46LIGHT_DIRECTION_ASCENDING\x10\x01\x12\x1f\n\x1b\x46LIGHT_DIRECTION_DESCENDING\x10\x02*~\n\x14ObservationDirection\x12%\n!OBSERVATION_DIRECTION_UNSPECIFIED\x10\x00\x12\x1e\n\x1aOBSERVATION_DIRECTION_LEFT\x10\x01\x12\x1f\n\x1bOBSERVATION_DIRECTION_RIGHT\x10\x02*\x99\x01\n\x10OpendataProvider\x12!\n\x1dOPENDATA_PROVIDER_UNSPECIFIED\x10\x00\x12\x19\n\x15OPENDATA_PROVIDER_ASF\x10\x01\x12*\n&OPENDATA_PROVIDER_COPERNICUS_DATASPACE\x10\x02\x12\x1b\n\x17OPENDATA_PROVIDER_UMBRA\x10\x03*\xf1\x02\n\x0fProcessingLevel\x12 \n\x1cPROCESSING_LEVEL_UNSPECIFIED\x10\x00\x12\x17\n\x13PROCESSING_LEVEL_L0\x10\x0c\x12\x17\n\x13PROCESSING_LEVEL_L1\x10\n\x12\x18\n\x14PROCESSING_LEVEL_L1A\x10\x01\x12\x18\n\x14PROCESSING_LEVEL_L1B\x10\x02\x12\x18\n\x14PROCESSING_LEVEL_L1C\x10\x03\x12\x17\n\x13PROCESSING_LEVEL_L2\x10\x04\x12\x18\n\x14PROCESSING_LEVEL_L2A\x10\x05\x12\x18\n\x14PROCESSING_LEVEL_L2B\x10\x06\x12\x17\n\x13PROCESSING_LEVEL_L3\x10\x07\x12\x18\n\x14PROCESSING_LEVEL_L3A\x10\x08\x12\x17\n\x13PROCESSING_LEVEL_L4\x10\t\x12#\n\x1fPROCESSING_LEVEL_NOT_APPLICABLE\x10\x0b*\x98\x02\n\x0cPolarization\x12\x1c\n\x18POLARIZATION_UNSPECIFIED\x10\x00\x12\x13\n\x0fPOLARIZATION_HH\x10\x01\x12\x13\n\x0fPOLARIZATION_HV\x10\x02\x12\x13\n\x0fPOLARIZATION_VH\x10\x03\x12\x13\n\x0fPOLARIZATION_VV\x10\x04\x12\x18\n\x14POLARIZATION_DUAL_HH\x10\x05\x12\x18\n\x14POLARIZATION_DUAL_HV\x10\x06\x12\x18\n\x14POLARIZATION_DUAL_VH\x10\x07\x12\x18\n\x14POLARIZATION_DUAL_VV\x10\x08\x12\x16\n\x12POLARIZATION_HH_HV\x10\t\x12\x16\n\x12POLARIZATION_VV_VH\x10\n*\xf1\x02\n\x0f\x41\x63quisitionMode\x12 \n\x1c\x41\x43QUISITION_MODE_UNSPECIFIED\x10\x00\x12\x17\n\x13\x41\x43QUISITION_MODE_SM\x10\x01\x12\x17\n\x13\x41\x43QUISITION_MODE_EW\x10\x02\x12\x17\n\x13\x41\x43QUISITION_MODE_IW\x10\x03\x12\x17\n\x13\x41\x43QUISITION_MODE_WV\x10\x04\x12\x1e\n\x1a\x41\x43QUISITION_MODE_SPOTLIGHT\x10\n\x12\x19\n\x15\x41\x43QUISITION_MODE_NOBS\x10\x14\x12\x19\n\x15\x41\x43QUISITION_MODE_EOBS\x10\x15\x12\x19\n\x15\x41\x43QUISITION_MODE_DASC\x10\x16\x12\x19\n\x15\x41\x43QUISITION_MODE_ABSR\x10\x17\x12\x18\n\x14\x41\x43QUISITION_MODE_VIC\x10\x18\x12\x18\n\x14\x41\x43QUISITION_MODE_RAW\x10\x19\x12\x18\n\x14\x41\x43QUISITION_MODE_TST\x10\x1a\x42\xb5\x01\n\x0f\x63om.datasets.v1B\x13WellKnownTypesProtoP\x01Z@github.com/tilebox/tilebox-go/protogen/go/datasets/v1;datasetsv1\xa2\x02\x03\x44XX\xaa\x02\x0b\x44\x61tasets.V1\xca\x02\x0b\x44\x61tasets\\V1\xe2\x02\x17\x44\x61tasets\\V1\\GPBMetadata\xea\x02\x0c\x44\x61tasets::V1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'datasets.v1.well_known_types_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\017com.datasets.v1B\023WellKnownTypesProtoP\001Z@github.com/tilebox/tilebox-go/protogen/go/datasets/v1;datasetsv1\242\002\003DXX\252\002\013Datasets.V1\312\002\013Datasets\\V1\342\002\027Datasets\\V1\\GPBMetadata\352\002\014Datasets::V1'
  _globals['_FLIGHTDIRECTION']._serialized_start=1916
  _globals['_FLIGHTDIRECTION']._serialized_end=2032
  _globals['_OBSERVATIONDIRECTION']._serialized_start=2034
  _globals['_OBSERVATIONDIRECTION']._serialized_end=2160
  _globals['_OPENDATAPROVIDER']._serialized_start=2163
  _globals['_OPENDATAPROVIDER']._serialized_end=2316
  _globals['_PROCESSINGLEVEL']._serialized_start=2319
  _globals['_PROCESSINGLEVEL']._serialized_end=2688
  _globals['_POLARIZATION']._serialized_start=2691
  _globals['_POLARIZATION']._serialized_end=2971
  _globals['_ACQUISITIONMODE']._serialized_start=2974
  _globals['_ACQUISITIONMODE']._serialized_end=3343
  _globals['_UUID']._serialized_start=116
  _globals['_UUID']._serialized_end=142
  _globals['_VEC3']._serialized_start=144
  _globals['_VEC3']._serialized_end=192
  _globals['_QUATERNION']._serialized_start=194
  _globals['_QUATERNION']._serialized_end=270
  _globals['_LATLON']._serialized_start=272
  _globals['_LATLON']._serialized_end=338
  _globals['_LATLONALT']._serialized_start=340
  _globals['_LATLONALT']._serialized_end=437
  _globals['_GEOBUFDATA']._serialized_start=440
  _globals['_GEOBUFDATA']._serialized_end=1914
  _globals['_GEOBUFDATA_FEATURE']._serialized_start=754
  _globals['_GEOBUFDATA_FEATURE']._serialized_end=1011
  _globals['_GEOBUFDATA_GEOMETRY']._serialized_start=1014
  _globals['_GEOBUFDATA_GEOMETRY']._serialized_end=1478
  _globals['_GEOBUFDATA_GEOMETRY_TYPE']._serialized_start=1302
  _globals['_GEOBUFDATA_GEOMETRY_TYPE']._serialized_end=1478
  _globals['_GEOBUFDATA_FEATURECOLLECTION']._serialized_start=1481
  _globals['_GEOBUFDATA_FEATURECOLLECTION']._serialized_end=1661
  _globals['_GEOBUFDATA_VALUE']._serialized_start=1664
  _globals['_GEOBUFDATA_VALUE']._serialized_end=1901
# @@protoc_insertion_point(module_scope)

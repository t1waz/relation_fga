# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: messages.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x0emessages.proto"D\n\x12StoreRelationTuple\x12\x0c\n\x04user\x18\x01 \x01(\t\x12\x10\n\x08relation\x18\x02 \x01(\t\x12\x0e\n\x06object\x18\x03 \x01(\t"p\n\x11StoreWriteRequest\x12\x10\n\x08store_id\x18\x01 \x01(\t\x12#\n\x06writes\x18\x02 \x03(\x0b\x32\x13.StoreRelationTuple\x12$\n\x07\x64\x65letes\x18\x03 \x03(\x0b\x32\x13.StoreRelationTuple"$\n\x12StoreWriteResponse\x12\x0e\n\x06status\x18\x01 \x01(\t"\x87\x01\n\x11StoreCheckRequest\x12\x0c\n\x04user\x18\x01 \x01(\t\x12\x12\n\npermission\x18\x02 \x01(\t\x12\x0e\n\x06object\x18\x03 \x01(\t\x12\x10\n\x08store_id\x18\x04 \x01(\t\x12.\n\x11\x63ontextual_tuples\x18\x05 \x03(\x0b\x32\x13.StoreRelationTuple"%\n\x12StoreCheckResponse\x12\x0f\n\x07\x61llowed\x18\x01 \x01(\x08"#\n\x12StoreCreateRequest\x12\r\n\x05model\x18\x01 \x01(\t"7\n\x13StoreCreateResponse\x12\x0e\n\x06status\x18\x01 \x01(\t\x12\x10\n\x08store_id\x18\x02 \x01(\t"5\n\x12StoreUpdateRequest\x12\x10\n\x08store_id\x18\x01 \x01(\t\x12\r\n\x05model\x18\x02 \x01(\t"7\n\x13StoreUpdateResponse\x12\x0e\n\x06status\x18\x01 \x01(\t\x12\x10\n\x08store_id\x18\x02 \x01(\t"$\n\x10StoreViewRequest\x12\x10\n\x08store_id\x18\x01 \x01(\t"4\n\x11StoreViewResponse\x12\x10\n\x08store_id\x18\x01 \x01(\t\x12\r\n\x05model\x18\x02 \x01(\t"\x12\n\x10StoreListRequest"&\n\x11StoreListResponse\x12\x11\n\tstore_ids\x18\x01 \x03(\t"\x8b\x01\n\x17StoreListObjectsRequest\x12\x10\n\x08store_id\x18\x01 \x01(\t\x12\x0c\n\x04user\x18\x02 \x01(\t\x12\x12\n\npermission\x18\x03 \x01(\t\x12\x0c\n\x04type\x18\x04 \x01(\t\x12.\n\x11\x63ontextual_tuples\x18\x05 \x03(\x0b\x32\x13.StoreRelationTuple"+\n\x18StoreListObjectsResponse\x12\x0f\n\x07objects\x18\x01 \x03(\t"B\n\x0cStoreReadObj\x12\x0f\n\x02id\x18\x01 \x01(\tH\x00\x88\x01\x01\x12\x11\n\x04type\x18\x02 \x01(\tH\x01\x88\x01\x01\x42\x05\n\x03_idB\x07\n\x05_type"\xa6\x01\n\x10StoreReadRequest\x12\x10\n\x08store_id\x18\x01 \x01(\t\x12\x15\n\x08relation\x18\x02 \x01(\tH\x00\x88\x01\x01\x12"\n\x06source\x18\x03 \x01(\x0b\x32\r.StoreReadObjH\x01\x88\x01\x01\x12"\n\x06target\x18\x04 \x01(\x0b\x32\r.StoreReadObjH\x02\x88\x01\x01\x42\x0b\n\t_relationB\t\n\x07_sourceB\t\n\x07_target"9\n\x11StoreReadResponse\x12$\n\x07objects\x18\x01 \x03(\x0b\x32\x13.StoreRelationTupleb\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "messages_pb2", _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _globals["_STORERELATIONTUPLE"]._serialized_start = 18
    _globals["_STORERELATIONTUPLE"]._serialized_end = 86
    _globals["_STOREWRITEREQUEST"]._serialized_start = 88
    _globals["_STOREWRITEREQUEST"]._serialized_end = 200
    _globals["_STOREWRITERESPONSE"]._serialized_start = 202
    _globals["_STOREWRITERESPONSE"]._serialized_end = 238
    _globals["_STORECHECKREQUEST"]._serialized_start = 241
    _globals["_STORECHECKREQUEST"]._serialized_end = 376
    _globals["_STORECHECKRESPONSE"]._serialized_start = 378
    _globals["_STORECHECKRESPONSE"]._serialized_end = 415
    _globals["_STORECREATEREQUEST"]._serialized_start = 417
    _globals["_STORECREATEREQUEST"]._serialized_end = 452
    _globals["_STORECREATERESPONSE"]._serialized_start = 454
    _globals["_STORECREATERESPONSE"]._serialized_end = 509
    _globals["_STOREUPDATEREQUEST"]._serialized_start = 511
    _globals["_STOREUPDATEREQUEST"]._serialized_end = 564
    _globals["_STOREUPDATERESPONSE"]._serialized_start = 566
    _globals["_STOREUPDATERESPONSE"]._serialized_end = 621
    _globals["_STOREVIEWREQUEST"]._serialized_start = 623
    _globals["_STOREVIEWREQUEST"]._serialized_end = 659
    _globals["_STOREVIEWRESPONSE"]._serialized_start = 661
    _globals["_STOREVIEWRESPONSE"]._serialized_end = 713
    _globals["_STORELISTREQUEST"]._serialized_start = 715
    _globals["_STORELISTREQUEST"]._serialized_end = 733
    _globals["_STORELISTRESPONSE"]._serialized_start = 735
    _globals["_STORELISTRESPONSE"]._serialized_end = 773
    _globals["_STORELISTOBJECTSREQUEST"]._serialized_start = 776
    _globals["_STORELISTOBJECTSREQUEST"]._serialized_end = 915
    _globals["_STORELISTOBJECTSRESPONSE"]._serialized_start = 917
    _globals["_STORELISTOBJECTSRESPONSE"]._serialized_end = 960
    _globals["_STOREREADOBJ"]._serialized_start = 962
    _globals["_STOREREADOBJ"]._serialized_end = 1028
    _globals["_STOREREADREQUEST"]._serialized_start = 1031
    _globals["_STOREREADREQUEST"]._serialized_end = 1197
    _globals["_STOREREADRESPONSE"]._serialized_start = 1199
    _globals["_STOREREADRESPONSE"]._serialized_end = 1256
# @@protoc_insertion_point(module_scope)

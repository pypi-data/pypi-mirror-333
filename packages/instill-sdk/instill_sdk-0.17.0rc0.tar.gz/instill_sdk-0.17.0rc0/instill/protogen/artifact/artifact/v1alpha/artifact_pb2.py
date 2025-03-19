# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: artifact/artifact/v1alpha/artifact.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from artifact.artifact.v1alpha import object_pb2 as artifact_dot_artifact_dot_v1alpha_dot_object__pb2
from common.healthcheck.v1beta import healthcheck_pb2 as common_dot_healthcheck_dot_v1beta_dot_healthcheck__pb2
from common.run.v1alpha import run_pb2 as common_dot_run_dot_v1alpha_dot_run__pb2
from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from google.api import resource_pb2 as google_dot_api_dot_resource__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n(artifact/artifact/v1alpha/artifact.proto\x12\x19\x61rtifact.artifact.v1alpha\x1a&artifact/artifact/v1alpha/object.proto\x1a+common/healthcheck/v1beta/healthcheck.proto\x1a\x1c\x63ommon/run/v1alpha/run.proto\x1a\x1fgoogle/api/field_behavior.proto\x1a\x19google/api/resource.proto\x1a\x1cgoogle/protobuf/struct.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"\x95\x01\n\x0fLivenessRequest\x12i\n\x14health_check_request\x18\x01 \x01(\x0b\x32-.common.healthcheck.v1beta.HealthCheckRequestB\x03\xe0\x41\x01H\x00R\x12healthCheckRequest\x88\x01\x01\x42\x17\n\x15_health_check_request\"v\n\x10LivenessResponse\x12\x62\n\x15health_check_response\x18\x01 \x01(\x0b\x32..common.healthcheck.v1beta.HealthCheckResponseR\x13healthCheckResponse\"\x96\x01\n\x10ReadinessRequest\x12i\n\x14health_check_request\x18\x01 \x01(\x0b\x32-.common.healthcheck.v1beta.HealthCheckRequestB\x03\xe0\x41\x01H\x00R\x12healthCheckRequest\x88\x01\x01\x42\x17\n\x15_health_check_request\"w\n\x11ReadinessResponse\x12\x62\n\x15health_check_response\x18\x01 \x01(\x0b\x32..common.healthcheck.v1beta.HealthCheckResponseR\x13healthCheckResponse\"\x9f\x01\n\rRepositoryTag\x12\x17\n\x04name\x18\x01 \x01(\tB\x03\xe0\x41\x05R\x04name\x12\x13\n\x02id\x18\x02 \x01(\tB\x03\xe0\x41\x05R\x02id\x12\x1b\n\x06\x64igest\x18\x03 \x01(\tB\x03\xe0\x41\x01R\x06\x64igest\x12\x43\n\x0bupdate_time\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.TimestampB\x06\xe0\x41\x03\xe0\x41\x01R\nupdateTime\"\xb4\x01\n\x19ListRepositoryTagsRequest\x12%\n\tpage_size\x18\x01 \x01(\x05\x42\x03\xe0\x41\x01H\x00R\x08pageSize\x88\x01\x01\x12\x1c\n\x04page\x18\x02 \x01(\x05\x42\x03\xe0\x41\x01H\x01R\x04page\x88\x01\x01\x12;\n\x06parent\x18\x03 \x01(\tB#\xe0\x41\x02\xfa\x41\x1d\n\x1b\x61pi.instill.tech/RepositoryR\x06parentB\x0c\n\n_page_sizeB\x07\n\x05_page\"\xaa\x01\n\x1aListRepositoryTagsResponse\x12<\n\x04tags\x18\x01 \x03(\x0b\x32(.artifact.artifact.v1alpha.RepositoryTagR\x04tags\x12\x1d\n\ntotal_size\x18\x02 \x01(\x05R\ttotalSize\x12\x1b\n\tpage_size\x18\x03 \x01(\x05R\x08pageSize\x12\x12\n\x04page\x18\x04 \x01(\x05R\x04page\"X\n\x1a\x43reateRepositoryTagRequest\x12:\n\x03tag\x18\x01 \x01(\x0b\x32(.artifact.artifact.v1alpha.RepositoryTagR\x03tag\"Y\n\x1b\x43reateRepositoryTagResponse\x12:\n\x03tag\x18\x01 \x01(\x0b\x32(.artifact.artifact.v1alpha.RepositoryTagR\x03tag\"2\n\x17GetRepositoryTagRequest\x12\x17\n\x04name\x18\x01 \x01(\tB\x03\xe0\x41\x02R\x04name\"V\n\x18GetRepositoryTagResponse\x12:\n\x03tag\x18\x01 \x01(\x0b\x32(.artifact.artifact.v1alpha.RepositoryTagR\x03tag\"5\n\x1a\x44\x65leteRepositoryTagRequest\x12\x17\n\x04name\x18\x01 \x01(\tB\x03\xe0\x41\x02R\x04name\"\x1d\n\x1b\x44\x65leteRepositoryTagResponse\"\xd1\x03\n\tObjectURL\x12\x10\n\x03uid\x18\x01 \x01(\tR\x03uid\x12#\n\rnamespace_uid\x18\x02 \x01(\tR\x0cnamespaceUid\x12\x1d\n\nobject_uid\x18\x03 \x01(\tR\tobjectUid\x12>\n\rurl_expire_at\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\x0burlExpireAt\x12$\n\x0eminio_url_path\x18\x05 \x01(\tR\x0cminioUrlPath\x12(\n\x10\x65ncoded_url_path\x18\x06 \x01(\tR\x0e\x65ncodedUrlPath\x12\x12\n\x04type\x18\x07 \x01(\tR\x04type\x12;\n\x0b\x63reate_time\x18\x08 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\ncreateTime\x12;\n\x0bupdate_time\x18\t \x01(\x0b\x32\x1a.google.protobuf.TimestampR\nupdateTime\x12@\n\x0b\x64\x65lete_time\x18\n \x01(\x0b\x32\x1a.google.protobuf.TimestampH\x00R\ndeleteTime\x88\x01\x01\x42\x0e\n\x0c_delete_time\"$\n\x10GetObjectRequest\x12\x10\n\x03uid\x18\x01 \x01(\tR\x03uid\"N\n\x11GetObjectResponse\x12\x39\n\x06object\x18\x01 \x01(\x0b\x32!.artifact.artifact.v1alpha.ObjectR\x06object\"k\n\x13GetObjectURLRequest\x12\x10\n\x03uid\x18\x01 \x01(\tR\x03uid\x12-\n\x10\x65ncoded_url_path\x18\x02 \x01(\tH\x00R\x0e\x65ncodedUrlPath\x88\x01\x01\x42\x13\n\x11_encoded_url_path\"[\n\x14GetObjectURLResponse\x12\x43\n\nobject_url\x18\x01 \x01(\x0b\x32$.artifact.artifact.v1alpha.ObjectURLR\tobjectUrl\"\x87\x02\n\x13UpdateObjectRequest\x12\x10\n\x03uid\x18\x01 \x01(\tR\x03uid\x12\x17\n\x04size\x18\x02 \x01(\x03H\x00R\x04size\x88\x01\x01\x12\x17\n\x04type\x18\x03 \x01(\tH\x01R\x04type\x88\x01\x01\x12$\n\x0bis_uploaded\x18\x04 \x01(\x08H\x02R\nisUploaded\x88\x01\x01\x12M\n\x12last_modified_time\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.TimestampH\x03R\x10lastModifiedTime\x88\x01\x01\x42\x07\n\x05_sizeB\x07\n\x05_typeB\x0e\n\x0c_is_uploadedB\x15\n\x13_last_modified_time\"Q\n\x14UpdateObjectResponse\x12\x39\n\x06object\x18\x01 \x01(\x0b\x32!.artifact.artifact.v1alpha.ObjectR\x06object\"\x99\x04\n\x07\x43\x61talog\x12\x1f\n\x0b\x63\x61talog_uid\x18\x01 \x01(\tR\ncatalogUid\x12\x1d\n\ncatalog_id\x18\x02 \x01(\tR\tcatalogId\x12\x12\n\x04name\x18\x03 \x01(\tR\x04name\x12 \n\x0b\x64\x65scription\x18\x04 \x01(\tR\x0b\x64\x65scription\x12\x1f\n\x0b\x63reate_time\x18\x05 \x01(\tR\ncreateTime\x12\x1f\n\x0bupdate_time\x18\x06 \x01(\tR\nupdateTime\x12\x1d\n\nowner_name\x18\x07 \x01(\tR\townerName\x12\x12\n\x04tags\x18\x08 \x03(\tR\x04tags\x12\x31\n\x14\x63onverting_pipelines\x18\t \x03(\tR\x13\x63onvertingPipelines\x12/\n\x13splitting_pipelines\x18\n \x03(\tR\x12splittingPipelines\x12/\n\x13\x65mbedding_pipelines\x18\x0b \x03(\tR\x12\x65mbeddingPipelines\x12\'\n\x0f\x64ownstream_apps\x18\x0c \x03(\tR\x0e\x64ownstreamApps\x12\x1f\n\x0btotal_files\x18\r \x01(\rR\ntotalFiles\x12!\n\x0ctotal_tokens\x18\x0e \x01(\rR\x0btotalTokens\x12!\n\x0cused_storage\x18\x0f \x01(\x04R\x0busedStorage\"\x83\x01\n\x14\x43reateCatalogRequest\x12!\n\x0cnamespace_id\x18\x01 \x01(\tR\x0bnamespaceId\x12\x12\n\x04name\x18\x02 \x01(\tR\x04name\x12 \n\x0b\x64\x65scription\x18\x03 \x01(\tR\x0b\x64\x65scription\x12\x12\n\x04tags\x18\x04 \x03(\tR\x04tags\"U\n\x15\x43reateCatalogResponse\x12<\n\x07\x63\x61talog\x18\x01 \x01(\x0b\x32\".artifact.artifact.v1alpha.CatalogR\x07\x63\x61talog\"8\n\x13ListCatalogsRequest\x12!\n\x0cnamespace_id\x18\x01 \x01(\tR\x0bnamespaceId\"V\n\x14ListCatalogsResponse\x12>\n\x08\x63\x61talogs\x18\x01 \x03(\x0b\x32\".artifact.artifact.v1alpha.CatalogR\x08\x63\x61talogs\"\x8e\x01\n\x14UpdateCatalogRequest\x12\x1d\n\ncatalog_id\x18\x01 \x01(\tR\tcatalogId\x12 \n\x0b\x64\x65scription\x18\x02 \x01(\tR\x0b\x64\x65scription\x12\x12\n\x04tags\x18\x03 \x03(\tR\x04tags\x12!\n\x0cnamespace_id\x18\x04 \x01(\tR\x0bnamespaceId\"U\n\x15UpdateCatalogResponse\x12<\n\x07\x63\x61talog\x18\x01 \x01(\x0b\x32\".artifact.artifact.v1alpha.CatalogR\x07\x63\x61talog\"X\n\x14\x44\x65leteCatalogRequest\x12!\n\x0cnamespace_id\x18\x01 \x01(\tR\x0bnamespaceId\x12\x1d\n\ncatalog_id\x18\x02 \x01(\tR\tcatalogId\"U\n\x15\x44\x65leteCatalogResponse\x12<\n\x07\x63\x61talog\x18\x01 \x01(\x0b\x32\".artifact.artifact.v1alpha.CatalogR\x07\x63\x61talog\"\xce\x06\n\x04\x46ile\x12\x1e\n\x08\x66ile_uid\x18\x01 \x01(\tB\x03\xe0\x41\x03R\x07\x66ileUid\x12\x17\n\x04name\x18\x02 \x01(\tB\x03\xe0\x41\x02R\x04name\x12<\n\x04type\x18\x03 \x01(\x0e\x32#.artifact.artifact.v1alpha.FileTypeB\x03\xe0\x41\x02R\x04type\x12X\n\x0eprocess_status\x18\x04 \x01(\x0e\x32,.artifact.artifact.v1alpha.FileProcessStatusB\x03\xe0\x41\x03R\rprocessStatus\x12,\n\x0fprocess_outcome\x18\x05 \x01(\tB\x03\xe0\x41\x03R\x0eprocessOutcome\x12%\n\x0bretrievable\x18\x06 \x01(\x08\x42\x03\xe0\x41\x03R\x0bretrievable\x12\x1d\n\x07\x63ontent\x18\x07 \x01(\tB\x03\xe0\x41\x01R\x07\x63ontent\x12 \n\towner_uid\x18\x08 \x01(\tB\x03\xe0\x41\x03R\x08ownerUid\x12$\n\x0b\x63reator_uid\x18\t \x01(\tB\x03\xe0\x41\x03R\ncreatorUid\x12$\n\x0b\x63\x61talog_uid\x18\n \x01(\tB\x03\xe0\x41\x03R\ncatalogUid\x12@\n\x0b\x63reate_time\x18\x0b \x01(\x0b\x32\x1a.google.protobuf.TimestampB\x03\xe0\x41\x03R\ncreateTime\x12@\n\x0bupdate_time\x18\x0c \x01(\x0b\x32\x1a.google.protobuf.TimestampB\x03\xe0\x41\x03R\nupdateTime\x12@\n\x0b\x64\x65lete_time\x18\r \x01(\x0b\x32\x1a.google.protobuf.TimestampB\x03\xe0\x41\x03R\ndeleteTime\x12\x17\n\x04size\x18\x0e \x01(\x03\x42\x03\xe0\x41\x03R\x04size\x12&\n\x0ctotal_chunks\x18\x0f \x01(\x05\x42\x03\xe0\x41\x03R\x0btotalChunks\x12&\n\x0ctotal_tokens\x18\x10 \x01(\x05\x42\x03\xe0\x41\x03R\x0btotalTokens\x12N\n\x11\x65xternal_metadata\x18\x11 \x01(\x0b\x32\x17.google.protobuf.StructB\x03\xe0\x41\x01H\x00R\x10\x65xternalMetadata\x88\x01\x01\x42\x14\n\x12_external_metadata\"\x9b\x01\n\x18UploadCatalogFileRequest\x12&\n\x0cnamespace_id\x18\x01 \x01(\tB\x03\xe0\x41\x02R\x0bnamespaceId\x12\"\n\ncatalog_id\x18\x02 \x01(\tB\x03\xe0\x41\x02R\tcatalogId\x12\x33\n\x04\x66ile\x18\x03 \x01(\x0b\x32\x1f.artifact.artifact.v1alpha.FileR\x04\x66ile\"P\n\x19UploadCatalogFileResponse\x12\x33\n\x04\x66ile\x18\x01 \x01(\x0b\x32\x1f.artifact.artifact.v1alpha.FileR\x04\x66ile\":\n\x18\x44\x65leteCatalogFileRequest\x12\x1e\n\x08\x66ile_uid\x18\x01 \x01(\tB\x03\xe0\x41\x02R\x07\x66ileUid\"6\n\x19\x44\x65leteCatalogFileResponse\x12\x19\n\x08\x66ile_uid\x18\x01 \x01(\tR\x07\x66ileUid\">\n\x1aProcessCatalogFilesRequest\x12 \n\tfile_uids\x18\x01 \x03(\tB\x03\xe0\x41\x02R\x08\x66ileUids\"T\n\x1bProcessCatalogFilesResponse\x12\x35\n\x05\x66iles\x18\x01 \x03(\x0b\x32\x1f.artifact.artifact.v1alpha.FileR\x05\x66iles\":\n\x16ListCatalogFilesFilter\x12 \n\tfile_uids\x18\x02 \x03(\tB\x03\xe0\x41\x01R\x08\x66ileUids\"\xf1\x01\n\x17ListCatalogFilesRequest\x12!\n\x0cnamespace_id\x18\x01 \x01(\tR\x0bnamespaceId\x12\x1d\n\ncatalog_id\x18\x02 \x01(\tR\tcatalogId\x12 \n\tpage_size\x18\x03 \x01(\x05\x42\x03\xe0\x41\x01R\x08pageSize\x12\"\n\npage_token\x18\x04 \x01(\tB\x03\xe0\x41\x01R\tpageToken\x12N\n\x06\x66ilter\x18\x05 \x01(\x0b\x32\x31.artifact.artifact.v1alpha.ListCatalogFilesFilterB\x03\xe0\x41\x01R\x06\x66ilter\"\x80\x02\n\x18ListCatalogFilesResponse\x12\x35\n\x05\x66iles\x18\x01 \x03(\x0b\x32\x1f.artifact.artifact.v1alpha.FileR\x05\x66iles\x12\x1d\n\ntotal_size\x18\x02 \x01(\x05R\ttotalSize\x12\x1b\n\tpage_size\x18\x03 \x01(\x05R\x08pageSize\x12&\n\x0fnext_page_token\x18\x04 \x01(\tR\rnextPageToken\x12I\n\x06\x66ilter\x18\x05 \x01(\x0b\x32\x31.artifact.artifact.v1alpha.ListCatalogFilesFilterR\x06\x66ilter\"\xcd\x06\n\nCatalogRun\x12\x15\n\x03uid\x18\x01 \x01(\tB\x03\xe0\x41\x03R\x03uid\x12$\n\x0b\x63\x61talog_uid\x18\x02 \x01(\tB\x03\xe0\x41\x03R\ncatalogUid\x12#\n\tfile_uids\x18\x03 \x03(\tB\x06\xe0\x41\x03\xe0\x41\x01R\x08\x66ileUids\x12H\n\x06\x61\x63tion\x18\x04 \x01(\x0e\x32+.artifact.artifact.v1alpha.CatalogRunActionB\x03\xe0\x41\x03R\x06\x61\x63tion\x12:\n\x06status\x18\x05 \x01(\x0e\x32\x1d.common.run.v1alpha.RunStatusB\x03\xe0\x41\x03R\x06status\x12:\n\x06source\x18\x06 \x01(\x0e\x32\x1d.common.run.v1alpha.RunSourceB\x03\xe0\x41\x03R\x06source\x12\x32\n\x0etotal_duration\x18\x07 \x01(\x05\x42\x06\xe0\x41\x03\xe0\x41\x01H\x00R\rtotalDuration\x88\x01\x01\x12(\n\trunner_id\x18\x08 \x01(\tB\x06\xe0\x41\x03\xe0\x41\x01H\x01R\x08runnerId\x88\x01\x01\x12.\n\x0cnamespace_id\x18\t \x01(\tB\x06\xe0\x41\x03\xe0\x41\x01H\x02R\x0bnamespaceId\x88\x01\x01\x12>\n\x07payload\x18\x0b \x01(\x0b\x32\x17.google.protobuf.StructB\x06\xe0\x41\x03\xe0\x41\x01H\x03R\x07payload\x88\x01\x01\x12>\n\nstart_time\x18\x0c \x01(\x0b\x32\x1a.google.protobuf.TimestampB\x03\xe0\x41\x03R\tstartTime\x12L\n\rcomplete_time\x18\x0f \x01(\x0b\x32\x1a.google.protobuf.TimestampB\x06\xe0\x41\x03\xe0\x41\x01H\x04R\x0c\x63ompleteTime\x88\x01\x01\x12!\n\x05\x65rror\x18\x10 \x01(\tB\x06\xe0\x41\x03\xe0\x41\x01H\x05R\x05\x65rror\x88\x01\x01\x12\x30\n\rcredit_amount\x18\x11 \x01(\x02\x42\x06\xe0\x41\x03\xe0\x41\x01H\x06R\x0c\x63reditAmount\x88\x01\x01\x42\x11\n\x0f_total_durationB\x0c\n\n_runner_idB\x0f\n\r_namespace_idB\n\n\x08_payloadB\x10\n\x0e_complete_timeB\x08\n\x06_errorB\x10\n\x0e_credit_amount\"\xc7\x01\n\x17ListCatalogRunsResponse\x12M\n\x0c\x63\x61talog_runs\x18\x01 \x03(\x0b\x32%.artifact.artifact.v1alpha.CatalogRunB\x03\xe0\x41\x03R\x0b\x63\x61talogRuns\x12\"\n\ntotal_size\x18\x02 \x01(\x05\x42\x03\xe0\x41\x03R\ttotalSize\x12\x17\n\x04page\x18\x03 \x01(\x05\x42\x03\xe0\x41\x03R\x04page\x12 \n\tpage_size\x18\x04 \x01(\x05\x42\x03\xe0\x41\x03R\x08pageSize\"\xfe\x01\n\x16ListCatalogRunsRequest\x12&\n\x0cnamespace_id\x18\x01 \x01(\tB\x03\xe0\x41\x02R\x0bnamespaceId\x12\"\n\ncatalog_id\x18\x02 \x01(\tB\x03\xe0\x41\x02R\tcatalogId\x12\x17\n\x04page\x18\x03 \x01(\x05\x42\x03\xe0\x41\x01R\x04page\x12 \n\tpage_size\x18\x04 \x01(\x05\x42\x03\xe0\x41\x01R\x08pageSize\x12 \n\x06\x66ilter\x18\x06 \x01(\tB\x03\xe0\x41\x01H\x00R\x06\x66ilter\x88\x01\x01\x12#\n\x08order_by\x18\x07 \x01(\tB\x03\xe0\x41\x01H\x01R\x07orderBy\x88\x01\x01\x42\t\n\x07_filterB\x0b\n\t_order_by*\xa9\x02\n\x11\x46ileProcessStatus\x12#\n\x1f\x46ILE_PROCESS_STATUS_UNSPECIFIED\x10\x00\x12\"\n\x1e\x46ILE_PROCESS_STATUS_NOTSTARTED\x10\x01\x12\x1f\n\x1b\x46ILE_PROCESS_STATUS_WAITING\x10\x02\x12\"\n\x1e\x46ILE_PROCESS_STATUS_CONVERTING\x10\x03\x12 \n\x1c\x46ILE_PROCESS_STATUS_CHUNKING\x10\x04\x12!\n\x1d\x46ILE_PROCESS_STATUS_EMBEDDING\x10\x05\x12!\n\x1d\x46ILE_PROCESS_STATUS_COMPLETED\x10\x06\x12\x1e\n\x1a\x46ILE_PROCESS_STATUS_FAILED\x10\x07*\xba\x02\n\x08\x46ileType\x12\x19\n\x15\x46ILE_TYPE_UNSPECIFIED\x10\x00\x12\x12\n\x0e\x46ILE_TYPE_TEXT\x10\x01\x12\x11\n\rFILE_TYPE_PDF\x10\x02\x12\x16\n\x12\x46ILE_TYPE_MARKDOWN\x10\x03\x12\x11\n\rFILE_TYPE_PNG\x10\x04\x12\x12\n\x0e\x46ILE_TYPE_JPEG\x10\x05\x12\x11\n\rFILE_TYPE_JPG\x10\x06\x12\x12\n\x0e\x46ILE_TYPE_HTML\x10\x07\x12\x12\n\x0e\x46ILE_TYPE_DOCX\x10\x08\x12\x11\n\rFILE_TYPE_DOC\x10\t\x12\x11\n\rFILE_TYPE_PPT\x10\n\x12\x12\n\x0e\x46ILE_TYPE_PPTX\x10\x0b\x12\x11\n\rFILE_TYPE_XLS\x10\x0c\x12\x12\n\x0e\x46ILE_TYPE_XLSX\x10\r\x12\x11\n\rFILE_TYPE_CSV\x10\x0e*\x80\x02\n\x10\x43\x61talogRunAction\x12\"\n\x1e\x43\x41TALOG_RUN_ACTION_UNSPECIFIED\x10\x00\x12\x1d\n\x19\x43\x41TALOG_RUN_ACTION_CREATE\x10\x01\x12\x1d\n\x19\x43\x41TALOG_RUN_ACTION_UPDATE\x10\x02\x12\x1d\n\x19\x43\x41TALOG_RUN_ACTION_DELETE\x10\x03\x12\"\n\x1e\x43\x41TALOG_RUN_ACTION_CREATE_FILE\x10\x04\x12#\n\x1f\x43\x41TALOG_RUN_ACTION_PROCESS_FILE\x10\x05\x12\"\n\x1e\x43\x41TALOG_RUN_ACTION_DELETE_FILE\x10\x06\x42\x81\x02\n\x1d\x63om.artifact.artifact.v1alphaB\rArtifactProtoP\x01ZKgithub.com/instill-ai/protogen-go/artifact/artifact/v1alpha;artifactv1alpha\xa2\x02\x03\x41\x41X\xaa\x02\x19\x41rtifact.Artifact.V1alpha\xca\x02\x19\x41rtifact\\Artifact\\V1alpha\xe2\x02%Artifact\\Artifact\\V1alpha\\GPBMetadata\xea\x02\x1b\x41rtifact::Artifact::V1alphab\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'artifact.artifact.v1alpha.artifact_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\035com.artifact.artifact.v1alphaB\rArtifactProtoP\001ZKgithub.com/instill-ai/protogen-go/artifact/artifact/v1alpha;artifactv1alpha\242\002\003AAX\252\002\031Artifact.Artifact.V1alpha\312\002\031Artifact\\Artifact\\V1alpha\342\002%Artifact\\Artifact\\V1alpha\\GPBMetadata\352\002\033Artifact::Artifact::V1alpha'
  _LIVENESSREQUEST.fields_by_name['health_check_request']._options = None
  _LIVENESSREQUEST.fields_by_name['health_check_request']._serialized_options = b'\340A\001'
  _READINESSREQUEST.fields_by_name['health_check_request']._options = None
  _READINESSREQUEST.fields_by_name['health_check_request']._serialized_options = b'\340A\001'
  _REPOSITORYTAG.fields_by_name['name']._options = None
  _REPOSITORYTAG.fields_by_name['name']._serialized_options = b'\340A\005'
  _REPOSITORYTAG.fields_by_name['id']._options = None
  _REPOSITORYTAG.fields_by_name['id']._serialized_options = b'\340A\005'
  _REPOSITORYTAG.fields_by_name['digest']._options = None
  _REPOSITORYTAG.fields_by_name['digest']._serialized_options = b'\340A\001'
  _REPOSITORYTAG.fields_by_name['update_time']._options = None
  _REPOSITORYTAG.fields_by_name['update_time']._serialized_options = b'\340A\003\340A\001'
  _LISTREPOSITORYTAGSREQUEST.fields_by_name['page_size']._options = None
  _LISTREPOSITORYTAGSREQUEST.fields_by_name['page_size']._serialized_options = b'\340A\001'
  _LISTREPOSITORYTAGSREQUEST.fields_by_name['page']._options = None
  _LISTREPOSITORYTAGSREQUEST.fields_by_name['page']._serialized_options = b'\340A\001'
  _LISTREPOSITORYTAGSREQUEST.fields_by_name['parent']._options = None
  _LISTREPOSITORYTAGSREQUEST.fields_by_name['parent']._serialized_options = b'\340A\002\372A\035\n\033api.instill.tech/Repository'
  _GETREPOSITORYTAGREQUEST.fields_by_name['name']._options = None
  _GETREPOSITORYTAGREQUEST.fields_by_name['name']._serialized_options = b'\340A\002'
  _DELETEREPOSITORYTAGREQUEST.fields_by_name['name']._options = None
  _DELETEREPOSITORYTAGREQUEST.fields_by_name['name']._serialized_options = b'\340A\002'
  _FILE.fields_by_name['file_uid']._options = None
  _FILE.fields_by_name['file_uid']._serialized_options = b'\340A\003'
  _FILE.fields_by_name['name']._options = None
  _FILE.fields_by_name['name']._serialized_options = b'\340A\002'
  _FILE.fields_by_name['type']._options = None
  _FILE.fields_by_name['type']._serialized_options = b'\340A\002'
  _FILE.fields_by_name['process_status']._options = None
  _FILE.fields_by_name['process_status']._serialized_options = b'\340A\003'
  _FILE.fields_by_name['process_outcome']._options = None
  _FILE.fields_by_name['process_outcome']._serialized_options = b'\340A\003'
  _FILE.fields_by_name['retrievable']._options = None
  _FILE.fields_by_name['retrievable']._serialized_options = b'\340A\003'
  _FILE.fields_by_name['content']._options = None
  _FILE.fields_by_name['content']._serialized_options = b'\340A\001'
  _FILE.fields_by_name['owner_uid']._options = None
  _FILE.fields_by_name['owner_uid']._serialized_options = b'\340A\003'
  _FILE.fields_by_name['creator_uid']._options = None
  _FILE.fields_by_name['creator_uid']._serialized_options = b'\340A\003'
  _FILE.fields_by_name['catalog_uid']._options = None
  _FILE.fields_by_name['catalog_uid']._serialized_options = b'\340A\003'
  _FILE.fields_by_name['create_time']._options = None
  _FILE.fields_by_name['create_time']._serialized_options = b'\340A\003'
  _FILE.fields_by_name['update_time']._options = None
  _FILE.fields_by_name['update_time']._serialized_options = b'\340A\003'
  _FILE.fields_by_name['delete_time']._options = None
  _FILE.fields_by_name['delete_time']._serialized_options = b'\340A\003'
  _FILE.fields_by_name['size']._options = None
  _FILE.fields_by_name['size']._serialized_options = b'\340A\003'
  _FILE.fields_by_name['total_chunks']._options = None
  _FILE.fields_by_name['total_chunks']._serialized_options = b'\340A\003'
  _FILE.fields_by_name['total_tokens']._options = None
  _FILE.fields_by_name['total_tokens']._serialized_options = b'\340A\003'
  _FILE.fields_by_name['external_metadata']._options = None
  _FILE.fields_by_name['external_metadata']._serialized_options = b'\340A\001'
  _UPLOADCATALOGFILEREQUEST.fields_by_name['namespace_id']._options = None
  _UPLOADCATALOGFILEREQUEST.fields_by_name['namespace_id']._serialized_options = b'\340A\002'
  _UPLOADCATALOGFILEREQUEST.fields_by_name['catalog_id']._options = None
  _UPLOADCATALOGFILEREQUEST.fields_by_name['catalog_id']._serialized_options = b'\340A\002'
  _DELETECATALOGFILEREQUEST.fields_by_name['file_uid']._options = None
  _DELETECATALOGFILEREQUEST.fields_by_name['file_uid']._serialized_options = b'\340A\002'
  _PROCESSCATALOGFILESREQUEST.fields_by_name['file_uids']._options = None
  _PROCESSCATALOGFILESREQUEST.fields_by_name['file_uids']._serialized_options = b'\340A\002'
  _LISTCATALOGFILESFILTER.fields_by_name['file_uids']._options = None
  _LISTCATALOGFILESFILTER.fields_by_name['file_uids']._serialized_options = b'\340A\001'
  _LISTCATALOGFILESREQUEST.fields_by_name['page_size']._options = None
  _LISTCATALOGFILESREQUEST.fields_by_name['page_size']._serialized_options = b'\340A\001'
  _LISTCATALOGFILESREQUEST.fields_by_name['page_token']._options = None
  _LISTCATALOGFILESREQUEST.fields_by_name['page_token']._serialized_options = b'\340A\001'
  _LISTCATALOGFILESREQUEST.fields_by_name['filter']._options = None
  _LISTCATALOGFILESREQUEST.fields_by_name['filter']._serialized_options = b'\340A\001'
  _CATALOGRUN.fields_by_name['uid']._options = None
  _CATALOGRUN.fields_by_name['uid']._serialized_options = b'\340A\003'
  _CATALOGRUN.fields_by_name['catalog_uid']._options = None
  _CATALOGRUN.fields_by_name['catalog_uid']._serialized_options = b'\340A\003'
  _CATALOGRUN.fields_by_name['file_uids']._options = None
  _CATALOGRUN.fields_by_name['file_uids']._serialized_options = b'\340A\003\340A\001'
  _CATALOGRUN.fields_by_name['action']._options = None
  _CATALOGRUN.fields_by_name['action']._serialized_options = b'\340A\003'
  _CATALOGRUN.fields_by_name['status']._options = None
  _CATALOGRUN.fields_by_name['status']._serialized_options = b'\340A\003'
  _CATALOGRUN.fields_by_name['source']._options = None
  _CATALOGRUN.fields_by_name['source']._serialized_options = b'\340A\003'
  _CATALOGRUN.fields_by_name['total_duration']._options = None
  _CATALOGRUN.fields_by_name['total_duration']._serialized_options = b'\340A\003\340A\001'
  _CATALOGRUN.fields_by_name['runner_id']._options = None
  _CATALOGRUN.fields_by_name['runner_id']._serialized_options = b'\340A\003\340A\001'
  _CATALOGRUN.fields_by_name['namespace_id']._options = None
  _CATALOGRUN.fields_by_name['namespace_id']._serialized_options = b'\340A\003\340A\001'
  _CATALOGRUN.fields_by_name['payload']._options = None
  _CATALOGRUN.fields_by_name['payload']._serialized_options = b'\340A\003\340A\001'
  _CATALOGRUN.fields_by_name['start_time']._options = None
  _CATALOGRUN.fields_by_name['start_time']._serialized_options = b'\340A\003'
  _CATALOGRUN.fields_by_name['complete_time']._options = None
  _CATALOGRUN.fields_by_name['complete_time']._serialized_options = b'\340A\003\340A\001'
  _CATALOGRUN.fields_by_name['error']._options = None
  _CATALOGRUN.fields_by_name['error']._serialized_options = b'\340A\003\340A\001'
  _CATALOGRUN.fields_by_name['credit_amount']._options = None
  _CATALOGRUN.fields_by_name['credit_amount']._serialized_options = b'\340A\003\340A\001'
  _LISTCATALOGRUNSRESPONSE.fields_by_name['catalog_runs']._options = None
  _LISTCATALOGRUNSRESPONSE.fields_by_name['catalog_runs']._serialized_options = b'\340A\003'
  _LISTCATALOGRUNSRESPONSE.fields_by_name['total_size']._options = None
  _LISTCATALOGRUNSRESPONSE.fields_by_name['total_size']._serialized_options = b'\340A\003'
  _LISTCATALOGRUNSRESPONSE.fields_by_name['page']._options = None
  _LISTCATALOGRUNSRESPONSE.fields_by_name['page']._serialized_options = b'\340A\003'
  _LISTCATALOGRUNSRESPONSE.fields_by_name['page_size']._options = None
  _LISTCATALOGRUNSRESPONSE.fields_by_name['page_size']._serialized_options = b'\340A\003'
  _LISTCATALOGRUNSREQUEST.fields_by_name['namespace_id']._options = None
  _LISTCATALOGRUNSREQUEST.fields_by_name['namespace_id']._serialized_options = b'\340A\002'
  _LISTCATALOGRUNSREQUEST.fields_by_name['catalog_id']._options = None
  _LISTCATALOGRUNSREQUEST.fields_by_name['catalog_id']._serialized_options = b'\340A\002'
  _LISTCATALOGRUNSREQUEST.fields_by_name['page']._options = None
  _LISTCATALOGRUNSREQUEST.fields_by_name['page']._serialized_options = b'\340A\001'
  _LISTCATALOGRUNSREQUEST.fields_by_name['page_size']._options = None
  _LISTCATALOGRUNSREQUEST.fields_by_name['page_size']._serialized_options = b'\340A\001'
  _LISTCATALOGRUNSREQUEST.fields_by_name['filter']._options = None
  _LISTCATALOGRUNSREQUEST.fields_by_name['filter']._serialized_options = b'\340A\001'
  _LISTCATALOGRUNSREQUEST.fields_by_name['order_by']._options = None
  _LISTCATALOGRUNSREQUEST.fields_by_name['order_by']._serialized_options = b'\340A\001'
  _globals['_FILEPROCESSSTATUS']._serialized_start=7459
  _globals['_FILEPROCESSSTATUS']._serialized_end=7756
  _globals['_FILETYPE']._serialized_start=7759
  _globals['_FILETYPE']._serialized_end=8073
  _globals['_CATALOGRUNACTION']._serialized_start=8076
  _globals['_CATALOGRUNACTION']._serialized_end=8332
  _globals['_LIVENESSREQUEST']._serialized_start=310
  _globals['_LIVENESSREQUEST']._serialized_end=459
  _globals['_LIVENESSRESPONSE']._serialized_start=461
  _globals['_LIVENESSRESPONSE']._serialized_end=579
  _globals['_READINESSREQUEST']._serialized_start=582
  _globals['_READINESSREQUEST']._serialized_end=732
  _globals['_READINESSRESPONSE']._serialized_start=734
  _globals['_READINESSRESPONSE']._serialized_end=853
  _globals['_REPOSITORYTAG']._serialized_start=856
  _globals['_REPOSITORYTAG']._serialized_end=1015
  _globals['_LISTREPOSITORYTAGSREQUEST']._serialized_start=1018
  _globals['_LISTREPOSITORYTAGSREQUEST']._serialized_end=1198
  _globals['_LISTREPOSITORYTAGSRESPONSE']._serialized_start=1201
  _globals['_LISTREPOSITORYTAGSRESPONSE']._serialized_end=1371
  _globals['_CREATEREPOSITORYTAGREQUEST']._serialized_start=1373
  _globals['_CREATEREPOSITORYTAGREQUEST']._serialized_end=1461
  _globals['_CREATEREPOSITORYTAGRESPONSE']._serialized_start=1463
  _globals['_CREATEREPOSITORYTAGRESPONSE']._serialized_end=1552
  _globals['_GETREPOSITORYTAGREQUEST']._serialized_start=1554
  _globals['_GETREPOSITORYTAGREQUEST']._serialized_end=1604
  _globals['_GETREPOSITORYTAGRESPONSE']._serialized_start=1606
  _globals['_GETREPOSITORYTAGRESPONSE']._serialized_end=1692
  _globals['_DELETEREPOSITORYTAGREQUEST']._serialized_start=1694
  _globals['_DELETEREPOSITORYTAGREQUEST']._serialized_end=1747
  _globals['_DELETEREPOSITORYTAGRESPONSE']._serialized_start=1749
  _globals['_DELETEREPOSITORYTAGRESPONSE']._serialized_end=1778
  _globals['_OBJECTURL']._serialized_start=1781
  _globals['_OBJECTURL']._serialized_end=2246
  _globals['_GETOBJECTREQUEST']._serialized_start=2248
  _globals['_GETOBJECTREQUEST']._serialized_end=2284
  _globals['_GETOBJECTRESPONSE']._serialized_start=2286
  _globals['_GETOBJECTRESPONSE']._serialized_end=2364
  _globals['_GETOBJECTURLREQUEST']._serialized_start=2366
  _globals['_GETOBJECTURLREQUEST']._serialized_end=2473
  _globals['_GETOBJECTURLRESPONSE']._serialized_start=2475
  _globals['_GETOBJECTURLRESPONSE']._serialized_end=2566
  _globals['_UPDATEOBJECTREQUEST']._serialized_start=2569
  _globals['_UPDATEOBJECTREQUEST']._serialized_end=2832
  _globals['_UPDATEOBJECTRESPONSE']._serialized_start=2834
  _globals['_UPDATEOBJECTRESPONSE']._serialized_end=2915
  _globals['_CATALOG']._serialized_start=2918
  _globals['_CATALOG']._serialized_end=3455
  _globals['_CREATECATALOGREQUEST']._serialized_start=3458
  _globals['_CREATECATALOGREQUEST']._serialized_end=3589
  _globals['_CREATECATALOGRESPONSE']._serialized_start=3591
  _globals['_CREATECATALOGRESPONSE']._serialized_end=3676
  _globals['_LISTCATALOGSREQUEST']._serialized_start=3678
  _globals['_LISTCATALOGSREQUEST']._serialized_end=3734
  _globals['_LISTCATALOGSRESPONSE']._serialized_start=3736
  _globals['_LISTCATALOGSRESPONSE']._serialized_end=3822
  _globals['_UPDATECATALOGREQUEST']._serialized_start=3825
  _globals['_UPDATECATALOGREQUEST']._serialized_end=3967
  _globals['_UPDATECATALOGRESPONSE']._serialized_start=3969
  _globals['_UPDATECATALOGRESPONSE']._serialized_end=4054
  _globals['_DELETECATALOGREQUEST']._serialized_start=4056
  _globals['_DELETECATALOGREQUEST']._serialized_end=4144
  _globals['_DELETECATALOGRESPONSE']._serialized_start=4146
  _globals['_DELETECATALOGRESPONSE']._serialized_end=4231
  _globals['_FILE']._serialized_start=4234
  _globals['_FILE']._serialized_end=5080
  _globals['_UPLOADCATALOGFILEREQUEST']._serialized_start=5083
  _globals['_UPLOADCATALOGFILEREQUEST']._serialized_end=5238
  _globals['_UPLOADCATALOGFILERESPONSE']._serialized_start=5240
  _globals['_UPLOADCATALOGFILERESPONSE']._serialized_end=5320
  _globals['_DELETECATALOGFILEREQUEST']._serialized_start=5322
  _globals['_DELETECATALOGFILEREQUEST']._serialized_end=5380
  _globals['_DELETECATALOGFILERESPONSE']._serialized_start=5382
  _globals['_DELETECATALOGFILERESPONSE']._serialized_end=5436
  _globals['_PROCESSCATALOGFILESREQUEST']._serialized_start=5438
  _globals['_PROCESSCATALOGFILESREQUEST']._serialized_end=5500
  _globals['_PROCESSCATALOGFILESRESPONSE']._serialized_start=5502
  _globals['_PROCESSCATALOGFILESRESPONSE']._serialized_end=5586
  _globals['_LISTCATALOGFILESFILTER']._serialized_start=5588
  _globals['_LISTCATALOGFILESFILTER']._serialized_end=5646
  _globals['_LISTCATALOGFILESREQUEST']._serialized_start=5649
  _globals['_LISTCATALOGFILESREQUEST']._serialized_end=5890
  _globals['_LISTCATALOGFILESRESPONSE']._serialized_start=5893
  _globals['_LISTCATALOGFILESRESPONSE']._serialized_end=6149
  _globals['_CATALOGRUN']._serialized_start=6152
  _globals['_CATALOGRUN']._serialized_end=6997
  _globals['_LISTCATALOGRUNSRESPONSE']._serialized_start=7000
  _globals['_LISTCATALOGRUNSRESPONSE']._serialized_end=7199
  _globals['_LISTCATALOGRUNSREQUEST']._serialized_start=7202
  _globals['_LISTCATALOGRUNSREQUEST']._serialized_end=7456
# @@protoc_insertion_point(module_scope)

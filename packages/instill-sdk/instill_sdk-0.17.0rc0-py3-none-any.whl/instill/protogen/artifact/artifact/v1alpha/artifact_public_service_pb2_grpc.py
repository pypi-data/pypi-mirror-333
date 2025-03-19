# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from artifact.artifact.v1alpha import artifact_pb2 as artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2
from artifact.artifact.v1alpha import chunk_pb2 as artifact_dot_artifact_dot_v1alpha_dot_chunk__pb2
from artifact.artifact.v1alpha import file_catalog_pb2 as artifact_dot_artifact_dot_v1alpha_dot_file__catalog__pb2
from artifact.artifact.v1alpha import object_pb2 as artifact_dot_artifact_dot_v1alpha_dot_object__pb2
from artifact.artifact.v1alpha import qa_pb2 as artifact_dot_artifact_dot_v1alpha_dot_qa__pb2


class ArtifactPublicServiceStub(object):
    """ArtifactPublicService exposes the public endpoints that allow clients to
    manage artifacts.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Liveness = channel.unary_unary(
                '/artifact.artifact.v1alpha.ArtifactPublicService/Liveness',
                request_serializer=artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.LivenessRequest.SerializeToString,
                response_deserializer=artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.LivenessResponse.FromString,
                )
        self.Readiness = channel.unary_unary(
                '/artifact.artifact.v1alpha.ArtifactPublicService/Readiness',
                request_serializer=artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.ReadinessRequest.SerializeToString,
                response_deserializer=artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.ReadinessResponse.FromString,
                )
        self.CreateCatalog = channel.unary_unary(
                '/artifact.artifact.v1alpha.ArtifactPublicService/CreateCatalog',
                request_serializer=artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.CreateCatalogRequest.SerializeToString,
                response_deserializer=artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.CreateCatalogResponse.FromString,
                )
        self.ListCatalogs = channel.unary_unary(
                '/artifact.artifact.v1alpha.ArtifactPublicService/ListCatalogs',
                request_serializer=artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.ListCatalogsRequest.SerializeToString,
                response_deserializer=artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.ListCatalogsResponse.FromString,
                )
        self.UpdateCatalog = channel.unary_unary(
                '/artifact.artifact.v1alpha.ArtifactPublicService/UpdateCatalog',
                request_serializer=artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.UpdateCatalogRequest.SerializeToString,
                response_deserializer=artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.UpdateCatalogResponse.FromString,
                )
        self.DeleteCatalog = channel.unary_unary(
                '/artifact.artifact.v1alpha.ArtifactPublicService/DeleteCatalog',
                request_serializer=artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.DeleteCatalogRequest.SerializeToString,
                response_deserializer=artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.DeleteCatalogResponse.FromString,
                )
        self.UploadCatalogFile = channel.unary_unary(
                '/artifact.artifact.v1alpha.ArtifactPublicService/UploadCatalogFile',
                request_serializer=artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.UploadCatalogFileRequest.SerializeToString,
                response_deserializer=artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.UploadCatalogFileResponse.FromString,
                )
        self.DeleteCatalogFile = channel.unary_unary(
                '/artifact.artifact.v1alpha.ArtifactPublicService/DeleteCatalogFile',
                request_serializer=artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.DeleteCatalogFileRequest.SerializeToString,
                response_deserializer=artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.DeleteCatalogFileResponse.FromString,
                )
        self.ProcessCatalogFiles = channel.unary_unary(
                '/artifact.artifact.v1alpha.ArtifactPublicService/ProcessCatalogFiles',
                request_serializer=artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.ProcessCatalogFilesRequest.SerializeToString,
                response_deserializer=artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.ProcessCatalogFilesResponse.FromString,
                )
        self.ListCatalogFiles = channel.unary_unary(
                '/artifact.artifact.v1alpha.ArtifactPublicService/ListCatalogFiles',
                request_serializer=artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.ListCatalogFilesRequest.SerializeToString,
                response_deserializer=artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.ListCatalogFilesResponse.FromString,
                )
        self.ListChunks = channel.unary_unary(
                '/artifact.artifact.v1alpha.ArtifactPublicService/ListChunks',
                request_serializer=artifact_dot_artifact_dot_v1alpha_dot_chunk__pb2.ListChunksRequest.SerializeToString,
                response_deserializer=artifact_dot_artifact_dot_v1alpha_dot_chunk__pb2.ListChunksResponse.FromString,
                )
        self.GetSourceFile = channel.unary_unary(
                '/artifact.artifact.v1alpha.ArtifactPublicService/GetSourceFile',
                request_serializer=artifact_dot_artifact_dot_v1alpha_dot_chunk__pb2.GetSourceFileRequest.SerializeToString,
                response_deserializer=artifact_dot_artifact_dot_v1alpha_dot_chunk__pb2.GetSourceFileResponse.FromString,
                )
        self.UpdateChunk = channel.unary_unary(
                '/artifact.artifact.v1alpha.ArtifactPublicService/UpdateChunk',
                request_serializer=artifact_dot_artifact_dot_v1alpha_dot_chunk__pb2.UpdateChunkRequest.SerializeToString,
                response_deserializer=artifact_dot_artifact_dot_v1alpha_dot_chunk__pb2.UpdateChunkResponse.FromString,
                )
        self.SimilarityChunksSearch = channel.unary_unary(
                '/artifact.artifact.v1alpha.ArtifactPublicService/SimilarityChunksSearch',
                request_serializer=artifact_dot_artifact_dot_v1alpha_dot_chunk__pb2.SimilarityChunksSearchRequest.SerializeToString,
                response_deserializer=artifact_dot_artifact_dot_v1alpha_dot_chunk__pb2.SimilarityChunksSearchResponse.FromString,
                )
        self.QuestionAnswering = channel.unary_unary(
                '/artifact.artifact.v1alpha.ArtifactPublicService/QuestionAnswering',
                request_serializer=artifact_dot_artifact_dot_v1alpha_dot_qa__pb2.QuestionAnsweringRequest.SerializeToString,
                response_deserializer=artifact_dot_artifact_dot_v1alpha_dot_qa__pb2.QuestionAnsweringResponse.FromString,
                )
        self.GetFileCatalog = channel.unary_unary(
                '/artifact.artifact.v1alpha.ArtifactPublicService/GetFileCatalog',
                request_serializer=artifact_dot_artifact_dot_v1alpha_dot_file__catalog__pb2.GetFileCatalogRequest.SerializeToString,
                response_deserializer=artifact_dot_artifact_dot_v1alpha_dot_file__catalog__pb2.GetFileCatalogResponse.FromString,
                )
        self.ListCatalogRuns = channel.unary_unary(
                '/artifact.artifact.v1alpha.ArtifactPublicService/ListCatalogRuns',
                request_serializer=artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.ListCatalogRunsRequest.SerializeToString,
                response_deserializer=artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.ListCatalogRunsResponse.FromString,
                )
        self.GetObjectUploadURL = channel.unary_unary(
                '/artifact.artifact.v1alpha.ArtifactPublicService/GetObjectUploadURL',
                request_serializer=artifact_dot_artifact_dot_v1alpha_dot_object__pb2.GetObjectUploadURLRequest.SerializeToString,
                response_deserializer=artifact_dot_artifact_dot_v1alpha_dot_object__pb2.GetObjectUploadURLResponse.FromString,
                )
        self.GetObjectDownloadURL = channel.unary_unary(
                '/artifact.artifact.v1alpha.ArtifactPublicService/GetObjectDownloadURL',
                request_serializer=artifact_dot_artifact_dot_v1alpha_dot_object__pb2.GetObjectDownloadURLRequest.SerializeToString,
                response_deserializer=artifact_dot_artifact_dot_v1alpha_dot_object__pb2.GetObjectDownloadURLResponse.FromString,
                )


class ArtifactPublicServiceServicer(object):
    """ArtifactPublicService exposes the public endpoints that allow clients to
    manage artifacts.
    """

    def Liveness(self, request, context):
        """Check if the artifact server is alive

        See https://github.com/grpc/grpc/blob/master/doc/health-checking.md.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Readiness(self, request, context):
        """Check if the artifact server is ready

        See https://github.com/grpc/grpc/blob/master/doc/health-checking.md
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateCatalog(self, request, context):
        """Create a catalog

        Creates a catalog.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListCatalogs(self, request, context):
        """Get all catalogs info

        Returns a paginated list of catalogs.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateCatalog(self, request, context):
        """Update a catalog info

        Updates the information of a catalog.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteCatalog(self, request, context):
        """Delete a catalog

        Deletes a catalog.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UploadCatalogFile(self, request, context):
        """Create a file

        Creates a file.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteCatalogFile(self, request, context):
        """Delete a file

        Deletes a file.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ProcessCatalogFiles(self, request, context):
        """Process catalog files

        Processes catalog files.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListCatalogFiles(self, request, context):
        """List catalog files

        Returns a paginated list of catalog files.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListChunks(self, request, context):
        """List catalog chunks

        Returns a paginated list of catalog chunks.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetSourceFile(self, request, context):
        """Get catalog single-source-of-truth file

        Gets the single-source-of-truth file of a catalog.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateChunk(self, request, context):
        """Update catalog chunk

        Updates a catalog chunk.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SimilarityChunksSearch(self, request, context):
        """Retrieve similar chunks

        Returns the similar chunks.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def QuestionAnswering(self, request, context):
        """Ask a question

        Asks a question.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetFileCatalog(self, request, context):
        """Get file catalog

        Get the catalog file.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListCatalogRuns(self, request, context):
        """List Catalog Runs

        Returns a paginated list of catalog runs.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetObjectUploadURL(self, request, context):
        """Get Object Upload URL

        Returns the upload URL of an object.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetObjectDownloadURL(self, request, context):
        """Get Object Download URL

        Returns the download URL of an object.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ArtifactPublicServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Liveness': grpc.unary_unary_rpc_method_handler(
                    servicer.Liveness,
                    request_deserializer=artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.LivenessRequest.FromString,
                    response_serializer=artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.LivenessResponse.SerializeToString,
            ),
            'Readiness': grpc.unary_unary_rpc_method_handler(
                    servicer.Readiness,
                    request_deserializer=artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.ReadinessRequest.FromString,
                    response_serializer=artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.ReadinessResponse.SerializeToString,
            ),
            'CreateCatalog': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateCatalog,
                    request_deserializer=artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.CreateCatalogRequest.FromString,
                    response_serializer=artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.CreateCatalogResponse.SerializeToString,
            ),
            'ListCatalogs': grpc.unary_unary_rpc_method_handler(
                    servicer.ListCatalogs,
                    request_deserializer=artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.ListCatalogsRequest.FromString,
                    response_serializer=artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.ListCatalogsResponse.SerializeToString,
            ),
            'UpdateCatalog': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateCatalog,
                    request_deserializer=artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.UpdateCatalogRequest.FromString,
                    response_serializer=artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.UpdateCatalogResponse.SerializeToString,
            ),
            'DeleteCatalog': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteCatalog,
                    request_deserializer=artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.DeleteCatalogRequest.FromString,
                    response_serializer=artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.DeleteCatalogResponse.SerializeToString,
            ),
            'UploadCatalogFile': grpc.unary_unary_rpc_method_handler(
                    servicer.UploadCatalogFile,
                    request_deserializer=artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.UploadCatalogFileRequest.FromString,
                    response_serializer=artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.UploadCatalogFileResponse.SerializeToString,
            ),
            'DeleteCatalogFile': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteCatalogFile,
                    request_deserializer=artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.DeleteCatalogFileRequest.FromString,
                    response_serializer=artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.DeleteCatalogFileResponse.SerializeToString,
            ),
            'ProcessCatalogFiles': grpc.unary_unary_rpc_method_handler(
                    servicer.ProcessCatalogFiles,
                    request_deserializer=artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.ProcessCatalogFilesRequest.FromString,
                    response_serializer=artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.ProcessCatalogFilesResponse.SerializeToString,
            ),
            'ListCatalogFiles': grpc.unary_unary_rpc_method_handler(
                    servicer.ListCatalogFiles,
                    request_deserializer=artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.ListCatalogFilesRequest.FromString,
                    response_serializer=artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.ListCatalogFilesResponse.SerializeToString,
            ),
            'ListChunks': grpc.unary_unary_rpc_method_handler(
                    servicer.ListChunks,
                    request_deserializer=artifact_dot_artifact_dot_v1alpha_dot_chunk__pb2.ListChunksRequest.FromString,
                    response_serializer=artifact_dot_artifact_dot_v1alpha_dot_chunk__pb2.ListChunksResponse.SerializeToString,
            ),
            'GetSourceFile': grpc.unary_unary_rpc_method_handler(
                    servicer.GetSourceFile,
                    request_deserializer=artifact_dot_artifact_dot_v1alpha_dot_chunk__pb2.GetSourceFileRequest.FromString,
                    response_serializer=artifact_dot_artifact_dot_v1alpha_dot_chunk__pb2.GetSourceFileResponse.SerializeToString,
            ),
            'UpdateChunk': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateChunk,
                    request_deserializer=artifact_dot_artifact_dot_v1alpha_dot_chunk__pb2.UpdateChunkRequest.FromString,
                    response_serializer=artifact_dot_artifact_dot_v1alpha_dot_chunk__pb2.UpdateChunkResponse.SerializeToString,
            ),
            'SimilarityChunksSearch': grpc.unary_unary_rpc_method_handler(
                    servicer.SimilarityChunksSearch,
                    request_deserializer=artifact_dot_artifact_dot_v1alpha_dot_chunk__pb2.SimilarityChunksSearchRequest.FromString,
                    response_serializer=artifact_dot_artifact_dot_v1alpha_dot_chunk__pb2.SimilarityChunksSearchResponse.SerializeToString,
            ),
            'QuestionAnswering': grpc.unary_unary_rpc_method_handler(
                    servicer.QuestionAnswering,
                    request_deserializer=artifact_dot_artifact_dot_v1alpha_dot_qa__pb2.QuestionAnsweringRequest.FromString,
                    response_serializer=artifact_dot_artifact_dot_v1alpha_dot_qa__pb2.QuestionAnsweringResponse.SerializeToString,
            ),
            'GetFileCatalog': grpc.unary_unary_rpc_method_handler(
                    servicer.GetFileCatalog,
                    request_deserializer=artifact_dot_artifact_dot_v1alpha_dot_file__catalog__pb2.GetFileCatalogRequest.FromString,
                    response_serializer=artifact_dot_artifact_dot_v1alpha_dot_file__catalog__pb2.GetFileCatalogResponse.SerializeToString,
            ),
            'ListCatalogRuns': grpc.unary_unary_rpc_method_handler(
                    servicer.ListCatalogRuns,
                    request_deserializer=artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.ListCatalogRunsRequest.FromString,
                    response_serializer=artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.ListCatalogRunsResponse.SerializeToString,
            ),
            'GetObjectUploadURL': grpc.unary_unary_rpc_method_handler(
                    servicer.GetObjectUploadURL,
                    request_deserializer=artifact_dot_artifact_dot_v1alpha_dot_object__pb2.GetObjectUploadURLRequest.FromString,
                    response_serializer=artifact_dot_artifact_dot_v1alpha_dot_object__pb2.GetObjectUploadURLResponse.SerializeToString,
            ),
            'GetObjectDownloadURL': grpc.unary_unary_rpc_method_handler(
                    servicer.GetObjectDownloadURL,
                    request_deserializer=artifact_dot_artifact_dot_v1alpha_dot_object__pb2.GetObjectDownloadURLRequest.FromString,
                    response_serializer=artifact_dot_artifact_dot_v1alpha_dot_object__pb2.GetObjectDownloadURLResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'artifact.artifact.v1alpha.ArtifactPublicService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ArtifactPublicService(object):
    """ArtifactPublicService exposes the public endpoints that allow clients to
    manage artifacts.
    """

    @staticmethod
    def Liveness(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/artifact.artifact.v1alpha.ArtifactPublicService/Liveness',
            artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.LivenessRequest.SerializeToString,
            artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.LivenessResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Readiness(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/artifact.artifact.v1alpha.ArtifactPublicService/Readiness',
            artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.ReadinessRequest.SerializeToString,
            artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.ReadinessResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateCatalog(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/artifact.artifact.v1alpha.ArtifactPublicService/CreateCatalog',
            artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.CreateCatalogRequest.SerializeToString,
            artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.CreateCatalogResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListCatalogs(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/artifact.artifact.v1alpha.ArtifactPublicService/ListCatalogs',
            artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.ListCatalogsRequest.SerializeToString,
            artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.ListCatalogsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateCatalog(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/artifact.artifact.v1alpha.ArtifactPublicService/UpdateCatalog',
            artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.UpdateCatalogRequest.SerializeToString,
            artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.UpdateCatalogResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteCatalog(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/artifact.artifact.v1alpha.ArtifactPublicService/DeleteCatalog',
            artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.DeleteCatalogRequest.SerializeToString,
            artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.DeleteCatalogResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UploadCatalogFile(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/artifact.artifact.v1alpha.ArtifactPublicService/UploadCatalogFile',
            artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.UploadCatalogFileRequest.SerializeToString,
            artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.UploadCatalogFileResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteCatalogFile(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/artifact.artifact.v1alpha.ArtifactPublicService/DeleteCatalogFile',
            artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.DeleteCatalogFileRequest.SerializeToString,
            artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.DeleteCatalogFileResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ProcessCatalogFiles(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/artifact.artifact.v1alpha.ArtifactPublicService/ProcessCatalogFiles',
            artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.ProcessCatalogFilesRequest.SerializeToString,
            artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.ProcessCatalogFilesResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListCatalogFiles(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/artifact.artifact.v1alpha.ArtifactPublicService/ListCatalogFiles',
            artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.ListCatalogFilesRequest.SerializeToString,
            artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.ListCatalogFilesResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListChunks(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/artifact.artifact.v1alpha.ArtifactPublicService/ListChunks',
            artifact_dot_artifact_dot_v1alpha_dot_chunk__pb2.ListChunksRequest.SerializeToString,
            artifact_dot_artifact_dot_v1alpha_dot_chunk__pb2.ListChunksResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetSourceFile(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/artifact.artifact.v1alpha.ArtifactPublicService/GetSourceFile',
            artifact_dot_artifact_dot_v1alpha_dot_chunk__pb2.GetSourceFileRequest.SerializeToString,
            artifact_dot_artifact_dot_v1alpha_dot_chunk__pb2.GetSourceFileResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateChunk(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/artifact.artifact.v1alpha.ArtifactPublicService/UpdateChunk',
            artifact_dot_artifact_dot_v1alpha_dot_chunk__pb2.UpdateChunkRequest.SerializeToString,
            artifact_dot_artifact_dot_v1alpha_dot_chunk__pb2.UpdateChunkResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SimilarityChunksSearch(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/artifact.artifact.v1alpha.ArtifactPublicService/SimilarityChunksSearch',
            artifact_dot_artifact_dot_v1alpha_dot_chunk__pb2.SimilarityChunksSearchRequest.SerializeToString,
            artifact_dot_artifact_dot_v1alpha_dot_chunk__pb2.SimilarityChunksSearchResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def QuestionAnswering(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/artifact.artifact.v1alpha.ArtifactPublicService/QuestionAnswering',
            artifact_dot_artifact_dot_v1alpha_dot_qa__pb2.QuestionAnsweringRequest.SerializeToString,
            artifact_dot_artifact_dot_v1alpha_dot_qa__pb2.QuestionAnsweringResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetFileCatalog(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/artifact.artifact.v1alpha.ArtifactPublicService/GetFileCatalog',
            artifact_dot_artifact_dot_v1alpha_dot_file__catalog__pb2.GetFileCatalogRequest.SerializeToString,
            artifact_dot_artifact_dot_v1alpha_dot_file__catalog__pb2.GetFileCatalogResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListCatalogRuns(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/artifact.artifact.v1alpha.ArtifactPublicService/ListCatalogRuns',
            artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.ListCatalogRunsRequest.SerializeToString,
            artifact_dot_artifact_dot_v1alpha_dot_artifact__pb2.ListCatalogRunsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetObjectUploadURL(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/artifact.artifact.v1alpha.ArtifactPublicService/GetObjectUploadURL',
            artifact_dot_artifact_dot_v1alpha_dot_object__pb2.GetObjectUploadURLRequest.SerializeToString,
            artifact_dot_artifact_dot_v1alpha_dot_object__pb2.GetObjectUploadURLResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetObjectDownloadURL(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/artifact.artifact.v1alpha.ArtifactPublicService/GetObjectDownloadURL',
            artifact_dot_artifact_dot_v1alpha_dot_object__pb2.GetObjectDownloadURLRequest.SerializeToString,
            artifact_dot_artifact_dot_v1alpha_dot_object__pb2.GetObjectDownloadURLResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

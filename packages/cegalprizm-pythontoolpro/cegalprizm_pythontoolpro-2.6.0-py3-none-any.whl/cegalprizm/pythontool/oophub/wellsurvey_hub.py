# Copyright 2025 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



from cegalprizm.pythontool.grpc.petrelinterface_pb2 import PetrelObjectRef, ProtoBool

from cegalprizm.pythontool.grpc.petrelinterface_pb2 import XyzWellSurvey_RecordCount_Response, XyzWellSurvey_GetXs_Response, XyzWellSurvey_GetYs_Response
from cegalprizm.pythontool.grpc.petrelinterface_pb2 import XyzWellSurvey_GetZs_Response, XyzWellSurvey_GetMds_Response, XyzWellSurvey_GetIncls_Response
from cegalprizm.pythontool.grpc.petrelinterface_pb2 import XyzWellSurvey_GetAzims_Response, XyzWellSurvey_SetSurveyAsDefinitive_Response
from cegalprizm.pythontool.grpc.petrelinterface_pb2 import XyzWellSurvey_TieInMd_Response, XyzWellSurvey_SetTieInMd_Response
from cegalprizm.pythontool.grpc.petrelinterface_pb2 import XyzWellSurvey_IsSidetrack_Response, WellSurvey_IsDefinitive_Response
from cegalprizm.pythontool.grpc.petrelinterface_pb2 import XyzWellSurvey_GetParentPythonBoreholeObject_Response

from cegalprizm.pythontool.grpc.petrelinterface_pb2 import XytvdWellSurvey_RecordCount_Response, XytvdWellSurvey_GetXs_Response, XytvdWellSurvey_GetYs_Response
from cegalprizm.pythontool.grpc.petrelinterface_pb2 import XytvdWellSurvey_GetTvds_Response, XytvdWellSurvey_GetZs_Response, XytvdWellSurvey_GetMds_Response
from cegalprizm.pythontool.grpc.petrelinterface_pb2 import XytvdWellSurvey_GetIncls_Response, XytvdWellSurvey_GetAzims_Response
from cegalprizm.pythontool.grpc.petrelinterface_pb2 import XytvdWellSurvey_SetSurveyAsDefinitive_Response, XytvdWellSurvey_TieInMd_Response
from cegalprizm.pythontool.grpc.petrelinterface_pb2 import XytvdWellSurvey_SetTieInMd_Response, XytvdWellSurvey_IsSidetrack_Response
from cegalprizm.pythontool.grpc.petrelinterface_pb2 import XytvdWellSurvey_GetParentPythonBoreholeObject_Response

from cegalprizm.pythontool.grpc.petrelinterface_pb2 import DxdytvdWellSurvey_RecordCount_Response, DxdytvdWellSurvey_AzimuthReferenceIsGridNorth_Response
from cegalprizm.pythontool.grpc.petrelinterface_pb2 import DxdytvdWellSurvey_GetDxs_Response, DxdytvdWellSurvey_GetDys_Response
from cegalprizm.pythontool.grpc.petrelinterface_pb2 import DxdytvdWellSurvey_GetXs_Response, DxdytvdWellSurvey_GetYs_Response
from cegalprizm.pythontool.grpc.petrelinterface_pb2 import DxdytvdWellSurvey_GetTvds_Response, DxdytvdWellSurvey_GetZs_Response
from cegalprizm.pythontool.grpc.petrelinterface_pb2 import DxdytvdWellSurvey_GetMds_Response, DxdytvdWellSurvey_GetIncls_Response
from cegalprizm.pythontool.grpc.petrelinterface_pb2 import DxdytvdWellSurvey_GetAzims_Response, DxdytvdWellSurvey_SetSurveyAsDefinitive_Response
from cegalprizm.pythontool.grpc.petrelinterface_pb2 import DxdytvdWellSurvey_TieInMd_Response, DxdytvdWellSurvey_SetTieInMd_Response
from cegalprizm.pythontool.grpc.petrelinterface_pb2 import DxdytvdWellSurvey_IsSidetrack_Response, DxdytvdWellSurvey_GetParentPythonBoreholeObject_Response

from cegalprizm.pythontool.grpc.petrelinterface_pb2 import MdinclazimWellSurvey_RecordCount_Response, MdinclazimWellSurvey_AzimuthReferenceIsGridNorth_Response
from cegalprizm.pythontool.grpc.petrelinterface_pb2 import MdinclazimWellSurvey_GetMds_Response, MdinclazimWellSurvey_GetIncls_Response
from cegalprizm.pythontool.grpc.petrelinterface_pb2 import MdinclazimWellSurvey_GetXs_Response, MdinclazimWellSurvey_GetYs_Response
from cegalprizm.pythontool.grpc.petrelinterface_pb2 import MdinclazimWellSurvey_GetZs_Response, MdinclazimWellSurvey_GetAzims_Response
from cegalprizm.pythontool.grpc.petrelinterface_pb2 import MdinclazimWellSurvey_SetSurveyAsDefinitive_Response, MdinclazimWellSurvey_IsSidetrack_Response
from cegalprizm.pythontool.grpc.petrelinterface_pb2 import MdinclazimWellSurvey_TieInMd_Response, MdinclazimWellSurvey_SetTieInMd_Response
from cegalprizm.pythontool.grpc.petrelinterface_pb2 import MdinclazimWellSurvey_GetParentPythonBoreholeObject_Response, MdinclazimWellSurvey_IsAzimuthReferenceGridNorth_Response

from cegalprizm.pythontool.grpc.petrelinterface_pb2 import ExplicitWellSurvey_RecordCount_Response, ExplicitWellSurvey_GetXs_Response, ExplicitWellSurvey_GetYs_Response
from cegalprizm.pythontool.grpc.petrelinterface_pb2 import ExplicitWellSurvey_GetZs_Response, ExplicitWellSurvey_GetMds_Response, ExplicitWellSurvey_GetIncls_Response
from cegalprizm.pythontool.grpc.petrelinterface_pb2 import ExplicitWellSurvey_GetAzims_Response, ExplicitWellSurvey_SetSurveyAsDefinitive_Response
from cegalprizm.pythontool.grpc.petrelinterface_pb2 import ExplicitWellSurvey_TieInMd_Response, ExplicitWellSurvey_SetTieInMd_Response
from cegalprizm.pythontool.grpc.petrelinterface_pb2 import ExplicitWellSurvey_IsSidetrack_Response, ExplicitWellSurvey_GetParentPythonBoreholeObject_Response

from .base_hub import BaseHub
import typing

class XyzWellSurveyHub(BaseHub):
    def GetXyzWellSurveyGrpc(self, msg) -> PetrelObjectRef:
        return self._wrapper("cegal.pythontool.GetXyzWellSurveyGrpc", PetrelObjectRef, msg) # type: ignore
    
    def GetXyzWellSurvey(self, msg) -> PetrelObjectRef:
        return self._unary_wrapper("cegal.pythontool.GetXyzWellSurvey", PetrelObjectRef, msg) # type: ignore
    
    def XyzWellSurvey_RecordCount(self, msg) -> XyzWellSurvey_RecordCount_Response:
        return self._unary_wrapper("cegal.pythontool.XyzWellSurvey_RecordCount", XyzWellSurvey_RecordCount_Response, msg) # type: ignore
    
    def XyzWellSurvey_GetXs(self, msg) -> typing.Iterable[XyzWellSurvey_GetXs_Response]:
        return self._server_streaming_wrapper("cegal.pythontool.XyzWellSurvey_GetXs", XyzWellSurvey_GetXs_Response, msg) # type: ignore
    
    def XyzWellSurvey_GetYs(self, msg) -> typing.Iterable[XyzWellSurvey_GetYs_Response]:
        return self._server_streaming_wrapper("cegal.pythontool.XyzWellSurvey_GetYs", XyzWellSurvey_GetYs_Response, msg) # type: ignore
    
    def XyzWellSurvey_GetZs(self, msg) -> typing.Iterable[XyzWellSurvey_GetZs_Response]:
        return self._server_streaming_wrapper("cegal.pythontool.XyzWellSurvey_GetZs", XyzWellSurvey_GetZs_Response, msg) # type: ignore
    
    def XyzWellSurvey_GetMds(self, msg) -> typing.Iterable[XyzWellSurvey_GetMds_Response]:
        return self._server_streaming_wrapper("cegal.pythontool.XyzWellSurvey_GetMds", XyzWellSurvey_GetMds_Response, msg) # type: ignore
    
    def XyzWellSurvey_GetIncls(self, msg) -> typing.Iterable[XyzWellSurvey_GetIncls_Response]:
        return self._server_streaming_wrapper("cegal.pythontool.XyzWellSurvey_GetIncls", XyzWellSurvey_GetIncls_Response, msg) # type: ignore
    
    def XyzWellSurvey_GetAzims(self, msg) -> typing.Iterable[XyzWellSurvey_GetAzims_Response]:
        return self._server_streaming_wrapper("cegal.pythontool.XyzWellSurvey_GetAzims", XyzWellSurvey_GetAzims_Response, msg) # type: ignore
    
    def XyzWellSurvey_SetRecords(self, iterable_requests) -> ProtoBool:
        return self._client_streaming_wrapper("cegal.pythontool.XyzWellSurvey_SetRecords", ProtoBool, iterable_requests) # type: ignore
    
    def XyzWellSurvey_SetSurveyAsDefinitive(self, msg) -> XyzWellSurvey_SetSurveyAsDefinitive_Response:
        return self._unary_wrapper("cegal.pythontool.XyzWellSurvey_SetSurveyAsDefinitive", XyzWellSurvey_SetSurveyAsDefinitive_Response, msg) # type: ignore
    
    def XyzWellSurvey_TieInMd(self, msg) -> XyzWellSurvey_TieInMd_Response:
        return self._unary_wrapper("cegal.pythontool.XyzWellSurvey_TieInMd", XyzWellSurvey_TieInMd_Response, msg) # type: ignore
    
    def XyzWellSurvey_SetTieInMd(self, msg) -> XyzWellSurvey_SetTieInMd_Response:
        return self._unary_wrapper("cegal.pythontool.XyzWellSurvey_SetTieInMd", XyzWellSurvey_SetTieInMd_Response, msg) # type: ignore
    
    def XyzWellSurvey_IsSidetrack(self, msg) -> XyzWellSurvey_IsSidetrack_Response:
        return self._unary_wrapper("cegal.pythontool.XyzWellSurvey_IsSidetrack", XyzWellSurvey_IsSidetrack_Response, msg) # type: ignore

    def XyzWellSurvey_IsDefinitive(self, msg) -> WellSurvey_IsDefinitive_Response:
        return self._unary_wrapper("cegal.pythontool.XyzWellSurvey_IsDefinitive", WellSurvey_IsDefinitive_Response, msg) # type: ignore

    def XyzWellSurvey_GetParentPythonBoreholeObject(self, msg) -> XyzWellSurvey_GetParentPythonBoreholeObject_Response:
        return self._unary_wrapper("cegal.pythontool.XyzWellSurvey_GetParentPythonBoreholeObject", XyzWellSurvey_GetParentPythonBoreholeObject_Response, msg) # type: ignore

    def XyzWellSurvey_IsAlgorithmMinimumCurvature(self, msg) -> ProtoBool: 
        return self._unary_wrapper("cegal.pythontool.XyzWellSurvey_IsAlgorithmMinimumCurvature", ProtoBool, msg) # type: ignore

    def XyzWellSurvey_SetAlgorithmToMinimumCurvature(self, msg) -> ProtoBool: 
        return self._unary_wrapper("cegal.pythontool.XyzWellSurvey_SetAlgorithmToMinimumCurvature", ProtoBool, msg) # type: ignore
    
    def XyzWellSurvey_IsCalculationValid(self, msg) -> ProtoBool:
        return self._unary_wrapper("cegal.pythontool.XyzWellSurvey_IsCalculationValid", ProtoBool, msg) # type: ignore

class XytvdWellSurveyHub(BaseHub):
    def GetXytvdWellSurveyGrpc(self, msg) -> PetrelObjectRef:
        return self._wrapper("cegal.pythontool.GetXytvdWellSurveyGrpc", PetrelObjectRef, msg) # type: ignore
    
    def GetXytvdWellSurvey(self, msg) -> PetrelObjectRef:
        return self._unary_wrapper("cegal.pythontool.GetXytvdWellSurvey", PetrelObjectRef, msg) # type: ignore
    
    def XytvdWellSurvey_RecordCount(self, msg) -> XytvdWellSurvey_RecordCount_Response:
        return self._unary_wrapper("cegal.pythontool.XytvdWellSurvey_RecordCount", XytvdWellSurvey_RecordCount_Response, msg) # type: ignore
    
    def XytvdWellSurvey_GetXs(self, msg) -> typing.Iterable[XytvdWellSurvey_GetXs_Response]:
        return self._server_streaming_wrapper("cegal.pythontool.XytvdWellSurvey_GetXs", XytvdWellSurvey_GetXs_Response, msg) # type: ignore
    
    def XytvdWellSurvey_GetYs(self, msg) -> typing.Iterable[XytvdWellSurvey_GetYs_Response]:
        return self._server_streaming_wrapper("cegal.pythontool.XytvdWellSurvey_GetYs", XytvdWellSurvey_GetYs_Response, msg) # type: ignore
    
    def XytvdWellSurvey_GetTvds(self, msg) -> typing.Iterable[XytvdWellSurvey_GetTvds_Response]:
        return self._server_streaming_wrapper("cegal.pythontool.XytvdWellSurvey_GetTvds", XytvdWellSurvey_GetTvds_Response, msg) # type: ignore
    
    def XytvdWellSurvey_GetZs(self, msg) -> typing.Iterable[XytvdWellSurvey_GetZs_Response]:
        return self._server_streaming_wrapper("cegal.pythontool.XytvdWellSurvey_GetZs", XytvdWellSurvey_GetZs_Response, msg) # type: ignore
    
    def XytvdWellSurvey_GetMds(self, msg) -> typing.Iterable[XytvdWellSurvey_GetMds_Response]:
        return self._server_streaming_wrapper("cegal.pythontool.XytvdWellSurvey_GetMds", XytvdWellSurvey_GetMds_Response, msg) # type: ignore
    
    def XytvdWellSurvey_GetIncls(self, msg) -> typing.Iterable[XytvdWellSurvey_GetIncls_Response]:
        return self._server_streaming_wrapper("cegal.pythontool.XytvdWellSurvey_GetIncls", XytvdWellSurvey_GetIncls_Response, msg) # type: ignore
    
    def XytvdWellSurvey_GetAzims(self, msg) -> typing.Iterable[XytvdWellSurvey_GetAzims_Response]:
        return self._server_streaming_wrapper("cegal.pythontool.XytvdWellSurvey_GetAzims", XytvdWellSurvey_GetAzims_Response, msg) # type: ignore
    
    def XytvdWellSurvey_SetRecords(self, iterable_requests) -> ProtoBool:
        return self._client_streaming_wrapper("cegal.pythontool.XytvdWellSurvey_SetRecords", ProtoBool, iterable_requests) # type: ignore
    
    def XytvdWellSurvey_SetSurveyAsDefinitive(self, msg) -> XytvdWellSurvey_SetSurveyAsDefinitive_Response:
        return self._unary_wrapper("cegal.pythontool.XytvdWellSurvey_SetSurveyAsDefinitive", XytvdWellSurvey_SetSurveyAsDefinitive_Response, msg) # type: ignore
    
    def XytvdWellSurvey_TieInMd(self, msg) -> XytvdWellSurvey_TieInMd_Response:
        return self._unary_wrapper("cegal.pythontool.XytvdWellSurvey_TieInMd", XytvdWellSurvey_TieInMd_Response, msg) # type: ignore
    
    def XytvdWellSurvey_SetTieInMd(self, msg) -> XytvdWellSurvey_SetTieInMd_Response:
        return self._unary_wrapper("cegal.pythontool.XytvdWellSurvey_SetTieInMd", XytvdWellSurvey_SetTieInMd_Response, msg) # type: ignore
    
    def XytvdWellSurvey_IsSidetrack(self, msg) -> XytvdWellSurvey_IsSidetrack_Response:
        return self._unary_wrapper("cegal.pythontool.XytvdWellSurvey_IsSidetrack", XytvdWellSurvey_IsSidetrack_Response, msg) # type: ignore

    def XytvdWellSurvey_IsDefinitive(self, msg) -> WellSurvey_IsDefinitive_Response:
        return self._unary_wrapper("cegal.pythontool.XytvdWellSurvey_IsDefinitive", WellSurvey_IsDefinitive_Response, msg) # type: ignore

    def XytvdWellSurvey_GetParentPythonBoreholeObject(self, msg) -> XytvdWellSurvey_GetParentPythonBoreholeObject_Response:
        return self._unary_wrapper("cegal.pythontool.XytvdWellSurvey_GetParentPythonBoreholeObject", XytvdWellSurvey_GetParentPythonBoreholeObject_Response, msg) # type: ignore

    def XytvdWellSurvey_IsAlgorithmMinimumCurvature(self, msg) -> ProtoBool: 
        return self._unary_wrapper("cegal.pythontool.XytvdWellSurvey_IsAlgorithmMinimumCurvature", ProtoBool, msg) # type: ignore

    def XytvdWellSurvey_SetAlgorithmToMinimumCurvature(self, msg) -> ProtoBool: 
        return self._unary_wrapper("cegal.pythontool.XytvdWellSurvey_SetAlgorithmToMinimumCurvature", ProtoBool, msg) # type: ignore

    def XytvdWellSurvey_IsCalculationValid(self, msg) -> ProtoBool:
        return self._unary_wrapper("cegal.pythontool.XytvdWellSurvey_IsCalculationValid", ProtoBool, msg) # type: ignore

class DxdytvdWellSurveyHub(BaseHub):
    def GetDxdytvdWellSurveyGrpc(self, msg) -> PetrelObjectRef:
        return self._wrapper("cegal.pythontool.GetDxdytvdWellSurveyGrpc", PetrelObjectRef, msg) # type: ignore
    
    def GetDxdytvdWellSurvey(self, msg) -> PetrelObjectRef:
        return self._unary_wrapper("cegal.pythontool.GetDxdytvdWellSurvey", PetrelObjectRef, msg) # type: ignore
    
    def DxdytvdWellSurvey_RecordCount(self, msg) -> DxdytvdWellSurvey_RecordCount_Response:
        return self._unary_wrapper("cegal.pythontool.DxdytvdWellSurvey_RecordCount", DxdytvdWellSurvey_RecordCount_Response, msg) # type: ignore
    
    def DxdytvdWellSurvey_AzimuthReferenceIsGridNorth(self, msg) -> DxdytvdWellSurvey_AzimuthReferenceIsGridNorth_Response:
        return self._unary_wrapper("cegal.pythontool.DxdytvdWellSurvey_AzimuthReferenceIsGridNorth", DxdytvdWellSurvey_AzimuthReferenceIsGridNorth_Response, msg) # type: ignore
    
    def DxdytvdWellSurvey_SetAzimuthReference(self, msg) -> ProtoBool:
        return self._unary_wrapper("cegal.pythontool.DxdytvdWellSurvey_SetAzimuthReference", ProtoBool, msg)

    def DxdytvdWellSurvey_GetDxs(self, msg) -> typing.Iterable[DxdytvdWellSurvey_GetDxs_Response]:
        return self._server_streaming_wrapper("cegal.pythontool.DxdytvdWellSurvey_GetDxs", DxdytvdWellSurvey_GetDxs_Response, msg) # type: ignore
    
    def DxdytvdWellSurvey_GetDys(self, msg) -> typing.Iterable[DxdytvdWellSurvey_GetDys_Response]:
        return self._server_streaming_wrapper("cegal.pythontool.DxdytvdWellSurvey_GetDys", DxdytvdWellSurvey_GetDys_Response, msg) # type: ignore
    
    def DxdytvdWellSurvey_GetTvds(self, msg) -> typing.Iterable[DxdytvdWellSurvey_GetTvds_Response]:
        return self._server_streaming_wrapper("cegal.pythontool.DxdytvdWellSurvey_GetTvds", DxdytvdWellSurvey_GetTvds_Response, msg) # type: ignore
    
    def DxdytvdWellSurvey_GetXs(self, msg) -> typing.Iterable[DxdytvdWellSurvey_GetXs_Response]:
        return self._server_streaming_wrapper("cegal.pythontool.DxdytvdWellSurvey_GetXs", DxdytvdWellSurvey_GetXs_Response, msg) # type: ignore
    
    def DxdytvdWellSurvey_GetYs(self, msg) -> typing.Iterable[DxdytvdWellSurvey_GetYs_Response]:
        return self._server_streaming_wrapper("cegal.pythontool.DxdytvdWellSurvey_GetYs", DxdytvdWellSurvey_GetYs_Response, msg) # type: ignore
    
    def DxdytvdWellSurvey_GetZs(self, msg) -> typing.Iterable[DxdytvdWellSurvey_GetZs_Response]:
        return self._server_streaming_wrapper("cegal.pythontool.DxdytvdWellSurvey_GetZs", DxdytvdWellSurvey_GetZs_Response, msg) # type: ignore
    
    def DxdytvdWellSurvey_GetMds(self, msg) -> typing.Iterable[DxdytvdWellSurvey_GetMds_Response]:
        return self._server_streaming_wrapper("cegal.pythontool.DxdytvdWellSurvey_GetMds", DxdytvdWellSurvey_GetMds_Response, msg) # type: ignore
    
    def DxdytvdWellSurvey_GetIncls(self, msg) -> typing.Iterable[DxdytvdWellSurvey_GetIncls_Response]:
        return self._server_streaming_wrapper("cegal.pythontool.DxdytvdWellSurvey_GetIncls", DxdytvdWellSurvey_GetIncls_Response, msg) # type: ignore
    
    def DxdytvdWellSurvey_GetAzims(self, msg) -> typing.Iterable[DxdytvdWellSurvey_GetAzims_Response]:
        return self._server_streaming_wrapper("cegal.pythontool.DxdytvdWellSurvey_GetAzims", DxdytvdWellSurvey_GetAzims_Response, msg) # type: ignore
    
    def DxdytvdWellSurvey_SetRecords(self, iterable_requests) -> ProtoBool:
        return self._client_streaming_wrapper("cegal.pythontool.DxdytvdWellSurvey_SetRecords", ProtoBool, iterable_requests) # type: ignore
    
    def DxdytvdWellSurvey_SetSurveyAsDefinitive(self, msg) -> DxdytvdWellSurvey_SetSurveyAsDefinitive_Response:
        return self._unary_wrapper("cegal.pythontool.DxdytvdWellSurvey_SetSurveyAsDefinitive", DxdytvdWellSurvey_SetSurveyAsDefinitive_Response, msg) # type: ignore
    
    def DxdytvdWellSurvey_TieInMd(self, msg) -> DxdytvdWellSurvey_TieInMd_Response:
        return self._unary_wrapper("cegal.pythontool.DxdytvdWellSurvey_TieInMd", DxdytvdWellSurvey_TieInMd_Response, msg) # type: ignore
    
    def DxdytvdWellSurvey_SetTieInMd(self, msg) -> DxdytvdWellSurvey_SetTieInMd_Response:
        return self._unary_wrapper("cegal.pythontool.DxdytvdWellSurvey_SetTieInMd", DxdytvdWellSurvey_SetTieInMd_Response, msg) # type: ignore
    
    def DxdytvdWellSurvey_IsSidetrack(self, msg) -> DxdytvdWellSurvey_IsSidetrack_Response:
        return self._unary_wrapper("cegal.pythontool.DxdytvdWellSurvey_IsSidetrack", DxdytvdWellSurvey_IsSidetrack_Response, msg) # type: ignore

    def DxdytvdWellSurvey_IsDefinitive(self, msg) -> WellSurvey_IsDefinitive_Response:
        return self._unary_wrapper("cegal.pythontool.DxdytvdWellSurvey_IsDefinitive", WellSurvey_IsDefinitive_Response, msg) # type: ignore

    def DxdytvdWellSurvey_GetParentPythonBoreholeObject(self, msg) -> DxdytvdWellSurvey_GetParentPythonBoreholeObject_Response:
        return self._unary_wrapper("cegal.pythontool.DxdytvdWellSurvey_GetParentPythonBoreholeObject", DxdytvdWellSurvey_GetParentPythonBoreholeObject_Response, msg) # type: ignore

    def DxdytvdWellSurvey_IsAlgorithmMinimumCurvature(self, msg) -> ProtoBool:
        return self._unary_wrapper("cegal.pythontool.DxdytvdWellSurvey_IsAlgorithmMinimumCurvature", ProtoBool, msg) # type: ignore

    def DxdytvdWellSurvey_SetAlgorithmToMinimumCurvature(self, msg) -> ProtoBool:
        return self._unary_wrapper("cegal.pythontool.DxdytvdWellSurvey_SetAlgorithmToMinimumCurvature", ProtoBool, msg) # type: ignore

    def DxdytvdWellSurvey_IsCalculationValid(self, msg) -> ProtoBool:
        return self._unary_wrapper("cegal.pythontool.DxdytvdWellSurvey_IsCalculationValid", ProtoBool, msg) # type: ignore

class MdinclazimWellSurveyHub(BaseHub):
    def GetMdinclazimWellSurveyGrpc(self, msg) -> PetrelObjectRef:
        return self._wrapper("cegal.pythontool.GetMdinclazimWellSurveyGrpc", PetrelObjectRef, msg) # type: ignore
    
    def GetMdinclazimWellSurvey(self, msg) -> PetrelObjectRef:
        return self._unary_wrapper("cegal.pythontool.GetMdinclazimWellSurvey", PetrelObjectRef, msg) # type: ignore
    
    def MdinclazimWellSurvey_RecordCount(self, msg) -> MdinclazimWellSurvey_RecordCount_Response:
        return self._unary_wrapper("cegal.pythontool.MdinclazimWellSurvey_RecordCount", MdinclazimWellSurvey_RecordCount_Response, msg) # type: ignore
    
    def MdinclazimWellSurvey_AzimuthReferenceIsGridNorth(self, msg) -> MdinclazimWellSurvey_AzimuthReferenceIsGridNorth_Response:
        return self._unary_wrapper("cegal.pythontool.MdinclazimWellSurvey_AzimuthReferenceIsGridNorth", MdinclazimWellSurvey_AzimuthReferenceIsGridNorth_Response, msg) # type: ignore
    
    def MdinclazimWellSurvey_GetMds(self, msg) -> typing.Iterable[MdinclazimWellSurvey_GetMds_Response]:
        return self._server_streaming_wrapper("cegal.pythontool.MdinclazimWellSurvey_GetMds", MdinclazimWellSurvey_GetMds_Response, msg) # type: ignore
    
    def MdinclazimWellSurvey_GetIncls(self, msg) -> typing.Iterable[MdinclazimWellSurvey_GetIncls_Response]:
        return self._server_streaming_wrapper("cegal.pythontool.MdinclazimWellSurvey_GetIncls", MdinclazimWellSurvey_GetIncls_Response, msg) # type: ignore
    
    def MdinclazimWellSurvey_GetAzims(self, msg) -> typing.Iterable[MdinclazimWellSurvey_GetAzims_Response]:
        return self._server_streaming_wrapper("cegal.pythontool.MdinclazimWellSurvey_GetAzims", MdinclazimWellSurvey_GetAzims_Response, msg) # type: ignore
    
    def MdinclazimWellSurvey_GetXs(self, msg) -> typing.Iterable[MdinclazimWellSurvey_GetXs_Response]:
        return self._server_streaming_wrapper("cegal.pythontool.MdinclazimWellSurvey_GetXs", MdinclazimWellSurvey_GetXs_Response, msg) # type: ignore
    
    def MdinclazimWellSurvey_GetYs(self, msg) -> typing.Iterable[MdinclazimWellSurvey_GetYs_Response]:
        return self._server_streaming_wrapper("cegal.pythontool.MdinclazimWellSurvey_GetYs", MdinclazimWellSurvey_GetYs_Response, msg) # type: ignore
    
    def MdinclazimWellSurvey_GetZs(self, msg) -> typing.Iterable[MdinclazimWellSurvey_GetZs_Response]:
        return self._server_streaming_wrapper("cegal.pythontool.MdinclazimWellSurvey_GetZs", MdinclazimWellSurvey_GetZs_Response, msg) # type: ignore
    
    def MdinclazimWellSurvey_IsAzimuthReferenceGridNorth(self, msg) -> MdinclazimWellSurvey_IsAzimuthReferenceGridNorth_Response:
        return self._unary_wrapper("cegal.pythontool.MdinclazimWellSurvey_IsAzimuthReferenceGridNorth", MdinclazimWellSurvey_IsAzimuthReferenceGridNorth_Response, msg) # type: ignore
    
    def MdinclazimWellSurvey_SetAzimuthReference(self, msg) -> ProtoBool:
        return self._unary_wrapper("cegal.pythontool.MdinclazimWellSurvey_SetAzimuthReference", ProtoBool, msg)
    
    def MdinclazimWellSurvey_SetRecords(self, iterable_requests) -> ProtoBool:
        return self._client_streaming_wrapper("cegal.pythontool.MdinclazimWellSurvey_SetRecords", ProtoBool, iterable_requests) # type: ignore
    
    def MdinclazimWellSurvey_SetSurveyAsDefinitive(self, msg) -> MdinclazimWellSurvey_SetSurveyAsDefinitive_Response:
        return self._unary_wrapper("cegal.pythontool.MdinclazimWellSurvey_SetSurveyAsDefinitive", MdinclazimWellSurvey_SetSurveyAsDefinitive_Response, msg) # type: ignore
    
    def MdinclazimWellSurvey_TieInMd(self, msg) -> MdinclazimWellSurvey_TieInMd_Response:
        return self._unary_wrapper("cegal.pythontool.MdinclazimWellSurvey_TieInMd", MdinclazimWellSurvey_TieInMd_Response, msg) # type: ignore
    
    def MdinclazimWellSurvey_SetTieInMd(self, msg) -> MdinclazimWellSurvey_SetTieInMd_Response:
        return self._unary_wrapper("cegal.pythontool.MdinclazimWellSurvey_SetTieInMd", MdinclazimWellSurvey_SetTieInMd_Response, msg) # type: ignore
    
    def MdinclazimWellSurvey_IsSidetrack(self, msg) -> MdinclazimWellSurvey_IsSidetrack_Response:
        return self._unary_wrapper("cegal.pythontool.MdinclazimWellSurvey_IsSidetrack", MdinclazimWellSurvey_IsSidetrack_Response, msg) # type: ignore

    def MdinclazimWellSurvey_IsDefinitive(self, msg) -> WellSurvey_IsDefinitive_Response:
        return self._unary_wrapper("cegal.pythontool.MdinclazimWellSurvey_IsDefinitive", WellSurvey_IsDefinitive_Response, msg) # type: ignore

    def MdinclazimWellSurvey_GetParentPythonBoreholeObject(self, msg) -> MdinclazimWellSurvey_GetParentPythonBoreholeObject_Response:
        return self._unary_wrapper("cegal.pythontool.MdinclazimWellSurvey_GetParentPythonBoreholeObject", MdinclazimWellSurvey_GetParentPythonBoreholeObject_Response, msg) # type: ignore

    def MdinclazimWellSurvey_IsCalculationValid(self, msg) -> ProtoBool:
        return self._unary_wrapper("cegal.pythontool.MdinclazimWellSurvey_IsCalculationValid", ProtoBool, msg) # type: ignore

class ExplicitWellSurveyHub(BaseHub):
    def GetExplicitWellSurveyGrpc(self, msg) -> PetrelObjectRef:
        return self._wrapper("cegal.pythontool.GetExplicitWellSurveyGrpc", PetrelObjectRef, msg) # type: ignore
    
    def GetExplicitWellSurvey(self, msg) -> PetrelObjectRef:
        return self._unary_wrapper("cegal.pythontool.GetExplicitWellSurvey", PetrelObjectRef, msg) # type: ignore
    
    def ExplicitWellSurvey_RecordCount(self, msg) -> ExplicitWellSurvey_RecordCount_Response:
        return self._unary_wrapper("cegal.pythontool.ExplicitWellSurvey_RecordCount", ExplicitWellSurvey_RecordCount_Response, msg) # type: ignore
    
    def ExplicitWellSurvey_GetXs(self, msg) -> typing.Iterable[ExplicitWellSurvey_GetXs_Response]:
        return self._server_streaming_wrapper("cegal.pythontool.ExplicitWellSurvey_GetXs", ExplicitWellSurvey_GetXs_Response, msg) # type: ignore
    
    def ExplicitWellSurvey_GetYs(self, msg) -> typing.Iterable[ExplicitWellSurvey_GetYs_Response]:
        return self._server_streaming_wrapper("cegal.pythontool.ExplicitWellSurvey_GetYs", ExplicitWellSurvey_GetYs_Response, msg) # type: ignore
    
    def ExplicitWellSurvey_GetZs(self, msg) -> typing.Iterable[ExplicitWellSurvey_GetZs_Response]:
        return self._server_streaming_wrapper("cegal.pythontool.ExplicitWellSurvey_GetZs", ExplicitWellSurvey_GetZs_Response, msg) # type: ignore
    
    def ExplicitWellSurvey_GetMds(self, msg) -> typing.Iterable[ExplicitWellSurvey_GetMds_Response]:
        return self._server_streaming_wrapper("cegal.pythontool.ExplicitWellSurvey_GetMds", ExplicitWellSurvey_GetMds_Response, msg) # type: ignore
    
    def ExplicitWellSurvey_GetIncls(self, msg) -> typing.Iterable[ExplicitWellSurvey_GetIncls_Response]:
        return self._server_streaming_wrapper("cegal.pythontool.ExplicitWellSurvey_GetIncls", ExplicitWellSurvey_GetIncls_Response, msg) # type: ignore
    
    def ExplicitWellSurvey_GetAzims(self, msg) -> typing.Iterable[ExplicitWellSurvey_GetAzims_Response]:
        return self._server_streaming_wrapper("cegal.pythontool.ExplicitWellSurvey_GetAzims", ExplicitWellSurvey_GetAzims_Response, msg) # type: ignore
    
    def ExplicitWellSurvey_SetSurveyAsDefinitive(self, msg) -> ExplicitWellSurvey_SetSurveyAsDefinitive_Response:
        return self._unary_wrapper("cegal.pythontool.ExplicitWellSurvey_SetSurveyAsDefinitive", ExplicitWellSurvey_SetSurveyAsDefinitive_Response, msg) # type: ignore
    
    def ExplicitWellSurvey_TieInMd(self, msg) -> ExplicitWellSurvey_TieInMd_Response:
        return self._unary_wrapper("cegal.pythontool.ExplicitWellSurvey_TieInMd", ExplicitWellSurvey_TieInMd_Response, msg) # type: ignore
    
    def ExplicitWellSurvey_SetTieInMd(self, msg) -> ExplicitWellSurvey_SetTieInMd_Response:
        return self._unary_wrapper("cegal.pythontool.ExplicitWellSurvey_SetTieInMd", ExplicitWellSurvey_SetTieInMd_Response, msg) # type: ignore
    
    def ExplicitWellSurvey_IsSidetrack(self, msg) -> ExplicitWellSurvey_IsSidetrack_Response:
        return self._unary_wrapper("cegal.pythontool.ExplicitWellSurvey_IsSidetrack", ExplicitWellSurvey_IsSidetrack_Response, msg) # type: ignore

    def ExplicitWellSurvey_IsDefinitive(self, msg) -> WellSurvey_IsDefinitive_Response:
        return self._unary_wrapper("cegal.pythontool.ExplicitWellSurvey_IsDefinitive", WellSurvey_IsDefinitive_Response, msg) # type: ignore

    def ExplicitWellSurvey_GetParentPythonBoreholeObject(self, msg) -> ExplicitWellSurvey_GetParentPythonBoreholeObject_Response:
        return self._unary_wrapper("cegal.pythontool.ExplicitWellSurvey_GetParentPythonBoreholeObject", ExplicitWellSurvey_GetParentPythonBoreholeObject_Response, msg)  # type: ignore
    
    def ExplicitWellSurvey_IsCalculationValid(self, msg) -> ProtoBool:
        return self._unary_wrapper("cegal.pythontool.ExplicitWellSurvey_IsCalculationValid", ProtoBool, msg) # type: ignore
# Copyright 2025 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



from cegalprizm.pythontool.grpc.petrelinterface_pb2 import PetrelObjectRef, ProtoBool, Primitives, PetrelObjectGuid, PetrelObjectGuids
from cegalprizm.pythontool.grpc.petrelinterface_pb2 import Borehole_GetCrs_Response, Borehole_GetWellDatum_Response
from cegalprizm.pythontool.grpc.petrelinterface_pb2 import Borehole_GetElevationTimePosition_Response, Borehole_GetTvdPosition_Response
from cegalprizm.pythontool.grpc.petrelinterface_pb2 import LogValues, Borehole_GetObservedDataSets_Response, PetrelObject_GetDate_Response
from cegalprizm.pythontool.grpc.petrelinterface_pb2 import Borehole_GetNumberOfObservedDataSets_Response, Borehole_GetWellSurveysRefs_Response
from cegalprizm.pythontool.grpc.petrelinterface_pb2 import Borehole_GetNumberOfWellSurveys_Response, Borehole_GetUWI_Response, Borehole_GetWellSymbolDescription_Response
from .base_hub import BaseHub
import typing

class BoreholeHub(BaseHub):
    def GetBoreholeGrpc(self, msg) -> PetrelObjectRef:
        return self._wrapper("cegal.pythontool.GetBoreholeGrpc", PetrelObjectRef, msg) # type: ignore

    def Borehole_GetCrs(self, msg) -> Borehole_GetCrs_Response:
        return self._unary_wrapper("cegal.pythontool.Borehole_GetCrs", Borehole_GetCrs_Response, msg) # type: ignore
    
    def GetBorehole(self, msg) -> PetrelObjectRef:
        return self._unary_wrapper("cegal.pythontool.GetBorehole", PetrelObjectRef, msg) # type: ignore
    
    def CreateBorehole(self, msg) -> PetrelObjectGuid:
        return self._unary_wrapper("cegal.pythontool.CreateBorehole", PetrelObjectGuid, msg) # type: ignore
    
    def Borehole_GetWellDatum(self, msg) -> Borehole_GetWellDatum_Response:
        return self._unary_wrapper("cegal.pythontool.Borehole_GetWellDatum", Borehole_GetWellDatum_Response, msg)
    
    def Borehole_SetWellDatum(self, msg) -> ProtoBool:
        return self._unary_wrapper("cegal.pythontool.Borehole_SetWellDatum", ProtoBool, msg)
    
    def Borehole_GetElevationTimePosition(self, msg) -> Borehole_GetElevationTimePosition_Response:
        return self._unary_wrapper("cegal.pythontool.Borehole_GetElevationTimePosition", Borehole_GetElevationTimePosition_Response, msg) # type: ignore
    
    def Borehole_GetTvdPosition(self, msg) -> Borehole_GetTvdPosition_Response:
        return self._unary_wrapper("cegal.pythontool.Borehole_GetTvdPosition", Borehole_GetTvdPosition_Response, msg) # type: ignore
    
    def Borehole_GetAllLogs(self, msg) -> PetrelObjectGuids:
        return self._unary_wrapper("cegal.pythontool.Borehole_GetAllLogs", PetrelObjectGuids, msg) # type: ignore
    
    def Borehole_GetLogsValues(self, msg) -> typing.Iterable[LogValues]:
        return self._server_streaming_wrapper("cegal.pythontool.Borehole_GetLogsValues", LogValues, msg) # type: ignore
 
    def Borehole_GetObservedDataSets(self, msg) -> typing.Iterable[Borehole_GetObservedDataSets_Response]:
        return self._server_streaming_wrapper("cegal.pythontool.Borehole_GetObservedDataSets", Borehole_GetObservedDataSets_Response, msg) # type: ignore
 
    def Borehole_GetNumberOfObservedDataSets(self, msg) -> Borehole_GetNumberOfObservedDataSets_Response:
        return self._unary_wrapper("cegal.pythontool.Borehole_GetNumberOfObservedDataSets", Borehole_GetNumberOfObservedDataSets_Response, msg) # type: ignore

    def Borehole_GetWellSurveys(self, msg) -> typing.Iterable[Borehole_GetWellSurveysRefs_Response]:
        return self._server_streaming_wrapper("cegal.pythontool.Borehole_GetWellSurveys", Borehole_GetWellSurveysRefs_Response, msg) # type: ignore

    def Borehole_GetNumberOfWellSurveys(self, msg) -> Borehole_GetNumberOfWellSurveys_Response:
        return self._unary_wrapper("cegal.pythontool.Borehole_GetNumberOfWellSurveys", Borehole_GetNumberOfWellSurveys_Response, msg) # type: ignore

    def Borehole_CompletionsSetExists(self, msg) -> ProtoBool:
        return self._unary_wrapper("cegal.pythontool.Borehole_CompletionsSetExists", ProtoBool, msg)
    
    def Borehole_GetWellHeadCoordinates(self, msg) -> Primitives.Double2:
        return self._unary_wrapper("cegal.pythontool.Borehole_GetWellHeadCoordinates", Primitives.Double2, msg)
 
    def Borehole_SetWellHeadCoordinates(self, msg) -> ProtoBool:
        return self._unary_wrapper("cegal.pythontool.Borehole_SetWellHeadCoordinates", ProtoBool, msg)

    def Borehole_CreateTrajectory(self, msg) -> PetrelObjectGuid:
        return self._unary_wrapper("cegal.pythontool.Borehole_CreateTrajectory", PetrelObjectGuid, msg)
    
    def Borehole_CreateSidetrack(self, msg) -> PetrelObjectGuid:
        return self._unary_wrapper("cegal.pythontool.Borehole_CreateSidetrack", PetrelObjectGuid, msg)
    
    def Borehole_IsSidetrack(self, msg) -> ProtoBool:
        return self._unary_wrapper("cegal.pythontool.Borehole_IsSidetrack", ProtoBool, msg)
    
    def Borehole_GetUwi(self, msg) -> Borehole_GetUWI_Response: #type: ignore
        return self._unary_wrapper("cegal.pythontool.Borehole_GetUWI", Borehole_GetUWI_Response, msg)
    
    def Borehole_SetUwi(self, msg) -> ProtoBool: #type: ignore
        return self._unary_wrapper("cegal.pythontool.Borehole_SetUWI", ProtoBool, msg)

    def Borehole_GetWellSymbolDescription(self, msg) -> Borehole_GetWellSymbolDescription_Response:
        return self._unary_wrapper("cegal.pythontool.Borehole_GetWellSymbolDescription", Borehole_GetWellSymbolDescription_Response, msg)

    def Borehole_SetWellSymbolDescription(self, msg) -> ProtoBool:
        return self._unary_wrapper("cegal.pythontool.Borehole_SetWellSymbolDescription", ProtoBool, msg)

    def Borehole_GetSpudDate(self, msg) -> PetrelObject_GetDate_Response:
        return self._unary_wrapper("cegal.pythontool.Borehole_GetSpudDate", PetrelObject_GetDate_Response, msg)

    def Borehole_SetSpudDate(self, msg) -> ProtoBool:
        return self._unary_wrapper("cegal.pythontool.Borehole_SetSpudDate", ProtoBool, msg)
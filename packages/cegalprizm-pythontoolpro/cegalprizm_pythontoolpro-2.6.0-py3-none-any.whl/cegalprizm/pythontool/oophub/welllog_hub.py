# Copyright 2025 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



from cegalprizm.pythontool.grpc.petrelinterface_pb2 import PetrelObjectRef
from cegalprizm.pythontool.grpc.petrelinterface_pb2 import WellLog_DisplayUnitSymbol_Response, WellLog_GetSamples_Response
from cegalprizm.pythontool.grpc.petrelinterface_pb2 import WellLog_GetParentPythonBoreholObject_Response, WellLog_SetSamples_Response
from cegalprizm.pythontool.grpc.petrelinterface_pb2 import WellLog_GetGlobalWellLog_Response, DiscreteWellLog_GetAllDictionaryCodes_Response
from cegalprizm.pythontool.grpc.petrelinterface_pb2 import WellLog_GetTuple_Response, WellLog_GetValues_Response
from .base_hub import BaseHub

class WellLogHub(BaseHub):
    def GetWellLogGrpc(self, msg) -> PetrelObjectRef:
        return self._wrapper("cegal.pythontool.GetWellLogGrpc", PetrelObjectRef, msg) # type: ignore
    
    def GetWellLog(self, msg) -> PetrelObjectRef:
        return self._unary_wrapper("cegal.pythontool.GetWellLog", PetrelObjectRef, msg) # type: ignore
    
    def WellLog_DisplayUnitSymbol(self, msg) -> WellLog_DisplayUnitSymbol_Response:
        return self._unary_wrapper("cegal.pythontool.WellLog_DisplayUnitSymbol", WellLog_DisplayUnitSymbol_Response, msg) # type: ignore
    
    def WellLog_GetParentPythonBoreholeObject(self, msg) -> WellLog_GetParentPythonBoreholObject_Response:
        return self._unary_wrapper("cegal.pythontool.WellLog_GetParentPythonBoreholeObject", WellLog_GetParentPythonBoreholObject_Response, msg) # type: ignore
    
    def WellLog_SetSamples(self, msg) -> WellLog_SetSamples_Response:
        return self._unary_wrapper("cegal.pythontool.WellLog_SetSamples", WellLog_SetSamples_Response, msg) # type: ignore
    
    def WellLog_GetSamples(self, msg) -> WellLog_GetSamples_Response:
        return self._unary_wrapper("cegal.pythontool.WellLog_GetSamples", WellLog_GetSamples_Response, msg) # type: ignore
    
    def WellLog_GetGlobalWellLog(self, msg) -> WellLog_GetGlobalWellLog_Response:
        return self._unary_wrapper("cegal.pythontool.WellLog_GetGlobalWellLog", WellLog_GetGlobalWellLog_Response, msg) # type: ignore
    
    def DiscreteWellLog_GetAllDictionaryCodes(self, msg) -> DiscreteWellLog_GetAllDictionaryCodes_Response:
        return self._unary_wrapper("cegal.pythontool.DiscreteWellLog_GetAllDictionaryCodes", DiscreteWellLog_GetAllDictionaryCodes_Response, msg) # type: ignore

    def WellLog_GetTupleValues(self, msg) -> WellLog_GetTuple_Response:
        return self._server_streaming_wrapper("cegal.pythontool.WellLog_GetTupleValues", WellLog_GetTuple_Response, msg)

    def WellLog_GetLogValues(self, msg) -> WellLog_GetValues_Response:
        return self._server_streaming_wrapper("cegal.pythontool.WellLog_GetLogValues", WellLog_GetValues_Response, msg)
    
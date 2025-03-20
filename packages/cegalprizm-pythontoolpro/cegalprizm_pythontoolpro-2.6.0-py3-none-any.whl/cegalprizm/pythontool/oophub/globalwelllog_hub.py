# Copyright 2025 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



from cegalprizm.pythontool.grpc.petrelinterface_pb2 import PetrelObjectRef
from cegalprizm.pythontool.grpc.petrelinterface_pb2 import GlobalWellLog_GetAllLogs_Response, GlobalWellLog_GetWellLogByBoreholeName_Response
from cegalprizm.pythontool.grpc.petrelinterface_pb2 import GlobalWellLog_DisplayUnitSymbol_Response, GlobalWellLog_CreateWellLog_Response
from cegalprizm.pythontool.grpc.petrelinterface_pb2 import GlobalWellLog_CreateDictionaryWellLog_Response, DiscreteWellLog_GetAllDictionaryCodes_Response
from .base_hub import BaseHub


class GlobalWellLogHub(BaseHub):
    def GetGlobalWellLogGrpc(self, msg) -> PetrelObjectRef:
        return self._wrapper("cegal.pythontool.GetGlobalWellLogGrpc", PetrelObjectRef, msg)
    
    def GetGlobalWellLog(self, msg) -> PetrelObjectRef:
        return self._unary_wrapper("cegal.pythontool.GetGlobalWellLog", PetrelObjectRef, msg)
    
    def GlobalWellLog_GetAllLogs(self, msg) -> GlobalWellLog_GetAllLogs_Response:
        return self._unary_wrapper("cegal.pythontool.GlobalWellLog_GetAllLogs", GlobalWellLog_GetAllLogs_Response, msg)
    
    def GlobalWellLog_GetWellLogByBoreholeNameOrGuid(self, msg) -> GlobalWellLog_GetWellLogByBoreholeName_Response:
        return self._unary_wrapper("cegal.pythontool.GlobalWellLog_GetWellLogByBoreholeNameOrGuid", GlobalWellLog_GetWellLogByBoreholeName_Response, msg)

    def GlobalWellLog_DisplayUnitSymbol(self, msg) -> GlobalWellLog_DisplayUnitSymbol_Response:
        return self._unary_wrapper("cegal.pythontool.GlobalWellLog_DisplayUnitSymbol", GlobalWellLog_DisplayUnitSymbol_Response, msg)

    def GlobalWellLog_CreateWellLog(self, msg) -> GlobalWellLog_CreateWellLog_Response:
        return self._unary_wrapper("cegal.pythontool.GlobalWellLog_CreateWellLog", GlobalWellLog_CreateWellLog_Response, msg)
    
    def GlobalWellLog_CreateDictionaryWellLog(self, msg) -> GlobalWellLog_CreateDictionaryWellLog_Response:
        return self._unary_wrapper("cegal.pythontool.GlobalWellLog_CreateDictionaryWellLog", GlobalWellLog_CreateDictionaryWellLog_Response, msg)

    def GlobalWellLog_GetAllDictionaryCodes(self, msg) -> DiscreteWellLog_GetAllDictionaryCodes_Response:
        return self._unary_wrapper("cegal.pythontool.GlobalWellLog_GetAllDictionaryCodes", DiscreteWellLog_GetAllDictionaryCodes_Response, msg)
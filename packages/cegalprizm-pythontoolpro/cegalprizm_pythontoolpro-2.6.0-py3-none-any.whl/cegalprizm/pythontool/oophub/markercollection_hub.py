# Copyright 2025 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.



from cegalprizm.pythontool.grpc.petrelinterface_pb2 import PetrelObjectRef, ProtoBool, PropertyRangeData, PetrelObjectGuid
from cegalprizm.pythontool.grpc.petrelinterface_pb2 import PetrelObject_GetName_Response, MarkerCollection_SetName_Response
from cegalprizm.pythontool.grpc.petrelinterface_pb2 import MarkerCollection_AddMarker_Response, MarkerCollection_GetMarkerDroid_Response
from .base_hub import BaseHub
import typing
class MarkerCollectionHub(BaseHub):
    def GetMarkerCollection(self, msg) -> PetrelObjectRef:
        return self._unary_wrapper("cegal.pythontool.GetMarkerCollection", PetrelObjectRef, msg) # type: ignore

    def MarkerCollection_GetName(self, msg) -> PetrelObject_GetName_Response:
        return self._unary_wrapper("cegal.pythontool.MarkerCollection_GetName", PetrelObject_GetName_Response, msg) # type: ignore

    def MarkerCollection_SetName(self, msg) -> MarkerCollection_SetName_Response:
        return self._unary_wrapper("cegal.pythontool.MarkerCollection_SetName", MarkerCollection_SetName_Response, msg) # type: ignore

    def MarkerCollection_GetValues(self, msg) -> typing.Iterable[PropertyRangeData]:
        return self._server_streaming_wrapper("cegal.pythontool.MarkerCollection_GetValues", PropertyRangeData, msg) # type: ignore

    def MarkerCollection_SetPropertyValues(self, iterable_requests) -> ProtoBool:
        return self._client_streaming_wrapper("cegal.pythontool.MarkerCollection_SetPropertyValues", ProtoBool, iterable_requests) # type: ignore

    def MarkerCollection_GetAttributes(self, msg) -> PetrelObjectRef:
        return self._server_streaming_wrapper("cegal.pythontool.MarkerCollection_GetAttributes", PetrelObjectRef, msg) # type: ignore

    def MarkerCollection_AddAttribute(self, msg) -> ProtoBool:
        return self._client_streaming_wrapper("cegal.pythontool.MarkerCollection_AddAttribute", ProtoBool, msg) # type: ignore

    def MarkerCollection_AddEmptyAttribute(self, msg) -> ProtoBool:
        return self._unary_wrapper("cegal.pythontool.MarkerCollection_AddEmptyAttribute", ProtoBool, msg) # type: ignore

    def MarkerCollection_GetStratigraphies(self, msg) -> PetrelObjectRef:
        return self._server_streaming_wrapper("cegal.pythontool.MarkerCollection_GetStratigraphies", PetrelObjectRef, msg) # type: ignore

    def MarkerCollection_AddMarker(self, msg) -> MarkerCollection_AddMarker_Response:
        return self._unary_wrapper("cegal.pythontool.MarkerCollection_AddMarker", MarkerCollection_AddMarker_Response, msg) # type: ignore

    def MarkerCollection_AddManyMarkers(self, msg) -> MarkerCollection_AddMarker_Response:
        return self._client_streaming_wrapper("cegal.pythontool.MarkerCollection_AddManyMarkers", MarkerCollection_AddMarker_Response, msg)
    
    def MarkerCollection_GetMarkerDroid(self, msg) -> MarkerCollection_GetMarkerDroid_Response:
        return self._unary_wrapper("cegal.pythontool.MarkerCollection_GetMarkerDroid", MarkerCollection_GetMarkerDroid_Response, msg)
    
    def MarkerCollection_DeleteMarker(self, msg) -> ProtoBool:
        return self._unary_wrapper("cegal.pythontool.MarkerCollection_DeleteMarker", ProtoBool, msg)
    
    def MarkerCollection_DeleteManyMarkers(self, msg) -> ProtoBool:
        return self._client_streaming_wrapper("cegal.pythontool.MarkerCollection_DeleteManyMarkers", ProtoBool, msg)
    
    def MarkerCollection_GetAttributeParent(self, msg) -> PetrelObjectGuid:
        return self._unary_wrapper("cegal.pythontool.MarkerCollection_GetAttributeParent", PetrelObjectGuid, msg)
    
    def MarkerCollection_GetAttributeUniqueName(self, msg) -> PetrelObject_GetName_Response:
        return self._unary_wrapper("cegal.pythontool.MarkerCollection_GetAttributeUniqueName", PetrelObject_GetName_Response, msg)

    def MarkerCollection_GetStratigraphyUniqueName(self, msg) -> PetrelObject_GetName_Response:
        return self._unary_wrapper("cegal.pythontool.MarkerCollection_GetStratigraphyUniqueName", PetrelObject_GetName_Response, msg)

    def MarkerCollection_GetStratigraphyParent(self, msg) -> PetrelObjectGuid:
        return self._unary_wrapper("cegal.pythontool.MarkerCollection_GetStratigraphyParent", PetrelObjectGuid, msg)


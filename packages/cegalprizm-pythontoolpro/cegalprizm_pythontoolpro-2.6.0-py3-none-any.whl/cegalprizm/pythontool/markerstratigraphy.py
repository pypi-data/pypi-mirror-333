# Copyright 2025 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.




import typing
from cegalprizm.pythontool import PetrelObject, PetrelObjectWithPetrelNameSetter

if typing.TYPE_CHECKING:
    from cegalprizm.pythontool.grpc.markerstratigraphy_grpc import MarkerStratigraphyGrpc
    from cegalprizm.pythontool.markercollection import MarkerCollection

class MarkerStratigraphy(PetrelObject, PetrelObjectWithPetrelNameSetter):
    """A class holding information about a MarkerStratigraphy"""

    def __init__(self, petrel_object_link: "MarkerStratigraphyGrpc", parent_markercollection: "MarkerCollection" = None):
        super(MarkerStratigraphy, self).__init__(petrel_object_link)
        self._markerstratigraphy_object_link = petrel_object_link
        self._parent_markercollection = petrel_object_link.GetStratigraphyParent() if parent_markercollection is None else parent_markercollection
        self._unique_name = petrel_object_link._unique_name
        self._droid = petrel_object_link._guid

    def __str__(self) -> str:
        """A readable representation"""
        return 'MarkerStratigraphy("{0}")'.format(self._unique_name)

    def __repr__(self) -> str:
        return str(self)

    def _get_name(self) -> str:
        return self._unique_name

    @property
    def markercollection(self):
        return self._parent_markercollection
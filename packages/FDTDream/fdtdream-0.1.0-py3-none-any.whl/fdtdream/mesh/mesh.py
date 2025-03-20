from typing import Union, TypedDict, Unpack, Any, Self
from itertools import product

import numpy as np
from numpy.typing import NDArray

from .settings import MeshGeneralSettings, MeshGeometry
from ..base_classes import SimulationObject, ModuleCollection
from ..interfaces import StructureInterface
from ..resources.functions import convert_length
from ..resources.literals import AXES


class MeshKwargs(TypedDict, total=False):
    x: float
    y: float
    z: float
    x_span: float
    y_span: float
    z_span: float
    based_on_a_structure: StructureInterface
    dx: float
    dy: float
    dz: float


class MeshSettings(ModuleCollection):

    general: MeshGeneralSettings
    geometry: MeshGeometry
    __slots__ = ["general", "geometry"]

    def __init__(self, parent_object) -> None:
        super().__init__(parent_object)

        # Assign the sub modules.
        self.general = MeshGeneralSettings(parent_object)
        self.geometry = MeshGeometry(parent_object)


class Mesh(SimulationObject):

    settings: MeshSettings
    _structure: Union[StructureInterface, None]
    __slots__ = ["_structure"]

    def __init__(self, name: str, sim, **kwargs: Unpack[MeshKwargs]) -> None:
        super().__init__(name, sim)

        # Initialize the _structure variable
        self._structure = None

        # Assign the settings module.
        self.settings = MeshSettings(self)

        # Filter and apply kwargs.
        self._process_kwargs(**kwargs)

    def _process_kwargs(self, copied: bool = False, **kwargs) -> None:
        """Filters and applies the kwargs specific to the Rectangle structure type."""

        # Abort if the kwargs are empty
        if not kwargs:
            return

        # Initialize dicts
        position = {}
        dimensions = {}
        steps = {}
        structure = None

        # Filter kwargs
        for k, v in kwargs.items():
            if k == "based_on_a_structure":
                structure = v
            elif k in ["dx", "dy", "dz"]:
                steps[k] = v
            elif k in ["x", "y", "z"]:
                position[k] = v
            elif k in ["x_span", "y_span", "z_span"]:
                dimensions[k] = v

        # Apply kwargs
        if structure:
            self.settings.geometry.set_based_on_a_structure(structure)
        if position:
            self.settings.geometry.set_position(**position)
        if dimensions:
            self.settings.geometry.set_dimensions(**dimensions)
        if steps:
            self.settings.general.set_maximum_mesh_step(**steps)

    def _get_corners(self, absolute: bool = False) -> NDArray:

        # If no parent structure, extrapolate corners based on the spans and position.
        if self._structure is None:
            return super()._get_corners(absolute)

        # Fetch the buffer
        buffer = np.float64(self._get("buffer", float))

        # Fetch the bounding_box of the parent structure
        bbox = self._structure._get_bounding_box(absolute)

        if buffer != 0:
            min_values, max_values = bbox[0], bbox[1]

            # Scale the bounding box with the buffer
            min_values -= buffer
            max_values += buffer

            # Recreate the bbox with scaled value
            bbox = np.vstack((min_values, max_values))

        # Create an array of all corners
        return np.array(list(product(*zip(bbox[0], bbox[1]))), dtype=np.float64)

    def max(self, axis: AXES, absolute: bool = False) -> float:
        if self._structure is None:
            return super().max(axis, absolute)
        else:
            return self._structure.max(axis, absolute) + convert_length(self._get("buffer", float), "m", self._units)

    def min(self, axis: AXES, absolute: bool = False) -> float:
        if self._structure is None:
            return super().min(axis, absolute)
        else:
            return self._structure.min(axis, absolute) - convert_length(self._get("buffer", float), "m", self._units)

    def span(self, axis: str) -> float:
        if self._structure is None:
            return super().span(axis)
        else:
            return self._structure.span(axis) + convert_length(self._get("buffer", float), "m", self._units) * 2

    # endregion User Methods

    def copy(self, name, **kwargs: Unpack[Any]) -> Self:

        # Copy using super() call.
        copied = super().copy(name, **kwargs)

        # Add to the meshes list of the parent simulation
        self._sim._meshes.append(copied)

        return copied

    @property
    def based_on_structure(self) -> Union[StructureInterface, None]:
        return self._structure

    @based_on_structure.setter
    def based_on_structure(self, structure: Union[StructureInterface, None]) -> None:
        if structure is None:
            self.settings.geometry.set_directly_defined()
        else:
            self.settings.geometry.set_based_on_a_structure(structure)

    @property
    def dx(self) -> float:
        return convert_length(self._get("dx", float), "m", self._units)

    @dx.setter
    def dx(self, dx: float):
        self.settings.general.set_maximum_mesh_step(dx=dx)

    @property
    def dy(self) -> float:
        return convert_length(self._get("dy", float), "m", self._units)

    @dy.setter
    def dy(self, dy: float):
        self.settings.general.set_maximum_mesh_step(dy=dy)

    @property
    def dz(self) -> float:
        return convert_length(self._get("dz", float), "m", self._units)

    @dz.setter
    def dz(self, dz: float):
        self.settings.general.set_maximum_mesh_step(dz=dz)

    @property
    def x(self) -> float:
        """
        Fetches and returns the object's x-coordinate from the parent simulation.
        If the "use relative coordinates" flag in Lumerical is True, this is what's returned.
        Units are dictated by what units are specified in the parent simulation.

        """
        if self._structure is None:
            x = self._get("x", float)
            return convert_length(x, "m", self._units)
        else:
            return self._structure.x

    @x.setter
    def x(self, x: float) -> None:
        """
        Sets the object's y-coordinate in the parent simulation.
        Units are dictated by what units are specified in the parent simulation.

        """
        self.settings.geometry.set_position(x=x)

    @property
    def y(self) -> float:
        """
        Fetches and returns the object's y-coordinate from the parent simulation.
        If the "use relative coordinates" flag in Lumerical is True, this is what's returned.
        Units are dictated by what units are specified in the parent simulation.

        """
        if self._structure is None:
            y = self._get("y", float)
            return convert_length(y, "m", self._units)
        else:
            return self._structure.y

    @y.setter
    def y(self, y: float) -> None:
        """
        Sets the object's y-coordinate in the parent simulation.
        Units are dictated by what units are specified in the parent simulation.

        """
        self.settings.geometry.set_position(y=y)

    @property
    def z(self) -> float:
        """
        Fetches and returns the object's z-coordinate from the parent simulation.
        If the "use relative coordinates" flag in Lumerical is True, this is what's returned.
        Units are dictated by what units are specified in the parent simulation.

        """
        if self._structure is None:
            z = self._get("z", float)
            return convert_length(z, "m", self._units)
        else:
            return self._structure.z

    @z.setter
    def z(self, z: float) -> None:
        """
        Sets the object's z-coordinate in the parent simulation.
        Units are dictated by what units are specified in the parent simulation.

        """
        self.settings.geometry.set_position(z=z)

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, Any, cast, Iterable, Tuple, Self

import numpy as np
from numpy.typing import NDArray
from trimesh import Trimesh, transformations

from .settings import StructureSettings
from ..base_classes import SimulationObject
from ..interfaces import SimulationInterface, MeshInterface, StructureInterface
from ..resources.literals import AXES
from ..resources.functions import convert_length


class Structure(SimulationObject, StructureInterface, ABC):

    # region Class Body

    settings: StructureSettings
    _mesh: MeshInterface
    __slots__ = ["_mesh", "settings"]

    # endregion Class Body

    # region Dev methods

    def __init__(self, name: str, sim: SimulationInterface, *args, **kwargs) -> None:
        super().__init__(name, sim)

    def _getmaterial(self, name: Optional[str], parameter: Optional[str]) -> Any:
        """
        Reference to the getmaterial() method of the lumapi module.
        Fetches material data from the material database.

        Args:
            name: Name of the material. If not provided, all materials are provided.
            parameter: What parameter associated with the material to fetch. If not provided, all are returned.

        Returns:
            Any parameter or list of parameters based on the input.

        """
        return self._lumapi.getmaterial(name, parameter)

    def _get_mesh_order(self) -> int:
        """
        Fetches the mesh order of the structure's material.

        Returns:
            The mesh order from the material database if it's not overridden by the object.
            If it is, it will return this.

        """
        material = self._get("material", str)
        overridden = self._get("override mesh order from material database", bool)
        if overridden or material == "<Object defined dielectric>":
            return self._get("mesh order", int)
        else:
            return cast(self._getmaterial(material, "mesh order"), int)

    def _get_rotation_state(self) -> Tuple[NDArray, np.float64]:
        """
        Fetches the rotation state of the object.

        Returns:
            A tuple with the rotation vector first, and the rotation angle second (radians).
        """
        return self.settings.rotation._get_rotation_rot_vec()

    def _rotate_trimesh(self, mesh: Trimesh, position: NDArray) -> Trimesh:
        """
        Takes in a Trimesh object and rotates it based on the rotation state of the parent object.

        Args:
            mesh (Trimesh): The trimesh that will be rotated.
            position (NDArray): A 3D position vector converted to the units of the simulation.

        """

        # Fetch the rotation state
        rot_vec, angle = self._get_rotation_state()

        if angle == 0:
            return mesh
        else:
            # Create rotation matrix and apply rotation
            r = transformations.rotation_matrix(angle, rot_vec, position)
            return mesh.apply_transform(r)

    # endregion Dev. Methods

    # region User Methods

    def min(self, axis: AXES, absolute: bool = False) -> float:

        # Get the trimesh polygon
        poly = self._get_trimesh(absolute)

        # Fetch the min value from the polygon's vertices.
        mapping = {"x": 0, "y": 1, "z": 2}
        min_coords = np.min(poly.vertices, axis=0)
        return min_coords[mapping[axis]]

    def max(self, axis: AXES, absolute: bool = False) -> float:

        # Get the trimesh polygon
        poly = self._get_trimesh(absolute)

        # Fetch the min value from the polygon's vertices.
        mapping = {"x": 0, "y": 1, "z": 2}
        min_coords = np.max(poly.vertices, axis=0)
        return min_coords[mapping[axis]]

    def span(self, axis: AXES) -> float:
        """
        Calculates and returns the distance between the object's min and max coordinate along the specified axis,
        regardless of rotation state.

        Args:
            axis (str): x, y, or z.

        Returns:
            (float) the distance between the min and max coordinate occupied by the object along the specified axis.
        """

        # Fetch the trimesh polygon
        poly = self._get_trimesh()

        # Fetch the min value from the polygon's vertices.
        mapping = {"x": 0, "y": 1, "z": 2}
        min_coords = np.min(poly.vertices, axis=0)
        max_coords = np.max(poly.vertices, axis=0)

        # Calculate the span
        span = max_coords[mapping[axis]] - min_coords[mapping[axis]]

        return span

    def copy(self, name, **kwargs) -> Self:

        # Copy through super() call
        copied = super().copy(name, **kwargs)

        # Add the python object to the parent simulation
        self._sim._structures.append(copied)

        return copied

    # endregion User Methods

    # region User Properties

    @property
    def mesh(self) -> MeshInterface | None:
        """
        Returns:
            Reference to the mesh object associated with the structure. Returns None if no mesh is assigned.

        """
        return self._mesh

    # endregion User Properties

    # region Abstract Methods

    @abstractmethod
    def _get_scripted(self, position: Iterable) -> str:
        """
        Generates the Lumerical FDTD script that reproduces the objects at the position specified.

        Args:
            position: Position as a three element iterable, specified in meters.

        Returns:
            The script as a string.

        """
        ...

    @abstractmethod
    def _get_trimesh(self, absolute: bool = False) -> Trimesh:
        """
        Generates a 3D trimesh object based on the structure at it's absolute position.

        Args:
            absolute: Flag deciding if the trimesh has the absolute position or the relative.

        Returns:
            a trimesh.Trimesh object.
        """

    # endregion Abstract Methods



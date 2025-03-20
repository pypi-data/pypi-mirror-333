from __future__ import annotations

from abc import ABC
from copy import copy
from typing import TypedDict, Unpack, Sequence, Type, TypeVar, Self

import trimesh

from .rectangle import Rectangle, RectangleKwargs
from .settings import StructureSettings
from .structure import Structure
from ..base_classes import BaseGeometry
from ..resources.literals import AXES

T = TypeVar("T")


class GroupedStructure(Structure, ABC):
    _closest_parent: StructureGroup

    # Positional
    _x: float
    _y: float
    _z: float

    # Rotational
    _first_axis: str
    _second_axis: str
    _third_axis: str
    _rotation_1: float
    _rotation_2: float
    _rotation_3: float

    # Material
    _material: str
    _index: str
    _index_units: str
    _mesh_order: int
    _grid_attribute_name: str | None

    __slots__ = ["_x", "_y", "_z", "_first_axis", "_second_axis", "_third_axis", "_rotation_1", "_rotation_2",
                 "_rotation_3", "_material", "_index", "_index_units", "_mesh_order", "_grid_attribute_name",
                 "_closest_parent"]

    def _initialize_variables(self, closest_parent: StructureGroup) -> None:
        self._closest_parent = closest_parent
        self._x, self._y, self._z = 0, 0, 0
        self._first_axis, self._second_axis, self._third_axis = "none", "none", "none"
        self._rotation_1, self._rotation_2, self._rotation_3 = 0, 0, 0
        self._material = "<Object defined dielectric>"
        self._index = "1.4"
        self._grid_attribute_name = None

    def _get(self, parameter: str, parameter_type: Type[T]) -> T:
        return getattr(self, "_" + parameter.replace(" ", "_"))

    def _set(self, parameter: str, value: Type[T]) -> T:
        setattr(self, "_" + parameter.replace(" ", "_"), value)
        self._closest_parent._update()
        return value

    def copy(self, **kwargs) -> Self:
        copied = copy(self)
        self._closest_parent._structures.append(copied)
        copied.settings = self.settings._copy(copied)
        copied._process_kwargs(copied=True, **kwargs)
        return copied


class GroupedRectangle(Rectangle, GroupedStructure):
    _x_span: float
    _y_span: float
    _z_span: float

    __slots__ = ["_x_span", "_y_span", "_z_span"]

    def __init__(self, parent_group, name, sim, **kwargs):
        self._initialize_variables(parent_group)
        super().__init__(name, sim, **kwargs)
        self._parents.append(parent_group)

    def _initialize_variables(self, closest_parent: StructureGroup) -> None:
        super()._initialize_variables(closest_parent)
        self._x_span = 100e-9
        self._y_span = 100e-9
        self._z_span = 100e-9


class StructureGroupKwargs(TypedDict, total=False):
    """
    Key-value pairs that can be used in the StructureGroup structure type's constructor.
    """
    x: float
    y: float
    z: float
    rot_vec: AXES | Sequence[float]
    rot_angle: float
    rot_point: Sequence[float]


class StructureGroupSettings(StructureSettings):
    """
    A module containing submodules for settings specific to the Rectangle structure type.
    """
    geometry: BaseGeometry


class StructureGroup(Structure):
    _structures: list[GroupedStructure]

    def __init__(self, name, sim, **kwargs: Unpack[StructureGroupKwargs]) -> None:
        super().__init__(name, sim)

        self.settings = StructureGroupSettings(self, BaseGeometry)
        self._structures = []

        # Process kwargs
        self._process_kwargs(**kwargs)

    def _process_kwargs(self, copied: bool = False, **kwargs) -> None:
        """Filters and applies the kwargs specific to the StructureGroup structure type."""

        # Abort if the kwargs are empty
        if not kwargs:
            return

        # Initialize dicts
        position = {}
        rotation = {}

        # Filter kwargs
        for k, v in kwargs.items():
            if k in ["x", "y", "z"]:
                position[k] = v
            elif k in ["rot_vec", "rot_angle", "rot_point"]:
                rotation[k] = v

        # Apply kwargs
        if position:
            self.settings.geometry.set_position(**position)
        if rotation:
            self.settings.rotation.set_rotation(**rotation)

    def _update(self) -> None:
        scripts = [obj._get_scripted((obj._x, obj._y, obj._z)) for obj in self._structures]
        script = "deleteall;\n"
        for s in scripts:
            script += s
        self._set("script", script)

    def _get_trimesh(self, absolute: bool = False) -> trimesh.Trimesh:

        trimeshes = [obj._get_trimesh() for obj in self._structures]
        union = trimesh.boolean.union(trimeshes)
        return union

    def _get_scripted(self, position: Sequence[float, float, float]) -> str:

        script = (
            "addstructuregroup();\n"
            f"set('name', '{self._name}');\n"
            f"set('x', {position[0]});\n"
            f"set('y', {position[1]});\n"
            f"set('z', {position[2]});\n"
        )
        if self.settings.rotation.__getattribute__("_is_rotated"):
            axes, rotations = self.settings.rotation._get_rotation_euler()
            for axis, rotation, que, nr in zip(axes, rotations, ["first", "second", "third"], ["1", "2", "3"]):
                if rotation == 0:
                    continue
                else:
                    script += (
                        f"set('{que} axis', '{axis}');\n"
                        f"set('rotation {nr}', {rotation});\n"
                    )

        s = self._get('script', str).replace("\n", '"+\n"')
        if s.startswith("deletall;"):
            s = s[9:]
        subscript = '"'
        subscript += self._get('script', str).replace("\n", '"+\n"')
        if subscript.endswith('\n"'):
            subscript = subscript[:-3]

        script += f"set('script', {subscript});\n"

        return script

    def add_rect(self, **kwargs: Unpack[RectangleKwargs]) -> GroupedRectangle:
        rect = GroupedRectangle(self, self._name + "_struct", self._sim, **kwargs)
        self._structures.append(rect)
        return rect

    # endregion Dev Methods

    def copy(self, name, **kwargs: StructureGroupKwargs) -> Self:
        return super().copy(name, **kwargs)
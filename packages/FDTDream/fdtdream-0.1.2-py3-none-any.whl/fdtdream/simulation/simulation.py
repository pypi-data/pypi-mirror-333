from __future__ import annotations

import sys
import os
from typing import List, Any, ClassVar, Type, TypeVar

from .add import Add
from ..interfaces import SimulationInterface, SimulationObjectInterface
from ..lumapi import Lumapi
from ..resources import errors
from ..resources.functions import get_unique_name
from ..resources.literals import LENGTH_UNITS
from .. import structures
from .. import monitors
from .. import sources
from ..fdtd import FDTDRegion
from ..mesh import Mesh

T = TypeVar("T")

# Type to Class Map for loading simulation objects
_type_to_class_map: dict[str, type] = {

    # Structure types
    "Rectangle": structures.Rectangle,
    "Circle": structures.Circle,
    "Sphere": structures.Sphere,
    "Ring": structures.Ring,
    "Pyramid": structures.Pyramid,
    "Polygon": structures.Polygon,

    # Source types
    "GaussianSource": sources.GaussianBeam,
    "Cauchy-Lorentzian": sources.CauchyLorentzianBeam,
    "PlaneSource": sources.PlaneWave,

    # Monitor Types
    "IndexMonitor": monitors.IndexMonitor,
    "DFTMonitor": monitors.FreqDomainFieldAndPowerMonitor,

    # FDTD Types
    "FDTD": FDTDRegion,
    "Mesh": Mesh,

    # Group types:

}


class Simulation(SimulationInterface):

    # region Class Body
    global_source: sources.GlobalSource
    global_monitor: monitors.GlobalMonitor
    _loaded_objects: List[SimulationObjectInterface]
    _structures: List
    _sources: List
    _monitors: List
    _meshes: List
    _fdtd: Any
    _save_path: str
    add: Add
    __slots__ = ["_global_units", "_objects", "add", "_monitors", "_meshes", "_fdtd", "_loaded_objects",
                 "globa_source", "global_monitor"]
    # endregion Class Body

    # region Dev methods

    def __init__(self, lumapi: Lumapi, save_path: str, units: LENGTH_UNITS):

        # Assign the global source and monitor
        self.global_source = sources.GlobalSource(self)
        self.global_monitor = monitors.GlobalMonitor(self)  # type: ignore

        self._save_path = os.path.abspath(save_path)
        self._global_lumapi = lumapi
        self._global_units = units
        self._structures = []
        self._sources = []
        self._monitors = []
        self._meshes = []
        self._loaded_objects = []

        # Initialize FDTD Region variable
        self._fdtd = None

        # Assign module collections
        self.add = Add(self, self._lumapi, self._units, self._check_name)

    def _get_all_objects(self) -> list[SimulationObjectInterface]:
        """Fetches a list of all objects in the current simulation."""
        all_objects = []
        all_objects.extend(self._structures)
        all_objects.extend(self._sources)
        all_objects.extend(self._monitors)
        all_objects.extend(self._meshes)
        all_objects.extend(self._fdtd)
        return all_objects

    def _get_used_names(self) -> list[str]:
        """Fetches a list with the names of all objects in the current simulation."""
        names = [obj._name for obj in self._get_all_objects()]
        return names

    def _get_simulation_objects_in_scope(self, groupscope: str, autoset_new_unique_names: bool,
                                         iterated: List[dict[str, str]] = None) -> List[dict[str, str]]:
        """
        Recursively retrieves all simulation objects within a specified scope, including nested groups,
        returning a list of dictionaries with object details. Each dictionary contains the object's name,
        type, and scope information, providing a structured representation of the simulation hierarchy.

        Parameters:
        -----------
        groupscope : str
            The name of the group scope to explore, starting with the provided scope and iterating through
            nested groups if present.

        autoset_new_unique_names : bool
            If `True`, assigns unique names to objects by automatically adjusting names to avoid duplicates
            within the scope. This is helpful in complex simulations with potentially overlapping object names.

        iterated : List[Dict[str, str]], optional
            A list of dictionaries representing objects that have already been processed. This list is used
            during recursion to aggregate results across nested group scopes.

        Returns:
        --------
        List[Dict[str, str]]
            A list of dictionaries, each containing:
            - "name": The unique name of the object within the simulation.
            - "type": A string representing the object type as identified by the FDTD simulation program.
            - "scope": The name of the group or scope in which the object resides.

        """
        if iterated is None:
            iterated = []

        # Fetch reference to the lumerical API for reuse
        lumapi = self._lumapi()

        # Select the provided group as the groupscope and select all objects in it
        lumapi.groupscope(groupscope)
        lumapi.selectall()
        num_objects = int(lumapi.getnumber())

        # Iterate through all the objects in the group
        for i in range(num_objects):

            name = lumapi.get("name", i + 1).replace(" ", "_")
            sim_object_type = lumapi.get("type", i + 1)

            used_names = [sim_object["name"].replace(" ", "_") for sim_object in iterated]

            if autoset_new_unique_names and sim_object_type != "FDTD":

                unique_name = get_unique_name(name, used_names)

                lumapi.set("name", unique_name, i + 1)

            else:
                unique_name = name

            iterated.append(
                {"name": unique_name, "type": sim_object_type, "scope": groupscope.split("::")[-1]})

            # Check if the object is another group, run this method recursively
            if (sim_object_type == "Layout Group" or
                    (sim_object_type == "Structure Group" and
                     lumapi.getnamed(name, "construction group") == 0.0)):
                new_groupscope = groupscope + "::" + unique_name
                iterated = self._get_simulation_objects_in_scope(new_groupscope, autoset_new_unique_names,
                                                                 iterated)
                lumapi.groupscope(groupscope)

            lumapi.selectall()

        return iterated

    def _load_objects_from_file(self) -> None:
        """
        Reads an `.fsp` simulation file and creates Python objects corresponding to each simulation
        object, enabling programmatic manipulation of the simulation environment. For enhanced
        autocompletion and type hints, call `print_variable_declarations()` after executing this
        function.

        This method retrieves all simulation objects within the "::model" scope, iterates over them,
        and instantiates Python representations for each based on the object type. The created objects
        are assigned as attributes to the current instance, making them accessible as standard Python
        objects for easier manipulation.
        """

        objects = []

        simulation_objects = self._get_simulation_objects_in_scope("::model", True)

        for sim_object in simulation_objects:

            # Assign the fdtd region to the simulation
            if sim_object["type"] == "FDTD":
                instantiated_object = _type_to_class_map[sim_object["type"]](self)

            # Handle different types of construction groups
            elif sim_object["type"] == "Structure Group":
                # TODO Implement catching different structure group types here.
                # script = lumapi.getnamed(sim_object["name"], "script")
                continue

            # Handle other structure types:
            else:

                # Create an instance of the object
                instantiated_object = _type_to_class_map[sim_object["type"]](sim_object["name"], self)

                # Implement logic based on the object's type.
                if isinstance(instantiated_object, structures.Structure):
                    self._structures.append(instantiated_object)
                elif isinstance(instantiated_object, monitors.Monitor):
                    self._monitors.append(instantiated_object)
                elif isinstance(instantiated_object, sources.Source):
                    self._sources.append(instantiated_object)
                elif isinstance(instantiated_object, Mesh):
                    self._meshes.append(instantiated_object)

            # Handle cases where the object is a part of a parent group
            if sim_object["scope"] != "model":
                group = getattr(self, sim_object["scope"])
                group._children.append(instantiated_object)
                instantiated_object._parents.append(group)

            # Assign a variable to each object.
            if sim_object["name"] == "FDTD":
                setattr(self, "_fdtd", instantiated_object)
            else:
                setattr(self, sim_object["name"], instantiated_object)

            objects.append(instantiated_object)

        # Assign the list of loaded object to the class variable.
        self._loaded_objects = objects

    def _print_variable_declarations(self, simulation_variable_name: str, exit_after_printing: bool) -> None:
        """
        Prints type declarations for all active simulation objects, enabling autocompletion and type hints
        when manipulating a loaded simulation programmatically.

        This method retrieves all simulation objects within the "::model" scope and generates Python variable
        declarations for each object, formatted for easy copy-pasting into code. These declarations provide
        full autocompletion support, allowing for more streamlined development when interacting with a loaded
        `.fsp` file.

        Parameters:
        -----------
        simulation_variable_name : str
            The name to use for the simulation instance variable in the declarations, representing the
            simulation environment.

        exit_after_printing : bool
            If `True`, the program will exit immediately after printing the declarations. Useful for generating
            declarations without running additional code.
        """

        if self._loaded_objects is None:
            raise ValueError("No objects loaded yet.")

        simulation_objects = self._loaded_objects

        # Print the type declarations in the desired format
        print("# region Type Annotations")

        for sim_object in simulation_objects:

            object_class = sim_object.__class__

            if object_class.__name__ == "FDTDRegion":
                object_name = "fdtd"
                line = (
                    f"{object_name}: FDTDream"
                    f".i.{object_class.__name__} "
                    f"= getattr({simulation_variable_name}, '_{object_name}')"
                )
                if len(line) > 116:
                    line = (
                        f"{object_name}: FDTDream"
                        f".i.{object_class.__name__} "
                        f"= (\n\tgetattr({simulation_variable_name}, '_{object_name}'))")

            elif object_class is not None:
                object_name = sim_object._name
                line = (
                    f"{object_name}: FDTDream"
                    f".i.{object_class.__name__} "
                    f"= getattr({simulation_variable_name}, '{object_name}')")
                if len(line) > 116:
                    line = (
                        f"{object_name}: FDTDream"
                        f".i.{object_class.__name__} "
                        f"= (\n\tgetattr({simulation_variable_name}, '{object_name}'))")
            else:
                raise ValueError("Something wierd happened here.")
            print(line)

        print("# endregion Type Annotations")

        if exit_after_printing:
            sys.exit()

    def _units(self) -> LENGTH_UNITS:
        return self._global_units

    def _lumapi(self) -> Lumapi:
        return self._global_lumapi

    def _check_name(self, name: str) -> None:
        """Checks if an object with a given name exists. If it does, a FDTDreamNotUniqueError is raised."""
        if any(getattr(obj, "_name") == name for obj in self._structures):
            message = f"Expected unique name. Object with name '{name}' already exists."
            raise errors.FDTDreamNotUniqueNameError(message)

    def save(self, save_path: str = None, print_confirmation: bool = True) -> None:
        """
        Saves the lumerical simulation file to the default save path or to the speccified save path if provided.

        Args:
            save_path (str): Where to save the file, including the name. Does not need to contain the .fsp suffix.
                If not provided, the original save path is used.
            print_confirmation (bool): If True, prints 'File saved to: r"path"' to console.

        """
        path = os.path.abspath(save_path) if save_path is not None else self._save_path
        self._lumapi().save(path)
        if print_confirmation:
            print("File saved to: r'" + path + "'")

    # endregion

from .monitors import Monitors
from .sources import Sources
from .structures import Structures
from .fdtd import FDTD
from ...base_classes.object_modules import ModuleCollection


class Add(ModuleCollection):
    __slots__ = ["structures", "sources", "monitors", "fdtd"]
    structures: Structures
    sources: Sources
    monitors: Monitors
    fdtd: FDTD

    def __init__(self, sim, lumapi, units, check_name) -> None:
        self.structures = Structures(sim, lumapi, units, check_name)
        self.sources = Sources(sim, lumapi, units, check_name)
        self.monitors = Monitors(sim, lumapi, units, check_name)
        self.fdtd = FDTD(sim, lumapi, units, check_name)

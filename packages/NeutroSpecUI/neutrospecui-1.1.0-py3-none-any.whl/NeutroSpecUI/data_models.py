import pandas as pd
import numpy as np
from dataclasses import dataclass
from typing import TYPE_CHECKING, cast, Generic, TypeVar

from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtWidgets import QApplication

from NeutroSpecUI.simulate import SimulationModel

if TYPE_CHECKING:
    from NeutroSpecUI.app import NeutroApp


T = TypeVar("T")


@dataclass
class Parameter(Generic[T]):
    value: T
    locked: bool = False
    bounds: tuple = (-np.inf, np.inf)
    name: str = "Parameter"
    unit: str = ""
    factor: float = 1

    def toggle(self) -> None:
        self.locked = not self.locked

    def get_bounds(self) -> tuple:
        return self.bounds

    def get_actual_value(self) -> T:
        if isinstance(self.value, (int, float)):
            return self.value * self.factor  # type: ignore
        return self.value


@dataclass
class Material:
    name: str
    params: list[Parameter]

    def get_param_dict(self) -> dict[str, Parameter[float]]:
        return {param.name: param for param in self.params}

    def get_value_dict(self) -> dict[str, float | str]:
        return {
            "name": self.name,
        } | {param.name: param.get_actual_value() for param in self.params}

    @staticmethod
    def from_dict(data: dict) -> "Material":
        # TODO: check for dublicate names
        return Material(
            data["name"],
            [Parameter(**param) for param in data["params"]],
        )


class ExperimentData(QObject):
    """Class to hold all the data for an setup. This includes the data, simulation, and fit.

    Attributes:
        data (pd.DataFrame): The experimental data.
        sim (Simulation): The simulation settings.
        fit (Simulation): The fit settings.
        simulateSim (Signal): Signal to trigger simulation of the simulation.
        simulateFit (Signal): Signal to trigger simulation of the fit.
        updateData (Signal): Signal to trigger update of the data.
        updateSim (Signal): Signal to trigger update of the simulation.
        updateFit (Signal): Signal to trigger update of the fit.
    """

    simulateSim = Signal()
    simulateFit = Signal()

    updateData = Signal()
    updateSim = Signal()
    updateFit = Signal()

    def __init__(
        self,
        data: pd.DataFrame | None,
        materials: list[Material],
        static_params: list[Parameter],
        parent: QObject | None = None,
    ) -> None:
        super().__init__(parent)

        self.sim = SimulationModel(
            materials=[],
            static_params=Material("static_params", static_params),
            data=data,
        )
        self.fit = SimulationModel(
            materials=[],
            static_params=Material("static_params", static_params),
            data=data,
        )
        self.set_materials(materials)

        self.simulateSim.connect(self._simulateSim)
        self.simulateFit.connect(self._simulateFit)

        self.simulateSim.emit()
        self.simulateFit.emit()

    def set_data(self, data: pd.DataFrame | None) -> None:
        self.sim.data = data
        self.fit.data = data
        self.updateData.emit()

    def set_materials(self, materials: list[Material]) -> None:
        self.sim.materials = materials
        self.simulateSim.emit()

    def set_fit_sim(self, opt_sim: SimulationModel) -> None:
        self.fit = opt_sim
        self.simulateFit.emit()

    @Slot()
    def _simulateSim(self) -> None:
        app = cast("NeutroApp", QApplication.instance())
        self.sim_result = app.backend.simulate(self.sim)
        self.updateSim.emit()

    @Slot()
    def _simulateFit(self) -> None:
        app = cast("NeutroApp", QApplication.instance())
        self.fit_result = app.backend.simulate(self.fit)
        self.updateFit.emit()

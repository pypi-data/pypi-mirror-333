from typing import TYPE_CHECKING, cast, Any
from collections.abc import Sequence
from dataclasses import dataclass, field
import copy

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

from PySide6.QtWidgets import QApplication, QErrorMessage
from PySide6.QtCore import QThread, Signal, QObject

if TYPE_CHECKING:
    from NeutroSpecUI.data_models import Material, Parameter
    from NeutroSpecUI.app import NeutroApp


@dataclass
class SimulationResult:
    """Dataclass that holds the results of a simulation.

    Attributes:
        x (np.ndarray): The x values of the simulation.
        y (np.ndarray): The y values of the simulation.
        extras (dict): Dictionary of extra data returned by the simulation.
    """

    x: np.ndarray
    y: np.ndarray
    extras: dict = field(default_factory=dict)

    def __init__(self, x: np.ndarray, y: np.ndarray, **extras):
        self.x = x
        self.y = y
        self.extras = extras


@dataclass
class SimulationValues:
    """Dataclass that holds the values of a simulation model for easy access.

    Attributes:
        materials (list[dict[str, Any]]): List of materials in the simulation.
    """

    materials: list[dict[str, Any]]
    static_params: dict[str, Any]
    data: pd.DataFrame | None = None
    settings: dict = field(default_factory=dict)


@dataclass
class SimulationModel:
    """Dataclass that holds the simulation parameters and settings.

    Attributes:
        materials (list["Material"]): List of materials in the simulation.
        settings (dict): Dictionary of settings for the simulation.
    """

    materials: list["Material"]
    static_params: "Material"
    data: pd.DataFrame | None = None
    settings: dict = field(default_factory=dict)

    def __init__(
        self,
        materials: list["Material"],
        static_params: "Material",
        data: pd.DataFrame | None = None,
        **settings,
    ):
        self.materials = materials
        self.static_params = static_params
        self.data = data
        self.settings = settings

    def get_unlocked_parameters(self) -> list["Parameter"]:
        """Returns a list of all unlocked parameters in the simulation."""
        return [
            par
            for mat in self.materials + [self.static_params]
            for par in mat.params
            if not par.locked
        ]

    def set_by_vector(self, vector: Sequence) -> None:
        """Sets the parameter values in the simulation by a vector of values.

        Args:
            vector (Sequence): The vector of values to set the parameters to. The vector should be the same length as the number of unlocked parameters in the simulation.
        """
        params = self.get_unlocked_parameters()
        for i, param in enumerate(params):
            param.value = vector[i] / param.factor

    def get_vector(self) -> np.ndarray:
        """Returns a vector of the values of the unlocked parameters in the simulation."""
        return np.array(
            [param.value * param.factor for param in self.get_unlocked_parameters()]
        )

    def get_bounds(self) -> tuple[np.ndarray, np.ndarray]:
        """Returns a tuple of the lower and upper bounds of the unlocked parameters in the simulation."""
        lower_bounds = np.array(
            [param.bounds[0] for param in self.get_unlocked_parameters()]
        )
        upper_bounds = np.array(
            [param.bounds[1] for param in self.get_unlocked_parameters()]
        )

        return lower_bounds, upper_bounds

    def to_dataframe(self) -> pd.DataFrame:
        """Returns a dataframe of the simulation parameters.

        The dataframe contains the material name, parameter name, locked status, and value of each parameter in the simulation.
        """
        data = []

        for material in self.materials + [self.static_params]:
            for param_name, param in material.get_param_dict().items():
                data.append([material.name, param_name, param.locked, param.value])

        df = pd.DataFrame(
            columns=["material", "parameter", "locked", "value"], data=data
        )
        return df

    def get_value_sim(self) -> SimulationValues:
        """Returns a SimulationValues object with the easy access values of the simulation."""
        materials = [mat.get_value_dict() for mat in self.materials]
        static_params = self.static_params.get_value_dict()
        return SimulationValues(
            materials, static_params, data=self.data, settings=self.settings
        )

    def optimize_sim(self) -> "SimulationModel":
        """Optimizes the simulation parameters to fit the data.

        The optimization algorithm fits the simulation results returned by the backend "simulate" function to the data provided by the user. The optimization is done using the scipy curve_fit function and takes the standard deviation of the y values (sy) into account.

        Args:
            df (pd.DataFrame): The dataframe containing the data to fit. This will be parsed to x, y, sx, sy values by the backend "parse_data" function.

        Returns:
            Simulation: A new optimized simulation object.
        """
        sim = copy.deepcopy(self)  # copy the mats so we don't change the original

        app = cast("NeutroApp", QApplication.instance())
        simulate = app.backend.simulate
        parse_data = app.backend.parse_data

        x_real, y_real, sx, sy = parse_data(self.data)

        def f(x_new, *params):
            sim.set_by_vector(params)
            simulation = simulate(sim)

            if simulation is None:
                raise ValueError(
                    "Simulation failed. Simulate should not return None in fitting. Check your backend."
                )

            return np.interp(x_new, simulation.x, simulation.y)

        init_guess = sim.get_vector()
        print("Initial guess:", init_guess, "\n")

        popt, pcov = curve_fit(
            f,
            x_real,
            y_real,
            p0=init_guess,
            sigma=sy,
            bounds=sim.get_bounds(),
        )

        print("\nOptimal:", popt)
        sim.set_by_vector(popt)

        return sim


class FittingWorker(QObject):
    """Worker class that hosts the fitting algorithm for a separate thread.

    The worker can be moved to a separate thread to avoid blocking the main thread while the fitting algorithm is running. The worker emits a signal when the fitting is finished.

    Attributes:
        resultReady (Signal): Signal emitted when the fitting is finished.
    """

    resultReady = Signal(SimulationModel)
    error = Signal(Exception)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)

    def doWork(self, sim: SimulationModel) -> None:
        """Runs the fitting algorithm and emits the result signal."""
        try:
            opt_sim = sim.optimize_sim()
            self.resultReady.emit(opt_sim)
        except Exception as e:
            print("Fitting error:", e)
            self.error.emit(e)


class FittingController(QObject):
    """Controller class for the threading of fitting.

    The controller hosts the worker and the worker thread. It emits a signal when the fitting is finished. It also ensures that only one fitting thread is running at a time and that the fitting thread is properly closed when the application is closed.

    Attributes:
        resultReady (Signal): Signal emitted when the fitting is finished.
    """

    _operate = Signal(SimulationModel)
    resultReady = Signal(SimulationModel)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.worker = FittingWorker()
        self.workerThread = QThread(self)
        self.worker.moveToThread(self.workerThread)
        self._operate.connect(self.worker.doWork)
        self.worker.resultReady.connect(self.onResultReady)
        self.worker.error.connect(self.display_error)

        # Closes the fitting thread when the application is closed to prevent internal errors
        app = cast("NeutroApp", QApplication.instance())
        app.aboutToQuit.connect(self.workerThread.quit)
        app.aboutToQuit.connect(self.workerThread.wait)

    def fit(self, sim: SimulationModel) -> None:
        """Starts the fitting algorithm in a separate thread.

        Starting a new fitting thread while another is running will be ignored.

        Args:
            sim (Simulation): The simulation object to optimize.
        """
        if self.workerThread.isRunning():
            error_dialog = QErrorMessage()
            error_dialog.showMessage("Fitting is already running")
            error_dialog.exec()
            return

        print("Fitting starting")
        self.workerThread.start()
        self._operate.emit(sim)

    def display_error(self, error: Exception) -> None:
        """Slot that receives an error signal and displays an error message."""
        error_dialog = QErrorMessage()
        error_dialog.showMessage(str(error))
        self.workerThread.quit()
        self.workerThread.wait()
        error_dialog.exec()

    def onResultReady(self, opt_sim: SimulationModel) -> None:
        """Slot that receives the fitting result and emits the result signal while closing the fitting thread."""
        self.workerThread.quit()
        self.workerThread.wait()
        self.resultReady.emit(opt_sim)
        print("Fitting finished")

    def deleteLater(self):
        """Closes the fitting thread when the controller is deleted."""
        self.workerThread.quit()
        self.workerThread.wait()
        return super().deleteLater()

from abc import ABC
from typing import Type
from itertools import chain
from copy import copy, deepcopy
from dataclasses import is_dataclass, asdict

import pandas as pd
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from PySide6.QtCore import QObject

from NeutroSpecUI.simulate import SimulationModel, SimulationResult, SimulationValues
from NeutroSpecUI.data_models import Parameter
from NeutroSpecUI.widgets.settings_dialog import SettingsDialog


class Backend(ABC):
    """A class to define the backend interface.

    This class defines the interface for the backend. A backend provides custom data parsing, simulation, plotting functions, etc. for the UI. The backend should implement the functions defined here to work with the UI.
    """

    @staticmethod
    def parse_data(df: pd.DataFrame) -> tuple:
        """Parses the data from the read in dataframe.

        The UI will read in a dataframe when the user selects a data file. This function will be called to parse the data to `x, y, sx, sy` (x values, y values, x errors, y errors). sx and sy can be None or left out if the data does not have errors.

        Args:
            df (pd.DataFrame): The dataframe containing the data to parse.

        Returns:
            tuple: A tuple containing the x, y, sx, sy values.
        """
        print(
            "No data parsing function implemented. Check your Backend to implement it."
        )
        return None, None, None, None

    @staticmethod
    def default_settings() -> dict:
        """Returns the default settings for the simulation.

        You can define specific settings in the UI which can then be used in the simulation. This function should return a dictionary with the default settings for the simulation.

        Returns:
            dict: A dictionary containing the default settings for the simulation.
        """
        print(
            "No default settings function implemented. Check your Backend to implement it."
        )
        return {}

    @staticmethod
    def simulate(sim: SimulationValues) -> SimulationResult | None:
        """Simulates the given simulation object.

        This function should simulate the given simulation object and return a `SimulationResult` object. If the simulation fails, this function should return `None`. It can use the `sim.settings` dictionary to get the settings for the simulation.

        Args:
            sim (SimulationValues): The simulation object to simulate.

        Returns:
            SimulationResult | None: The result of the simulation or None if the simulation failed.
        """
        print("No simulation function implemented. Check your Backend to implement it.")
        return None

    @staticmethod
    def create_fig_axes() -> tuple[Figure, list[Axes]]:
        """Creates a figure and axes for plotting.

        This function should create a matplotlib figure and axes for plotting the data and simulation results. It should return the figure and axes to plot on.

        Returns:
            Figure, Axes (tuple[Figure, Axes]): The figure and axes to plot on.
        """
        print(
            "No create fig axes function implemented. Check your Backend to implement it."
        )
        fig = Figure()
        axes = fig.subplots()
        return fig, [axes]

    @staticmethod
    def plot_sim(res: SimulationResult, axes: list[Axes], **kwargs) -> None:
        """Plots the simulation result.

        Args:
            res (SimulationResult): The simulation result to plot.
            axes (list[Axes]): The list of axes to plot on.
        """
        print(
            "No simulation plot function implemented. Check your Backend to implement it."
        )
        return

    @staticmethod
    def plot_fit(res: SimulationResult, axes: list[Axes], **kwargs) -> None:
        """Plots the simulation result.

        Args:
            res (SimulationResult): The simulation result to plot.
            axes (list[Axes]): The list of axes to plot on.
        """
        print(
            "No simulation plot function implemented. Check your Backend to implement it."
        )
        return

    @staticmethod
    def plot_data(df: pd.DataFrame, axes: list[Axes], **kwargs) -> None:
        """Plots the data from the dataframe.

        Args:
            df (pd.DataFrame): The dataframe containing the data to plot.
            axes (list[Axes]): The list of axes to plot on.
        """
        print("No data plot function implemented. Check your Backend to implement it.")
        return

    @staticmethod
    def material_options() -> dict[str, dict[str, str | list[Parameter]]]:
        """Returns a dictionary of materials for the backend.

        This function should return a dictionary of materials that can be used in the simulation. Each material can have a 'name' and a list of 'params' which are parameters for the material. The different materials can then be selected in the UI and added to each experiment as individual layers.

        Returns:
            dict[str, dict[str, str | list[Parameter]]]: Material options for the backend.
        """
        print(
            "No material options function implemented. Check your Backend to implement it."
        )
        return {}

    @staticmethod
    def static_params() -> list[Parameter]:
        """Returns a list of static parameters for the backend.

        This function should return a list of static parameters that can be used in the simulation. These parameters will be displayed at the top of each experiment and can be used to set global parameters for an experiment like a scale factor or background value.

        Returns:
            list[Parameter]: The list of static parameters.
        """
        print(
            "No static params function implemented. Check your Backend to implement it."
        )
        return []


class BackendHandler(QObject):
    """A class to handle the backend functions for the UI.

    This class uses the provided backend to call the functions needed for the UI to work. It is used to abstract the backend from the UI and make it easier to switch between backends.
    """

    _backend: Type[Backend]
    _settings: dict = {}

    def __init__(
        self, backend: Type[Backend] = Backend, parent: QObject | None = None
    ) -> None:
        super().__init__(parent)
        self.load_backend(backend)

    def load_backend(self, backend: Type[Backend]) -> None:
        self._backend = backend
        self._settings = self._backend.default_settings()

    def create_fig_axes(self) -> tuple[Figure, list[Axes]]:
        return self._backend.create_fig_axes()

    def plot_sim(self, res: SimulationResult, axes: list[Axes], **kwargs) -> None:
        return self._backend.plot_sim(res, axes, **kwargs)

    def plot_fit(self, res: SimulationResult, axes: list[Axes], **kwargs) -> None:
        return self._backend.plot_fit(res, axes, **kwargs)

    def plot_data(self, df: pd.DataFrame, axes: list[Axes], **kwargs) -> None:
        return self._backend.plot_data(df, axes, **kwargs)

    def parse_data(self, df: pd.DataFrame) -> tuple:
        data = self._backend.parse_data(df)
        if len(data) < 2:
            raise ValueError(
                "Data parsing failed. parse_data should return at least x and y values."
            )
        x, y, sx, sy, *_ = chain(data, [None, None])
        return x, y, sx, sy

    def get_settings(self) -> dict:
        return self._settings

    def set_settings(self, settings: dict):
        self._settings = settings

    def open_settings_dialog(self):
        new_settings = SettingsDialog.get_settings(self._settings)

        has_changed = new_settings != self._settings
        self._settings = new_settings

        return has_changed

    def simulate(self, sim: SimulationModel) -> SimulationResult | None:
        value_sim = sim.get_value_sim()
        value_sim.settings = self.get_settings()
        result = self._backend.simulate(value_sim)
        if result is None:
            return None
        result.extras.update(sim.settings)
        return result

    def material_options(self):
        return _parse_options(self._backend.material_options())

    def static_params(self):
        static_params = self._backend.static_params()
        return [deepcopy(param) for param in static_params]


def _parse_options(options: object):
    if is_dataclass(options):
        return asdict(options)  # type: ignore
    if isinstance(options, list):
        return [_parse_options(val) for val in options]
    if isinstance(options, dict):
        return {key: _parse_options(val) for key, val in options.items()}
    return copy(options)

import numpy as np
import pandas as pd

from matplotlib.figure import Figure

from NeutroSpecUI.data_models import Parameter
from NeutroSpecUI.backends import Backend
from NeutroSpecUI.backends.neutro import simulation, plot
from NeutroSpecUI.simulate import SimulationValues, SimulationResult


class NeutroBackend(Backend):
    @staticmethod
    def parse_data(df: pd.DataFrame):
        x_real = df["q"].values
        y_real = df["refl"].values
        sx = df["q_res (FWHM)"].values
        sy = df["refl_err"].values

        return x_real, y_real, sx, sy

    @staticmethod
    def default_settings():
        return {
            "z_axis_lim": None,
            "z_axis_factor": 1.25,
            "q_axis_lim": None,
            "delta_q": 0.001,
            "delta_z": 0.5,
            "start_roughness": 0.1,
        }

    @staticmethod
    def simulate(sim: SimulationValues):
        # We need at least one material and the fluid
        if len(sim.materials) < 2:
            return None

        # Get settings like q_axis_lim, z_axis_lim
        settings = simulation.get_settings(sim.settings, sim.materials, sim.data)

        # Create axes (avoid q=0)
        z_axis = np.arange(
            settings["z_axis_lim"][0],
            settings["z_axis_lim"][1] + settings["delta_z"],
            step=settings["delta_z"],
        )
        q_axis = np.arange(
            settings["q_axis_lim"][0],
            settings["q_axis_lim"][1],
            step=settings["delta_q"],
        )[1:]

        # Get the index of the fluid material
        fluid_index = int(sim.static_params["fluid_index"])
        if fluid_index <= -len(sim.materials) or fluid_index >= len(sim.materials):
            raise IndexError("Fluid index out of bounds")
        elif fluid_index < 0:
            fluid_index = len(sim.materials) + fluid_index

        # Create fractions with fluid
        fractions = simulation.get_fractions(
            sim.materials,
            z_axis,
            fluid_index=fluid_index,
            start_roughness=sim.settings["start_roughness"],
        )

        rhos = np.array([mat["SLD"] for mat in sim.materials])
        sld = np.sum(fractions * rhos, axis=1)

        reflectivity = simulation.convolution_refl(
            sld, q_axis, delta_z=settings["delta_z"]
        )

        y = reflectivity * sim.static_params["scale"] + sim.static_params["background"]

        return SimulationResult(
            x=q_axis,
            y=y,
            fractions=fractions,
            SLD=sld,
            z_axis=z_axis,
            materials=sim.materials,
            **settings,
        )

    @staticmethod
    def create_fig_axes():
        fig = Figure(figsize=(5, 4), dpi=100)
        axes = [fig.add_subplot(1, 3, i) for i in range(1, 4)]
        return fig, axes

    @staticmethod
    def plot_data(df: pd.DataFrame, axes, **kwargs):
        plot.plot_reflectivity_data(df, ax=axes[2], **kwargs)

    @staticmethod
    def plot_sim(res: SimulationResult, axes, **kwargs):
        plot.plot_volume_fraction(res, ax=axes[0], **kwargs)
        plot.plot_sld(res, ax=axes[1], color="red", label="Sim", **kwargs)
        plot.plot_reflectivity(res, ax=axes[2], color="red", label="Sim", **kwargs)

    @staticmethod
    def plot_fit(res: SimulationResult, axes, **kwargs):
        plot.plot_volume_fraction(res, ax=axes[0], **kwargs)
        plot.plot_sld(res, ax=axes[1], color="green", label="Fit", **kwargs)
        plot.plot_reflectivity(res, ax=axes[2], color="green", label="Fit", **kwargs)

    @staticmethod
    def material_options():
        return {
            "Material": {
                "name": "Material",
                "params": [
                    Parameter(1, name="thickness", bounds=(0, 50)),
                    Parameter(
                        100,
                        name="fraction",
                        bounds=(0, 1),
                        locked=True,
                        unit="%",
                        factor=0.01,
                    ),
                    Parameter(1, name="roughness", bounds=(0, 20)),
                    Parameter(
                        1,
                        name="SLD",
                        bounds=(-1e-5, 1e-5),
                        unit="1e-6 \u00c5\u207b\u00b3",
                        factor=1e-6,
                    ),
                ],
            },
        }

    @staticmethod
    def static_params():
        return [
            Parameter(-1, name="fluid_index", locked=True),
            Parameter(1, name="scale", bounds=(0, 10)),
            Parameter(
                0, name="background", bounds=(0, 1), unit="1e-6 Å⁻³", factor=1e-6
            ),
        ]

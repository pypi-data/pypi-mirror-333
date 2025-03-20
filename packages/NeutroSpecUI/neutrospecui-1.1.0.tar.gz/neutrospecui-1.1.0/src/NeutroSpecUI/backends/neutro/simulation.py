import numpy as np
import pandas as pd
from scipy import special


def get_fractions(
    materials: list[dict[str, float]],
    z_axis: np.ndarray,
    fluid_index: int = -1,
    start_roughness: float = 0.1,
) -> np.ndarray:
    if not materials:
        raise ValueError("The materials list is empty")

    sigmas = np.array([start_roughness] + [mat["roughness"] for mat in materials])
    thicknesses = np.array([mat["thickness"] for mat in materials])
    fractions: np.typing.NDArray[np.float64] = np.array(
        [mat["fraction"] for mat in materials]
    )
    # Start positions from -thickness of first material
    positions = np.cumsum(
        [-materials[0]["thickness"]] + [mat["thickness"] for mat in materials][:-1]
    )

    # Calculate the start and stop of each material
    start: np.typing.NDArray[np.float64] = z_axis[:, np.newaxis] - positions
    stop: np.typing.NDArray[np.float64] = start - thicknesses

    # Calculate the volume of each material (step function)
    sigmas_scaled = sigmas * np.sqrt(2)
    step_ups = special.erf(start / sigmas_scaled[:-1])
    step_downs = special.erf(stop / sigmas_scaled[1:])

    # Make sure first / last material have no step up / down
    step_ups[:, 0] = 1
    step_downs[:, -1] = -1

    # Combine step up and step down to get the volume of each material
    volume: np.typing.NDArray[np.float64] = (step_ups - step_downs) / 2

    # Scale the fractions to the volume (make fluid space filling)
    scaled_fractions = fractions * volume
    solid_fractions = np.delete(scaled_fractions, fluid_index, axis=1)
    scaled_fractions[:, fluid_index] = 1 - np.sum(solid_fractions, axis=1)

    return scaled_fractions


def convolution(qs, q, delta_q_axis):
    width = delta_q_axis / (2 * np.sqrt(2 * np.log(2)))
    return np.exp(-((qs - q) ** 2) / (2.0 * width**2))


def convolution_refl(
    rho: np.ndarray,
    q_axis: np.ndarray,
    delta_z: float = 1,
    mult: int = 1,  # why did we multipy with 3?
):
    delta_qz = q_axis[1] - q_axis[0]
    n_qs = mult * len(q_axis)
    qs = q_axis[0] * (q_axis[-1] / q_axis[0]) ** np.linspace(0, 1, n_qs)

    refl = np.array([get_reflectivity(q, rho, delta_z) for q in qs])

    convolved_reflectivity = np.zeros_like(q_axis)
    for i in range(len(q_axis)):
        indices = np.where(np.abs(qs - q_axis[i]) <= 4 * delta_qz)[0]
        weights = convolution(qs[indices], q_axis[i], 2 * delta_qz)
        factors = weights / np.sum(weights)
        convolved_reflectivity[i] = np.sum(np.real_if_close(refl[indices] * factors))

    return convolved_reflectivity


def get_reflectivity(q: int, rho: np.ndarray, delta_z: float) -> np.float64:
    ci = complex(0, 1)
    c1 = complex(1, 0)
    c0 = complex(0, 0)
    k0 = complex(q / 2)

    # q_z = 4 * pi / lambda * sin(theta_i)
    k = np.sqrt(k0**2 - 4 * np.pi * (rho - rho[0]))

    rfres = (k[:-1] - k[1:]) / (k[:-1] + k[1:])

    # why dont we use hphase?
    # hphase = np.exp(ci * k[1:] * d)
    fphase = np.exp(2 * ci * k[1:] * delta_z)

    rp = np.zeros(len(rho), dtype=np.complex128)
    rp[-1] = c0
    rp[-2] = rfres[-1]
    for i2 in range(len(rho) - 3, -1, -1):
        rp[i2] = (rfres[i2] + rp[i2 + 1] * fphase[i2]) / (
            c1 + rfres[i2] * rp[i2 + 1] * fphase[i2]
        )

    reflectivity: np.float64 = np.abs(rp[0]) ** 2
    return reflectivity


def get_settings(settings: dict, materials: list[dict], data: pd.DataFrame) -> dict:
    if settings.get("q_axis_lim"):
        # if manually set, use that
        q_axis_lim = settings["q_axis_lim"]
    else:
        if data is None:
            # if no data, use default
            q_axis_lim = (0, 0.3)
        else:
            # if data, use min and max of q
            q_min = data["q"].min() / 1.25
            q_max = data["q"].max() * 1.25
            q_axis_lim = (q_min, q_max)

    if q_axis_lim[0] < 0 or q_axis_lim[1] < q_axis_lim[0]:
        raise ValueError("qz start should not be negative or smaller than the qz stop")

    if settings.get("z_axis_lim"):
        # if manually set, use that
        z_axis_lim = settings["z_axis_lim"]
    elif len(materials) == 0:
        # if no materials, use default
        z_axis_lim = (0, 1)
    elif len(materials) == 1:
        # if one material, use thickness and roughness
        start_roughness = materials[0]["roughness"] * 2 * np.sqrt(2)
        z_axis_lim = (0, materials[0]["thickness"] + start_roughness)
    else:
        # if more than one material, use total thickness and roughness
        total_width = sum(mat["thickness"] for mat in materials[1:-1])
        start_roughness = materials[0]["roughness"] * 2 * np.sqrt(2)
        end_roughness = materials[-2]["roughness"] * 2 * np.sqrt(2)
        z_axis_lim = (-start_roughness, total_width + end_roughness)

    return {
        **settings,
        "z_axis_lim": z_axis_lim,
        "q_axis_lim": q_axis_lim,
    }

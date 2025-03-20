#!/usr/bin/env python3

import argparse
import math
import typing as t
from collections.abc import Iterable
from collections.abc import Sequence
from functools import lru_cache
from pathlib import Path

import matplotlib.axes as mplax
import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
import pandas as pd

import artistools as at

H = 6.6260755e-27  # Planck constant [erg s]
KB = 1.38064852e-16  # Boltzmann constant [erg/K]
EV = 1.6021772e-12  # eV to ergs [eV/erg]
ONEOVERH = 1.509188961e26
HOVERKB = 4.799243681748932e-11
TWOOVERCLIGHTSQUARED = 2.2253001e-21
SAHACONST = 2.0706659e-16
MEGAPARSEC = 3.0857e24


@lru_cache(maxsize=4)
def read_files(modelpath: Path | str, timestep: int | None = None, modelgridindex: int | None = None):
    """Read radiation field data from a list of file paths into a pandas DataFrame."""
    radfielddata_allfiles: list[pd.DataFrame] = []
    modelpath = Path(modelpath)

    mpiranklist = at.get_mpiranklist(modelpath, modelgridindex=modelgridindex)
    for folderpath in at.get_runfolders(modelpath, timestep=timestep):
        for mpirank in mpiranklist:
            radfieldfilename = f"radfield_{mpirank:04d}.out"
            radfieldfilepath = Path(folderpath, radfieldfilename)
            radfieldfilepath = at.firstexisting(radfieldfilename, folder=folderpath, tryzipped=True)

            if modelgridindex is not None:
                filesize = Path(radfieldfilepath).stat().st_size / 1024 / 1024
                print(f"Reading {Path(radfieldfilepath).relative_to(modelpath.parent)} ({filesize:.2f} MiB)")

            radfielddata_thisfile = pd.read_csv(radfieldfilepath, sep=r"\s+")
            # radfielddata_thisfile[['modelgridindex', 'timestep']].apply(pd.to_numeric)

            if timestep is not None:
                radfielddata_thisfile = radfielddata_thisfile.query("timestep==@timestep")

            if modelgridindex is not None:
                radfielddata_thisfile = radfielddata_thisfile.query("modelgridindex==@modelgridindex")

            if not radfielddata_thisfile.empty:
                if timestep is not None and modelgridindex is not None:
                    return radfielddata_thisfile
                radfielddata_allfiles.append(radfielddata_thisfile)

    return pd.concat(radfielddata_allfiles, ignore_index=True)


def select_bin(radfielddata, nu=None, lambda_angstroms=None, modelgridindex=None, timestep=None):
    assert nu is None or lambda_angstroms is None

    if lambda_angstroms is not None:
        nu = 2.99792458e18 / lambda_angstroms
    else:
        assert nu is not None
        lambda_angstroms = 2.99792458e18 / nu

    dfselected = radfielddata.query(
        ("modelgridindex == @modelgridindex and " if modelgridindex else "")
        + ("timestep == @timestep and " if timestep else "")
        + "nu_lower <= @nu and nu_upper >= @nu and bin_num > -1"
    )

    assert not dfselected.empty
    return dfselected.iloc[0].bin_num, dfselected.iloc[0].nu_lower, dfselected.iloc[0].nu_upper


def get_binaverage_field(radfielddata, modelgridindex=None, timestep=None):
    """Get the dJ/dlambda constant average estimators of each bin."""
    # exclude the global fit parameters and detailed lines with negative "bin_num"
    bindata = radfielddata.copy().query(
        "bin_num >= 0"
        + (" & modelgridindex==@modelgridindex" if modelgridindex else "")
        + (" & timestep==@timestep" if timestep else "")
    )

    arr_lambda = 2.99792458e18 / bindata["nu_upper"].to_numpy()

    bindata["dlambda"] = bindata.apply(lambda row: 2.99792458e18 * (1 / row["nu_lower"] - 1 / row["nu_upper"]), axis=1)

    yvalues = bindata.apply(
        lambda row: (
            row["J"] / row["dlambda"] if (not math.isnan(row["J"] / row["dlambda"]) and row["T_R"] >= 0) else 0.0
        ),
        axis=1,
    ).to_numpy()

    # add the starting point
    arr_lambda = np.insert(arr_lambda, 0, 2.99792458e18 / bindata["nu_lower"].iloc[0])
    yvalues = np.insert(yvalues, 0, 0.0)

    return arr_lambda, yvalues


def j_nu_dbb(arr_nu_hz: Sequence[float] | npt.NDArray, W: float, T: float) -> list[float]:
    """Calculate the spectral energy density of a dilute blackbody radiation field.

    Parameters
    ----------
    arr_nu_hz : list
        A list of frequencies (in Hz) at which to calculate the spectral energy density.
    W : float
        The dilution factor of the blackbody radiation field.
    T : float
        The temperature of the blackbody radiation field (in Kelvin).

    Returns
    -------
    list
        A list of spectral energy density values (in CGS units) corresponding to the input frequencies.

    """
    if W > 0.0:
        try:
            return [W * 1.4745007e-47 * pow(nu_hz, 3) * 1.0 / (math.expm1(H * nu_hz / T / KB)) for nu_hz in arr_nu_hz]
        except OverflowError:
            print(f"WARNING: overflow error W {W}, T {T} (Did this happen in ARTIS too?)")

    return [0.0 for _ in arr_nu_hz]


def get_fullspecfittedfield(radfielddata, xmin, xmax, modelgridindex: int | None = None, timestep: int | None = None):
    row = (
        radfielddata.query(
            "bin_num == -1"
            + (" & modelgridindex==@modelgridindex" if modelgridindex else "")
            + (" & timestep==@timestep" if timestep else "")
        )
        .copy()
        .iloc[0]
    )
    nu_lower = 2.99792458e18 / xmin
    nu_upper = 2.99792458e18 / xmax
    arr_nu_hz = np.linspace(nu_lower, nu_upper, num=500)
    arr_j_nu = j_nu_dbb(arr_nu_hz, row["W"], row["T_R"])

    arr_lambda = 2.99792458e18 / arr_nu_hz
    arr_j_lambda = arr_j_nu * arr_nu_hz / arr_lambda

    return arr_lambda, arr_j_lambda


def get_fitted_field(
    radfielddata,
    modelgridindex: int | None = None,
    timestep: int | None = None,
    print_bins: bool = False,
    lambdamin: float | None = None,
    lambdamax: float | None = None,
) -> tuple[list[float], list[float]]:
    """Return the fitted dilute blackbody (list of lambda, list of j_nu) made up of all bins."""
    arr_lambda = []
    j_lambda_fitted = []

    radfielddata_subset = radfielddata.copy().query(
        "bin_num >= 0"
        + (" & modelgridindex==@modelgridindex" if modelgridindex else "")
        + (" & timestep==@timestep" if timestep else "")
    )

    if lambdamax is not None:
        nu_min = 2.99792458e18 / lambdamax

    if lambdamin is not None:
        nu_max = 2.99792458e18 / lambdamin

    for _, row in radfielddata_subset.iterrows():
        nu_lower = row["nu_lower"]
        nu_upper = row["nu_upper"]

        if lambdamax is not None:
            if nu_upper > nu_max:
                continue
            nu_lower = max(nu_lower, nu_min)
        if lambdamin is not None:
            if nu_lower < nu_min:
                continue
            nu_upper = min(nu_upper, nu_max)

        if row["W"] >= 0:
            arr_nu_hz_bin = np.linspace(nu_lower, nu_upper, num=200)
            arr_j_nu = j_nu_dbb(arr_nu_hz_bin, row["W"], row["T_R"])

            arr_lambda_bin = 2.99792458e18 / arr_nu_hz_bin
            arr_j_lambda_bin = arr_j_nu * arr_nu_hz_bin / arr_lambda_bin

            arr_lambda += list(arr_lambda_bin)
            j_lambda_fitted += list(arr_j_lambda_bin)
        else:
            arr_nu_hz_bin = [nu_lower, nu_upper]
            arr_j_lambda_bin = [0.0, 0.0]

            arr_lambda += [2.99792458e18 / nu for nu in arr_nu_hz_bin]
            j_lambda_fitted += arr_j_lambda_bin

        lambda_lower = 2.99792458e18 / row["nu_upper"]
        lambda_upper = 2.99792458e18 / row["nu_lower"]
        if (
            print_bins
            and (lambdamax is None or lambda_lower < lambdamax)
            and (lambdamin is None or lambda_upper > lambdamin)
        ):
            print(
                f"Bin lambda_lower {lambda_lower:.1f} W {row['W']:.1e} "
                f"contribs {row['ncontrib']} J_nu_avg {row['J_nu_avg']:.1e}"
            )

    return arr_lambda, j_lambda_fitted


def plot_line_estimators(axis, radfielddata, modelgridindex=None, timestep=None, **plotkwargs):
    """Plot the Jblue_lu values from the detailed line estimators on a spectrum."""
    ymax = -1

    radfielddataselected = radfielddata.query(
        "bin_num < -1"
        + (" & modelgridindex==@modelgridindex" if modelgridindex else "")
        + (" & timestep==@timestep" if timestep else "")
    )[["nu_upper", "J_nu_avg"]]

    radfielddataselected["lambda_angstroms"] = 2.99792458e18 / radfielddataselected["nu_upper"]
    radfielddataselected["Jb_lambda"] = (
        radfielddataselected["J_nu_avg"] * (radfielddataselected["nu_upper"] ** 2) / 2.99792458e18
    )

    ymax = radfielddataselected["Jb_lambda"].max()

    if not radfielddataselected.empty:
        axis.scatter(
            radfielddataselected["lambda_angstroms"],
            radfielddataselected["Jb_lambda"],
            label="Line estimators",
            s=0.2,
            **plotkwargs,
        )

    return ymax


def plot_specout(
    axis: mplax.Axes,
    specfilename: str | Path,
    timestep: int,
    peak_value: float | None = None,
    scale_factor: float | None = None,
    **plotkwargs,
) -> None:
    """Plot the ARTIS spectrum."""
    print(f"Plotting {specfilename}")

    specfilename = Path(specfilename)
    if specfilename.is_dir():
        modelpath = specfilename
    elif specfilename.is_file():
        modelpath = Path(specfilename).parent

    dfspectrum = at.spectra.get_spectrum(modelpath=modelpath, timestepmin=timestep)[-1].to_pandas(
        use_pyarrow_extension_array=True
    )
    label = "Emergent spectrum"
    if scale_factor is not None:
        label += " (scaled)"
        dfspectrum["f_lambda"] *= scale_factor

    if peak_value is not None:
        label += " (normalised)"
        dfspectrum["f_lambda"] = dfspectrum["f_lambda"] / dfspectrum["f_lambda"].max() * peak_value

    dfspectrum.plot(x="lambda_angstroms", y="f_lambda", ax=axis, label=label, **plotkwargs)


@lru_cache(maxsize=128)
def evaluate_phixs(
    modelpath: Path | str, lowerlevelindex: int, nu_threshold: float, arr_nu_hz: Iterable[float] | npt.NDArray
) -> npt.NDArray:
    adata = at.atomic.get_levels(modelpath, get_photoionisations=True)
    lower_ion_data = adata.query("Z == @atomic_number and ion_stage == @lower_ion_stage").iloc[0]
    lowerlevel = lower_ion_data.levels.iloc[lowerlevelindex]

    from scipy.interpolate import interp1d

    phixstable = lowerlevel.phixstable
    interp_sigma_bf = interp1d(
        phixstable[:, 0] * nu_threshold,
        phixstable[:, 1],
        kind="linear",
        bounds_error=True,
        fill_value=0.0,
        assume_sorted=True,
    )

    def sigma_bf(nu):
        nu_factor = nu / nu_threshold
        if nu_factor < phixstable[0, 0]:
            return 0.0
        if nu_factor > phixstable[-1, 0]:
            # return 0.
            return phixstable[-1, 1] * math.pow(phixstable[-1, 0] / nu_factor, 3)

        # return interp(nu_factor, phixstable[:, 0], phixstable[:, 1], left=0.)
        return interp_sigma_bf(nu)

    return np.array([sigma_bf(nu) for nu in arr_nu_hz])


def get_kappa_bf_ion(
    atomic_number: int,
    lower_ion_stage: int,
    modelgridindex: int,
    timestep: int,
    modelpath: Path | str,
    arr_nu_hz: Iterable[float] | npt.NDArray,
    max_levels: int,
) -> npt.NDArray:
    adata = at.atomic.get_levels(modelpath, get_photoionisations=True)
    estimators = at.estimators.read_estimators(modelpath, timestep=timestep, modelgridindex=modelgridindex)
    T_e = estimators[timestep, modelgridindex]["Te"]

    ion_data = adata.query("Z == @atomic_number and ion_stage == @lower_ion_stage").iloc[0]
    upper_ion_data = adata.query("Z == @atomic_number and ion_stage == (@lower_ion_stage + 1)").iloc[0]

    ionstr = at.get_ionstring(atomic_number, lower_ion_stage, sep="_", style="spectral")
    lowerionpopdensity = estimators[timestep, modelgridindex][f"nnion_{ionstr}"]

    ion_popfactor_sum = sum(
        level.g * math.exp(-level.energy_ev * EV / KB / T_e) for _, level in ion_data.levels[:max_levels].iterrows()
    )
    array_kappa_bf_nu_ion: npt.NDArray = np.zeros_like(arr_nu_hz)
    for levelnum, lowerlevel in ion_data.levels[:max_levels].iterrows():
        levelpopfrac = lowerlevel.g * math.exp(-lowerlevel.energy_ev * EV / KB / T_e) / ion_popfactor_sum

        for upperlevelnum, phixsfrac in lowerlevel.phixstargetlist:
            upperlevel = upper_ion_data.levels.iloc[upperlevelnum]

            nu_threshold = ONEOVERH * (ion_data.ion_pot - lowerlevel.energy_ev + upperlevel.energy_ev) * EV

            arr_sigma_bf = evaluate_phixs(modelpath, levelnum, nu_threshold, tuple(arr_nu_hz)) * phixsfrac

            array_kappa_bf_nu_ion += arr_sigma_bf * levelpopfrac * lowerionpopdensity

    return array_kappa_bf_nu_ion


def get_recombination_emission(
    atomic_number: int,
    upper_ion_stage: int,
    arr_nu_hz,
    modelgridindex: int,
    timestep: int,
    modelpath: Path | str,
    max_levels: int,
    use_lte_pops: bool = False,
):
    from scipy import integrate

    adata = at.atomic.get_levels(modelpath, get_photoionisations=True)

    lower_ion_stage = upper_ion_stage - 1
    upperionstr = at.get_ionstring(atomic_number, upper_ion_stage)
    lowerionstr = at.get_ionstring(atomic_number, lower_ion_stage)
    upper_ion_data = adata.query("Z == @atomic_number and ion_stage == @upper_ion_stage").iloc[0]
    lower_ion_data = adata.query("Z == @atomic_number and ion_stage == @lower_ion_stage").iloc[0]

    estimtsmgi = at.estimators.read_estimators(modelpath, timestep=timestep, modelgridindex=modelgridindex)[
        timestep, modelgridindex
    ]

    upperionstr = at.get_ionstring(atomic_number, upper_ion_stage, sep="_", style="spectral")
    upperionpopdensity = estimtsmgi[f"nnion_{upperionstr}"]

    T_e = estimtsmgi["Te"]
    nne = estimtsmgi["nne"]

    print(f"Recombination from {upperionstr} -> {lowerionstr} ({upperionstr} pop = {upperionpopdensity:.1e}/cm3)")

    if use_lte_pops:
        upper_level_popfactor_sum = sum(
            upperlevel.g * math.exp(-upperlevel.energy_ev * EV / KB / T_e)
            for _upperlevelnum, upperlevel in lower_ion_data.levels[:200].iterrows()
        )
    else:
        dfnltepops = at.nltepops.read_files(modelpath, modelgridindex=modelgridindex, timestep=timestep)
        dfnltepops_upperion = dfnltepops.query("Z==@atomic_number & ion_stage==@upper_ion_stage")
        upperion_nltepops = {x.level: x["n_NLTE"] for _, x in dfnltepops_upperion.iterrows()}

    arr_j_nu_lowerlevel = {}
    arr_alpha_dnu = np.zeros_like(arr_nu_hz)
    alpha_ion2 = 0.0
    nnionfrac = 0.0
    for levelnum, lowerlevel in lower_ion_data.levels[:max_levels].iterrows():
        for upperlevelnum, phixsfrac in lowerlevel.phixstargetlist:
            upperlevel = upper_ion_data.levels.iloc[upperlevelnum]

            if use_lte_pops:
                levelpopfrac = (
                    upperlevel.g * math.exp(-upperlevel.energy_ev * EV / KB / T_e) / upper_level_popfactor_sum
                )
            elif len(upperion_nltepops) == 1:  # top ion has only one level
                levelpopfrac = upperion_nltepops[0] / upperionpopdensity
            else:
                levelpopfrac = upperion_nltepops[upperlevelnum] / upperionpopdensity

            nu_threshold = ONEOVERH * (lower_ion_data.ion_pot - lowerlevel.energy_ev + upperlevel.energy_ev) * EV

            arr_sigma_bf = (
                evaluate_phixs(modelpath, atomic_number, lower_ion_stage, levelnum, nu_threshold, tuple(arr_nu_hz))
                * phixsfrac
            )

            sfac = (
                SAHACONST * lowerlevel.g / upperlevel.g * math.pow(T_e, -1.5) * math.exp(HOVERKB * nu_threshold / T_e)
            )

            arr_alpha_level_dnu = (
                4.0
                * math.pi
                * sfac
                * (TWOOVERCLIGHTSQUARED * arr_sigma_bf * np.power(arr_nu_hz, 2) * np.exp(-HOVERKB * arr_nu_hz / T_e))
                * levelpopfrac
            )

            arr_j_nu_lowerlevel[upperlevelnum, levelnum] = (
                arr_alpha_level_dnu / 4 / math.pi * H * arr_nu_hz * upperionpopdensity * nne
            )

            arr_alpha_dnu += arr_alpha_level_dnu

            nnionfrac += levelpopfrac

            # arr_nu_hz2 = nu_threshold * lowerlevel.phixstable[:, 0]
            arr_nu_hz2 = nu_threshold * np.linspace(1.0, 1.0 + 0.03 * (100 + 1), num=3 * 100 + 1, endpoint=False)
            arr_sigma_bf2 = (
                evaluate_phixs(modelpath, atomic_number, lower_ion_stage, levelnum, nu_threshold, tuple(arr_nu_hz2))
                * phixsfrac
            )
            arr_alpha_level_dnu2 = (
                4.0
                * math.pi
                * sfac
                * (TWOOVERCLIGHTSQUARED * arr_sigma_bf2 * np.power(arr_nu_hz2, 2) * np.exp(-HOVERKB * arr_nu_hz2 / T_e))
                * levelpopfrac
            )
            alpha_level2 = np.abs(integrate.trapezoid(arr_alpha_level_dnu2, x=arr_nu_hz2))
            alpha_ion2 += alpha_level2

            # alpha_level = np.abs(integrate.trapezoid(arr_alpha_level_dnu, x=arr_nu_hz))
            lambda_threshold = 2.99792458e18 / nu_threshold
            print(
                f" {upperionstr} level {upperlevelnum} -> {lowerionstr} level {levelnum}"
                f" threshold {lambda_threshold:7.1f} Å"
                f" Alpha_R_contrib {alpha_level2:.2e} {lowerlevel.levelname}"
                f" upperlevelpop {upperion_nltepops[upperlevelnum]:.2e}"
            )

    alpha_ion = np.abs(integrate.trapezoid(arr_alpha_dnu, x=arr_nu_hz))
    print(f"  {upperionstr} Alpha_R = {alpha_ion:.2e}   Alpha_R*nne = {nne * alpha_ion:.2e}")
    print(f"  {upperionstr} Alpha_R2 = {alpha_ion2:.2e} Alpha_R2*nne = {nne * alpha_ion2:.2e}")

    # vmax = at.inputmodel.get_modeldata_tuple(modelpath)[0]['vel_r_max_kmps'].iloc[-1] * 1e5
    # t_seconds = at.get_timestep_times(modelpath, loc="start")[timestep] * 86400.0

    # mean_free_path = vmax * t_seconds

    arr_j_nu = arr_alpha_dnu / 4 / math.pi * H * arr_nu_hz * upperionpopdensity * nne
    return arr_j_nu, arr_j_nu_lowerlevel


def get_ion_gamma_dnu(modelpath, modelgridindex, timestep, atomic_number, ion_stage, arr_nu_hz, J_nu_arr, max_levels):
    """Calculate the contribution to the photoionisation rate coefficient per J_nu at each frequency nu for an ion."""
    from scipy import integrate

    estimators = at.estimators.read_estimators(modelpath, timestep=timestep, modelgridindex=modelgridindex)

    T_e = estimators[timestep, modelgridindex]["Te"]
    T_R = estimators[timestep, modelgridindex]["TR"]

    adata = at.atomic.get_levels(modelpath, get_photoionisations=True)
    ion_data = adata.query("Z == @atomic_number and ion_stage == @ion_stage").iloc[0]
    upper_ion_data = adata.query("Z == @atomic_number and ion_stage == (@ion_stage + 1)").iloc[0]
    ionstr = at.get_ionstring(atomic_number, ion_stage)

    ion_popfactor_sum = sum(
        level.g * math.exp(-level.energy_ev * EV / KB / T_e) for _, level in ion_data.levels[:max_levels].iterrows()
    )
    arr_gamma_dnu = np.zeros_like(arr_nu_hz)
    for levelnum, level in ion_data.levels[:max_levels].iterrows():
        levelpopfrac = level.g * math.exp(-level.energy_ev * EV / KB / T_e) / ion_popfactor_sum

        for upperlevelnum, phixsfrac in level.phixstargetlist:
            upperlevel = upper_ion_data.levels.iloc[upperlevelnum]
            nu_threshold = ONEOVERH * (ion_data.ion_pot - level.energy_ev + upperlevel.energy_ev) * EV

            arr_sigma_bf = (
                evaluate_phixs(modelpath, atomic_number, ion_stage, levelnum, nu_threshold, tuple(arr_nu_hz))
                * phixsfrac
            )

            arr_corrfactors = 1 - np.exp(-HOVERKB * arr_nu_hz / T_R)
            assert min(arr_corrfactors) > 0.50
            assert max(arr_corrfactors) <= 1.0

            arr_gamma_level_dnu = (
                4 * math.pi * ONEOVERH * arr_sigma_bf / arr_nu_hz * J_nu_arr * arr_corrfactors * levelpopfrac
            )

            arr_gamma_dnu += arr_gamma_level_dnu

            gamma_r_level = np.abs(integrate.trapezoid(arr_gamma_level_dnu, x=arr_nu_hz))
            lambda_threshold = 2.99792458e18 / nu_threshold

            print(
                f"  level {levelnum} pop_frac {levelpopfrac:.2f} upperlevel {upperlevelnum}"
                f" threshold {lambda_threshold:.1f} Å "
                f" gamma_R_level({ionstr}) {gamma_r_level:.2e} {level.levelname}"
            )

    return arr_gamma_dnu


def calculate_photoionrates(axes, modelpath, radfielddata, modelgridindex, timestep, xmin, xmax, ymax):
    from scipy import integrate

    axes[0].set_ylabel(r"$\sigma$ [cm$^2$]")

    # recomblowerionlist = ((26, 1), (26, 2), (26, 3), (26, 4), (27, 2), (27, 3), (28, 2), (28, 3), (28, 4))
    # photoionlist = ((26, 2), (28, 2))

    recomblowerionlist = ((26, 3),)
    photoionlist = ((26, 2),)
    kappalowerionlist = ((26, 2), (26, 3))
    adata = at.atomic.get_levels(modelpath, get_photoionisations=True)

    fieldlist = []

    arr_lambda_fitted, j_lambda_fitted = get_fitted_field(
        radfielddata, modelgridindex=modelgridindex, timestep=timestep, print_bins=True, lambdamin=xmin, lambdamax=xmax
    )

    arr_lambda_fitted, j_lambda_fitted = (
        list(lst)
        for lst in zip(
            *[pt for pt in zip(arr_lambda_fitted, j_lambda_fitted, strict=False) if xmin <= pt[0] <= xmax], strict=False
        )
    )

    estimators = at.estimators.read_estimators(modelpath, timestep=timestep, modelgridindex=modelgridindex)

    max_levels = 20

    T_e = estimators[timestep, modelgridindex]["Te"]
    nne = estimators[timestep, modelgridindex]["nne"]
    print(f"T_e {T_e:.1f} K, nne {nne:.1e} /cm3")

    arraylambda_angstrom_recomb = np.linspace(xmin, xmax, num=10000)
    arr_nu_hz_recomb = 2.99792458e18 / np.array(arraylambda_angstrom_recomb)

    # calculate bound-free opacity
    array_kappa_bf_nu = np.zeros_like(arr_nu_hz_recomb)
    for atomic_number, lower_ion_stage in kappalowerionlist:
        array_kappa_bf_nu += get_kappa_bf_ion(
            atomic_number, lower_ion_stage, modelgridindex, timestep, modelpath, arr_nu_hz_recomb, max_levels
        )

    # calculate recombination emission
    J_lambda_recomb_total = np.zeros_like(arraylambda_angstrom_recomb)

    lw = 1.0
    for atomic_number, lower_ion_stage in recomblowerionlist:
        # lw -= 0.1
        upperionstr = at.get_ionstring(atomic_number, lower_ion_stage + 1)

        j_emiss_nu_recomb, arr_j_nu_lowerleveldict = get_recombination_emission(
            atomic_number, lower_ion_stage + 1, arr_nu_hz_recomb, modelgridindex, timestep, modelpath, max_levels
        )

        for (upperlevelnum, lowerlevelnum), arr_j_emiss_nu_lowerlevel in arr_j_nu_lowerleveldict.items():
            J_nu_recomb = np.array([
                j_emiss_nu / kappa_bf if j_emiss_nu > 0 else 0.0
                for j_emiss_nu, kappa_bf in zip(arr_j_emiss_nu_lowerlevel, array_kappa_bf_nu, strict=False)
            ])

            J_contrib = np.abs(integrate.trapezoid(J_nu_recomb, x=arr_nu_hz_recomb))

            J_lambda_recomb_level = J_nu_recomb * arr_nu_hz_recomb / arraylambda_angstrom_recomb
            fieldlabel = (
                f"{upperionstr} level {upperlevelnum} -> {at.roman_numerals[lower_ion_stage]} level {lowerlevelnum}"
            )
            axes[2].plot(arraylambda_angstrom_recomb, J_lambda_recomb_level, label=fieldlabel, lw=lw)
            fieldlist += [(arraylambda_angstrom_recomb, J_lambda_recomb_level, fieldlabel)]

        # calculate intensity from emission and opacity to (assuming dJ/ds = 0)
        J_nu_recomb = np.array([
            j_emiss_nu / kappa_bf if j_emiss_nu > 0 else 0.0
            for j_emiss_nu, kappa_bf in zip(j_emiss_nu_recomb, array_kappa_bf_nu, strict=False)
        ])

        J_contrib = np.abs(integrate.trapezoid(J_nu_recomb, x=arr_nu_hz_recomb))

        J_lambda_recomb = J_nu_recomb * arr_nu_hz_recomb / arraylambda_angstrom_recomb

        print(f"  Contribution to J = {J_contrib:.1e} ergs/s/cm2")

        J_lambda_recomb_total += J_lambda_recomb

        # contribution of all levels of the ion
        fieldlabel = f"{upperionstr} -> {at.roman_numerals[lower_ion_stage]} recombination"
        axes[2].plot(arraylambda_angstrom_recomb, J_lambda_recomb, label=fieldlabel, lw=lw)
        fieldlist += [(arraylambda_angstrom_recomb, J_lambda_recomb, fieldlabel)]

    # fieldlabel = f'Summed recombination'
    # axes[2].plot(arraylambda_angstrom_recomb, J_lambda_recomb_total, label=fieldlabel)
    # fieldlist += [(arraylambda_angstrom_recomb, J_lambda_recomb_total, fieldlabel)]
    ymax = max(ymax, J_lambda_recomb_total)

    lw = 1.0
    # fieldlist += [(arr_lambda_fitted, j_lambda_fitted, 'binned field')]

    for atomic_number, ion_stage in photoionlist:
        ionstr = at.get_ionstring(atomic_number, ion_stage)
        ion_data = adata.query("Z == @atomic_number and ion_stage == @ion_stage").iloc[0]

        for levelnum, level in ion_data.levels[:max_levels].iterrows():
            nu_threshold = ONEOVERH * (ion_data.ion_pot - level.energy_ev) * EV
            arr_sigma_bf = evaluate_phixs(
                modelpath, atomic_number, ion_stage, levelnum, nu_threshold, tuple(arr_nu_hz_recomb)
            )
            if levelnum < 5:
                axes[0].plot(
                    arraylambda_angstrom_recomb, arr_sigma_bf, label=rf"$\sigma_{{bf}}$({ionstr} {level.levelname})"
                )

        for arraylambda_angstrom, J_lambda_arr, linelabel in fieldlist:
            # lw -= 0.4
            arr_nu_hz = 2.99792458e18 / np.array(arraylambda_angstrom)
            print(f"{ionstr} photoionisation rate coeffs using radiation field due to {linelabel}")
            J_nu_arr = np.array(J_lambda_arr) * arraylambda_angstrom / arr_nu_hz

            arr_gamma_dnu = get_ion_gamma_dnu(
                modelpath, modelgridindex, timestep, atomic_number, ion_stage, arr_nu_hz, J_nu_arr, max_levels
            )

            # xlist = arr_lambda_fitted
            arr_gamma_dlambda = arr_gamma_dnu * arr_nu_hz / arraylambda_angstrom

            axes[1].plot(
                arraylambda_angstrom,
                arr_gamma_dlambda,
                lw=lw,
                label=r"d$\Gamma_R$(" + ionstr + " due to " + linelabel + r")/d$\lambda$",
            )

            gamma_r_ion = abs(integrate.trapezoid(arr_gamma_dlambda, x=arraylambda_angstrom))
            print(f"  Gamma_R({ionstr} due to {linelabel}): {gamma_r_ion:.2e}")

    axes[0].set_yscale("log")
    # axes[1].set_yscale('log')
    # axes[2].set_yscale('log')
    return ymax


def get_binedges(radfielddata: pd.DataFrame) -> list[float]:
    return [2.99792458e18 / radfielddata["nu_lower"].iloc[1], *list(2.99792458e18 / radfielddata["nu_upper"][1:])]


def plot_celltimestep(modelpath, timestep, outputfile, xmin, xmax, modelgridindex, args, normalised=False):
    """Plot a cell at a timestep things like the bin edges, fitted field, and emergent spectrum (from all cells)."""
    radfielddata = read_files(modelpath, timestep=timestep, modelgridindex=modelgridindex)
    if radfielddata.empty:
        print(f"No data for timestep {timestep:d} modelgridindex {modelgridindex:d}")
        return False

    modelname = at.get_model_name(modelpath)
    time_days = at.get_timestep_times(modelpath)[timestep]
    print(f"Plotting {modelname} timestep {timestep:d} (t={time_days:.3f}d)")
    T_R = radfielddata.query("bin_num == -1").iloc[0].T_R
    print(f"T_R = {T_R}")

    nrows = 3 if args.photoionrates else 1
    fig, axes = plt.subplots(
        nrows=nrows,
        ncols=1,
        sharex=True,
        figsize=(
            args.figscale * at.get_config()["figwidth"],
            args.figscale * at.get_config()["figwidth"] * (0.25 + nrows * 0.4),
        ),
        tight_layout={"pad": 0.2, "w_pad": 0.0, "h_pad": 0.0},
    )

    if isinstance(axes, mplax.Axes):
        axes = np.array([axes])
    assert isinstance(axes, np.ndarray)
    axis = axes[-1]

    assert isinstance(axis, mplax.Axes)
    ymax = 0.0

    xlist, yvalues = get_fullspecfittedfield(radfielddata, xmin, xmax, modelgridindex=modelgridindex, timestep=timestep)

    label = r"Dilute blackbody model "
    # label += r'(T$_{\mathrm{R}}$'
    # label += f'= {row["T_R"]} K)')
    axis.plot(xlist, yvalues, label=label, color="purple", linewidth=1.5)
    ymax = max(yvalues)

    if not args.nobandaverage:
        arr_lambda, yvalues = get_binaverage_field(radfielddata, modelgridindex=modelgridindex, timestep=timestep)
        axis.step(arr_lambda, yvalues, where="pre", label="Band-average field", color="green", linewidth=1.5)
        ymax = max([ymax] + [point[1] for point in zip(arr_lambda, yvalues, strict=False) if xmin <= point[0] <= xmax])

    arr_lambda_fitted, j_lambda_fitted = get_fitted_field(
        radfielddata, modelgridindex=modelgridindex, timestep=timestep
    )
    ymax = max(
        [ymax]
        + [point[1] for point in zip(arr_lambda_fitted, j_lambda_fitted, strict=False) if xmin <= point[0] <= xmax]
    )

    axis.plot(arr_lambda_fitted, j_lambda_fitted, label="Radiation field model", alpha=0.8, color="blue", linewidth=1.5)

    ymax3 = plot_line_estimators(
        axis, radfielddata, modelgridindex=modelgridindex, timestep=timestep, zorder=-2, color="red"
    )

    ymax = args.ymax if args.ymax >= 0 else max(ymax, ymax3)
    try:
        specfilename = at.firstexisting("spec.out", folder=modelpath, tryzipped=True)
    except FileNotFoundError:
        print("Could not find spec.out")
        args.nospec = True

    if not args.nospec:
        plotkwargs = {}
        if not normalised:
            modeldata, _, _ = at.inputmodel.get_modeldata_tuple(modelpath)
            # outer velocity
            v_surface = modeldata.loc[int(radfielddata.modelgridindex.max())].vel_r_max_kmps * 1e5
            r_surface = time_days * 864000 * v_surface
            r_observer = MEGAPARSEC
            scale_factor = (r_observer / r_surface) ** 2 / (2 * math.pi)
            print(
                "Scaling emergent spectrum flux at 1 Mpc to specific intensity "
                f"at surface (v={v_surface:.3e}, r={r_surface:.3e} {r_observer:.3e}) scale_factor: {scale_factor:.3e}"
            )
            plotkwargs["scale_factor"] = scale_factor
        else:
            plotkwargs["peak_value"] = ymax

        plot_specout(axis, specfilename, timestep, zorder=-1, color="black", alpha=0.6, linewidth=1.0, **plotkwargs)

    if args.showbinedges:
        binedges = get_binedges(radfielddata)
        axis.vlines(binedges, ymin=0.0, ymax=ymax, linewidth=0.5, color="red", label="", zorder=-1, alpha=0.4)

    velocity = at.inputmodel.get_modeldata_tuple(modelpath)[0]["vel_r_max_kmps"][modelgridindex]

    figure_title = f"{modelname} {velocity:.0f} km/s at {time_days:.0f}d"
    # figure_title += '\ncell {modelgridindex} timestep {timestep}'

    if not args.notitle:
        axis.set_title(figure_title, fontsize=11)

    if args.photoionrates:
        ymax = calculate_photoionrates(
            axes,
            modelpath,
            radfielddata,
            modelgridindex=modelgridindex,
            timestep=timestep,
            xmin=xmin,
            xmax=xmax,
            ymax=ymax,
        )
        axes[0].legend(loc="best", handlelength=2, frameon=False, numpoints=1, fontsize=4)
        axes[1].legend(loc="best", handlelength=2, frameon=False, numpoints=1, fontsize=4)

    # axis.annotate(figure_title,
    #               xy=(0.02, 0.96), xycoords='axes fraction',
    #               horizontalalignment='left', verticalalignment='top', fontsize=8)

    axis.set_xlabel(r"Wavelength ($\mathrm{{\AA}}$)")
    axis.set_ylabel(r"J$_\lambda$ [{}erg/s/cm$^2$/$\mathrm{{\AA}}$]")
    from matplotlib import ticker

    axis.xaxis.set_minor_locator(ticker.MultipleLocator(base=500))
    axis.set_xlim(left=xmin, right=xmax)
    axis.set_ylim(bottom=0.0, top=ymax)

    axis.yaxis.set_major_formatter(at.plottools.ExponentLabelFormatter(axis.get_ylabel()))

    axis.legend(loc="best", handlelength=2, frameon=False, numpoints=1, fontsize=9)

    print(f"Saving to {outputfile}")
    fig.savefig(str(outputfile), format="pdf")
    plt.close()
    return True


def plot_bin_fitted_field_evolution(axis, radfielddata, nu_line, modelgridindex, **plotkwargs):
    bin_num, _nu_lower, _nu_upper = select_bin(radfielddata, nu=nu_line, modelgridindex=modelgridindex)
    # print(f"Selected bin_num {bin_num} to get a binned radiation field estimator")
    radfielddataselected = radfielddata.query(
        f"bin_num == {bin_num} and modelgridindex == @modelgridindex and nu_lower <= @nu_line and nu_upper >= @nu_line"
    ).copy()

    radfielddataselected["Jb_nu_at_line"] = radfielddataselected.apply(
        lambda x: j_nu_dbb([nu_line], x.W, x.T_R)[0], axis=1
    )

    radfielddataselected = radfielddataselected.eval(
        "Jb_lambda_at_line = Jb_nu_at_line * (@nu_line ** 2) / 2.99792458e18"
    )
    lambda_angstroms = 2.99792458e18 / nu_line

    radfielddataselected.plot(
        x="timestep",
        y="Jb_lambda_at_line",
        ax=axis,
        label=f"Fitted field from bin at {lambda_angstroms:.1f} Å",
        **plotkwargs,
    )


def plot_global_fitted_field_evolution(axis, radfielddata, nu_line, modelgridindex, **plotkwargs):  # noqa: ARG001
    radfielddataselected = radfielddata.query("bin_num == -1 and modelgridindex == @modelgridindex").copy()

    radfielddataselected["J_nu_fullspec_at_line"] = radfielddataselected.apply(
        lambda x: j_nu_dbb([nu_line], x.W, x.T_R)[0], axis=1
    )

    radfielddataselected = radfielddataselected.eval(
        "J_lambda_fullspec_at_line = J_nu_fullspec_at_line * (@nu_line ** 2) / 2.99792458e18"
    )
    lambda_angstroms = 2.99792458e18 / nu_line

    radfielddataselected.plot(
        x="timestep",
        y="J_lambda_fullspec_at_line",
        ax=axis,
        label=f"Full-spec fitted field at {lambda_angstroms:.1f} Å",
        **plotkwargs,
    )


def plot_line_estimator_evolution(
    axis, radfielddata, bin_num, modelgridindex=None, timestep_min=None, timestep_max=None, **plotkwargs
):
    """Plot the Jblue_lu values over time for a detailed line estimators."""
    radfielddataselected = (
        radfielddata.query(
            "bin_num == @bin_num"
            + (" & modelgridindex == @modelgridindex" if modelgridindex else "")
            + (" & timestep >= @timestep_min" if timestep_min else "")
            + (" & timestep <= @timestep_max" if timestep_max else "")
        )[["timestep", "nu_upper", "J_nu_avg"]]
        .eval("lambda_angstroms = 2.99792458e18 / nu_upper")
        .eval("Jb_lambda = J_nu_avg * (nu_upper ** 2) / 2.99792458e18")
    )

    axis.plot(
        radfielddataselected["timestep"],
        radfielddataselected["Jb_lambda"],
        label=f"Jb_lu bin_num {bin_num}",
        **plotkwargs,
    )


def plot_timeevolution(modelpath, outputfile, modelgridindex, args: argparse.Namespace):
    """Plot a estimator evolution over time for a cell. This is not well tested and should be checked."""
    print(f"Plotting time evolution of cell {modelgridindex:d}")

    radfielddata = read_files(modelpath, modelgridindex=modelgridindex)
    radfielddataselected = radfielddata.query("modelgridindex == @modelgridindex")

    nlinesplotted = 200
    fig, axes = plt.subplots(
        nlinesplotted,
        1,
        sharex=True,
        figsize=(
            args.figscale * at.get_config()["figwidth"],
            args.figscale * at.get_config()["figwidth"] * (0.25 + nlinesplotted * 0.35),
        ),
        tight_layout={"pad": 0.2, "w_pad": 0.0, "h_pad": 0.0},
    )

    if isinstance(axes, mplax.Axes):
        axes = np.array([axes])

    assert isinstance(axes, np.ndarray)

    timestep = at.get_timestep_of_timedays(modelpath, 330)
    time_days = at.get_timestep_time(modelpath, timestep)

    dftopestimators = radfielddataselected.query("timestep==@timestep and bin_num < -1").copy()
    dftopestimators["lambda_angstroms"] = 2.99792458e18 / dftopestimators["nu_upper"]
    dftopestimators["Jb_lambda"] = dftopestimators["J_nu_avg"] * (dftopestimators["nu_upper"] ** 2) / 2.99792458e18
    dftopestimators = dftopestimators.sort_values("Jb_lambda", ascending=False, inplace=False).iloc[:nlinesplotted]
    print(f"Top estimators at timestep {timestep} t={time_days:.1f}")
    print(dftopestimators)

    for ax, bin_num_estimator, nu_line in zip(
        axes, dftopestimators.bin_num.to_numpy(), dftopestimators.nu_upper.to_numpy(), strict=False
    ):
        lambda_angstroms = 2.99792458e18 / nu_line
        print(f"Selected line estimator with bin_num {bin_num_estimator}, lambda={lambda_angstroms:.1f}")
        plot_line_estimator_evolution(ax, radfielddataselected, bin_num_estimator, modelgridindex=modelgridindex)

        plot_bin_fitted_field_evolution(ax, radfielddata, nu_line, modelgridindex=modelgridindex)

        plot_global_fitted_field_evolution(ax, radfielddata, nu_line, modelgridindex=modelgridindex)
        ax.annotate(
            rf"$\lambda$={lambda_angstroms:.1f} Å in cell {modelgridindex:d}\n",
            xy=(0.02, 0.96),
            xycoords="axes fraction",
            horizontalalignment="left",
            verticalalignment="top",
            fontsize=10,
        )

        ax.set_ylabel(r"J$_\lambda$ [erg/s/cm$^2$/$\mathrm{{\AA}}$]")
        ax.legend(loc="best", handlelength=2, frameon=False, numpoints=1)

    axes[-1].set_xlabel(r"Timestep")
    # axis.xaxis.set_minor_locator(ticker.MultipleLocator(base=100))
    # axis.set_xlim(left=xmin, right=xmax)
    # axis.set_ylim(bottom=0.0, top=ymax)

    print(f"Saving to {outputfile}")
    fig.savefig(str(outputfile), format="pdf")
    plt.close()


def addargs(parser: argparse.ArgumentParser) -> None:
    """Add arguments to an argparse parser object."""
    parser.add_argument("-modelpath", default=".", type=Path, help="Path to ARTIS folder")

    parser.add_argument(
        "-xaxis", "-x", default="lambda", choices=["lambda", "timestep"], help="Horizontal axis variable."
    )

    parser.add_argument("-timedays", "-time", "-t", help="Time in days to plot")

    parser.add_argument("-timestep", "-ts", action="append", help="Timestep number to plot")

    parser.add_argument("-modelgridindex", "-cell", action="append", help="Modelgridindex to plot")

    parser.add_argument("-velocity", "-v", type=float, default=-1, help="Specify cell by velocity")

    parser.add_argument("--nospec", action="store_true", help="Don't plot the emergent specrum")

    parser.add_argument("--showbinedges", action="store_true", help="Plot vertical lines at the bin edges")

    parser.add_argument("-xmin", type=int, default=1000, help="Plot range: minimum wavelength in Angstroms")

    parser.add_argument("-xmax", type=int, default=20000, help="Plot range: maximum wavelength in Angstroms")

    parser.add_argument("-ymax", type=int, default=-1, help="Plot range: maximum J_nu")

    parser.add_argument("--normalised", action="store_true", help="Normalise the spectra to their peak values")

    parser.add_argument("--notitle", action="store_true", help="Suppress the top title from the plot")

    parser.add_argument("--nobandaverage", action="store_true", help="Suppress the band-average line")

    parser.add_argument("--photoionrates", action="store_true", help="Suppress the band-average line")

    parser.add_argument(
        "-figscale", type=float, default=1.0, help="Scale factor for plot area. 1.0 is for single-column"
    )

    parser.add_argument("-o", action="store", dest="outputfile", type=Path, help="Filename for PDF file")


def main(args: argparse.Namespace | None = None, argsraw: Sequence[str] | None = None, **kwargs: t.Any) -> None:
    """Plot the radiation field estimators."""
    if args is None:
        parser = argparse.ArgumentParser(formatter_class=at.CustomArgHelpFormatter, description=__doc__)
        addargs(parser)
        at.set_args_from_dict(parser, kwargs)
        args = parser.parse_args([] if kwargs else argsraw)

    at.set_mpl_style()

    defaultoutputfile = (
        Path("plotradfield_cell{modelgridindex:03d}_ts{timestep:03d}.pdf")
        if args.xaxis == "lambda"
        else Path("plotradfield_cell{modelgridindex:03d}_evolution.pdf")
    )

    if not args.outputfile:
        args.outputfile = defaultoutputfile
    elif args.outputfile.is_dir():
        args.outputfile /= defaultoutputfile

    modelpath = args.modelpath

    pdf_list = []
    modelgridindexlist = []

    if args.velocity >= 0.0:
        modelgridindexlist = [at.inputmodel.get_mgi_of_velocity_kms(modelpath, args.velocity)]
    elif args.modelgridindex is None:
        modelgridindexlist = [0]
    else:
        modelgridindexlist = at.parse_range_list(args.modelgridindex)

    timesteplast = len(at.get_timestep_times(modelpath)) - 1
    if args.timedays:
        timesteplist = [at.get_timestep_of_timedays(modelpath, args.timedays)]
    elif args.timestep:
        timesteplist = at.parse_range_list(args.timestep, dictvars={"last": timesteplast})
    else:
        print("Using last timestep.")
        timesteplist = [timesteplast]

    for modelgridindex in modelgridindexlist:
        if args.xaxis == "lambda":
            for timestep in timesteplist:
                outputfile = str(args.outputfile).format(modelgridindex=modelgridindex, timestep=timestep)
                if plot_celltimestep(
                    modelpath,
                    timestep,
                    outputfile,
                    xmin=args.xmin,
                    xmax=args.xmax,
                    modelgridindex=modelgridindex,
                    args=args,
                    normalised=args.normalised,
                ):
                    pdf_list.append(outputfile)
        elif args.xaxis == "timestep":
            outputfile = str(args.outputfile).format(modelgridindex=modelgridindex)
            plot_timeevolution(modelpath, outputfile, modelgridindex, args)
        else:
            print("Unknown plot type {args.plot}")
            raise AssertionError

    if len(pdf_list) > 1:
        print(pdf_list)
        at.merge_pdf_files(pdf_list)


if __name__ == "__main__":
    main()

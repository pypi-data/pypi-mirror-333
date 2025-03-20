from __future__ import annotations

import multiprocessing
from functools import partial
from multiprocessing import Pool
from typing import Literal
from typing import Tuple

import numpy
import tqdm
from scipy.optimize import curve_fit
from silx.math.medianfilter import medfilt2d
from skimage.transform import rescale

import darfix

from ..io.progress import display_progress
from ..math import Vector3D


def gaussian(x, a, b, c, d):
    """
    Function to calculate the Gaussian with constants a, b, and c

    :param float x: Value to evaluate
    :param float a: height of the curve's peak
    :param float b: position of the center of the peak
    :param float c: standard deviation
    :param float d: lowest value of the curve (value of the limits)

    :returns: result of the function on x
    :rtype: float
    """
    return d + a * numpy.exp(-numpy.power(x - b, 2) / (2 * numpy.power(c, 2)))


def multi_gaussian(M, x0, y0, xalpha, yalpha, A, C, bg):
    """
    Bivariate case of the multigaussian PDF + background
    """
    x, y = M
    return bg + A * numpy.exp(
        -0.5
        / (1 - C**2)
        * (
            ((x - x0) / xalpha) ** 2
            + ((y - y0) / yalpha) ** 2
            - 2 * C * (x - x0) * (y - y0) / xalpha / yalpha
        )
    )


def generator(data, moments=None, indices=None):
    """
    Generator that returns the rocking curve for every pixel

    :param ndarray data: data to analyse
    :param moments: array of same shape as data with the moments values per pixel and image, optional
    :type moments: Union[None, ndarray]
    """
    for i in range(data.shape[1]):
        for j in range(data.shape[2]):
            if indices is None:
                new_data = data[:, i, j]
            else:
                new_data = numpy.zeros(data.shape[0])
                new_data[indices] = data[indices, i, j]
            if moments is not None:
                yield new_data, moments[:, i, j]
            yield new_data, None


def generator_2d(data, moments=None):
    """
    Generator that returns the rocking curve for every pixel

    :param ndarray data: data to analyse
    :param moments: array of same shape as data with the moments values per pixel and image, optional
    :type moments: Union[None, ndarray]
    """
    for i in range(data.shape[2]):
        for j in range(data.shape[3]):
            yield data[:, :, i, j], None


def fit_rocking_curve(
    y_values, values=None, num_points=None, int_thresh=None, method: str = "trf"
):
    """
    Fit rocking curve.

    :param tuple y_values: the first element is the dependent data and the second element are
        the moments to use as starting values for the fit
    :param values: The independent variable where the data is measured, optional
    :type values: Union[None, list]
    :param int num_points: Number of points to evaluate the data on, optional
    :param float int_thresh: Intensity threshold. If not None, only the rocking curves with
        higher ptp (range of values) are fitted, others are assumed to be noise and not important
        data. This parameter is used to accelerate the fit. Optional.

    :returns: If curve was fitted, the fitted curve, else item[0]
    :rtype: list
    """
    y, moments = y_values
    y = numpy.asanyarray(y)
    x = numpy.asanyarray(values) if values is not None else numpy.arange(len(y))
    ptp_y = numpy.ptp(y)
    if int_thresh is not None and ptp_y < int_thresh:
        return y, [0, x[0], 0, min(y)]
    if moments is not None:
        p0 = [ptp_y, moments[0], moments[1], min(y)]
    else:
        _sum = sum(y)
        if _sum > 0:
            mean = sum(x * y) / sum(y)
            sigma = numpy.sqrt(sum(y * (x - mean) ** 2) / sum(y))
        else:
            mean, sigma = numpy.nan, numpy.nan
        p0 = [ptp_y, mean, sigma, min(y)]
    if numpy.isnan(mean) or numpy.isnan(sigma):
        return y, p0
    if numpy.isclose(p0[2], 0):
        return y, p0
    if num_points is None:
        num_points = len(y)
    epsilon = 1e-2
    bounds = numpy.array(
        [
            [min(ptp_y, min(y)) - epsilon, min(x) - epsilon, 0, -numpy.inf],
            [max(max(y), ptp_y) + epsilon, max(x) + epsilon, numpy.inf, numpy.inf],
        ]
    )

    p0 = numpy.array(p0)
    p0[p0 < bounds[0]] = bounds[0][p0 < bounds[0]]
    p0[p0 > bounds[1]] = bounds[1][p0 > bounds[1]]
    try:
        pars, cov = curve_fit(
            f=gaussian, xdata=x, ydata=y, p0=p0, bounds=bounds, method=method
        )
        y_gauss = gaussian(numpy.linspace(x[0], x[-1], num_points), *pars)
        y_gauss[numpy.isnan(y_gauss)] = 0
        y_gauss[y_gauss < 0] = 0
        pars[2] *= darfix.config.FWHM_VAL
        return y_gauss, pars
    except RuntimeError:
        p0[2] *= darfix.config.FWHM_VAL
        return y, p0
    except ValueError:
        p0[2] *= darfix.config.FWHM_VAL
        return y, p0


def fit_2d_rocking_curve(y_values, values, shape, int_thresh=None, method: str = "trf"):
    assert method in ("trf", "lm", "dogbox")
    y, moments = y_values
    y = numpy.asanyarray(y)
    ptp_y = numpy.ptp(y)
    values = numpy.asanyarray(values)
    _sum = sum(y)
    if numpy.isclose(_sum, 0, rtol=1e-03):
        return y, [numpy.nan, numpy.nan, numpy.nan, numpy.nan, ptp_y, 0, 0]
    x0 = sum(values[0] * y) / _sum
    y0 = sum(values[1] * y) / _sum
    xalpha = numpy.sqrt(sum(y * (values[0] - x0) ** 2) / _sum)
    yalpha = numpy.sqrt(sum(y * (values[1] - y0) ** 2) / _sum)
    if (int_thresh is not None and ptp_y < int_thresh) or xalpha == 0 or yalpha == 0:
        return y, [x0, y0, xalpha, yalpha, ptp_y, 0, 0]
    X, Y = numpy.meshgrid(
        values[0, : shape[0]], values[1].reshape(numpy.flip(shape))[:, 0]
    )
    xdata = numpy.vstack((X.ravel(), Y.ravel()))
    epsilon = 1e-3
    if method in ("trf", "dogbox"):
        bounds = (
            [
                min(values[0]) - epsilon,
                min(values[1]) - epsilon,
                -numpy.inf,
                -numpy.inf,
                min(ptp_y, min(y)) - epsilon,
                -1,
                -numpy.inf,
            ],
            [
                max(values[0]) + epsilon,
                max(values[1]) + epsilon,
                numpy.inf,
                numpy.inf,
                max(ptp_y, max(y)) + epsilon,
                1,
                numpy.inf,
            ],
        )
    else:
        bounds = (-numpy.inf, numpy.inf)

    try:
        pars, cov = curve_fit(
            f=multi_gaussian,
            xdata=xdata,
            ydata=y,
            p0=[x0, y0, xalpha, yalpha, ptp_y, 0, 0],
            bounds=bounds,
            method=method,
        )
        y_gauss = multi_gaussian([X, Y], *pars)
        pars[2] *= darfix.config.FWHM_VAL
        pars[3] *= darfix.config.FWHM_VAL
        return y_gauss.ravel(), pars
    except RuntimeError:
        return y, [
            x0,
            y0,
            darfix.config.FWHM_VAL * xalpha,
            darfix.config.FWHM_VAL * yalpha,
            ptp_y,
            0,
            0,
        ]


def fit_data(
    data,
    moments=None,
    values=None,
    shape=None,
    indices=None,
    int_thresh=15,
    method: str = "trf",
    _tqdm=False,
):
    """
    Fit data in axis 0 of data

    :param bool _tqdm: If True, execut fitting under tqdm library.
    :returns: fitted data
    """

    g = generator(data, moments)
    cpus = multiprocessing.cpu_count()
    curves, maps = [], []
    with Pool(cpus - 1) as p:
        if _tqdm:
            for curve, pars in tqdm.tqdm(
                p.imap(
                    partial(
                        fit_rocking_curve,
                        values=values,
                        int_thresh=int_thresh,
                        method=method,
                    ),
                    g,
                ),
                total=data.shape[1] * data.shape[2],
            ):
                curves.append(list(curve))
                maps.append(list(pars))
        else:
            for curve, pars in p.map(
                partial(
                    fit_rocking_curve,
                    values=values,
                    int_thresh=int_thresh,
                    method=method,
                ),
                g,
            ):
                curves.append(list(curve))
                maps.append(list(pars))

    return numpy.array(curves).T.reshape(data.shape), numpy.array(maps).T.reshape(
        (4, data.shape[-2], data.shape[-1])
    )


def fit_2d_data(
    data,
    values,
    shape,
    moments=None,
    int_thresh=15,
    indices=None,
    method: str = "trf",
    _tqdm=False,
):
    """
    Fit data in axis 0 of data

    :param bool _tqdm: If True, execut fitting under tqdm library.
    :returns: fitted data
    """
    g = generator(data, moments, indices)
    cpus = multiprocessing.cpu_count()
    curves, maps = [], []
    with Pool(cpus - 1) as p:
        if _tqdm:
            for curve, pars in tqdm.tqdm(
                p.imap(
                    partial(
                        fit_2d_rocking_curve,
                        values=values,
                        shape=shape,
                        int_thresh=int_thresh,
                        method=method,
                    ),
                    g,
                ),
                total=data.shape[-2] * data.shape[-1],
            ):
                curves.append(list(curve))
                maps.append(list(pars))
        else:
            for curve, pars in p.map(
                partial(
                    fit_2d_rocking_curve,
                    values=values,
                    shape=shape,
                    int_thresh=int_thresh,
                    method=method,
                ),
                g,
            ):
                curves.append(list(curve))
                maps.append(list(pars))
    curves = numpy.array(curves).T
    if indices is not None:
        curves = curves[indices]
    return curves.reshape(data[indices].shape), numpy.array(maps).T.reshape(
        (7, data.shape[-2], data.shape[-1])
    )


def compute_moments(values, data, smooth: bool = True):
    """
    Compute first, second, third and fourth moment of data on values.

    :param values: 1D array of X-values
    :param data: nD array of Y-values with `len(weight) == len(values)`
    :returns: The four first moments to distribution Y(X)
    """
    if len(values) != len(data):
        raise ValueError("the length of 'values' and 'data' is not equal")

    wsum = numpy.sum(data, axis=0, dtype=numpy.float64)
    values = numpy.asarray(values, dtype=numpy.float64)

    # Moments
    # mean = sum(w * x) / sum(w)
    # var  = sum(w * (x - mean)^2) / sum(w)
    # skew = sum(w * ((x - mean)/sigma)^3) / sum(w)
    # kurt = sum(w * ((x - mean)/sigma)^4) / sum(w) - 3
    #
    # The loops below are there to avoid creating another array
    # in memory with the same shape as `weights`.

    with numpy.errstate(invalid="ignore", divide="ignore"):
        mean = sum(
            w * x
            for x, w in zip(
                display_progress(values, desc="Moments: compute mean 1/4"), data
            )
        )
        mean /= wsum

        var = sum(
            w * ((x - mean) ** 2)
            for x, w in zip(
                display_progress(values, desc="Moments: compute var 2/4"), data
            )
        )
        var /= wsum
        sigma = numpy.sqrt(var)
        fwhm = darfix.config.FWHM_VAL * sigma

        skew = sum(
            w * (((x - mean) / sigma) ** 3)
            for x, w in zip(
                display_progress(values, desc="Moments: compute skew 3/4"), data
            )
        )
        skew /= wsum

        kurt = sum(
            w * (((x - mean) / sigma) ** 4)
            for x, w in zip(
                display_progress(values, desc="Moments: compute kurt 4/4"), data
            )
        )
        kurt /= wsum
        kurt -= 3  # Fisher’s definition

    if smooth:
        mean = medfilt2d(mean)
        fwhm = medfilt2d(fwhm)
        skew = medfilt2d(skew)
        kurt = medfilt2d(kurt)

    return mean, fwhm, skew, kurt


def compute_peak_position(data, values=None, center_data=False):
    """
    Compute peak position map

    :param bool center_data: If True, the values are centered on 0.
    """
    if values is not None:
        values = numpy.asanyarray(values)
        x = numpy.array(numpy.argmax(data, axis=0))
        if center_data:
            middle = float(min(values) + numpy.ptp(values)) / 2
            values -= middle
        image = [values[i] for i in x.flatten()]
        image = numpy.reshape(image, x.shape)
    else:
        image = numpy.array(numpy.argmax(data, axis=0))
        if center_data:
            middle = len(data) / 2
            vals = numpy.linspace(-middle, middle, len(data))
            image = image * numpy.ptp(vals) / len(data) + numpy.min(vals)
    return image


def compute_rsm(
    H: int, W: int, d: float, ffz: float, mainx: float, rotate: bool = False
) -> Tuple[numpy.ndarray, numpy.ndarray]:
    """
    Transformation to azimuthal coordinates.

    :param int H: height of the image in pixels.
    :param int W: width of the image in pixels.
    :param float d: Distance in micrometers of each pixel.
    :param float ffz: motor 'ffz' value.
    :param float mainx: motor 'mainx' value.

    :returns: Tuple of two arrays of size (W, H)
    :rtype: (X1, X2) : ndarray
    """
    if rotate:
        y = (numpy.arange(H) - H / 2) * d
        z = ffz - (W / 2 - numpy.arange(W)) * d
        y, z = numpy.meshgrid(y, z, indexing="ij")
    else:
        y = (numpy.arange(W) - W / 2) * d
        z = ffz - (H / 2 - numpy.arange(H)) * d
        z, y = numpy.meshgrid(z, y, indexing="ij")
    eta = numpy.arctan2(y, z)
    twotheta = numpy.arctan2(numpy.sqrt(y * y + z * z), mainx)
    return numpy.degrees(eta), numpy.degrees(twotheta)


def compute_magnification(
    H: int,
    W: int,
    d: float,
    obx: float,
    obpitch: float,
    mainx: float,
    topography_orientation: int | None = None,
    center: bool = True,
) -> Tuple[numpy.ndarray, numpy.ndarray]:
    """
    :param int H: height of the image in pixels.
    :param int W: width of the image in pixels.
    :param float d: Distance in micrometers of each pixel.
    :param float obx: motor 'obx' value.
    :param float obpitch: motor 'obpitch' value in the middle of the dataset.
    :param float mainx: motor 'mainx' value.

    :returns: Tuple of two arrays of size (H, W)
    :rtype: (X1, X2) : ndarray
    """

    pix_arr = list(numpy.meshgrid(numpy.arange(H), numpy.arange(W)))
    d1 = obx / numpy.cos(numpy.radians(obpitch))
    d2 = mainx / numpy.cos(numpy.radians(obpitch)) - d1
    M = d2 / d1
    d /= M
    if center:
        pix_arr[0] = (pix_arr[0] - W / 2) * d
        pix_arr[1] = (H / 2 - pix_arr[1]) * d
    else:
        pix_arr[0] = pix_arr[0] * d
        pix_arr[1] = (H - 1 - pix_arr[1]) * d
    if topography_orientation is not None:
        pix_arr[topography_orientation] /= numpy.sin(numpy.radians(obpitch))
    return pix_arr[0], pix_arr[1]


def rescale_data(data, scale):
    new_data = None
    for i, image in enumerate(data):
        simage = rescale(image, scale, anti_aliasing=True, preserve_range=True)
        if new_data is None:
            new_data = numpy.empty((len(data),) + simage.shape, dtype=data.dtype)
        new_data[i] = simage
    return new_data


def calculate_RSM_histogram(
    data: numpy.ndarray,
    diffry_values: numpy.ndarray,
    twotheta: numpy.ndarray,
    eta: numpy.ndarray,
    Q: Vector3D,
    a: float,
    map_range: float,
    units: Literal["poulsen", "gorfman"] | None = None,
    map_shape: Vector3D | None = None,
    n: Vector3D | None = None,
    E: float | None = None,
):
    """
    ***Code originally written by Mads Carslen***

    Calculate reciprocal space map from a 'diffry' scan without the objective lens.
    The RSM is calculated as a multidimensional histogram;

    :param data:
    :param diffry_values:
    :param twotheta:
    :param eta:
    :param Q: Scattering vector in oriented pseudocubic coordinates.
    :param a: pseudocubic lattice parameter
    :param map_range: range (in all 3 directions) of the histogram. Center-to edge-distance.
    :param units: either 'poulsen'  [10.1107/S1600576717011037] or 'gorfman' [https://arxiv.org/pdf/2110.14311.pdf]. Default: 'poulsen'
    :param map_shape: Number of bins in each direction
    :param n: surface normal of the sample in oriented pseudocubic hkl
    :param E: energy
    """

    if units is None:
        units = "poulsen"
    if map_shape is None:
        map_shape = (50, 50, 50)
    if n is None:
        n = (1, 0, 0)
    if E is None:
        E = 17.0

    k = 2 * numpy.pi / (12.391 / E)

    diffry_center = numpy.mean(diffry_values)
    img_shape = data[0].shape
    if units == "gorfman":
        # Build orientation matrix
        sampl_z = numpy.array(Q) / numpy.linalg.norm(
            numpy.array(Q)
        )  # assume scattering vector is z
        sampl_x = n - sampl_z * numpy.dot(sampl_z, n) / numpy.linalg.norm(
            n
        )  # orthogonalize
        sampl_x /= numpy.linalg.norm(sampl_x)  # nomalize

        sampl_y = numpy.cross(sampl_z, sampl_x)
        lab_to_lat = numpy.stack((sampl_x, sampl_y, sampl_z))
    elif units == "poulsen":
        lab_to_lat = numpy.identity(3)

    # Calculate lab frame q vector for each pixel
    k0 = numpy.array([k, 0, 0])  # Lab frame incidetn wavevector
    twotheta = numpy.radians(twotheta)
    eta = numpy.radians(eta)
    kh = k * numpy.stack(
        [
            numpy.cos(twotheta),
            numpy.sin(twotheta) * numpy.sin(eta),
            numpy.sin(twotheta) * numpy.cos(eta),
        ]
    )  # Lab frame scattered wavevector
    q = kh - k0[:, numpy.newaxis, numpy.newaxis]
    if units == "gorfman":
        q = q * a / 2 / numpy.pi
    elif units == "poulsen":
        q = q * a / 2 / numpy.pi / numpy.linalg.norm(Q)

    # flatten to match syntax for histogramdd
    q = q.reshape(3, img_shape[0] * img_shape[1])
    # Rotate from lab frame to sample frame
    theta_ref = numpy.arcsin(2 * numpy.pi * numpy.linalg.norm(Q) / a / k / 2)
    q = numpy.stack(
        [
            q[0, ...] * numpy.cos(theta_ref) + q[2, ...] * numpy.sin(theta_ref),
            q[1, ...],
            q[2, ...] * numpy.cos(theta_ref) - q[0, ...] * numpy.sin(theta_ref),
        ]
    )

    # Make histogram ranges
    q_mean = numpy.mean(q, axis=1)
    diffry_mean = numpy.radians(numpy.mean(diffry_values) - diffry_center)
    q_mean = numpy.stack(
        [
            q_mean[0] * numpy.cos(diffry_mean) - q_mean[2] * numpy.sin(diffry_mean),
            q_mean[1],
            q_mean[2] * numpy.cos(diffry_mean) + q_mean[0] * numpy.sin(diffry_mean),
        ]
    )

    if units == "gorfman":
        q_mean = lab_to_lat.transpose() @ q_mean

    ranges = (
        (q_mean[0] - map_range, q_mean[0] + map_range),
        (q_mean[1] - map_range, q_mean[1] + map_range),
        (q_mean[2] - map_range, q_mean[2] + map_range),
    )  # hkl units

    # initialize sum arrays
    sum_inte = numpy.zeros(map_shape)
    sum_freq = numpy.zeros(map_shape)

    loop = tqdm.tqdm(data)
    # Loop through images
    for i, image in enumerate(loop):
        # read angle
        diffry = numpy.radians(diffry_values[i] - diffry_center)
        # rotate q back to zero-motor frame
        q_rot = numpy.stack(
            [
                q[0, ...] * numpy.cos(diffry) - q[2, ...] * numpy.sin(diffry),
                q[1, ...],
                q[2, ...] * numpy.cos(diffry) + q[0, ...] * numpy.sin(diffry),
            ]
        )
        # Rotate into lattice frame
        q_rot = lab_to_lat.transpose() @ q_rot
        # Do binning
        sum_inte += numpy.histogramdd(
            q_rot.transpose(), map_shape, ranges, weights=image.flatten()
        )[0]
        sum_freq += numpy.histogramdd(q_rot.transpose(), map_shape, ranges)[0]

    edges = numpy.histogramdd(q_rot.transpose(), map_shape, ranges)[1]
    # Setting sum_freq to NaN where it is 0 to avoid division by 0 (`arr` will be NaN there)
    sum_freq[sum_freq == 0] = numpy.nan
    arr = sum_inte / sum_freq

    if units == "poulsen":
        edges[2] = edges[2] - 1

    return arr, edges

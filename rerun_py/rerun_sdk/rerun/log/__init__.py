from typing import Optional, Sequence, Union

import numpy as np
import numpy.typing as npt

ColorDtype = Union[np.uint8, np.float32, np.float64]
Color = Union[npt.NDArray[ColorDtype], Sequence[Union[int, float]]]
Colors = Union[Sequence[Color], npt.NDArray[ColorDtype]]

OptionalClassIds = Optional[Union[int, npt.ArrayLike]]
OptionalKeyPointIds = Optional[Union[int, npt.ArrayLike]]


def _to_sequence(array: Optional[npt.ArrayLike]) -> Optional[Sequence[float]]:
    return np.require(array, float).tolist()  # type: ignore[no-any-return]


def _normalize_colors(colors: Optional[Union[Color, Colors]] = None) -> npt.NDArray[np.uint8]:
    """
    Normalize flexible colors arrays.

    Float colors are assumed to be in 0-1 gamma sRGB space.
    All other colors are assumed to be in 0-255 gamma sRGB space.

    If there is an alpha, we assume it is in linear space, and separate (NOT pre-multiplied).
    """
    if colors is None:
        # An empty array represents no colors.
        return np.array((), dtype=np.uint8)
    else:
        colors_array = np.array(colors, copy=False)

        # Rust expects colors in 0-255 uint8
        if colors_array.dtype.type in [np.float32, np.float64]:
            # Assume gamma-space colors
            return np.require(np.round(colors_array * 255.0), np.uint8)

        return np.require(colors_array, np.uint8)


def _normalize_ids(class_ids: OptionalClassIds = None) -> npt.NDArray[np.uint16]:
    """Normalize flexible class id arrays."""
    if class_ids is None:
        return np.array((), dtype=np.uint16)
    else:
        # TODO(andreas): Does this need optimizing for the case where class_ids is already an np array?
        return np.atleast_1d(np.array(class_ids, dtype=np.uint16, copy=False))


def _normalize_radii(radii: Optional[npt.ArrayLike] = None) -> npt.NDArray[np.float32]:
    """Normalize flexible radii arrays."""
    if radii is None:
        return np.array((), dtype=np.float32)
    else:
        return np.atleast_1d(np.array(radii, dtype=np.float32, copy=False))


def _normalize_labels(labels: Optional[Union[str, Sequence[str]]]) -> Sequence[str]:
    if labels is None:
        return []
    else:
        return labels

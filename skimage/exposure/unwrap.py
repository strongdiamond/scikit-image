import numpy as np

import _unwrap_2d
import _unwrap_3d


def unwrap(wrapped_array,
           wrap_around_axis_0=False,
           wrap_around_axis_1=False,
           wrap_around_axis_2=False):
    '''From ``image``, wrapped to lie in the interval [-pi, pi), recover the
    original, unwrapped image.

    Parameters
    ----------
    image : 2D or 3D ndarray, optionally a masked array
    wrap_around : bool or sequence of bool

    Returns
    -------
    image_unwrapped : array_like
    '''
    wrapped_array = np.require(wrapped_array, np.float32, ['C'])
    if wrapped_array.ndim not in [2,3]:
        raise ValueError('input array needs to have 2 or 3 dimensions')

    wrapped_array_masked = np.ma.asarray(wrapped_array)
    unwrapped_array = np.empty_like(wrapped_array_masked.data)
    if wrapped_array.ndim == 2:
        _unwrap_2d._unwrap2D(wrapped_array_masked.data,
                           np.ma.getmaskarray(wrapped_array_masked).astype(np.uint8),
                           unwrapped_array,
                           bool(wrap_around_axis_0), bool(wrap_around_axis_1))
    elif wrapped_array.ndim == 3:
        _unwrap_3d._unwrap3D(wrapped_array_masked.data,
                           np.ma.getmaskarray(wrapped_array_masked).astype(np.uint8),
                           unwrapped_array,
                           bool(wrap_around_axis_0), bool(wrap_around_axis_1), bool(wrap_around_axis_2))

    if np.ma.isMaskedArray(wrapped_array):
        return np.ma.array(unwrapped_array, mask = wrapped_array_masked.mask)
    else:
        return unwrapped_array

    #TODO: set_fill to minimum value
    #TODO: check for empty mask, not a single contiguous pixel


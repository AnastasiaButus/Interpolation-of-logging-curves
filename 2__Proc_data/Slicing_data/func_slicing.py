import numpy as np


def slice_1d(x, y, x_wind, step = 1):
    """ Slices one set of data from 1 well.

    x: x-data array (seism data).
    y: y-data array (GIS data).
    x_wind: size of x-window to slice.
    step: step of slicing.
    """
    x_hlf_wind = x_wind//2
    x = np.array(x)
    y = np.array(y)
    x_sl, y_sl = [], []

    for i in range(x_hlf_wind, len(y)-x_hlf_wind, step):
        x_sl.append(x[i-x_hlf_wind:i+x_hlf_wind+1])
        y_sl.append(y[i])

    return np.array(x_sl), np.array(y_sl)


def slice_2d(m_x, m_y, x_wind, step = 1):
    """ Slices matrexes set of data from several wells.

    m_x: list of x-data arrays (seism data) from several wells.
    y: list of y-data arrays (GIS data) from several wells.
    x_wind: size of x-window to slice.
    step: step of slicing.
    """
    ar_x, ar_y = slice_1d(m_x[0], m_y[0], x_wind, step = 1)
    m_x_sl, m_y_sl = np.array(ar_x), np.array(ar_y)


    for j in range(1, len(m_y)):
        ar_x, ar_y = slice_1d(m_x[j], m_y[j], x_wind)
        #print(f"ar_x: {ar_x}")
        #print(f"ar_y: {ar_y}")
        if len(ar_x)*len(ar_y)!=0:
            m_x_sl = np.concatenate([m_x_sl, ar_x], axis = 0)
            m_y_sl = np.concatenate([m_y_sl, ar_y], axis = 0)


    return m_x_sl, m_y_sl



def slice_1d_with_v(x, y, v, x_wind, step = 1):
    """ Slices one set of data from 1 well. Including velocity.

    x: x-data array (seism data).
    y: y-data array (GIS data).
    v: velocity value.
    x_wind: size of x-window to slice.
    step: step of slicing.
    """
    x_hlf_wind = x_wind//2
    x = np.array(x)
    y = np.array(y)
    x_sl, y_sl = [], []

    for i in range(x_hlf_wind, len(y)-x_hlf_wind, step):
        x_sl.append(np.concatenate([x[i-x_hlf_wind:i+x_hlf_wind+1], np.array([v])]))
        y_sl.append(y[i])

    return np.array(x_sl), np.array(y_sl)


def slice_2d_with_v(m_x, m_y, ar_v, x_wind, step = 1):
    """ Slices matrexes set of data from several wells. 
    Including velocity in x data.

    m_x: list of x-data arrays (seism data) from several wells.
    y: list of y-data arrays (GIS data) from several wells.
    ar_v: list of velocities in several wells.
    x_wind: size of x-window to slice.
    step: step of slicing.
    """
    ar_x, ar_y = slice_1d_with_v(m_x[0], m_y[0], ar_v[0], x_wind, step = 1)
    m_x_sl, m_y_sl = np.array(ar_x), np.array(ar_y)


    for j in range(1, len(m_y)):
        ar_x, ar_y = slice_1d_with_v(m_x[j], m_y[j], ar_v[j], x_wind)
        #print(f"ar_x: {ar_x}")
        #print(f"ar_y: {ar_y}")
        if len(ar_x)*len(ar_y)!=0:
            m_x_sl = np.concatenate([m_x_sl, ar_x], axis = 0)
            m_y_sl = np.concatenate([m_y_sl, ar_y], axis = 0)


    return m_x_sl, m_y_sl
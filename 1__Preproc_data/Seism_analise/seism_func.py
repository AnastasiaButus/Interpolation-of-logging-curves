import numpy as np
import segyio


def get_seism_cube(file_dir="", file_name="J1-3_plus_minus_150ms"):
    """ Reads seisma data and returns seiasma cube

    file_dir - directory to file
    file_name - name of the csv file
    """
    amp4 = segyio.tools.cube(f"{file_dir}/{file_name}")

    return amp4


def seism_vectors(main_array,
                  x_coord, y_coord):

    """ This function recieves seisma data, x+y coordinates of well`s
    and some constants. Returns array of seisma and it`s coordinates.

    main_array - 3D np.array of seisma
    x_coord - vector of x coordinates in meters of well`s
    y_coord - vector of y coordinates in meters of well`s
    """
    # Getting indexes for seism from coordinates
    x_index = (np.round( (np.array(x_coord)-524272.72)/(9630.30/392) )).astype('int')
    y_index = (np.round( (np.array(y_coord)-6410041.47)/((18876.79/768)) )).astype('int')

    # Filtering out-of-bounds indexes
    mask = ((x_index<main_array.shape[1])*(x_index>=0)*(y_index<main_array.shape[0])*(y_index>=0))

    for x, y, x_i, y_i, m in zip(x_coord, y_coord, x_index, y_index, mask):
        print(f"x={x}\ty={y}\tx_index={x_i}\ty_index={y_i}\tin={m}")

    result_matrix = []
    ar_null = np.array([None]*main_array.shape[2])
    for x, y, valid_flag in zip(x_index, y_index, mask):
        if valid_flag: 
            result_matrix.append(main_array[y, x, :])
        else:
            result_matrix.append(ar_null)

    result_matrix = np.array(result_matrix)



    return result_matrix, mask


def get_seism_index(z_cube_len,
                    z_top, z_bottom,
                    t_top, t_bottom,
                    delta_t=2,
                    index_top=900, index_bottom=1300):
    """ Evaluates indexes for z-values of list of seisma cube.
    
    z_top, z_bottom - bounds of krovla, podoshva in meters
    t_top, t_bottom - bounds of krovla, podoshva in mseconds,    
    delta_t - discretisation step of seisma in mseconds
    index_top, index_bottom - indexes of cutting seisma cube
    """
    # Getting massive of depth values. Suggesting velocity=const.
    t = np.linspace(index_top*delta_t, (index_bottom-1)*delta_t, z_cube_len)
    z_mult = []
    for z_top_i, z_bottom_i, t_top_i, t_bottom_i in zip(z_top, z_bottom, t_top, t_bottom):
        z_mult.append( (t - t_top_i)/(t_bottom_i-t_top_i)*(z_top_i-z_bottom_i) + z_top_i) 
    
    z_mult = np.array(z_mult)
    #z = np.mean(z_mult, axis=0)
    #z_std = (np.std(z_mult, ddof=1, axis=0))/len(z_mult)**0.5

    return z_mult
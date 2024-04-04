import os
import pandas as pd

import lasio


def get_df_well_coord(dir_name_coord = "omsk", 
                      file_name_coord = "Coord.xlsx"):
    """ Reads excel file with coordinates and returns df.

    dir_name_coord - path to directory with file wirh coordinates.
    file_name_coord - file name with coordinates.
    """
    df_coord = pd.read_excel(f"{dir_name_coord}/{file_name_coord}", index_col=0)

    return df_coord


def get_well_gis(well_name, name_signal, df_coord,
                 dir_name_las = "omsk"):
    """ Reads lasio files and returns (pd.Series of signal, (x, y) well`s buttom coordinates)

    well_name - name of well.
    name_signal - type of signal. One from [ 'BK', 'NKT', 'IK', 'GK', 'SP', 'RT' ].
    df_coord - df with wells coordinates.
    dir_name_las - path to directory with .las files.
    """
    las = lasio.read(f"{dir_name_las}/{well_name}.las")
    dic_gis = {well_name: las[name_signal]}
    df_gis = pd.DataFrame(dic_gis, index=las["DEPT"])
    df_gis = df_gis.dropna(how='all') # To delete no data points

    coord = df_coord.loc[well_name]


    return df_gis, coord


def get_all_gis(name_signal,
                dir_name_las = "omsk"):
    """ Reads all lasio files and creates 2 dictions:
    1-st with signal df; 2-nd with (x,y) coordinates of well`s buttom.

    name_signal - type of signal. One from [ 'BK', 'NKT', 'IK', 'GK', 'SP', 'RT' ].
    df_coord - df with wells coordinates.
    dir_name_las - path to directory with .las files.
    """
    df_signals = pd.DataFrame()

    df_coord_0 = get_df_well_coord()
    
    for file in os.listdir(dir_name_las):
        if (file[0]=='g') and (file[1:4].isdigit()) and (file[4:]==".las"): # Filterng right well files
            gis = get_well_gis(file[:4], name_signal, df_coord_0)


            df_signals = pd.concat([df_signals, gis[0]], axis=1, join='outer')

            print(f"file: {file} processed", end='\r')
            
    df_coord = df_coord_0.loc[df_signals.columns]


    return df_signals, df_coord
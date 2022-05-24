from collections import defaultdict
from itertools import cycle
from loguru import logger
import os
import toml
import json
import csv
import pandas as pd
from copy import copy

from .utils import(
    Scale,
    stof
)
from .data import(
    Devices,
)

def read_specs(path:str) -> Devices:
    """_summary_
    Reads the contents of YAML and JSON files and returns a dictionary
    containing the labelled information from within the files
    Args:
        path (str): path to read the file from

    Raises:
        FileNotFoundError: _description_
        ValueError: _description_
        IOError: _description_

    Returns:
        dict: data structure containing the extracted information from the YAML / JSON file
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"File {path} not found")
    head,tail = os.path.split(path)
    name, extension = os.path.splitext(tail)
    if extension not in [ ".toml", ".json"]:
        raise ValueError(f"File {path} is not a valid specification file. Only .toml and .json are accepted")
    struct = {}
    try:
        with open(path, 'r') as file:
            if extension == ".toml":
                struct = toml.load(file)
            elif extension == ".json":
                struct = json.load(file)
    except:
        raise IOError(f"File {path} could not be read")
    devices = Devices()
    devices.parse_data(struct)
    return devices if bool(struct) else None

def read_data(path: str) -> pd.DataFrame:
    """_summary_
    Reads a CSV data file and returns a pandas dataframe
    Args:
        path (str): path to read the file from

    Raises:
        FileNotFoundError: _description_
        ValueError: _description_
        IOError: _description_

    Returns:
        pandas DataFrame: dataframe containing the extracted information from the CSV file
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"File {path} not found")
    head,tail = os.path.split(path)
    name, extension = os.path.splitext(tail)
    if extension !=  ".csv":
        raise ValueError(f"File {path} is not a valid specification file. Only .csv files are accepted")
    df = None
    try:
        with open(path, 'r') as file:
            df = pd.read_csv(file)
    except:
        raise IOError(f"File {path} could not be read")
    return df

def read_lut(path: str) -> pd.DataFrame:
    """_summary_
    Reads a Cadence Look Up Table exported to CSV
    and unfolds it to return a Pandas DataFrame that only
    includes raw axis
    Args:
        path (str): path to read the file from

    Raises:
        FileNotFoundError: _description_
        ValueError: _description_
        IOError: _description_

    Returns:
        pandas DataFrame: dataframe containing the extracted information from the CSV file
    """
    lut = read_data(path)
    original_lut_size = len(lut)
    # detect variables present in lut name
    head,tail = os.path.split(path)
    name, extension = os.path.splitext(tail)
    attrs = name.split('_')
    detected_vars={}
    sweeped_vars = []
    for attr in attrs:
        tokens=attr.split('-')
        var_name = tokens[0]
        if var_name == "sweep":
            sweeped_vars.append([tokens[1], tokens[2]])
            break
        var_alpha=""
        scale = None
        for token in tokens[1:]:
            if token.isnumeric():
                var_alpha = ".".join([var_alpha,token]) if var_alpha != "" else token
            else:
                scale = token
        #convert the detected variable into float
        # and multiply it by the respective found scale
        var = 0.0
        try:
            var = float(var_alpha)
        except:
            raise ValueError(f"Wrong LUT naming format: {name}.")
        scaling_factor = 1.0
        if scale != None:
            scaling_letters = [s.value[0] for s in Scale]
            if scale not in scaling_letters:
                raise ValueError(f"Unrecognized unit scaling token: {scale}")
            scaling_factor = [s.value[1] for s in Scale if s.value[0] == scale][0]
        var = var*scaling_factor
        # add the var and var_name to the detected_vars dict
        detected_vars[var_name] = var
# detect the variable sweeps present in the name of each column
    data=defaultdict(list)
    sweep_axis_value_space = defaultdict(list)
    for column in lut.columns[1:]:
        tokens = column.split(' ')
        var_name = tokens[0].split(':')[1]
        [data[var_name].append(val) for val in lut[column].values]
        if len(tokens)>2:
            var_name = tokens[1]
            var_value = float(tokens[2])
            if bool(sweep_axis_value_space.get(var_name)):
                if var_value not in sweep_axis_value_space.get(var_name):
                    sweep_axis_value_space[var_name].append(var_value)
            else:
                sweep_axis_value_space[var_name].append(var_value)
    max_col_len = 0
    # get the maximum true length of the entire expanded lut table
    for col in data.keys():
        if len(data[col]) > max_col_len:
            max_col_len = len(data[col])
    # adjoint the constant axis : vsb and lx
    for var_name in detected_vars.keys():
        data[var_name] = [detected_vars[var_name]]*max_col_len
    # adjoint the secondary sweeping variable - vds or vsd
    # and expand the short axis (x-axis) until it reaches the required length
    # adjoining the primary sweeping axis onto the data frame
    x_axis = lut.columns[0].split(' ')[0]
    x_axis = x_axis.replace(' ','')
    for var_name in sweep_axis_value_space.keys():
        for var_value in sweep_axis_value_space[var_name]:
            [data[var_name].append(val) for val in [var_value]*original_lut_size]
            [data[x_axis].append(val) for val in lut[lut.columns[0]].values]
    return pd.DataFrame(data)
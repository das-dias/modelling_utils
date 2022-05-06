from loguru import logger
import os
import yaml
import json
import csv
import pandas as pd
def read(path:str) -> dict:
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
    if extension not in [ ".yaml", ".yml", ".json"]:
        raise ValueError(f"File {path} is not a valid specification file. Only .yaml, .yml, .json are accepted")
    struct = {}
    try:
        with open(path, 'r') as file:
            if extension in [".yaml", ".yml"]:
                struct = yaml.safe_load(file)
            elif extension == ".json":
                struct = json.load(file)
    except:
        raise IOError(f"File {path} could not be read")
    return struct

def read_specs(path: str) -> dict:
    raise NotImplementedError("read_specs is not implemented")

def read_model(path: str) -> dict:
    raise NotImplementedError("read_model is not implemented")

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
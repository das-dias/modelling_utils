from http.client import UnimplementedFileMode
from loguru import logger
import os
import yaml
import json
import toml
import csv
import pandas as pd
def write(info: dict, path:str) -> None:
    """_summary_
    Writes the contents of a dictionary to a YAML or JSON file
    containing the labelled information from within the dictionary
    Args:
        path (str): path to read the file from
    Raises:
        FileNotFoundError: _description_
        ValueError: _description_
        IOError: _description_
    """
    raise NotImplementedError(f"write function not implemented")
    if not os.path.exists(path):
        raise FileNotFoundError(f"File {path} not found")
    head,tail = os.path.split(path)
    name, extension = os.path.splitext(tail)
    possible_formats = [ ".yaml", ".yml", ".json", "toml"]
    try:
        with open(path, 'w') as file:
            if extension in [".yaml", ".yml"]:
                yaml.dump(info, file)
            elif extension == ".json":
                json.dump(info, file)
            elif extension == ".toml":
                toml.dump(info, file)
            else:
                raise ValueError(f"File {path} is not a valid specification file. Only {possible_formats} are accepted")
    except:
        raise IOError(f"File {path} could not be opened")

def write_data(data: pd.DataFrame, path: str):
    """_summary_
    Writes a CSV data file from a pandas dataframe
    Args:
        data (pd.DataFrame) : dataframe to write to the file
        path (str)          : path to read the file from

    Raises:
        FileNotFoundError: _description_
        ValueError: _description_
        IOError: _description_

    Returns:
        pandas DataFrame: dataframe containing the extracted information from the CSV file
    """
    raise NotImplementedError(f"write_data function not implemented")
    if not os.path.exists(path):
        raise FileNotFoundError(f"File {path} not found")
    head,tail = os.path.split(path)
    name, extension = os.path.splitext(tail)
    if extension !=  ".csv":
        raise ValueError(f"File {path} is not a valid specification file. Only .csv files are accepted")
    df = None
    try:
        data.to_csv(path)
    except:
        raise IOError(f"File {path} could not be opened")
    return df
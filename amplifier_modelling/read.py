from loguru import logger
import os
import yaml
import json

def _read(path:str) -> dict:
    """_summary_
    
    Args:
        path (str): _description_

    Raises:
        FileNotFoundError: _description_
        ValueError: _description_
        IOError: _description_

    Returns:
        dict: _description_
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"File {path} not found")
    head,tail = os.path.split(path)
    name, extension = os.path.splitext(tail)
    if extension not in [ ".yaml", ".yml", ".json" ]:
        raise ValueError(f"File {path} is not a valid specification file. Only .yaml, .yml, .json are accepted")
    struct = {}
    try:
        with open(path, 'r') as file:
            if extension in [".yaml", ".yml"]:
                struct = yaml.safe_load(file)
            elif extension == ".json":
                specs = json.load(file)
    except:
        raise IOError(f"File {path} could not be read")
    return struct

def read_specs(path: str) -> dict:
    try:
        specs = _read(path)
    except:
        logger.error(f"Could not read specs from {path}")
        return None
    logger.info(f"Read specs from {path}")
    # test if the specification fields are valid
    #...
    return specs # if all is well, return the specs

def read_model(path: str) -> dict:
    try:
        model = _read(path)
    except:
        logger.error(f"Could not read model from {path}")
        return None
    logger.info(f"Read model from {path}")
    # test if the specification fields are valid
    #...
    return model # if all is well, return the specs
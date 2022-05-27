""" ***********************************
* *[author] Diogo André (git-hub : das-dias)
* *[date] 21-05-2022
* *[filename] data.py
* *[summary] Python lang file implementing the data structures enabling the
*               device control variables parsing environment
* ***********************************
"""
from collections import defaultdict
from re import S
import numpy as np
from pandas import DataFrame
from enum import Enum
import os
from .utils import(
    Scale,
    Units,
    stof
)


class TomlSections(Enum):
    """_summary_
    Enumerator for the types of sections in
    parsing toml files
    Args:
        Enum (_type_): _description_
    """
    CONTROL="control"
    SPIT="spit"

class TomlControlKeywords(Enum):
    """_summary_
    Enumerator for the possible keywords
    in the parsing toml file's [control] section
    Args:
        Enum (_type_): _description_
    """
    DEVICE="device"
    DEVICES="devices"
    VARACTOR="varactor"
    VARACTORS="varactors"
    SWITCH="switch"
    SWITCHES="switches"
    TYPE="type"
    RON="ron" # target on resistance for the switch
    CVAR="cvar" # target varactor capacitance
    VGS="vgs"
    VSG="vsg"
    VDS="vds"
    VSD="vsd"
    GMOVERID="gmoverid"
    LENGTH="l"
    VSB="vsb"
    VBS="vbs"
    ID="id"

class TomlSpitKeywords(Enum):
    """_summary_
    Enumerator for the possible keywords
    in the parsing toml file's [spit] section
    Args:
        Enum (_type_): _description_
    """
    OUTPUTDIR="outputdir"
    VARS="vars"
    PLOT="plot"

class TomlSpitVariables(Enum):
    """_summary_
    Enumerator for the possible keywords
    in the parsing toml file's [spit] posssible variables
    Args:
        Enum (_type_): _description_
    """
    VGS="vgs"
    VSG="vsg"
    WIDTH="w"
    GDS="gds"
    GM="gm"
    GMBS="gmbs"
    SELF_GAIN="selfgain"
    F_T="ft"
    F_OSC="fosc"
    CGS="cgs"
    CGD="cgd"
    CGB="cgb"
    CSB="csb"
    CDB="cdb"
    CVAR="cvar" # actual varactor capacitance
    R_ON="ron"
    REGION="region"
    ALL="all"

class TomlSpitPlot(Enum):
    TRUE="true"
    FALSE="false"
    
class TomlControlType(Enum):
    NMOS="nch"
    PMOS="pch"
    
class MosCell:
    """_summary_
    Object implementing the CMOS device
    control and main spice parameters
    Args:
        object (_type_): _description_
    """
    __slots__=[
        "name",
        "type",
        "vds",
        "vsd",
        "vsb",
        "vbs",
        "gmoverid",
        "l",
        "id",
        "vgs",
        "vsg",
        "w",
        "cgs",
        "cgd",
        "cgb",
        "csb",
        "cdb",
        "cdep",
        "cgg",
        "cvar",
        "gm",
        "gmbs",
        "gds",
        "self_gain",
        "ft",
        "fosc",
        "ron",
        "region",
        "vdsat",
    ]
    __UNITS__={
        "name":"",
        "type":"",
        "vds":Units.VOLTAGE.value,
        "vsd":Units.VOLTAGE.value,
        "vsb":Units.VOLTAGE.value,
        "vbs":Units.VOLTAGE.value,
        "gmoverid":Units.VOLTAGE.value+"^-1",
        "l":Units.METER.value,
        "id":Units.AMPERE.value,
        "vgs":Units.VOLTAGE.value,
        "vsg":Units.VOLTAGE.value,
        "w":Units.METER.value,
        "cgs":Units.FARAD.value,
        "cgd":Units.FARAD.value,
        "cgb":Units.FARAD.value,
        "csb":Units.FARAD.value,
        "cdb":Units.FARAD.value,
        "cgg":Units.FARAD.value,
        "cdep":Units.FARAD.value,
        "cvar":Units.FARAD.value,
        "gmbs":Units.SIEMENS.value,
        "gm":Units.SIEMENS.value,
        "gds":Units.SIEMENS.value,
        "self_gain":"VV^-01",
        "ft":Units.HERTZ.value,
        "fosc":Units.HERTZ.value,
        "ron":Units.OHM.value,
        "region":"",
        "vdsat":Units.VOLTAGE.value,
    }
    def __init__(
        self,
        name:str="m0",
        type:str="nch",
        vds:float=0.0,
        vsb:float=0.0,
        gmoverid:float=1.0,
        l:float=30*Scale.NANO.value[1],
        id:float=0.0,
        vgs:float=0.0,
        ron:float=0.0,
        cvar:float =0.0
    ):
        self.name=name
        self.type=type
        # input vars
        # varactor 
        self.cvar=cvar if bool(cvar) else None
        #switch
        self.ron = ron if bool(ron) else None
        # cell
        self.vds:float=vds
        self.vsd:float=-vds
        self.vsb:float=vsb
        self.vbs:float=-vsb
        self.gmoverid:float=gmoverid
        self.l:float=l
        self.id:float=id
        # output vars
        self.vgs:float=vgs if bool(vgs) else None
        self.vsg:float=-self.vgs if bool(self.vgs) else None
        self.w:float=None
        self.cgs:float=None
        self.cgd:float=None
        self.cgb:float=None
        self.csb:float=None
        self.cdb:float=None
        self.gmbs:float=None
        self.gm:float=None
        self.gds:float=None
        self.self_gain:float=None
        self.ft:float=None
        self.fosc:float=None
        self.region:float=None
        self.vdsat:float=None
        self.cdep:float=None
        self.cgg:float=None
        
        
    def __str__(self)->str:
        vars = [var for var in dir(self) if not var.startswith('__')]
        vals = [getattr(self, var) for var in vars]
        obj={key:val for (key,val) in zip(vars,vals)}
        result=""
        for var,val in obj.items():
            if type(val)==float:
                result+="{:.2f} ".format(val)
            else:
                result += f"{val} "
        return result

    def __parse_data__(self, key:str, val)->None:
        if key == TomlControlKeywords.DEVICE.value or key == TomlControlKeywords.VARACTOR.value or key == TomlControlKeywords.SWITCH:
            if type(val) != str:
                raise ValueError("Device name must be a string")
            self.name = val
        elif key == TomlControlKeywords.TYPE.value:
            if type(val) != str:
                raise ValueError("Device type must be a string")
            if val not in [TomlControlType.NMOS.value, TomlControlType.PMOS.value]:
                raise ValueError(f"Device type must be \"{TomlControlType.NMOS.value}\" or \"{TomlControlType.PMOS.value}\"")
            self.type = val
        elif key == TomlControlKeywords.CVAR.value:
            if type(val) not in [float, str, int]:
                raise ValueError("Varactor Cap. CVAR must be parsed as a float, integer or string")
            if type(val) == str:
                self.cvar = stof(val)
            else:
                self.cvar = float(val)
        elif key == TomlControlKeywords.RON.value:
            if type(val) not in [float, str, int]:
                raise ValueError("Switch On Resistance RON must be parsed as a float, integer or string")
            if type(val) == str:
                self.ron = stof(val)
            else:
                self.ron = float(val)
        elif key == TomlControlKeywords.VGS.value:
            if self.type != TomlControlType.NMOS.value:
                raise ValueError("VGS value to be specified is only valid for NMOS devices")
            if type(val) not in [float, str, int]:
                raise ValueError("VGS value must parsed as a float, integer or string")
            if type(val) == str:
                self.vgs = stof(val)
                self.vsg = -self.vgs
            else:
                self.vgs = float(val)
                self.vsg = -self.vgs
        elif key == TomlControlKeywords.VSG.value:
            if self.type != TomlControlType.PMOS.value:
                raise ValueError("VSG value to be specified is only valid for PMOS devices")
            if type(val) not in [float, str, int]:
                raise ValueError("VSG value must parsed as a float, integer or string")
            if type(val) == str:
                self.vsg = stof(val)
                self.vgs = -self.vsg
            else:
                self.vsg = float(val)
                self.vgs = -self.vsg
        elif key == TomlControlKeywords.VDS.value:
            if self.type != TomlControlType.NMOS.value:
                raise ValueError("VDS value to be specified is only valid for NMOS devices")
            if type(val) not in [float, str, int]:
                raise ValueError("VDS value must parsed as a float, integer or string")
            if type(val) == str:
                self.vds = stof(val)
                self.vsd = -self.vds
            else:
                self.vds = float(val)
                self.vsd = -self.vds
        elif key == TomlControlKeywords.VSD.value:
            if self.type != TomlControlType.PMOS.value:
                raise ValueError("VSD value to be specified is only valid for PMOS devices")
            if type(val) not in [float, str, int]:
                raise ValueError("VSD value must parsed as a float, integer or string")
            if type(val) == str:
                self.vsd = stof(val)
                self.vds = -self.vsd
            else:
                self.vsd = float(val)
                self.vds = -self.vsd
        elif key == TomlControlKeywords.VSB.value:
            if self.type != TomlControlType.NMOS.value:
                raise ValueError("VSB value to be specified is only valid for NMOS devices")
            if type(val) not in [float, str, int]:
                raise ValueError("Vsb value must parsed as a float, integer or string")
            if type(val) == str:
                self.vsb = stof(val)
                self.vbs = -self.vsb
            else:
                self.vsb = float(val)
                self.vbs = -self.vsb
        elif key == TomlControlKeywords.VBS.value:
            if self.type != TomlControlType.PMOS.value:
                raise ValueError("VBS value to be specified is only valid for PMOS devices")
            if type(val) not in [float, str, int]:
                raise ValueError("VBS value must parsed as a float, integer or string")
            if type(val) == str:
                self.vbs = stof(val)
                self.vsb = -self.vbs
            else:
                self.vbs = float(val)
                self.vsb = -self.vsb
        elif key == TomlControlKeywords.GMOVERID.value:
            if type(val) not in [float, str, int]:
                raise ValueError("Gm/Id value must parsed as a float, integer or string")
            if type(val) == str:
                self.gmoverid = stof(val)
            else:
                self.gmoverid = float(val)
        elif key == TomlControlKeywords.LENGTH.value:
            if type(val) not in [float, str]:
                raise ValueError("Channel Length (L) value must parsed as a float or string")
            if type(val) == str:
                self.l = stof(val)
            else:
                self.l = val
        elif key == TomlControlKeywords.ID.value:
            if type(val) not in [float, str]:
                raise ValueError("Drive Current (Id) value must parsed as a float or string")
            if type(val) == str:
                self.id = stof(val)
            else:
                self.id = val
        else:
            raise ValueError(f"{key} is not a valid control variable for a CMOS device")
                
        
class Devices:
    """_summary_
    A class object ot save all the devices to which
    the gm/id sizing process will be applied, and the output
    specifications of each device
    """
    __slots__=["devices", "varactors", "switches", "spits", "plot", "output_dir"]
    def __init__(self):
        self.devices={}
        self.varactors={}
        self.switches={}
        self.spits=defaultdict(list)
        self.plot=False
        self.output_dir=None
    
    def __data_frame__(self, dev_type="cell")->DataFrame:
        """_summary_
        Converts the device dictionary to a Pandas dataframe
        Returns:
            DataFrame: _description_
        """
        vars = [var for var in dir(MosCell) if not var.startswith('__')]
        columns = [var+"["+MosCell.__UNITS__[var]+"]" for var in vars]
        data = {k:[] for k in columns}
        index = None
        if dev_type == "cell":
            for device in self.devices.values():
                for i,var in enumerate(vars):
                    data[columns[i]].append(getattr(device, var))
            order = ["name", "type", "vds", "vsb", "gmoverid", "l", "w", "id"]
            order = [var+"["+MosCell.__UNITS__[var]+"]" for var in order]
            order = order+[var for var in columns if var not in order]
            index = list(self.devices.keys())
        elif dev_type == "varactor":
            for varactor in self.varactors.values():
                for i,var in enumerate(vars):
                    data[columns[i]].append(getattr(varactor, var))
            order = ["name", "type", "vgs", "l", "w", "cvar"]
            order = [var+"["+MosCell.__UNITS__[var]+"]" for var in order]
            order = order+[var for var in columns if var not in order]
            index = self.varactors.keys()
        elif dev_type == "switch":
            for switch in self.switches.values():
                for i,var in enumerate(vars):
                    data[columns[i]].append(getattr(switch, var))
            order = ["name", "type", "vgs", "l", "w", "ron"]
            order = [var+"["+MosCell.__UNITS__[var]+"]" for var in order]
            order = order+[var for var in columns if var not in order]
            index = self.switches.keys()
        else:
            raise ValueError(f"Unknown device type: {dev_type}")
        return DataFrame(data, index=index)[order]

    def __str__(self) -> str:
        devices_df = self.__data_frame__(dev_type = "cell")
        vars_df = self.__data_frame__(dev_type = "varactor")
        swtchs_df = self.__data_frame__(dev_type = "switch")
        ret = "Devices:\n"
        ret += str(devices_df)+"\n" if not devices_df.empty else "--None--\n"
        ret += "Varactors:\n"
        ret += str(vars_df)+"\n" if not vars_df.empty else "--None--\n"
        ret += "Switches:\n"
        ret += str(swtchs_df)+"\n" if not swtchs_df.empty else "--None--\n"
        return ret
    
    def add(self, device, dev_type = "cell") -> None:
        """_summary_
        Adds a new device to the correct database of
        parsed devices
        Args:
            device (_type_): _description_
            dev_type (str, optional): Device type identifier. Defaults to "cell".

        Raises:
            KeyError: _description_
            ValueError: _description_
        """
        if device.name in list(self.devices.keys()) + list(self.varactors.keys()) + list(self.switches.keys()):
            raise KeyError(f"A device with the name \"{device.name}\" was already parsed.")
        if dev_type == "varactor":
            self.varactors[device.name] = device
        elif dev_type == "cell":
            self.devices[device.name] = device
        elif dev_type == "switch":
            self.switches[device.name] = device
        else:
            raise ValueError(f"Unknown device type: {dev_type}")

    def parse_data(self, data:dict) -> None:
        """_summary_
        Parses the data dictionary and adds the devices to the Devices object
        Args:
            data (dict): Dictionary containing the data to be parsed
        """
        for sec in data.keys():
            if sec == TomlSections.CONTROL.value:
                # get first data input of the control section
                key,token = list(data[sec].items())[0]
                if key == TomlControlKeywords.DEVICE.value:
                    # create a new device
                    device = MosCell(name=token)
                    for key,token in list(data[sec].items())[1:]:
                        device.__parse_data__(key, token)
                    self.add(device, dev_type="cell")
                elif key == TomlControlKeywords.VARACTOR.value:
                    # create a new varactor
                    varactor = MosCell(name=token)
                    for key,token in list(data[sec].items())[1:]:
                        varactor.__parse_data__(key, token)
                    self.add(varactor, dev_type="varactor")
                elif key == TomlControlKeywords.SWITCH.value:
                    # create a new switch
                    switch = MosCell(name=token)
                    for key,token in list(data[sec].items())[1:]:
                        switch.__parse_data__(key, token)
                    self.add(switch, dev_type="switch")
                elif key == TomlControlKeywords.DEVICES.value:
                    devices_names = [n for n in token]
                    for key,token in list(data[sec].items())[1:]:
                        if key not in devices_names:
                            raise ValueError(f"{key} is an unrecognized device name")
                        device = MosCell(name=key)
                        for subkey, subtoken in token.items():
                            device.__parse_data__(subkey, subtoken)
                        self.add(device)
                elif key == TomlControlKeywords.VARACTORS.value:
                    varactors_names = [n for n in token]
                    for key,token in list(data[sec].items())[1:]:
                        if key not in varactors_names:
                            raise ValueError(f"{key} is an unrecognized device name")
                        varactor = MosCell(name=key)
                        for subkey, subtoken in token.items():
                            varactor.__parse_data__(subkey, subtoken)
                        self.add(varactor, dev_type="varactor")
                elif key == TomlControlKeywords.SWITCHES.value:
                    switches_names = [n for n in token]
                    for key,token in list(data[sec].items())[1:]:
                        if key not in switches_names:
                            raise ValueError(f"{key} is an unrecognized device name")
                        switch = MosCell(name=key)
                        for subkey, subtoken in token.items():
                            switch.__parse_data__(subkey, subtoken)
                        self.add(switch, dev_type="switch")
                else:
                    raise ValueError(f"{key} is not a valid key for the first argument of {TomlSections.CONTROL.name} section. First argument must be {TomlControlKeywords.DEVICE.name} or {TomlControlKeywords.DEVICES.name}.")
            elif sec == TomlSections.SPIT.value:
                for key,token in data[sec].items():
                    if key == TomlSpitKeywords.OUTPUTDIR.value:
                        if type(token) != str:
                            raise ValueError(f"{TomlSpitKeywords.OUTPUTDIR.value} must be a string")
                        if not os.path.isdir(token):
                            os.mkdir(token)
                        self.output_dir = token
                    elif key == TomlSpitKeywords.PLOT.value:
                        if type(token) not in [bool, str]:
                            raise ValueError(f"{TomlSpitKeywords.PLOT.value} must be a boolean or a string")
                        if type(token) == str:
                            self.plot = token.lower() == "true"
                        else:
                            self.plot = token
                    elif key == TomlSpitKeywords.VARS.value:
                        acceptable_vars = ['all']
                        [acceptable_vars.append(v) for v in dir(MosCell) if not v.startswith('__')]
                        for subkey, subtoken in token.items():
                            
                            if subkey not in list(self.devices.keys()) + list(self.varactors.keys()) + list(self.switches.keys()):
                                raise ValueError(f"{subkey} is an unrecognized device name. Recognized devices are {list(self.devices.keys()) + list(self.varactors.keys()) + list(self.switches.keys())}")
                            for var in subtoken:    
                                if var not in acceptable_vars:
                                    raise ValueError(f"{var} is an unrecognized variable name")
                                if var != 'all':
                                    self.spits[subkey].append(var)
            else:
                raise ValueError(f"{sec} is not a valid section name")
        if len(self.devices) == 0 and len(self.varactors) == 0 and len(self.switches) == 0:
            raise ValueError("No devices were detected in the TOML setup file")
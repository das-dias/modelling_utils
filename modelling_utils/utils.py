""" ***********************************
* *[author] Diogo André (git-hub : das-dias)
* *[date] 2022-05-05
* *[filename] utils.py
* *[summary] Essential utilities for data processing and representation and other stuff
* ***********************************
"""
import pandas as pd
import itertools
from cycler import cycler
from enum import Enum
import numpy as np
from mpl_toolkits import mplot3d
import matplotlib as mpl
import matplotlib.pyplot as plt
import os
import seaborn as sns
__figs_path__ = os.path.join(os.getcwd(),"figs")
class Units(Enum):
    """_summary_
    Units enumerator
    """
    OHM="\u03A9"#capital Omega letter
    AMPERE="A"
    VOLTAGE="V"
    HERTZ="Hz"
    POWER="W"
    SIEMENS="S"
    FARAD="F"
    HENRY="H"
    METER="m"
    METER_SQR="m^2"
    DECIBEL="dB"
    TIME="s"
class Scale(Enum):
    """_summary_
    Unit scale enumerator
    """
    EXA=('E', pow(10,18))
    PETA=('P', pow(10,15))
    TERA=('T', pow(10,12))
    GIGA=('G', pow(10,9))
    MEGA=('M', pow(10,6))
    KILO=('k', pow(10,3))
    MILI=('m', pow(10,-3))
    MICRO=('u', pow(10,-6))
    NANO=('n', pow(10,-9))
    PICO=('p', pow(10,-12))
    FEMTO=('f', pow(10,-15))
    ATTO=('a', pow(10,-18))

def stof(val: str)->float:
    """_summary_
    Get a value from a string
    Args:
        val (str): String value in the format of "<value> <scale letter>"
    Raises:
        ValueError: invalid scaling factor
    Returns:
        float: the extracted floating point value
    """
    scaling_factor = 1.0
    tokens = val.split(" ")
    res = 0.0
    for token in tokens:
        if token.isnumeric():
            res = float(token)
        else:
            scale_letters = [scale.value[0] for scale in Scale]
            if token not in scale_letters:
                raise ValueError(f"Invalid scaling factor: {token}")
            scaling_factor = [scale.value[1] for scale in Scale if scale.value[0] == token][0]
    res *= scaling_factor
    return res

def timer(func):
    """_summary_
    Decorator to time a function
    Args:
        func (function): function to be timed
    Returns:
        function: the same function, but with a "runtime_ns" (time in nanoseconds) attribute
    """
    import time
    from loguru import logger
    def wrapper(*args, **kwargs):
        start = time.time_ns()
        result = func(*args, **kwargs)
        end = time.time_ns()
        delta = end - start
        func.runtime_ns = delta
        delta_mili = (delta * 1e-6) # obtain time in miliseconds
        mili_secs = f"{Scale.MILI.value[0]}{Units.TIME.value}"
        logger.info(f"\nFunction: {func.__name__}\tRuntime: {delta_mili:.3f} {mili_secs}.")
        return result
    return wrapper

def _set_2D_style():
    sns.set_style('whitegrid') # darkgrid, white grid, dark, white and ticks
    custom_cycler = (
        cycler(color=['r', 'g', 'b', 'y']) +
        cycler(linestyle=['-', '--', ':', '-.'])
    )
    plt.rc("lines", linewidth=4)    # line width
    plt.rc('axes', titlesize=18)     # fontsize of the axes title
    plt.rc('axes', labelsize=14)    # fontsize of the x and y labels
    plt.rc("axes", prop_cycle=custom_cycler) # define a cycler of colours and linestyle
    plt.rc('xtick', labelsize=13)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=13)    # fontsize of the tick labels
    plt.rc('legend', fontsize=13)    # legend fontsize
    plt.rc('font', size=13)          # controls default text sizes
    #define font family to use for all text
    mpl.rcParams['font.family'] = 'serif'

def _plot_graph_2D(
    x, 
    y, 
    label: str=None, 
    xlabel: str=None, 
    ylabel: str=None, 
    title: str=None, 
    filename: str=None,
    legend: bool=False,
    hold_off: bool=False,
    axis=None,
    show: bool=False,
    xlim: tuple=None,
    ylim: tuple=None
    ):
    if not bool(axis):
        axis = plt.axes()
    if not hold_off:
        axis.plot(x, y, label=label)  
        if bool(xlabel):
            axis.set_xlabel(xlabel)
        if bool(ylabel): 
            axis.set_ylabel(ylabel)
        if bool(title):    
            axis.set_title(title)
        if legend:
            axis.legend()
        if not bool(xlim):
            plt.xlim([x[0], x[-1]])
        else:
            plt.xlim([xlim[0], xlim[1]])
        if bool(ylim):
            plt.xlim([ylim[0], ylim[1]])
        if filename is not None:
            if not os.path.exists(__figs_path__):
                os.makedirs(__figs_path__)
            plt.savefig(os.path.join(__figs_path__,filename))
        if show:
            plt.show()
        plt.close()
    else:
        axis.plot(x, y, label=label)
    return axis
    
def _plot_graph_3D(
    x, 
    y, 
    z, 
    xlabel: str=None, 
    ylabel: str=None, 
    zlabel: str=None, 
    title: str=None, 
    filename: str=None, 
    type: str=None,
    show: bool=False
    ):
    # pretty plot
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    type = type if bool(type) else "line"
    if type.lower() in ["line", None]:
        ax.plot3D(x,y,z)
    elif type.lower() == "scatter":
        c = x+y
        ax.scatter(x, y, z, c=c)
    elif type.lower() == "surface":
        ax.plot_surface(x, y, z, cmap="seismic", edgecolor="grey")
    elif type.lower() == "wireframe":
        ax.plot_wireframe(x, y, z, color='blue')
    else:
        raise ValueError(f"Unsupported plot type: {type}")
    
    if title is not None:
        ax.set_title(title)
    if xlabel is not None:
        ax.set_xlabel(xlabel)
    if ylabel is not None:
        ax.set_ylabel(ylabel)
    if zlabel is not None:
        ax.set_label(zlabel)
    if bool(filename):
        if not os.path.exists(__figs_path__):
            os.makedirs(__figs_path__)
        plt.savefig(os.path.join(__figs_path__,filename))
    if show:
        plt.show()
    plt.close()

@timer
def plot_function(
    x, 
    y,
    z = None, 
    labels: list=[], 
    xlabel: str=None, 
    ylabel: str=None,
    zlabel: str=None,
    title: str=None,
    filename: str=None,
    type: str=None,
    show: bool=False,
    xlim: tuple=None,
    ylim: tuple=None
    ):
    """_summary_
    Plots a function in 2D (curve) or 3D space (surface) depending on the parsing of the z variable
    Args:
        x           (np.ndarray / list) : x values
        y           (np.ndarray / list) : y values
        z           (np.ndarray / None) : z values
        labels      (list)              : list of labels for the plot
        xlabel      (str)               : abciss axis title
        ylabel      (str)               : ordinate axis title
        zlabel      (str)               : ordinate axis title
        title       (str)               : title of the plot
        filename    (str)               : name of the file to save the plot
        type        (str)               : type of 3D plot to be made. Options : "line", "scatter", "surface", "wireframe" 
        line_style  (str)               : line style to be used for the 2D plot
    """
    _set_2D_style()
    if not all([isinstance(label, str) for label in labels]):
        raise TypeError("Labels should be strings")
    if not isinstance(z, np.ndarray):
        if isinstance(y, np.ndarray):
            _plot_graph_2D(
                x, y,
                label = labels[0] if len(labels)>0 else None,
                xlabel=xlabel, 
                ylabel=ylabel, 
                title=title, 
                filename=filename,
                show=show,
                xlim=xlim,
                ylim=ylim
                )
        elif isinstance(y, list):
            if len(labels) not in [len(y), 0]:
                raise ValueError("Labels and y values should have the same length or no labels at all")
            if not all([isinstance(i, np.ndarray) for i in y]):
                raise ValueError("y must be a list of numpy.ndarray")
            if isinstance(x, list):
                if not all([isinstance(i, np.ndarray) for i in x]):
                    raise ValueError("x must be a list of numpy.ndarray")
                funcs = list(zip(x, y))
                axis = None
                for i, xy in enumerate(funcs[:-1]):
                    x_vec, y_vec = xy
                    axis = _plot_graph_2D(
                        x_vec, y_vec,
                        label = labels[i] if len(labels)>0 else None,
                        xlabel=xlabel, 
                        ylabel=ylabel, 
                        title=title, 
                        filename=filename, 
                        legend=False,
                        hold_off= True,
                        axis=axis
                    )
                x_vec, y_vec = funcs[-1]
                _plot_graph_2D(
                    x_vec, y_vec,
                    label = labels[-1] if len(labels)>0 else None,
                    xlabel=xlabel, 
                    ylabel=ylabel, 
                    title=title, 
                    filename=filename,
                    legend=True,
                    hold_off= False,
                    show=show,
                    axis=axis,
                    xlim=xlim,
                    ylim=ylim
                )
            elif isinstance(x, np.ndarray):
                axis = None
                for i, y_vec in enumerate(y[:-1]):
                    axis = _plot_graph_2D(
                        x, y_vec,
                        label = labels[i] if len(labels)>0 else None, 
                        xlabel=xlabel, 
                        ylabel=ylabel, 
                        title=title, 
                        filename=filename,
                        legend=False,
                        hold_off= True,
                        axis=axis
                    )
                y_vec = y[-1]
                _plot_graph_2D(
                    x, y_vec,
                    label = labels[-1] if len(labels)>0 else None,
                    xlabel=xlabel, 
                    ylabel=ylabel, 
                    title=title, 
                    filename=filename,
                    legend=True,
                    hold_off= False,
                    show=show,
                    axis=axis,
                    xlim=xlim,
                    ylim=ylim
                )
            else:
                raise ValueError("x must be a list of numpy.ndarray or a numpy.ndarray")
        else:
            raise ValueError("y must be a list of numpy.ndarray or a numpy.ndarray")
    else :
        if not all([isinstance(v, np.ndarray) for v in [x,y,z]]):
            raise TypeError("All vectors must be of type numpy.ndarray")
        _plot_graph_3D(
            x, y, z, 
            xlabel=xlabel, 
            ylabel=ylabel, 
            zlabel=zlabel, 
            title=title, 
            filename=filename, 
            type=type,
            show=show
        )

@timer
def plot_hist(data, labels: list=[], xlabel: str=None, title: str=None, filename: str=None, show:bool=False, stat: str="probability"):
    """_summary_
    Plots a histogram of the data
    Args:
        data        (np.ndarray / list) : data to be plotted 
        labels      (list, optional)    : Data labels. Defaults to [].
        title       (str, optional)     : Title of the histogram plot. Defaults to None.
        filename    (str, optional)     : Name of the figure to save the histogram. Defaults to None.
    Raises:
        TypeError: _description_
        ValueError: _description_
        ValueError: _description_
        TypeError: _description_
    """
    _set_2D_style()
    if not all([isinstance(label, str) for label in labels]):
        raise TypeError("Labels should be strings")
    
    if isinstance(data, np.ndarray):
        sns.histplot(
            data=data,
            kde=True,
            binwidth = 0.05,
            stat=stat,
        ).set_xlabel(xlabel)
    elif isinstance(data, list):
        if len(labels) not in [len(data), 0]:
            raise ValueError("Labels and data must have the same length")
        
        if not all([isinstance(v, np.ndarray) for v in data]):
            raise ValueError("data must be a list of numpy.ndarray")
        dt = data
        if len(labels) != 0:
            dt = {label: v for label, v in zip(labels, data)}
        colours = [
            "#000000",
            "#D84242",
            "#4131F0",
            "#FF0000",
            "#D80AD0"
        ]
        sns.histplot( 
            data=dt, 
            kde=True, 
            binwidth=0.05,
            legend=True, 
            stat=stat,
            palette=[c for c,_ in zip(itertools.cycle(colours), dt.keys())]
        ).set_xlabel(xlabel)
    else:
        raise TypeError("data must be a numpy.ndarray or a list of numpy.ndarray")
    if bool(title):
        plt.title(title)
    if bool(filename):
        if not os.path.exists(__figs_path__):
            os.makedirs(__figs_path__)
        plt.savefig(os.path.join(__figs_path__,filename))
    if show:
        plt.show()
    plt.close()
    
def transform_dataset(lut: pd.DataFrame) -> pd.DataFrame:
    """_summary_
    Transforms the received look up table to
    include the Vds, vbs and L sweep as table columns
    Args:
        df (pd.DataFrame): imported look up 
                            table with the DC OP of 
                            the transistor
    Returns:
        pd.DataFrame: The modified, multi-space look up table
    """
    
""" ***********************************
* *[author] Diogo André (git-hub : das-dias)
* *[date] 2022-05-05
* *[filename] utils.py
* *[summary] Essential utilities for data processing and representation and other stuff
* ***********************************
"""
__figs_path__ = "/figs"

__line_styles__ = [
    "o-",
    "-.",
    "*-",
    ":",
    "-"
]
import itertools
from enum import Enum
import numpy as np
from mpl_toolkits import mplot3d
import matplotlib as mpl
import matplotlib.pyplot as plt
import os
import seaborn as sns

class Units(Enum):
    """
    Enum containing the units of the devices
    """
    VOLTAGE = "V"
    OHM = "Ω"
    CELSIUS = "°C"
    KELVIN = "K"
    TIME = "s"
    FREQUENCY = "Hz"
    FARAD = "F"
    HENRY = "H"
    AMPERE = "A"

class Scale(Enum):
    """
    Enum containing the scales of the units
    """
    GIGA = ("G", 1e9)
    MEGA = ("M", 1e6)
    KILO = ("k", 1e3)
    MILI = ("m", 1e-3)
    MICRO = ("u", 1e-6)
    NANO = ("n", 1e-9)
    PICO = ("p", 1e-12)
    FENTO = ("f", 1e-15)

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

def set_2D_style():
    #define font family to use for all text
    mpl.rcParams['font.family'] = 'serif'
    sns.set_style('whitegrid') # darkgrid, white grid, dark, white and ticks
    plt.rc('axes', titlesize=18)     # fontsize of the axes title
    plt.rc('axes', labelsize=14)    # fontsize of the x and y labels
    plt.rc('xtick', labelsize=13)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=13)    # fontsize of the tick labels
    plt.rc('legend', fontsize=13)    # legend fontsize
    plt.rc('font', size=13)          # controls default text sizes

def _plot_graph_2D(
    x, 
    y, 
    label: str=None, 
    xlabel: str=None, 
    ylabel: str=None, 
    title: str=None, 
    filename: str=None, 
    line_style: str=__line_styles__[0],
    legend: bool=False,
    hold_off: bool=False,
    axis=None
    ):
    # pretty plot
    if not bool(axis):
        ax = plt.axes()
    if not hold_off:
        ax.plot(x, y, linestyle=line_style)  
        if bool(xlabel):
            ax.xlabel(xlabel)
        if bool(ylabel): 
            ax.ylabel(ylabel)
        if bool(title):    
            ax.title(title)
        if legend:
            ax.legend()
        if filename is not None:
            if not os.path.exists(__figs_path__):
                os.makedirs(__figs_path__)
            plt.savefig(os.path.join(__figs_path__,filename))
        plt.show()
        plt.close()
    else:
        ax = axis.plot(x, y, label=label, linestyle=line_style)
    return ax
    
def _plot_graph_3D(
    x, 
    y, 
    z, 
    xlabel: str=None, 
    ylabel: str=None, 
    zlabel: str=None, 
    title: str=None, 
    filename: str=None, 
    type: str=None
    ):
    # pretty plot
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    if type.lower() in ["surface", None]:
        ax.plot_surface(x, y, z, cmap="seismic", edgecolor="grey")
    elif type.lower() is "wireframe":
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
    line_style: str=__line_styles__[0]
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
        type        (str)               : type of 3D plot to be made. Options : "surface", "wireframe" 
        line_style  (str)               : line style to be used for the 2D plot
    """
    if not all([isinstance(label, str) for label in labels]):
        raise TypeError("Labels should be strings")
    if not bool(z):
        if isinstance(y, np.ndarray):
            _plot_graph_2D(
                x, y,
                label = labels[0] if len(labels)>0 else None,
                xlabel=xlabel, 
                ylabel=ylabel, 
                title=title, 
                filename=filename, 
                line_style=line_style
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
                line_style = itertools.cycle(__line_styles__)
                for i, x_vec, y_vec in enumerate(funcs[:-1]):
                    _plot_graph_2D(
                        x_vec, y_vec,
                        label = labels[i] if len(labels)>0 else None,
                        xlabel=xlabel, 
                        ylabel=ylabel, 
                        title=title, 
                        filename=filename,
                        line_style=line_style, 
                        legend=False,
                        hold_off= True
                    )
                    line_style = next(line_style)
                x_vec, y_vec = funcs[-1]
                _plot_graph_2D(
                    x_vec, y_vec,
                    label = labels[-1] if len(labels)>0 else None,
                    xlabel=xlabel, 
                    ylabel=ylabel, 
                    title=title, 
                    filename=filename, 
                    line_style=line_style, 
                    legend=True,
                    hold_off= False
                )
            elif isinstance(x, np.ndarray):
                line_style = itertools.cycle(__line_styles__)
                for i, y_vec in enumerate(y[:-1]):
                    _plot_graph_2D(
                        x, y_vec,
                        label = labels[i] if len(labels)>0 else None, 
                        xlabel=xlabel, 
                        ylabel=ylabel, 
                        title=title, 
                        filename=filename, 
                        line_style=line_style, 
                        legend=False,
                        hold_off= True
                    )
                    line_style = next(line_style)
                y_vec = y[-1]
                _plot_graph_2D(
                    x, y_vec,
                    label = labels[-1] if len(labels)>0 else None,
                    xlabel=xlabel, 
                    ylabel=ylabel, 
                    title=title, 
                    filename=filename, 
                    line_style=line_style, 
                    legend=True,
                    hold_off= False
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
            type=type
        )

@timer
def plot_hist(data, labels: list=[], title: str=None, filename: str=None):
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
    if not all([isinstance(label, str) for label in labels]):
        raise TypeError("Labels should be strings")
    
    if isinstance(data, np.ndarray):
        sns.histplot(
            data, 
            x = labels[0] if len(labels)>0 else None,
            binwidth = 0.05
        )
    elif isinstance(data, list):
        if len(labels) not in [len(data), 0]:
            raise ValueError("Labels and data must have the same length")
        
        if not all([isinstance(v, np.ndarray) for v in data]):
            raise ValueError("data must be a list of numpy.ndarray")
    
        sns.histplot( data, hue=labels, binwidth=0.05)
    else:
        raise TypeError("data must be a numpy.ndarray or a list of numpy.ndarray")
    
    if bool(title):
        plt.title(title)
    if bool(filename):
        if not os.path.exists(__figs_path__):
            os.makedirs(__figs_path__)
        plt.savefig(os.path.join(__figs_path__,filename))
    plt.show()
    plt.close()
    
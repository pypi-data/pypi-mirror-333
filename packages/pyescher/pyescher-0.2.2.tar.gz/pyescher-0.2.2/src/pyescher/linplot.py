from __future__ import annotations

from typing import Callable, Literal
from itertools import cycle
import numpy as np
from abc import ABC, abstractmethod
import matplotlib as mpl
import matplotlib.pyplot as plt
from functools import wraps
from loguru import logger

SOLID_MARKERS = ('o','s','v','X','D','p')
THIN_MARKERS = (',','1','+','x','|')
NOLEGEND = '_nolegend_'

class Cyclable(ABC):

    def __init__(self):
        pass

    @property
    def CYCLE(cls) -> list:
        pass

def pick(value: any, default: any) -> any:
    if value is None:
        return default
    return value

class ColorDefinitions(Cyclable):
    BLACK: tuple[float,float,float,float] = (0,0,0,1)
    BLUE: tuple[float,float,float,float] = (0,0,0.8,1)
    RED: tuple[float,float,float,float] = (0.8,0,0,1)
    GREEN: tuple[float,float,float,float] = (0,0.5,0,1)
    YELLOW: tuple[float,float,float,float] = (0.6,0.6,0,1)
    CYAN: tuple[float,float,float,float] = (0.,0.6,0.6,1)
    MAGENTA: tuple[float,float,float,float] = (0.8,0,0.8,1)

    @property
    def CYCLE(self) -> list[tuple[float,float,float,float]]:
        return [self.BLUE, self.GREEN, self.RED, self.YELLOW, self.CYAN, self.MAGENTA]
    
    @classmethod
    def get(cls, color_name: str) -> tuple[float, float, float, float] | None:
        """Returns the corresponding color tuple for a given color name or abbreviation."""
        color_name = color_name.strip().lower()  # Normalize input

        # Mapping of possible inputs to actual class attributes
        color_map = {
            "black": cls.BLACK,
            "k": cls.BLACK,
            "blue": cls.BLUE,
            "b": cls.BLUE,
            "red": cls.RED,
            "r": cls.RED,
            "green": cls.GREEN,
            "g": cls.GREEN,
            "yellow": cls.YELLOW,
            "y": cls.YELLOW,
            "cyan": cls.CYAN,
            "c": cls.CYAN,
            "magenta": cls.MAGENTA,
            "m": cls.MAGENTA
        }

        if color_name not in color_map:
            logger.warning(f'No definition for color name "{color_name}", defaulting to black')
            return cls.BLACK
        else:
            return color_map.get(color_name)  # Returns None if not found
    
    @classmethod
    def interpret(cls, color: str | tuple) -> tuple:
        if isinstance(color, str):
            return cls.get(color)
        else:
            return color
    
DEFAULT_COLOR_DEFINITIONS = ColorDefinitions()

############## CLASSES

class PlotObject:
    MAX_SIZE = 1e30

    @property
    def y(self) -> np.ndarray:
        # Returns all numbers and clips the data to the plot objects limits
        # Also removes nan values by replacing them with zeros
        if self._transformation is None:
            
            return np.nan_to_num(np.clip(self._y, -self.MAX_SIZE, self.MAX_SIZE))
        else:
            return np.nan_to_num(np.clip(self._transformation(self._y), -self.MAX_SIZE, self.MAX_SIZE))
    
    @property
    def x(self) -> np.ndarray:
        return np.clip(self._x, -self.MAX_SIZE, self.MAX_SIZE)
    
    def __add__(self, other: PlotObject) -> PlotObject:
        if not isinstance(other, PlotObject):
            return TypeError(f'Only Line objects can be added to other Line objects, not of type {type(other)}')
        if not self._x == other._x:
            return ValueError(f'Cannot add two PlotObjects with dissimilar x-axes data')
        self._y = self._y + other._y
        return self
    
    def __sub__(self, other: PlotObject) -> PlotObject:
        if not isinstance(other, PlotObject):
            return TypeError(f'Only PlotObject objects can be subtracted from another PlotObject object, not of type {type(other)}')
        if not self._x == other._x:
            return ValueError(f'Cannot subtract two PlotObjects with dissimilar x-axes data')
        self._y = self._y - other._y
        return self
    
    def __len__(self) -> int:
        return len(self._y)
    
    def __mul__(self, other: PlotObject) -> PlotObject:
        if not isinstance(other, Line):
            return TypeError(f'Only PlotObject objects can be multiplied with another PlotObject object, not of type {type(other)}')
        if not self._x == other._x:
            return ValueError(f'Cannot multiply two PlotObjects with dissimilar x-axes data')
        self._y = self._y * other._y
        return self
    
    def set_default(self, **kwargs):
        for key, value in kwargs.items():
            if value is None:
                continue
            else:
                object.__setattr__(self,'_' +  key,value)
    
    def transform(self, transformer: Callable) -> PlotObject:
        self._y = transformer(self._y)
        return self

class Line(PlotObject):

    def __init__(self, 
                 xdata: np.ndarray, 
                 ydata: np.ndarray,
                 linestyle: str = None,
                 color: tuple[float,float,float,float] = None,
                 marker: str = None,
                 marker_size: float = 8,
                 width: float = 1.5,
                 label: str = NOLEGEND,
                 transformation: Callable = None):
        self._x: np.ndarray = xdata
        self._y: np.ndarray = ydata
        self._ls: str = linestyle
        self._col: tuple[float,float,float,float] = color
        self._marker: str = marker
        self._marker_size: float = marker_size
        self._width: float = width
        self._label: str = label
        self._transformation: Callable = transformation
    
    def set(self, 
                linestyle: str = None,
                color: tuple[float,float,float,float] = None,
                marker: str = None,
                markersize: float = 8,
                width: float = 1.5,
                ):
        self._ls: str = linestyle
        self._col: tuple[float,float,float,float] = color
        self._marker: str = marker
        self._marker_size: float = markersize
        self._width: float = width

class Scatter(PlotObject):
    def __init__(self, 
                 xdata: np.ndarray, 
                 ydata: np.ndarray,
                 size: float = 1.5,
                 color: tuple[float,float,float,float] = None,
                 label: str = NOLEGEND,
                 transformation: Callable = None):
        self._x: np.ndarray = xdata
        self._y: np.ndarray = ydata
        self._col: tuple[float,float,float,float] = color
        self._size: float = size
        self._label: str = label
        self._transformation: Callable = transformation

class PropertyCycler:

    property: str = 'none'
    def __init__(self):
        self.default_cycle_source: Cyclable = None
        self.default_properties: list = [None,]
        self.default_cycler: cycle = cycle(self.default_properties)
        self.active_cycler: cycle = None
        self.cycle: bool = False
        self.cycle_period: int = None
        self._active_cycler_data = None

    def reset_default(self) -> None:
        if self.default_cycle_source is not None:
            self.default_properties = self.default_cycle_source.CYCLE
        
        if isinstance(self.cycle_period,int):
            self._active_cycler_data = self.default_properties[:self.cycle_period]
        else:
            self._active_cycler_data = self.default_properties

        if not self.cycle:
            self._active_cycler_data = [self.default,]

        self.reset_cycle()

    def set_default(self, properties: list) -> None:
        self.default_properties = properties
    
    def reset_cycle(self) -> None:
        self.default_cycler = cycle(self._active_cycler_data)

    def initialize_cycler(self, lines: list[Line]) -> None:
        self.reset_default()
        content = []
        for line in lines:
            info = line.__getattribute__(self.property)
            if info is None:
                content.append(next(self.default_cycler))
            else:
                content.append(info)
        self.active_cycler = cycle(content)
        
    def get(self):
        return next(self.active_cycler)
        
class ColorCycler(PropertyCycler):
    property = '_col'
    def __init__(self):
        super().__init__()
        self.default_cycle_source: Cyclable = DEFAULT_COLOR_DEFINITIONS
        self.default: tuple[float,float,float,float] = (0,0,0,1)
        self.default_cycler: cycle = cycle(self.default_properties)
        self.active_cycler: cycle = None
        self.cycle: bool = True
        self.cycle_period: int = None

class StyleCycler(PropertyCycler):
    property = '_ls'
    def __init__(self):
        super().__init__()
        self.default_properties: list[str] = ['-','--',':','-.']
        self.default: str = '-'
        self.default_cycler: cycle = cycle(self.default_properties)
        self.active_cycler: cycle = None
        self.cycle: bool = False
        self.cycle_period: int = None

class MarkerCycler(PropertyCycler):
    property = '_marker'
    def __init__(self):
        super().__init__()
        self.default_properties: list[str] = SOLID_MARKERS
        self.default: str = 'o'
        self.default_cycler: cycle = cycle(self.default_properties)
        self.active_cycler: cycle = None
        self.cycle: bool = False
        self.cycle_period: int = None


################ DEFAULT CYCLERS


DEFAULT_COLOR_CYCLER = ColorCycler()

DEFAULT_STYLE_CYCLER = StyleCycler()

DEFAULT_MARKER_CYCLER = MarkerCycler()
DEFAULT_MARKER_COLOR_CYCLER = ColorCycler()
DEFAULT_MARKER_EDGE_COLOR_CYCLER = ColorCycler()


############### PLOT FUNCTIONS

def temprary_settings(func):
    """Decorator to save, reset, and restore Matplotlib settings around a function call."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Save current settings
        saved_rcParams = mpl.rcParams.copy()

        try:
            # Reset to default settings
            mpl.rcParams.update(mpl.rcParamsDefault)
            
            # Call the wrapped function
            result = func(*args, **kwargs)
            
        finally:
            # Restore original settings
            mpl.rcParams.update(saved_rcParams)

        return result

    return wrapper


############## Simple lines

def horizontal(xs: np.ndarray, height: float, 
               width: float = 1.5,
               linestyle: str = '-',
               marker: str = 'none',
               color: str = 'k') -> Line:
    return Line(xs, np.ones_like(xs)*height, linestyle=linestyle, color=color, width=width, marker=marker, label=NOLEGEND)



#########################

def copy_axes_to_clipboard(fig) -> None:
    logger.warning(f'Clipboard functionality not yet implemented')
    return None


@temprary_settings
def plot_lines(*plotobjects: list[PlotObject], 
               xlabel: str = 'x-ax',
               ylabel: str = 'y-ax',
               title: str = None,
               xlim: tuple[float, float] = None,
               ylim: tuple[float, float] = None,
               xmin: float = None,
               xmax: float = None,
               ymin: float = None,
               ymax: float = None,
               grid: bool = False,
               linecolor: tuple[float,float,float,float] | str = None,
               show_marker: bool = False,
               marker_edge: bool = False,
               marker_size: float = None,
               marker_edge_width: float = 1,
               nmarkers: int = None,
               cycle_colors: bool = True,
               cycle_linestyle: bool = False,
               cycle_markers: bool = False,
               cycle_marker_colors: bool = False,
               cycle_marker_edge_colors: bool = False,
               transformation: Callable = None,
               filename: str = None,
               display: bool = True,
               size: Literal['normal','small','wide','narrow','thin','sliver'] = 'normal',
               clipboard: bool = False,):

    fig, ax = plt.subplots(1,1)

    lines = [obj for obj in plotobjects if isinstance(obj,Line)]
    scatters = [obj for obj in plotobjects if isinstance(obj,Scatter)]

    for obj in plotobjects:
        obj.set_default(transformation=transformation)

    for line in lines:
        line.set_default(color=linecolor,
                 marker_size=marker_size)
        

    ### COLOR SETUP
    DEFAULT_COLOR_CYCLER.cycle = cycle_colors
    DEFAULT_COLOR_CYCLER.initialize_cycler(lines)
    
    ### Linestyle Setup
    DEFAULT_STYLE_CYCLER.cycle = cycle_linestyle
    DEFAULT_STYLE_CYCLER.initialize_cycler(lines)

    ### Marker Setup
    DEFAULT_MARKER_CYCLER.cycle = cycle_markers
    DEFAULT_MARKER_CYCLER.initialize_cycler(lines)
    DEFAULT_MARKER_COLOR_CYCLER.cycle = cycle_marker_colors
    DEFAULT_MARKER_COLOR_CYCLER.initialize_cycler(lines)
    DEFAULT_MARKER_EDGE_COLOR_CYCLER.cycle = cycle_marker_edge_colors
    DEFAULT_MARKER_EDGE_COLOR_CYCLER.initialize_cycler(lines)
    
    if marker_edge is False:
        marker_edge_width = 0

    pxmin = np.inf
    pxmax = -np.inf
    pymin = np.inf
    pymax = -np.inf

    for line in lines:
        
        pxmin = min(pxmin, np.min(line._x))
        pxmax = max(pxmax, np.max(line._x))
        pymin = min(pymin, np.min(line.y))
        pymax = max(pymax, np.max(line.y))


        if nmarkers is None:
            markevery = 1
        else:
            markevery = len(line)//nmarkers
            
        marker = DEFAULT_MARKER_CYCLER.get()
        marker_style = dict(
            marker=marker,
            markeredgewidth=marker_edge_width,
            markeredgecolor=ColorDefinitions.interpret(DEFAULT_MARKER_EDGE_COLOR_CYCLER.get()),
            markersize=line._marker_size,
            markerfacecolor=ColorDefinitions.interpret(DEFAULT_MARKER_COLOR_CYCLER.get()),
            markevery=markevery,
        )

        if not show_marker:
            marker_style = dict()

        color = ColorDefinitions.interpret(DEFAULT_COLOR_CYCLER.get())

        ax.plot(line._x, line.y, 
                color=color, 
                label=line._label,
                linestyle=DEFAULT_STYLE_CYCLER.get(),
                linewidth=line._width, 
                **marker_style,
                )

    ### COLOR SETUP
    DEFAULT_COLOR_CYCLER.cycle = cycle_colors
    DEFAULT_COLOR_CYCLER.initialize_cycler(scatters)

    for line in scatters:
        
        pxmin = min(pxmin, np.min(line._x))
        pxmax = max(pxmax, np.max(line._x))
        pymin = min(pymin, np.min(line.y))
        pymax = max(pymax, np.max(line.y))
            
        color = ColorDefinitions.interpret(DEFAULT_COLOR_CYCLER.get())
        ax.scatter(line._x, line.y, 
                color=color, 
                label=line._label,
                )
        
    spine_width = 1.5

    xlim = pick(xlim, (pick(xmin,pxmin),pick(xmax,pxmax)))
    ylim = pick(ylim, (pick(ymin,pymin),pick(ymax,pymax)))

    ax.set_xlim(xlim)
    ax.set_ylim(ylim)

    ax.minorticks_on()
    # Set tick direction for both major and minor ticks
    ax.tick_params(axis='both', which='major', width=1.5, direction='in', length=8, top=True, bottom=True, left=True, right=True)
    ax.tick_params(axis='both', which='minor', width=1.5, direction='in', length=4, top=True, bottom=True, left=True, right=True)

    if grid:
        # Set major grid to faint grey solid lines
        ax.grid(visible=grid, which='major', linestyle='-', color='grey', alpha=0.3)

        # Set minor grid to faint grey dotted lines
        ax.grid(visible=grid, which='minor', linestyle=':', color='grey', alpha=0.3)
    else:
        ax.grid(False, which='major')
        ax.grid(False, which='minor')

    ax.spines["top"].set_linewidth(spine_width)
    ax.spines["right"].set_linewidth(spine_width)
    ax.spines["bottom"].set_linewidth(spine_width)  # Different width
    ax.spines["left"].set_linewidth(spine_width)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    if title is not None:
        ax.set_title(title)

    ax.legend([line._label for line in lines], frameon=True, framealpha=1, edgecolor="black", facecolor="white")

    A4_width, A4_height = 8.27, 11.69  # A4 size in inches
    
    size_mapping = {
        "normal": (A4_width * 0.8, A4_height * 0.4),  # Default aspect ratio
        "small": (A4_width * 0.5, A4_height * 0.25),   # Smaller size
        "wide": (A4_width * 0.9, A4_height * 0.25),    # Wider but not too tall
        "narrow": (A4_width * 0.4, A4_height * 0.8),
        "thin": (A4_width * 0.7, A4_height * 0.18),
        "sliver": (A4_width * 0.2, A4_height * 0.4)   # Taller than normal
    }

    figsize = size_mapping.get(size, size_mapping["normal"])

    fig.set_size_inches(figsize)

    if clipboard:
        copy_axes_to_clipboard(fig)

    if filename is not None:
        plt.savefig(filename, bbox_inches='tight')
    
    if display:
        plt.show()
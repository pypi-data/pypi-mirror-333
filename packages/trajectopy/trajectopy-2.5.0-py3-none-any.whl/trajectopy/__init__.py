import logging

from rich.logging import RichHandler

logging.basicConfig(
    format="%(message)s",
    level=logging.INFO,
    handlers=[RichHandler(omit_repeated_times=False, log_time_format="%Y-%m-%d %H:%M:%S")],
)


__version__ = "2.5.0"


from trajectopy import settings
from trajectopy.alignment import *
from trajectopy.evaluation import *
from trajectopy.matching import *
from trajectopy.merging import *
from trajectopy.plotting import *
from trajectopy.pointset import PointSet
from trajectopy.report import *
from trajectopy.rotationset import RotationSet
from trajectopy.sorting import *
from trajectopy.trajectory import Trajectory

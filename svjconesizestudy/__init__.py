import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gROOT.ProcessLine("gErrorIgnoreLevel = kError;")
ROOT.gStyle.SetOptStat(0)

from .logger import setup_logger
setup_logger()

from . import utils
from . import rootutils
from .event import *
from .dataformats import *
from .datacontainers import *

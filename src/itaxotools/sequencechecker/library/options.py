#!/usr/bin/env python3

from enum import Enum, auto

from PySide6.QtUiTools import QUiLoader


class Option(Enum):
    CountSequences = auto()
    MeanMinMax = auto()
    ACGTpercent = auto()
    MissingPercent = auto()
    CountEmpty = auto()
    ListMissingOnly = auto()
    ListUnaligned = auto()
    ListEmtpy = auto()
    Detailed = auto()

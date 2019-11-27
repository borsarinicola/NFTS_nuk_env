import hiero.core
import hiero.ui
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *


class set12(QAction):
    def __init__(self):
        sel = hiero.selectedItems
        x = 0 
        for each in sel: 
            if x < len(sel):
                sel[x].setFramerate(12)
                x = x+1

                
class set12_5(QAction):
    def __init__(self):
        sel = hiero.selectedItems
        x = 0 
        for each in sel: 
            if x < len(sel):
                sel[x].setFramerate(12.5)
                x = x+1

class set15(QAction):
    def __init__(self):
        sel = hiero.selectedItems
        x = 0 
        for each in sel: 
            if x < len(sel):
                sel[x].setFramerate(15)
                x = x+1


class set24(QAction):
    def __init__(self):
        sel = hiero.selectedItems
        x = 0 
        for each in sel: 
            if x < len(sel):
                sel[x].setFramerate(24)
                x = x+1

                
class set25(QAction):
    def __init__(self):
        sel = hiero.selectedItems
        x = 0 
        for each in sel: 
            if x < len(sel):
                sel[x].setFramerate(25)
                x = x+1

class set30(QAction):
    def __init__(self):
        sel = hiero.selectedItems
        x = 0 
        for each in sel: 
            if x < len(sel):
                sel[x].setFramerate(30)
                x = x+1

                
class set48(QAction):
    def __init__(self):
        sel = hiero.selectedItems
        x = 0 
        for each in sel: 
            if x < len(sel):
                sel[x].setFramerate(48)
                x = x+1

class set50(QAction):
    def __init__(self):
        sel = hiero.selectedItems
        x = 0 
        for each in sel: 
            if x < len(sel):
                sel[x].setFramerate(50)
                x = x+1

                
class set60(QAction):
    def __init__(self):
        sel = hiero.selectedItems
        x = 0 
        for each in sel: 
            if x < len(sel):
                sel[x].setFramerate(60)
                x = x+1
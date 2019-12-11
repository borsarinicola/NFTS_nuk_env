import hiero.core
import hiero.ui

def set(framerate):
	sel = hiero.selectedItems
	x = 0 
	for each in sel: 
	    if x < len(sel):
	        sel[x].setFramerate(framerate)
	        x = x+1
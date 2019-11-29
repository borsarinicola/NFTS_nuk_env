####################################
#Nicola Borsari nLabelShortcut - 29 November 2019 - v1.0


'''

This script allows to write the $gui expression in the disable knob of the selected node
Using it again or on animated disable nodes will reset value to 0

'''


import nuke




def nDollargui():
    selection = nuke.selectedNodes() #store selection into list
    x = 0 #counter for loop
   
    for each in selection:
        processing = selection[x]
   
        if x <= len(selection):
   
            x = x+1 

            if processing.knob('disable').isAnimated() == False:
                processing.knob('disable').setExpression('$gui')

            else:
                processing.knob('disable').clearAnimated()
                processing.knob('disable').setValue(0)

    return
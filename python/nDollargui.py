####################################
#Nicola Borsari nLabelShortcut - 23 November 2021 - v1.1


'''

This script allows to write the $gui expression in the disable knob of the selected node
Using it again or on animated disable nodes will reset value to 0

'''


import nuke



def nDollargui():
    selection = nuke.selectedNodes() #store selection into list
   
    for node in selection:
        if node.knob('disable').isAnimated() == False:
            node.knob('disable').setExpression('$gui')

        else:
            node.knob('disable').clearAnimated()
            node.knob('disable').setValue(0)

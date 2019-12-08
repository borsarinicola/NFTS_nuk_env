####################################
#Nicola Borsari nLabelShortcut - 8 December 2019 - v3.5

import nuke


def nLabelShortcut():

    selection = nuke.selectedNodes() #store selection into list

    for x in selection:

        #storing selected node name into variable
        selectionName = x.knob('name').getValue()

        #storing node existing lable into variable
        oldLabel = x.knob('label').getValue()

        #asking for new label while autofilling with the existing one
        INlabel = nuke.getInput("New Label for " + selectionName, oldLabel)

        #set 
        x.knob('label').setValue(INlabel)          

    return
####################################
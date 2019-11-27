####################################
#Nicola Borsari nLabelShortcut - 17 August 2019 - v3.0

import nuke
import os
import os.path
import nukescripts

def nLabelShortcut():

    selection = nuke.selectedNodes() #store selection into list
    x = 0 #counter for loop

    for each in selection:
        processing = selection[x]

        if x <= len(selection):

            x = x+1

            #clear selection and prepare a new one for processing 
            nukescripts.clear_selection_recursive()
            processing.knob("selected").setValue(True)

            #storing selected node name into variable
            selectionName = nuke.selectedNode().knob('name').getValue()

            #storing node existing lable into variable
            oldLabel = nuke.selectedNode().knob('label').getValue()

            #asking for new label while autofilling with the existing one
            INlabel = nuke.getInput("New Label for " + selectionName, oldLabel)

            #set 
            nuke.selectedNode().knob('label').setValue(INlabel)          
    
        else:

            break    

    return
####################################
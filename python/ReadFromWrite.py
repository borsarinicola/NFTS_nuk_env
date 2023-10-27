import nuke
import os
import os.path
import nukescripts

def ReadFromWrite():

    selected = nuke.selectedNode()
    if selected.Class() == "Write":
        if selected["use_limit"].value() is True:
            first_frame = selected["first"].value()
            last_frame = selected["last"].value()
        else:
            first_frame = nuke.Root()["first_frame"].value()
            last_frame = nuke.Root()["last_frame"].value()

        read = nuke.nodes.Read(
            file=selected["file"].value(),
            colorspace=selected["colorspace"].value(),
            first=first_frame,
            last=last_frame,
            origfirst=nuke.Root()["first_frame"].value(),
            origlast=nuke.Root()["last_frame"].value())
        read.setXpos(selected.xpos()+100)
        read.setYpos(selected.ypos())
    else:
        nuke.message("Please select a Write node.")
    return
####################################

"""
NFTS - National Film and Television School.
latest update by Nicola Borsari: 2023-10-24
"""

####################################

# Import standard Python modules.

import os
import nuke  # pylint: disable=import-error
import nukescripts  # pylint: disable=import-error

####################################

# Import Custom Python scripts.

# pylint: disable=import-error, unused-import, wrong-import-order, wrong-import-position
import AnimationMaker
import sb_backdrop
import sb_revealInFileBrowser
import ReadFromWrite
import nLabelShortcut
import animatedSnap3D
import CycleOperations

import NFTSCopyPaste
import NFTShelp

####################################


# Override default backdrop function with sb_backdrop

nukescripts.autoBackdrop = sb_backdrop
nuke.toolbar("Nodes").addCommand("Other/Backdrop", "sb_backdrop.sb_backdrop()", "alt+b")

####################################

# shared_toolsets

import shared_toolsets

sharedToolSetsPath = os.path.join(os.getenv("NFTS_COMP_ENV_ROOT"), "SharedToolSets")
shared_toolsets.setSharedToolSetsPath(sharedToolSetsPath)

toolbar = nuke.menu("Nodes")
shared_toolsets.createToolsetsMenu(toolbar)

####################################

# Add a NFTS Tools toolbar.

import tools_loader
tools_loader.create_gizmo_menu(tools_loader.NFTS_gizmos_root)


# add python tools to NFTS menu

NFTS = nuke.toolbar("Nodes").addMenu("NFTS_tools/python", icon="python.png")
NFTS.addCommand("ReadFromWrite", "ReadFromWrite.ReadFromWrite()", "shift+r")
NFTS.addCommand(
    "sb RevealInFileBrowser",
    "sb_revealInFileBrowser.sb_revealInFileBrowser()",
    "alt+shift+r",
)
NFTS.addCommand("nLabelShortcut", "nLabelShortcut.nLabelShortcut()", "shift+l")
NFTS.addCommand("ShuffleAll", "import shuffleAll\nshuffleAll.shuffleAll()")
NFTS.addCommand(
    "nDeepAutocrop", "import nDeepAutocrop\nnDeepAutocrop.nDeepAutocrop()"
)
NFTS.addCommand(
    "nDollarGUI", "import nDollargui\nnDollargui.nExecuting()", "alt+d"
)
NFTS.addCommand(
    "Cycle Operations/Cycle Operations Forwards",
    "CycleOperations.CycleOperations()",
    "alt+x",
)
NFTS.addCommand(
    "Cycle Operations/Cycle Operations Backwards",
    "CycleOperations.CycleOperations(False)",
    "alt+shift+x",
)


####################################

# 3DE4 lens distortion

if equalizer_version_check.EQUALIZER:  # pylint: disable=undefined-variable
    toolbar = nuke.menu("Nodes")
    eq = toolbar.addMenu("3DEqualizer", icon="3DE.png")
    eq.addCommand(
        "LD_3DE4_Anamorphic_Standard_Degree_4",
        "nuke.createNode('LD_3DE4_Anamorphic_Standard_Degree_4')",
    )
    eq.addCommand(
        "LD_3DE4_Anamorphic_Degree_6", "nuke.createNode('LD_3DE4_Anamorphic_Degree_6')"
    )
    eq.addCommand(
        "LD_3DE4_Radial_Standard_Degree_4",
        "nuke.createNode('LD_3DE4_Radial_Standard_Degree_4')",
    )
    eq.addCommand(
        "LD_3DE4_Radial_Fisheye_Degree_8",
        "nuke.createNode('LD_3DE4_Radial_Fisheye_Degree_8')",
    )
    eq.addCommand(
        "LD_3DE_Classic_LD_Model", "nuke.createNode('LD_3DE_Classic_LD_Model')"
    )


####################################


# Add Cryptomatte menu icons for Nuke 12 or Older
if nuke.NUKE_VERSION_MAJOR < 13:
    import cryptomatte_utilities

    cryptomatte_utilities.setup_cryptomatte_ui()


####################################

# add extra main menu functions


nuke.menu("Nuke").addCommand(
    "Edit/Convert Gizmos to Groups", "import Gizmo2Group\nGizmo2Group.Gizmo2Group()"
)  # add gizmo to group conversion - importing it when in use
nuke.menu("Nuke").addCommand(
    "Edit/Autocrop Selected Nodes", "nukescripts.autocrop()"
)  # add gizmo to group conversion - importing it when in use
nuke.menu("Nuke").addCommand(
    "File/Package Script",
    "import Gizmo2Group\nGizmo2Group.Gizmo2Group()\nimport WrapItUp\nWrapItUp.WrapItUp()",
)  # add packages script - importing it when used - runs also gizmo to group

# Check Nuke or Nuke X and add menu only if cheap nuke is running
if not nuke.env["nukex"]:
    nuke.menu("Nuke").addCommand(
        "File/Switch to NukeX ", "import nukeSwitch\nnukeSwitch.versionSwitch()"
    )


###################################


# add defaults


# default preferences
nuke.toNode("preferences")["LocalizationPauseOnProjectLoad"].setValue(True)
nuke.toNode("preferences")["maxPanels"].setValue(1)
nuke.toNode("preferences")["GridHeight"].setValue(50)
nuke.toNode("preferences")["dag_snap_threshold"].setValue(10)
nuke.toNode("preferences")["ArrowColorUp"].setValue(0xFF0000FF)


# default projects settings
nuke.knobDefault("Root.project_directory", "[python {nuke.script_directory()}]")
nuke.knobDefault("Root.format", "HD_1080")
nuke.knobDefault("Root.first_frame", "1001")
nuke.knobDefault("Root.last_frame", "1100")
nuke.knobDefault("Root.fps", "25")


# personal default knobs values
nuke.knobDefault("Shuffle.label", "[value in]_[value out]")
nuke.knobDefault("ShuffleCopy.label", "[value in]_[value out]")
nuke.knobDefault("LayerContactSheet.showLayerNames", "True")
nuke.knobDefault("Remove.channels", "alpha")
nuke.knobDefault("AppendClip.firstFrame", "1001")
nuke.knobDefault("Write.create_directories", "True")
nuke.knobDefault("Write.exr.compression", "4")  # RLE as default EXR compression
nuke.knobDefault("EXPTool.mode", "0")  # Stops as default Exposure Parameter
nuke.knobDefault("Roto.toolbox", "createBSpline") # Set default roto to Bspline
nuke.menu("Nodes").addCommand(
    "Time/FrameHold",
    "nuke.createNode('FrameHold')['first_frame'].setValue( nuke.frame() )",
    icon="FrameHold.png",
)


# create keep function add it to the channel menu
def crate_keep():
    """create a remove node and set it not keep rgba"""
    rem = nuke.createNode("Remove")
    rem.knob("operation").setValue("keep")
    rem.knob("channels").setValue("rgba")
    return rem


nuke.menu("Nodes").addCommand("Channel/Keep", "createkeep()", icon="Remove.png")
nuke.menu("Nodes").addCommand(
    "Filter/Dilate", "nuke.createNode('Dilate')", icon="ErodeFast.png"
)


# add custom resolutions to format list

DCP_2K_FULL = "2048 1152 DCP_2K_Full"
nuke.addFormat(DCP_2K_FULL)

DCP_2K_SCOPE = "2048 858 DCP_2K_Scope"
nuke.addFormat(DCP_2K_SCOPE)

DCP_2K_FLAT = "1998 1080 DCP_2K_Flat"
nuke.addFormat(DCP_2K_FLAT)


####################################


# custom shortcuts

toolbar = nuke.menu("Nodes")
toolbar.addCommand("Merge/KeyMix", 'nuke.createNode("Keymix")', "v")
toolbar.addCommand("Color/Math/Expression", 'nuke.createNode("Expression")', "e")
toolbar.addCommand("Color/Invert", 'nuke.createNode("Invert")', "alt+ctrl+i")
toolbar.addCommand("Merge/Premult", 'nuke.createNode("Premult")', "alt+shift+p")
toolbar.addCommand("Merge/Unpremult", 'nuke.createNode("Unpremult")', "alt+shift+u")
toolbar.addCommand("Channel/ChannelMerge", 'nuke.createNode("ChannelMerge")', "shift+m")
toolbar.addCommand("Transform/TransformMasked", 'nuke.createNode("TransformMasked")', "shift+t")


####################################

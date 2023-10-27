"""
NFTS - National Film and Television School.
latest update by Nicola Borsari: 2023-10-16

The file handles the NFTS pipe tools in the GUI
"""

####################################

# Import standard Python modules.
import nuke  # pylint: disable=import-error

####################################

# Import Custom Python scripts.
import callback_manager
import post_processing

####################################

# register callbakcs
callback_manager.register_pipeline_callbacks("OnScriptLoad")
callback_manager.register_pipeline_callbacks("OnScriptSave")
callback_manager.register_pipeline_callbacks("AfterRender")


#register make JPEGs menu
nuke.menu("Nuke").addCommand(
    "NFTS/Make JPEGs from selected Reads", lambda: post_processing.make_jpegs()
)

####################################

print("NFTS PIPE menu LOADED")

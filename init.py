####################################

'''
NFTS - National Film and Television School.
latest update by Nicola Borsari: 2019-11-08
'''

####################################

'''
Import standard Python modules.
'''


import nuke
import os
import shutil
import network_drive_remapping #imports the custom py that maps the letters between os for ISIS and servers


####################################

'''
Add plugin paths.
'''

nuke.pluginAddPath('./gizmos')
nuke.pluginAddPath('./gizmos/pixelfudger')
nuke.pluginAddPath('./gizmos/v_tools')
nuke.pluginAddPath('./gizmos/cryptomatte')
nuke.pluginAddPath('./gizmos/legacy')
nuke.pluginAddPath('./python')
nuke.pluginAddPath('./icons')
nuke.pluginAddPath('./3DE4')



#add 3DEqualizer
from equalizer_version_check import *

####################################


'''
Install Cryptomatte
'''

import cryptomatte_utilities
cryptomatte_utilities.setup_cryptomatte()


####################################

# NFTS CUSTOM PIPELINE, FUNCTIONS AND OVERRIDES


#check the existence of versioning in the file name
def script_has_version():
    filename = nuke.root().knob('name').value()
    try:
        nukescripts.version_get(filename, 'v')
        return True
    except:
        return False


# define a custom invremental save that also vesions up every write not in the script

def incrementalSave():
 

    nodes = nuke.allNodes('Write') + nuke.allNodes('DeepWrite')

    try:
        timeline_write = nuke.root().knob('timeline_write_node').value()
        nodes.remove(nuke.toNode(timeline_write))
    except:
        pass

    if script_has_version():
        nukescripts.clear_selection_recursive()
        for node in nodes:
            node.knob("selected").setValue(True)
            nukescripts.version_up()
            nukescripts.clear_selection_recursive()

    nukescripts.script_version_up()
    return



####################################


# old write pipeline (for legagy purposes)  - we need these to avoid old scripts braking


def write_studio_pipeline():
    pass

def writeBeforePipeline():
    pass

def writeAfterPipeline():
    pass


####################################


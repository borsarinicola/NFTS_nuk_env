####################################

'''
NFTS - National Film and Television School.
latest update: 2019-09-15
'''

####################################

'''
Import standard Python modules.
'''


import nuke
import os
import network_drive_mapping #imports the custom py that maps the letters between os for ISIS and servers


IS_GUI = False

####################################

'''
Add plugin paths.
'''

nuke.pluginAddPath('./gizmos')
nuke.pluginAddPath('./gizmos/pixelfudger')
nuke.pluginAddPath('./gizmos/v_tools')
nuke.pluginAddPath('./gizmos/cryptomatte')
nuke.pluginAddPath('./gizmos/legacy')
nuke.pluginAddPath('./KeenTools')
nuke.pluginAddPath('./python')
nuke.pluginAddPath('./icons')


# if statement to load 3DE based on the OS
if nuke.env['WIN32']:
    nuke.pluginAddPath("./3DE4/win")
if nuke.env['MACOS']:
    nuke.pluginAddPath("./3DE4/mac")

####################################

'''
Add viewer luts.
'''

nuke.ViewerProcess.register("Cineon", nuke.createNode, ("ViewerProcess_1DLUT","current Cineon" ))
nuke.ViewerProcess.register("AlexaV3LogC", nuke.createNode, ("ViewerProcess_1DLUT","current AlexaV3LogC" ))

####################################

'''
Install Cryptomatte
'''

import cryptomatte_utilities
cryptomatte_utilities.setup_cryptomatte()


####################################


def write_studio_pipeline():
    try:
        ns = nuke.root().knob('timeline_write_node').value()
        selection = nuke.allNodes() #store selection into list
        x = 0 #counter for loop
        
        for each in selection:
            processing = selection[x]
        
            if x <= len(selection):
        
                x = x+1
        
                #clear selection and prepare a new one for processing 
                nukescripts.clear_selection_recursive()
                processing.knob("selected").setValue(True)
                if 'Write' in nuke.selectedNode().Class():
                    nuke.selectedNode().knob('beforeRender').setValue("try:\n    ScriptVersionTest()\nexcept ValueError:\n    print 'skipping pipeline'\nelse:\n    createArtifact()")
                    nuke.selectedNode().knob('afterRender').setValue("try:\n    ScriptVersionTest()\nexcept ValueError:\n    print 'skipping pipeline'\nelse:\n    if nuke.ask('Do you want to version up your script?'):\n        incrementalSave()")
    
    except:
        print 'not studio'

    return




#override default incremental save with functions that also increments write nodes 

def incrementalSave():
    write_studio_pipeline()
    
    nuke.selectAll()
    selection = nuke.selectedNodes()
    x = 0
    
    for each in selection:
        processing = selection[x]
    
        if x <= len(selection):
            x = x+1
            nukescripts.clear_selection_recursive()
            processing.knob("selected").setValue(True)
            name = nuke.selectedNode().Class() 

            try:
                if 'Write' in name and nuke.selectedNode().knob('name').getValue() != nuke.root().knob('timeline_write_node').value():
                    nukescripts.version_up()

            except:

                if 'Write' in name:
                    nukescripts.version_up()


    nukescripts.script_version_up()

    return



def createArtifact():

	if IS_GUI == True:

		filepath = nuke.value("root.name")
		nukescript = filepath[:-3]
		nuke.selectAll()
		nuke.nodeCopy(nukescript + '_artifact.nk')
		nukescripts.clear_selection_recursive()
	
	return


# adds version up functionalities after render to write and deep write

def ScriptVersionTest():
    filename = nuke.root().knob('name').value()
    nukescripts.version_get(filename, 'v')
    return

nuke.knobDefault('Write.beforeRender', "try:\n    ScriptVersionTest()\nexcept ValueError:\n    print 'skipping pipeline'\nelse:\n    createArtifact()")
nuke.knobDefault('Write.afterRender', "try:\n    ScriptVersionTest()\nexcept ValueError:\n    print 'skipping pipeline'\nelse:\n    if nuke.ask('Do you want to version up your script?'):\n        incrementalSave()")
nuke.knobDefault('DeepWrite.beforeRender', "try:\n    ScriptVersionTest()\nexcept ValueError:\n    print 'skipping pipeline'\nelse:\n    createArtifact()")
nuke.knobDefault('DeepWrite.afterRender', "try:\n    ScriptVersionTest()\nexcept ValueError:\n    print 'skipping pipeline'\nelse:\n    if nuke.ask('Do you want to version up your script?'):\n        incrementalSave()")











####################################


if nuke.env['WIN32']:


	#install kentools for win nuke11.2


	# add KeenTools directory to python path to be able to import
	# python files from KeenTools directory
	import os
	import sys
	sys.path.append(os.path.dirname(os.path.abspath(__file__)))


	from version_check import check_nuke_version_and_os


	nuke.pluginAddPath('./icons')


	#from this point it's trying to load the plugin based on the OS


	if check_nuke_version_and_os('11.2', 'WIN', print_error_message=True):
	    nuke.pluginAddPath('./KeenTools/win')

	    # optional environment variable that can be set to specify the path to the data directory
	    # should be absolute or relative to the KeenTools library file (.so, .dll or .dylib)
	    # os.environ["KEENTOOLS_DATA_PATH"] = "../data"

	    # preload KeenTools so all the nodes will be available
	    nuke.load('KeenTools')
	else:
	    print('loading KeenTools for Nuke11.2 WIN skipped')


if nuke.env['MACOS']:


	# add KeenTools directory to python path to be able to import
	# python files from KeenTools directory
	import os
	import sys
	sys.path.append(os.path.dirname(os.path.abspath(__file__)))


	from version_check import check_nuke_version_and_os


	nuke.pluginAddPath('./icons')
	if check_nuke_version_and_os('11.2', 'OSX', print_error_message=True):
	    nuke.pluginAddPath('./KeenTools/mac')

	    # optional environment variable that can be set to specify the path to the data directory
	    # should be absolute or relative to the KeenTools library file (.so, .dll or .dylib)
	    # os.environ["KEENTOOLS_DATA_PATH"] = "../data"

	    # preload KeenTools so all the nodes will be available
	    nuke.load('KeenTools')
	else:
	    print('loading KeenTools for Nuke11.2 OSX skipped')





####################################


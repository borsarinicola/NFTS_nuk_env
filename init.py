####################################

'''
NFTS - National Film and Television School.
latest update: 2019-11-27
'''

####################################

'''
Import standard Python modules.
'''


import nuke
import os
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

#nuke.ViewerProcess.register("Cineon", nuke.createNode, ("ViewerProcess_1DLUT","current Cineon" ))
#nuke.ViewerProcess.register("AlexaV3LogC", nuke.createNode, ("ViewerProcess_1DLUT","current AlexaV3LogC" ))

####################################

'''
Install Cryptomatte
'''

import cryptomatte_utilities
cryptomatte_utilities.setup_cryptomatte()


####################################

# NFTS CUSTOM PIPELINE, FUNCTIONS AND OVERRIDES


#check the existence of versioning in the file name
def ScriptVersionTest():
    filename = nuke.root().knob('name').value()
    nukescripts.version_get(filename, 'v')
    return

#defice the creation of artifact by removing the last 3 characters form the file name (.nk) and adding _artifact.nk
def createArtifact():

	if nuke.GUI == True:

		filepath = nuke.value("root.name")
		nukescript = filepath[:-3]
		nuke.selectAll()
		nuke.nodeCopy(nukescript + '_artifact.nk')
		nukescripts.clear_selection_recursive()
	
	return

#define the before and after write functions with the version check - the try is not done in the script version test funciton for legacy purposes

def writeBeforePipeline():
    try:
        ScriptVersionTest()
    except ValueError:
        print 'skipping pipeline'
    else:
        createArtifact()
    return

def writeAfterPipeline():
    try:
        ScriptVersionTest()
    except ValueError:
        print 'skipping pipeline'
    else:
        if nuke.ask('Do you want to version up your script?'):
            incrementalSave()
    return


# old write pipeline (for legagy purposes)


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
					nuke.selectedNode().knob('beforeRender').setValue("writeBeforePipeline()")
					nuke.selectedNode().knob('afterRender').setValue("writeAfterPipeline()")
    
    except:
        print 'not studio'

    return



# define a custom invremental save that also vesions up every write not in the script

def incrementalSave():
 
    selection = nuke.allNodes()
   
    x = 0
    
    for each in selection:
        processing = selection[x]
    
        if x <= len(selection):
          
            nukescripts.clear_selection_recursive()
            processing.knob("selected").setValue(True)

            name = nuke.selectedNode().Class() 

            if 'Write' in name:
                nuke.selectedNode().knob('beforeRender').setValue("writeBeforePipeline()")
                nuke.selectedNode().knob('afterRender').setValue("writeAfterPipeline()")
                nukescripts.version_up()

            x = x + 1

    nukescripts.script_version_up()

    return


# adds the new pipleine definitions as default values in the python tab of write and deep write

nuke.knobDefault('Write.beforeRender', "writeBeforePipeline()")
nuke.knobDefault('Write.afterRender', "writeAfterPipeline()")
nuke.knobDefault('DeepWrite.beforeRender', "writeBeforePipeline()")
nuke.knobDefault('DeepWrite.afterRender', "writeAfterPipeline()")



####################################


#   install kentools for win nuke11.2


if nuke.env['WIN32']:


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


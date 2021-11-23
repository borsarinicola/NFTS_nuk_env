####################################

'''
NFTS - National Film and Television School.
latest update by Pietro Abati: 2020-10-26
'''

####################################

'''
Import standard Python modules.
'''

import os, sys, nuke

####################################

'''
Import Custom Python scripts.
'''

import sb_backdrop
import sb_revealInFileBrowser
import ReadFromWrite
import nLabelShortcut
import animatedSnap3D
import pixelfudger
import CycleOperations
import NFTSCopyPaste
import NFTShelp
import hieroFPS

try:
  import AnimationMaker
except:
  pass

####################################

'''
Override default backdrop function with sb_backdrop
'''

nukescripts.autoBackdrop = sb_backdrop
nuke.toolbar("Nodes").addCommand('Other/Backdrop', 'sb_backdrop.sb_backdrop()','alt+b')

####################################

'''
Add a NFTS Tools toolbar.
'''

NFTS = nuke.toolbar("Nodes").addMenu( "NFTS", icon="nfts.png" )
NFTS.addCommand('Python/ReadFromWrite','ReadFromWrite.ReadFromWrite()', 'shift+r')
NFTS.addCommand("Python/sb RevealInFileBrowser", "sb_revealInFileBrowser.sb_revealInFileBrowser()", "alt+shift+r")
NFTS.addCommand('Python/nLabelShortcut','nLabelShortcut.nLabelShortcut()', 'shift+l')
NFTS.addCommand('Python/ShuffleAll', 'import shuffleAll\nshuffleAll.shuffleAll()')
NFTS.addCommand('Python/nDeepAutocrop','import nDeepAutocrop\nnDeepAutocrop.nDeepAutocrop()')
NFTS.addCommand('Python/nDollarGUI','import nDollargui\nnDollargui.nDollargui()', 'alt+d')
NFTS.addCommand('Python/Cycle Operations/Cycle Operations Forwards', "CycleOperations.CycleOperations()", "alt+x")
NFTS.addCommand('Python/Cycle Operations/Cycle Operations Backwards', "CycleOperations.CycleOperations(False)", "alt+shift+x")
NFTS.addCommand("AlexaNoise", "nuke.createNode('AlexaNoise')" )
NFTS.addCommand("DespillMadness_v2", "nuke.createNode('DespillMadness_v2')")
NFTS.addCommand("ColourEdge_v2", "nuke.createNode('ColourEdge_v2')")
NFTS.addCommand("fractal_blur_v2", "nuke.createNode('fractal_blur_v2')" )
NFTS.addCommand("aPMatte", "nuke.createNode('aPMatte')" )
NFTS.addCommand("BlinkScriptMedian", "nuke.createNode('BlinkScriptMedian')" )
NFTS.addCommand("AspectGuide", "nuke.createNode('AspectGuide')" )
NFTS.addCommand("BumpDisplace", "nuke.createNode('BumpDisplace')" )
NFTS.addCommand("nFrameRebuild", "nuke.createNode('nFrameRebuild')['foi'].setValue( nuke.frame() )" )
NFTS.addCommand("DasGrain", "nuke.createNode('DasGrain')" )
NFTS.addCommand("nChannelViewer", "nuke.createNode('nChannelViewer')" )
NFTS.addCommand("despillToColor", "nuke.createNode('despillToColor')" )
NFTS.addCommand("apChroma", "nuke.createNode('apChroma')" )
NFTS.addCommand("apChromaMerge", "nuke.createNode('apChromaMerge')" )

####2020 adding
NFTS.addCommand('chromaticAberration', "nuke.createNode('chromaticAberration')", icon='chromaticAberration.png')
NFTS.addCommand('AutoFlare2', "nuke.createNode('AutoFlare2')", icon='AutoFlare2.png')
NFTS.addCommand('Exponential_Glow', "nuke.createNode('Exponential_Glow')", icon='Exponential_Glow.png')
NFTS.addCommand('rebuild_frames', "nuke.createNode('rebuild_frames')", icon='rebuild_frames.png')
NFTS.addCommand('HeatWave', "nuke.createNode('HeatWave')", icon='HeatWave.png')
NFTS.addCommand('Bokeh_shapes', "nuke.createNode('Bokeh_shapes')", icon='Bokeh_shapes.tif')


####################################

#3DE4 lens distortion 

if Equalizer == True:
    toolbar = nuke.menu('Nodes')
    eq = toolbar.addMenu('3DEqualizer', icon='3DE.png')
    eq.addCommand("LD_3DE4_Anamorphic_Standard_Degree_4", "nuke.createNode('LD_3DE4_Anamorphic_Standard_Degree_4')")
    eq.addCommand("LD_3DE4_Anamorphic_Degree_6", "nuke.createNode('LD_3DE4_Anamorphic_Degree_6')")
    eq.addCommand("LD_3DE4_Radial_Standard_Degree_4", "nuke.createNode('LD_3DE4_Radial_Standard_Degree_4')")
    eq.addCommand("LD_3DE4_Radial_Fisheye_Degree_8", "nuke.createNode('LD_3DE4_Radial_Fisheye_Degree_8')")
    eq.addCommand("LD_3DE_Classic_LD_Model", "nuke.createNode('LD_3DE_Classic_LD_Model')")


####################################



# V!ctor Tools Toolbar Definitions

toolbar = nuke.menu('Nodes')
VMenu = toolbar.addMenu('V!ctor', icon='V_Victor.png')
VMenu.addCommand('V_EdgeMatte', 'nuke.createNode("V_EdgeMatte")', icon='V_EdgeMatte.png')
VMenu.addCommand('V_ColorRenditionChart', 'nuke.createNode("V_ColorRenditionChart")', icon='V_ColorRenditionChart.png')
VMenu.addCommand('V_SliceTool', 'nuke.createNode("V_SliceTool")',  icon='V_SliceTool.png')
VMenu.addCommand('V_Slate', 'nuke.createNode("V_Slate")', icon='V_Slate.png')
VMenu.addCommand('V_Multilabeler', 'nuke.createNode("V_Multilabeler")', icon='V_Multilabeler.png')

####################################


#Install Cryptomatte

import cryptomatte_utilities
cryptomatte_utilities.setup_cryptomatte_ui()


####################################


# shared_toolsets

import shared_toolsets

sharedToolSetsPaths = {
"win32"  : "//digitalfxserver/CompEnvironment/SharedToolSets",     #WINDOWS
"darwin" : "/Volumes/CompEnvironment/SharedToolSets" #MACOS
}

def toolSetsFilenameFilter(filename):
  if nuke.env['MACOS']:
      # lowercase
      filename = filename.replace( '//digitalfxserver/CompEnvironment/', '/Volumes/CompEnvironment/' )
  elif nuke.env['WIN32']:
      # lowercase
      filename = filename.replace( '/Volumes/CompEnvironment/', '//digitalfxserver/CompEnvironment/' )
  return filename

platform = sys.platform

sharedToolSetsPath = sharedToolSetsPaths[platform]
shared_toolsets.setSharedToolSetsPath(sharedToolSetsPath)
shared_toolsets.addFileFilter(toolSetsFilenameFilter)

toolbar = nuke.menu("Nodes")
shared_toolsets.createToolsetsMenu(toolbar)


####################################

#install deadline submission script for win nuke11.2


import DeadlineNukeClient
menubar = nuke.menu("Nuke")
tbmenu = menubar.addMenu("&Thinkbox")

#advancedSumbission creates the artifact upon script sumbission
def advancedSubmission():
    nuke.scriptSave()
    DeadlineNukeClient.main()
    beforeWrite_cb()
    afterWrite_cb()

tbmenu.addCommand("Submit Nuke To Deadline", 'advancedSubmission()', 'Alt+R')

try:
    if nuke.env[ 'studio' ] or nuke.env[ 'NukeVersionMajor' ] >= 11:
        import DeadlineNukeFrameServerClient
        tbmenu.addCommand("Reserve Frame Server Slaves", DeadlineNukeFrameServerClient.main, "")
except:
    pass
try:
    import DeadlineNukeVrayStandaloneClient
    tbmenu.addCommand("Submit V-Ray Standalone to Deadline", DeadlineNukeVrayStandaloneClient.main, "")
except:
    pass


####################################

# add extra main menu functions


nuke.menu('Nuke').addCommand('Edit/Convert Gizmos to Groups','import Gizmo2Group\nGizmo2Group.Gizmo2Group()') # add gizmo to group conversion - importing it when in use
nuke.menu('Nuke').addCommand('Edit/Autocrop Selected Nodes','nukescripts.autocrop()') # add gizmo to group conversion - importing it when in use
nuke.menu("Nuke").addCommand('File/Package Script', 'import Gizmo2Group\nGizmo2Group.Gizmo2Group()\nimport WrapItUp\nWrapItUp.WrapItUp()')  # add packages script - importing it when used - runs also gizmo to group
nuke.menu("Nuke").addCommand('File/Save New Comp Version', 'incrementalSave()') #override save new comp version funtionalities

if nuke.env['nukex'] == False: # Check Nuke or Nuke X and add menu only if cheap nuke is running
    nuke.menu("Nuke").addCommand('File/Switch to NukeX ', 'import nukeSwitch\nnukeSwitch.versionSwitch()')



###################################


#add defaults


#default preferences
nuke.toNode('preferences')['LocalizationPauseOnProjectLoad'].setValue(True)
nuke.toNode('preferences')['maxPanels'].setValue(1)
nuke.toNode('preferences')['GridHeight'].setValue(50)
nuke.toNode('preferences')['dag_snap_threshold'].setValue(10)
nuke.toNode('preferences')['ArrowColorUp'].setValue(0xff0000ff)



#default projects settings
nuke.knobDefault('Root.project_directory', '[python {nuke.script_directory()}]')
nuke.knobDefault('Root.format', 'HD_1080')
nuke.knobDefault('Root.first_frame', '1001')
nuke.knobDefault('Root.last_frame', '1100')
nuke.knobDefault('Root.fps', '25')



# personal default knobs values
nuke.knobDefault('Shuffle.label','[value in]_[value out]')
nuke.knobDefault('ShuffleCopy.label','[value in]_[value out]')
nuke.knobDefault('LayerContactSheet.showLayerNames', 'True')
nuke.knobDefault('Remove.channels','alpha')
nuke.knobDefault('AppendClip.firstFrame','1001')
nuke.knobDefault('Write.create_directories', 'True')
nuke.knobDefault("Write.exr.compression","4")   #RLE as default EXR compression
nuke.knobDefault("EXPTool.mode", "0")   #Stops as default Exposure Parameter
nuke.knobDefault('Merge.bbox', 'B')  #sets the bbox to 'B' for your merge nodes
nuke.knobDefault('Viewer.full_frame_processing', 'True') #make full frame processing autoamtically on
nuke.knobDefault('TimeOffset.time_offset','1001') #sets Timeoffset value to 1001
nuke.knobDefault('ChannelMerge.operation','8') #sets the default operation of ChannelMerge to Multiply
nuke.menu('Nodes').addCommand( "Time/FrameHold", "nuke.createNode('FrameHold')['first_frame'].setValue( nuke.frame() )", icon='FrameHold.png')



#create keep function add it to the channel menu
def createkeep():
    rem = nuke.createNode('Remove')
    rem.knob('operation').setValue('keep')
    rem.knob('channels').setValue('rgba')
    return
nuke.menu('Nodes').addCommand( "Channel/Keep", "createkeep()", icon="Remove.png")
nuke.menu('Nodes').addCommand( "Filter/Dilate", "nuke.createNode('Dilate')", icon="ErodeFast.png")


#add custom resolutions to format list

#DCP_2K_Full = '2048 1152 DCP_2K_Full'
#nuke.addFormat(DCP_2K_Full)

#DCP_2K_Scope = '2048 858 DCP_2K_Scope'
#nuke.addFormat(DCP_2K_Scope)

#DCP_2K_Flat = '1998 1080 DCP_2K_Flat'
#nuke.addFormat(DCP_2K_Flat)



####################################


# custom shortcuts

toolbar = nuke.menu('Nodes')
toolbar.addCommand('Merge/KeyMix', 'nuke.createNode("Keymix")', 'v')
toolbar.addCommand('Color/Math/Expression', 'nuke.createNode("Expression")', 'e')
toolbar.addCommand('Color/Invert', 'nuke.createNode("Invert")', 'alt+ctrl+i')
toolbar.addCommand('Merge/Premult', 'nuke.createNode("Premult")', 'alt+shift+p')
toolbar.addCommand('Merge/Unpremult', 'nuke.createNode("Unpremult")', 'alt+shift+u')
toolbar.addCommand('Channel/ChannelMerge', 'nuke.createNode("ChannelMerge")', 'shift+m')
toolbar.addCommand('Transform/TransformMasked', 'nuke.createNode("TransformMasked")', 'shift+t')


####################################


# Pipeline functions necessary only in GUI mode


def createArtifact():

    nuke.scriptSave()
    script = nuke.value("root.name")
    filename, file_extension = os.path.splitext(script)
    artef = '{}_artifact.{}'.format(filename, file_extension)
    shutil.copyfile(script, artef)

def beforeWrite_cb():
    if script_has_version():
        createArtifact()

def afterWrite_cb():
    if script_has_version() and nuke.ask('Do you want to version up your script?'):
        incrementalSave()


# for some off reason these callbacks are added tiwce
nuke.addBeforeRender(beforeWrite_cb)
nuke.addAfterRender(afterWrite_cb)

# setting callback to remove the second one on script load - odd stuff
nuke.addOnScriptLoad(lambda: nuke.removeAfterRender(afterWrite_cb))


####################################

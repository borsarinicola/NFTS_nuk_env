####################################

'''
NFTS - National Film and Television School.
latest update: 2019-11-27
'''

####################################

'''
Import standard Python modules.
'''

import os, sys, nuke

####################################

'''
Import Python scripts.
'''

import sb_backdrop
import sb_revealInFileBrowser
import ReadFromWrite
import nLabelShortcut
import animatedSnap3D
import pixelfudger
import AnimationMaker
import CycleOperations


####################################

'''
Override default backdrop function with sb_backdrop
'''

nukescripts.autoBackdrop = sb_backdrop
nuke.toolbar("Nodes").addCommand('Other/Backdrop', 'sb_backdrop.sb_backdrop()','')

####################################

'''
Add a NFTS Tools toolbar.
'''

NFTS = nuke.toolbar("Nodes").addMenu( "NFTS", icon="nfts.png" )
NFTS.addCommand('ReadFromWrite','ReadFromWrite.ReadFromWrite()', 'shift+r')
NFTS.addCommand("sb RevealInFileBrowser", "sb_revealInFileBrowser.sb_revealInFileBrowser()", "alt+shift+r")
NFTS.addCommand('nLabelShortcut','nLabelShortcut.nLabelShortcut()', 'shift+l')
NFTS.addCommand("sb Backdrop", "sb_backdrop.sb_backdrop()", 'alt+b')
NFTS.addCommand("ShuffleAll", "nuke.createNode('ShuffleAll')")
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
NFTS.addCommand('Cycle Operations/Cycle Operations Forwards', "CycleOperations.CycleOperations()", "alt+x")
NFTS.addCommand('Cycle Operations/Cycle Operations Backwards', "CycleOperations.CycleOperations(False)", "alt+shift+x")



####################################

#3DE4 lens distortion 

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


#add NFTS CopyPaste


if nuke.env['WIN32']:
    Path = '//digitalfxserver/CompEnvironment/NFTS_CopyPaste_Data.nk'
if nuke.env['MACOS']:
    Path = '/Volumes/CompEnvironment/NFTS_CopyPaste_Data.nk'


def nftsCopy():
    nuke.nodeCopy(Path)
    return

def nftsPaste():
    nuke.nodePaste(Path)
    return

#add functions to menu
nuke.menu( 'Nuke' ).addCommand('NFTS Share/Share Selected Nodes', 'nftsCopy()', 'Alt+Shift+C')
nuke.menu( 'Nuke' ).addCommand('NFTS Share/Paste Shared Nodes', 'nftsPaste()', 'Alt+Shift+V')


####################################


# shared_toolsets

if nuke.GUI:

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

from version_check import *
import nuke
import os


if nuke.env['WIN32']:


    if 'available_keentools_versions' not in globals():
        available_keentools_versions = []
        proper_keentools_version_found = False

    current_keentools_version = (os.path.dirname(os.path.realpath(__file__)),
                                 '11.2', 'WIN')
    available_keentools_versions.append(current_keentools_version)


    toolbar = nuke.menu('Nodes')
    if check_nuke_version_and_os(current_keentools_version[1], current_keentools_version[2]):
        proper_keentools_version_found = True

        # add KeenTools menu to Nodes toolbar
        toolbar.removeItem('KeenTools')
        kt_menu = toolbar.addMenu('KeenTools', tooltip="""
            KeenTools v1.4.7
            loaded from "{0}"
            """.format(current_keentools_version[0]),
            icon='KeenTools.png')
        kt_menu.addCommand('GeoTracker', lambda: nuke.createNode('GeoTracker'), icon='GeoTracker.png')
        kt_menu.addCommand('PinTool', lambda: nuke.createNode('PinTool'), icon='PinTool.png')
        kt_menu.addCommand('ReadRiggedGeo', lambda: nuke.createNode('ReadRiggedGeo'), icon='ReadRiggedGeo.png')
        if 'ON' == 'ON':
            kt_menu.addCommand('FaceBuilder', lambda: nuke.createNode('FaceBuilder'), icon='FaceBuilder.png')
        if 'ON' == 'ON':
            kt_menu.addCommand('FaceTracker (beta)', lambda: nuke.createNode('FaceTracker'), icon='FaceTracker.png')
        if 'OFF' == 'ON':
            kt_menu.addCommand('FlowEvaluationTool', lambda: nuke.createNode('FlowEvaluationTool'), icon='KeenTools.png')
        if 'ON' == 'ON':
            kt_menu.addCommand('TextureBuilder (beta)', lambda: nuke.createNode('TextureBuilder'), icon='TextureBuilder.png')


    if not proper_keentools_version_found:
        # add a warning to menu

        def keentools_version_to_str(keentools_version):
            path, nuke_v, os = keentools_version
            return '  - Nuke{0} {1} at \n    "{2}"'.format(nuke_v, os, path)

        available_keentools_versions_str = '\n'.join(
            [keentools_version_to_str(x) for x in available_keentools_versions])
        warning_text = ("You are using Nuke{0} on {1}\n"
                        "There is no KeenTools for that configuration installed\n"
                        "\n"
                        "Available KeenTools installations:\n"
                        "{2}").format(
                            current_nuke_version(), current_platform(),
                            available_keentools_versions_str)
        toolbar.removeItem('KeenTools')
        toolbar.addCommand('KeenTools', lambda: nuke.message(warning_text), icon='KeenTools.png')

if nuke.env['MACOS']:

    if 'available_keentools_versions' not in globals():
        available_keentools_versions = []
        proper_keentools_version_found = False

    current_keentools_version = (os.path.dirname(os.path.realpath(__file__)),
                                 '11.2', 'OSX')
    available_keentools_versions.append(current_keentools_version)


    toolbar = nuke.menu('Nodes')
    if check_nuke_version_and_os(current_keentools_version[1], current_keentools_version[2]):
        proper_keentools_version_found = True

        # add KeenTools menu to Nodes toolbar
        toolbar.removeItem('KeenTools')
        kt_menu = toolbar.addMenu('KeenTools', tooltip="""
            KeenTools v1.4.7
            loaded from "{0}"
            """.format(current_keentools_version[0]),
            icon='KeenTools.png')
        kt_menu.addCommand('GeoTracker', lambda: nuke.createNode('GeoTracker'), icon='GeoTracker.png')
        kt_menu.addCommand('PinTool', lambda: nuke.createNode('PinTool'), icon='PinTool.png')
        kt_menu.addCommand('ReadRiggedGeo', lambda: nuke.createNode('ReadRiggedGeo'), icon='ReadRiggedGeo.png')
        if 'ON' == 'ON':
            kt_menu.addCommand('FaceBuilder', lambda: nuke.createNode('FaceBuilder'), icon='FaceBuilder.png')
        if 'ON' == 'ON':
            kt_menu.addCommand('FaceTracker (beta)', lambda: nuke.createNode('FaceTracker'), icon='FaceTracker.png')
        if 'OFF' == 'ON':
            kt_menu.addCommand('FlowEvaluationTool', lambda: nuke.createNode('FlowEvaluationTool'), icon='KeenTools.png')
        if 'ON' == 'ON':
            kt_menu.addCommand('TextureBuilder (beta)', lambda: nuke.createNode('TextureBuilder'), icon='TextureBuilder.png')


    if not proper_keentools_version_found:
        # add a warning to menu

        def keentools_version_to_str(keentools_version):
            path, nuke_v, os = keentools_version
            return '  - Nuke{0} {1} at \n    "{2}"'.format(nuke_v, os, path)

        available_keentools_versions_str = '\n'.join(
            [keentools_version_to_str(x) for x in available_keentools_versions])
        warning_text = ("You are using Nuke{0} on {1}\n"
                        "There is no KeenTools for that configuration installed\n"
                        "\n"
                        "Available KeenTools installations:\n"
                        "{2}").format(
                            current_nuke_version(), current_platform(),
                            available_keentools_versions_str)
        toolbar.removeItem('KeenTools')
        toolbar.addCommand('KeenTools', lambda: nuke.message(warning_text), icon='KeenTools.png')


####################################

#install deadline submission script for win nuke11.2


import DeadlineNukeClient
menubar = nuke.menu("Nuke")
tbmenu = menubar.addMenu("&Thinkbox")

#advancedSumbission creates the artifact upon script sumbission

def advancedSubmission():
    nuke.scriptSave()
    DeadlineNukeClient.main()
    createArtifact()
    if nuke.ask('Do you want to version up your script?'):
        incrementalSave()
    return

tbmenu.addCommand("Submit Nuke To Deadline", 'advancedSubmission()')

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

if nuke.env['nukex'] == False: # Check Nuke or Nuke X and add menu only if cheep nuke is running
    switchX = nuke.menu("Nuke").addCommand('File/Switch to NukeX ', 'import nukeSwitch\nnukeSwitch.versionSwitch()')



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
nuke.knobDefault('Write.create_directories', 'True')
nuke.knobDefault("Write.exr.compression","4")   #RLE as default EXR compression
nuke.knobDefault("EXPTool.mode", "0")   #Stops as default Exposure Parameter
nuke.menu('Nodes').addCommand( "Time/FrameHold", "nuke.createNode('FrameHold')['first_frame'].setValue( nuke.frame() )", icon='FrameHold.png')



#create keep function add it to the channel menu
def createkeep():
    nuke.createNode('Remove')
    rem = nuke.selectedNode()
    rem.knob('operation').setValue('keep')
    rem.knob('channels').setValue('rgba')
    return
nuke.menu('Nodes').addCommand( "Channel/Keep", "createkeep()", icon="Remove.png")
nuke.menu('Nodes').addCommand( "Filter/Dilate", "nuke.createNode('Dilate')", icon="ErodeFast.png")


#add custom resolutions to format list

DCP_2K_Full = '2048 1152 DCP_2K_Full'
nuke.addFormat(DCP_2K_Full)

DCP_2K_Scope = '2048 858 DCP_2K_Scope'
nuke.addFormat(DCP_2K_Scope)


DCP_2K_Flat = '1998 1080 DCP_2K_Flat'
nuke.addFormat(DCP_2K_Flat)



####################################


# custom shortcuts

toolbar = nuke.menu('Nodes')
toolbar.addCommand('Merge/KeyMix', 'nuke.createNode("Keymix")', 'v')
toolbar.addCommand('Color/Invert', 'nuke.createNode("Invert")', 'alt+ctrl+i')
toolbar.addCommand('Merge/Premult', 'nuke.createNode("Premult")', 'alt+shift+p')
toolbar.addCommand('Merge/Unpremult', 'nuke.createNode("Unpremult")', 'alt+shift+u')
toolbar.addCommand('Channel/ChannelMerge', 'nuke.createNode("ChannelMerge")', 'shift+m')
toolbar.addCommand('Color/Math/Expression', 'nuke.createNode("Expression")', 'e')
toolbar.addCommand('Transform/TransformMasked', 'nuke.createNode("TransformMasked")', 'shift+t')


####################################





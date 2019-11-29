####################################

'''
NFTS - National Film and Television School.
latest update by Nicola Borsari: 2019-11-08
'''

####################################

'''
This script cheks the current version of nuke and OS to load the right copy of the 3DE plugin

Currently the only supported versions are 11.2 - 11.3 - 12.0 for Mac and PC

'''

####################################

'''
Import standard Python modules.
'''

import os, nuke

####################################


nMajor = nuke.NUKE_VERSION_MAJOR
nMinor = nuke.NUKE_VERSION_MINOR

Equalizer = False #initialize the variable that will be used to load the GUI menus if True



if nuke.env['LINUX']:
    Equalizer = False #remove support for LINUX
else:

    #behaviour for nuke 11
    if nMajor == 11 and nMinor == 2 or nMajor == 11 and nMinor == 3:
        if nMinor == 2:
            if nuke.env['WIN32']:
                nuke.pluginAddPath("./3DE4/win/11.2")
            else:
                nuke.pluginAddPath("./3DE4/mac/11.2")
            Equalizer = True
        else:
            if nuke.env['WIN32']:
                nuke.pluginAddPath("./3DE4/win/11.3")
            else:
                nuke.pluginAddPath("./3DE4/mac/11.3")
            Equalizer = True

    #behavious for nuke 12
    if nMajor == 12 and nMinor == 0:
        Equalizer = True
        if nuke.env['WIN32']:
            nuke.pluginAddPath("./3DE4/win/12.0")
        else:
            nuke.pluginAddPath("./3DE4/mac/12.0")




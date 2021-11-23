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
    version = "{}.{}".format(nMajor, nMinor)

    if nuke.env['WIN32']:
        platform = 'win'
    else:
        platform = 'mac'
        
    if os.path.isdir(os.path.join(os.path.dirname(__file__), platform, version)):
        nuke.pluginAddPath('./3DE4/{}/{}'.format(platform, version))
        Equalizer = True
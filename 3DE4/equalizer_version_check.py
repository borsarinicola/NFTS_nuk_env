####################################

"""
NFTS - National Film and Television School.
latest update by Nicola Borsari: 2023-10-14
This script cheks the current version of nuke and OS to load the right copy of the 3DE plugin
Currently the suporting versions between are 11.2 and 14.0 for Mac and PC
"""

####################################

# Import standard Python modules.


import os
import nuke  # pylint: disable=import-error


####################################


nMajor = nuke.NUKE_VERSION_MAJOR
nMinor = nuke.NUKE_VERSION_MINOR

EQUALIZER = (
    False  # initialize the variable that will be used to load the GUI menus if True
)


if nuke.env["LINUX"]:
    EQUALIZER = False  # remove support for LINUX
else:
    VERSION = "{}.{}".format(nMajor, nMinor)

    if nuke.env["WIN32"]:
        PLATFORM = "windows"
    else:
        PLATFORM = "osx"

    if os.path.isdir(
        os.path.join(os.path.dirname(__file__), PLATFORM, "Nuke" + VERSION)
    ):
        nuke.pluginAddPath("./3DE4/{}/Nuke{}".format(PLATFORM, VERSION))
        EQUALIZER = True

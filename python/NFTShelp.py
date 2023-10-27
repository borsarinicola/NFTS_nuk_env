####################################

"""
NFTS - National Film and Television School.
latest update by Nicola Borsari: 2023-10-24
"""

####################################

"""

This file should be used to add help functionalities only.
to add to the existing Nuke help Nuke menu use h.addCommand 

"""

#####################################

# import standard modules

import webbrowser
import nuke # pylint: disable=import-error

# add environment help

menubar = nuke.menu("Nuke")
h = menubar.menu("NFTS").addMenu("Help")


h.addCommand(
    "NFTS Environment Help",
    lambda: webbrowser.open("https://github.com/borsarinicola/nfts_nuk_env"),
)

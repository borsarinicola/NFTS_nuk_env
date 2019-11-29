####################################

'''
NFTS - National Film and Television School.
latest update by Nicola Borsari: 2019-11-29
'''

####################################

'''

This file should be used to add help functionalities only.
to add to the existing Nuke help Nuke menu use h.addCommand 

'''

#####################################

#import standard modules

import os, sys, nuke, nukescripts

# add environment help 

menubar = nuke.menu("Nuke")
h = menubar.menu("&Help")


h.addCommand('NFTS Environment Help', 'nukescripts.start("https://github.com/borsarinicola/nfts_nuk_env")')
h.addCommand('Deadline Guidelines', 'nukescripts.start("file://digitalfxserver/CompEnvironment/documentation/deadline10_guidelines.pdf")')
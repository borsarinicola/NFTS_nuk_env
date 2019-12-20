####################################

'''
NFTS - National Film and Television School.
latest update by Nicola Borsari: 2019-11-28
'''

####################################

#import standard modules

import os, sys, nuke


#def and install NFTS CopyPaste
#thanks Lars for the idea of this tool


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
nuke.menu( 'Nuke' ).addCommand('NFTS/NFTS Share/Share Selected Nodes', 'NFTSCopyPaste.nftsCopy()', 'Alt+Shift+C')
nuke.menu( 'Nuke' ).addCommand('NFTS/NFTS Share/Paste Shared Nodes', 'NFTSCopyPaste.nftsPaste()', 'Alt+Shift+V')
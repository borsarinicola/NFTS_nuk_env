####################################

'''
NFTS - National Film and Television School.
latest update by Nicola Borsari: 2019-11-28
'''

####################################

#import standard modules

import os, sys, nuke

def shuffleAll():
    nuke.root()

    read=nuke.Root().selectedNode()
    layer=nuke.layers(read)


    for i in layer:
        if i =='rgb' or 'rgba' or 'alpha':
            try:        
                layer.remove('rgb')
                layer.remove('rgba')
                layer.remove('alpha')
            except:
        
                s=nuke.createNode("Shuffle", inpanel = False)
                s.knob('in').setValue(i)
                s.knob('out').setValue('rgba')
                s.knob('label').setValue('[value in]')
                s.setInput(0, read)
                s.knob('postage_stamp').setValue(0)
        nuke.root().end()
        
    return
####################################
#Nicola Borsari change clip FPS for nuke studio - 20 December 2019 - v1.0


import nuke

if nuke.env['studio'] == True: # check if we are running in nuke studio


    def setFPS():

        import hiero.core, hiero.ui # import hiero modules - importing outisde the function will return errors!

        view = hiero.ui.activeView()
        sel = view.getSelection() 
        framerate = nuke.getInput('New Framerate') # ask user for new framerate with input box
        x = 0
        for each in sel: 
            if x < len(sel): 
                sel[x].activeItem().setFramerate(framerate) #apply framerate
                x = x+1
        return

    nuke.menu( 'Nuke' ).addCommand('NFTS/Nuke Studio Tools/Change Clip FPS', 'hieroFPS.setFPS()','Alt+Shift+F') #add command into NFTS menu

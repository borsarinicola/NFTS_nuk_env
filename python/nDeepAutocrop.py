####################################
#Nicola Borsari nDeepAutoCrop - 13 August 2018 - v2.2

import nuke
import os
import os.path
import nukescripts

def nDeepAutocrop():

    selection = nuke.selectedNodes() #store selection into list

    i = 0 #counter for node class test loop


    # message variables 
    dtoimgerror = 'You have a DeepToImage node in your selection. This node does not output deep data and therefore it is not possible to run the DeepAutoCrop function!'
    successmsg = 'The DeepAutocrop has been successfully completed!'   
    nondeeperror = 'You have a non-deep node in your selection!'     


    def dAutocropFN():

        x = 0 #counter for process loop

        for each in selection:
            processing = selection[x]

            if x <= len(selection):

                x = x+1
            
                #clear selection and prepare a new one for processing 
                nukescripts.clear_selection_recursive()
                processing.knob("selected").setValue(True)

                #create tmp deep to image and store it in a tmp variable
                sSelection = nuke.selectedNode()
                deeptoimg = nuke.createNode('DeepToImage')
                    
                #create a crop to get root format and store in variable
                cropTool = nuke.createNode('Crop')
                cropTool.setInput(0,deeptoimg)
                cropBox = cropTool.knob('box').getValue()
                
                #create and run curvetool    
                curveNode = nuke.createNode('CurveTool')
                curveNode.knob('operation').setValue('AutoCrop')      
                curveNode.knob('name').setValue('tmp_AC')
                curveNode.knob('ROI').setValue(cropBox)    
                nuke.execute(curveNode, nuke.root().firstFrame(), nuke.root().lastFrame())
                
                #create, connect and copy anim to deepcrop
                cropNode = nuke.nodes.DeepCrop()            
                cropNode.knob('bbox').copyAnimations( curveNode.knob('autocropdata').animations() )
                cropNode.setInput(0,sSelection)
                cropNode.knob('use_znear').setValue(False)
                cropNode.knob('use_zfar').setValue(False)
                cropNode.knob('label').setValue('AutoCrop')
                
                #remove tmp nodes
                nuke.delete(deeptoimg)
                nuke.delete(cropTool)
                nuke.delete(curveNode)

            else:
                #break loop and give succes message            
                break       
        return


    for each in selection:
        name = selection[i].Class()
        if 'Deep' in name: #test if the node's class is Deep* to continue
            if 'ToImage' in name: #test if DeepToImage is in the node's class to break loop and give error
                nuke.message(dtoimgerror)
                break
            else:
                i = i+1
                if i == len(selection):
                    dAutocropFN() #if check passed, else run autocrop function
                    nuke.message(successmsg) #message use of succes
                    break
        else:
            nuke.message(nondeeperror) #message user if there's a non deep node in the selection
            break

    return

####################################
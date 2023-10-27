import nuke, os, sys

def Gizmo2Group():

	def isGizmo(node):
	    return 'gizmo_file' in node.knobs()
	     
	def getGizmos():
	    allNodes = nuke.allNodes()
	    if allNodes:
	        gizmos = [f for f in allNodes if isGizmo(f)]
	        if gizmos:
	            return gizmos
	    return False
	 
	def deselectAll():
	    # deselect all nodes.
	    for i in nuke.allNodes():
	        i.knob('selected').setValue(False)
	         
	def convertGizmoToGroup(gizmo):
	    # convert a gizmo to an identical group.
	    # delete the original, reconnect the group in the chain.
	    # rename the group to match the original.
	    inputs = []
	    for x in range(0, gizmo.maximumInputs()):
	        if gizmo.input(x):
	            # print('input: %s' % (gizmo.input(x).knob('name').value()))
	            inputs.append(gizmo.input(x))
	        else:
	            inputs.append(False)
	    origName = gizmo.knob('name').value()
	    origPosX = gizmo.xpos()
	    origPosY = gizmo.ypos()
	    deselectAll()
	    # select knob, then run gizmo.makeGroup()
	    gizmo.knob('selected').setValue(True)
	    newGroup = gizmo.makeGroup()
	    deselectAll()
	    # delete original
	    nuke.delete(gizmo)
	    newGroup.knob('name').setValue(origName)
	    newGroup['xpos'].setValue(origPosX)
	    newGroup['ypos'].setValue(origPosY)
	    # disconnect old inputs
	    # reconnect inputs
	    for x in range(0, newGroup.maximumInputs()):
	        newGroup.setInput(x,None) 
	        if inputs[x]:
	            newGroup.connectInput(x, inputs[x])
	        # print('connecting output: %s to input: %s' % (inputs[x].knob('name').value(), newGroup.input(x).name()))
	    return newGroup
	     
	def convertGizmosToGroups():
	    gizmos = getGizmos()
	    if gizmos:
	        for i in gizmos:
	            convertGizmoToGroup(i)
	    return
	            


	convertGizmosToGroups()
	nuke.scriptSave()
	return
	
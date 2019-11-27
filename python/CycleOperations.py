# Max van Leeuwen - maxvanleeuwen.com
# CycleOperations - 1.3
# 
# 
# The standard knob of the selected node will cycle through its options, forwards or backwards (depending on the used keyboard shortcut).
# 
# 
# The following nodes are supported:
# 
# Merge, ChannelMerge and MergeMat nodes will scroll through all operations, except if their respective list down below have one or more items in it. In this case, the node will scroll only through the items in that list!
# If a Switch node is selected, it will scroll through the Switch node's inputs.
# If a Colorspace or OCIOColorspace node is selected, it will swap the in and out colourspaces.
# If a Shuffle or ShuffleCopy node is selected, the 'in' knob will be cycled
# If a Keyer node is selected, the 'operation' knob will be cycled
# 
# Operation list example: ['minus', 'multiply', 'over', 'plus']


C_Merge = []
C_ChannelMerge = []
C_MergeMat = []


#########################################


import nuke


# function for nodes with possible operation lists
def Merge(n, cycle, forwards):

	try:


		# get knob
		k = n.knob('operation')


		# if custom list is used
		if len(cycle) > 0:

			# get knob value as str
			currOp = k.value()

			# check if current value is in cycle
			nextOp = ''
			if currOp in cycle:

				# get next or pevious item index (depending on forwards)
				index = cycle.index(currOp) + (1 if forwards else -1)

				# return to 0 if out of range
				if(index > (len(cycle)) - 1):
					index = 0

				# set new value
				nextOp = cycle[index]

			else:
				
				# reset to first in cycle
				nextOp = cycle[0]

			# set new value to knob
			n.knob("operation").setValue(nextOp)


		# if not, simply scroll through all options
		else:

			# current operation
			currOp = k.getValue()

			# operation count
			countOp = len(k.values())

			if forwards:

				# if last item in list, go to start
				if int(currOp) + 1 == countOp:
					k.setValue(0)
				
				else:
					k.setValue(int(currOp) + 1)
				    

			else:

				if currOp == 0:
					k.setValue(countOp - 1)
				else:
					k.setValue(int(currOp) - 1)

	except:
		pass


# function for Switch nodes
def Switch(n, forwards):

	try:
		

		# get current value
		currWhich = n.knob('which').getValue()
		# get amount of inputs on Switch (-1, to match input index which starts counting at 0)
		maxWhich = n.inputs() - 1.0

		# make Switch nodes with only one input alternate between 1 and 0
		if(maxWhich == 0):
			maxWhich = 1

		# new value for Which on Switch
		newWhich = -1.0
		if forwards:

			newWhich = currWhich + 1.0
			if maxWhich < newWhich:
				newWhich = 0.0

		else:

			newWhich = currWhich - 1.0
			if newWhich < 0.0:
				newWhich = maxWhich

		n.knob('which').setValue(newWhich)

	except:
		pass


def OCIOColorSpace(n):

	try:
		

		# get knobs
		k1 = n.knob('in_colorspace')
		k2 = n.knob('out_colorspace')

		# get values
		inC = k1.value()
		outC = k2.value()

		# set inverse values
		k1.setValue(outC)
		k2.setValue(inC)

	except:
		pass


def Shuffle(n, forwards):

	try:


		# get knob
		k = n.knob('in')

		# get current layer (str)
		currL = k.value()

		# get all existing layers
		listL = nuke.layers()

		# get index of current layer
		i = 0
		for eachL in listL:
			if eachL == currL:
				break
			i += 1

		# get new layer
		if forwards:
			if len(listL) == i + 1:
				newL = listL[0]
			else:
				newL = listL[i + 1]
		else:
			if i == 0:
				newL = listL[len(listL) - 1]
			else:
				newL = listL[i - 1]


		# set new layer
		k.setValue(newL)


		# get label knob
		label = n.knob('label')

		# get new label text
		labelText = '[value in]'

		# get current label text
		currLabel = label.getValue()

		# check if the label is already present
		if not labelText in currLabel:

			# add new line and original value before new label text, if a label already exists
			if currLabel is not '':
				label.setValue(currLabel + '\n' + labelText)
			else:
				label.setValue(labelText)

	except:
		pass


# generic node cycling (custom knob name)
def otherNode(n, knobName, forwards):

	try:


		# get knob
		k = n.knob(knobName)

		# get knob value (int)
		currOp = k.getValue()

		# operation count
		countOp = len(k.values())


		# if forwards scrolling
		if forwards:

			# if last item in list, go to start
			if int(currOp) + 1 == countOp:
				k.setValue(0)

			else:
				# go forward one item
				k.setValue(int(currOp + 1))


		# scroll backwards
		else:

			# if at first item, go to end
			if currOp == 0:
				k.setValue(countOp - 1)

			# go back one item
			else:
				k.setValue(int(currOp - 1))

	except:
		pass




# cycle for each node (forwards or backwards)
def CycleOperations(forwards = True):

	# call function with cycle for each node
	for i in nuke.selectedNodes():

		# nodes with custom operation lists
		if i.Class() == 'Merge2':
			Merge(i, C_Merge, forwards)
		if i.Class() == 'ChannelMerge':
			Merge(i, C_ChannelMerge, forwards)
		if i.Class() == 'MergeMat':
			Merge(i, C_MergeMat, forwards)

		# scroll through switch inputs
		if i.Class() == 'Switch':
			Switch(i, forwards)

		# swap colorspace in/outs
		if i.Class() == 'Colorspace':
			i.knob('swap').execute()
		if i.Class() == 'OCIOColorSpace':
			OCIOColorSpace(i)

		# cycle Shuffle
		if i.Class() == 'Shuffle' or i.Class() == "ShuffleCopy":
			Shuffle(i, forwards)

		# cycle Keyer
		if i.Class() == 'Keyer':
			otherNode(i, 'operation', forwards)




# autostart (if not imported) - only goes forwards, if called this way
if __name__ == "__main__":
	CycleOperations()
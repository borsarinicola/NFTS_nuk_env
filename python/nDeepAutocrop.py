"""
Nicola Borsari nDeepAutoCrop - 13 August 2018 - v2.2
"""

# pylint: disable=import-error
import nuke


def run():
    """runner funcion that also checks selection"""

    # message variables
    nondeeperror = "You have a non-deep node in your selection!"

    def n_deep_autocrop(nodes):

        """core function that does the work"""

        for node in nodes:

            # create tmp deep to image and store it in a tmp variable
            deeptoimg = nuke.createNode("DeepToImage")
            deeptoimg.setInput(0, node)
            deeptoimg.setXYpos(node.xpos(), node.ypos() + 100)

            # create a crop to get root format and store in variable
            crop = nuke.createNode("Crop")
            crop.setInput(0, deeptoimg)
            crop_bbox = crop.knob("box").getValue()

            # create and run curvetool
            curve_node = nuke.createNode("CurveTool")
            curve_node.knob("operation").setValue("AutoCrop")
            curve_node.knob("name").setValue("tmp_AC")
            curve_node.knob("ROI").setValue(crop_bbox)
            nuke.execute(curve_node, nuke.root().firstFrame(), nuke.root().lastFrame())

            # create, connect and copy anim to deepcrop
            deep_crop = nuke.nodes.DeepCrop()
            deep_crop.knob("bbox").copyAnimations(
                curve_node.knob("autocropdata").animations()
            )
            deep_crop.setInput(0, node)
            deep_crop.knob("use_znear").setValue(False)
            deep_crop.knob("use_zfar").setValue(False)
            deep_crop.knob("label").setValue("AutoCrop")

            # remove tmp nodes
            nuke.delete(deeptoimg)
            nuke.delete(crop)
            nuke.delete(curve_node)

    selection = nuke.selectedNodes()

    for node in selection:
        node_class = node.Class().lower()
        if "deep" not in node_class or "deeptoimage" in node_class:
            nuke.message(nondeeperror)
            return None

    n_deep_autocrop(selection)

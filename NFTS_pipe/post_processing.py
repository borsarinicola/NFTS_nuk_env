"""
NFTS - National Film and Television School.
latest update by Nicola Borsari: 2023-10-16

The file contains usefull functions to process files after rendering
"""

import os
import re
import nuke  # pylint: disable=import-error


import callback_manager


def has_frame_padding(filepath):
    """
    Checks if there is frame padding in the filepath. This is done by looking for % or # padding
    @param filepath - Path to the file to check
    @return True if there is at least one % or # padding False if not or if either pattern is not
    """
    # Define patterns to match frame padding using '%' or '#'
    percent_padding_pattern = r"%[0-9]+d"
    hash_padding_pattern = "#+"

    # Use re.search to find the patterns in the filepath
    percent_match = re.search(percent_padding_pattern, filepath)
    hash_match = re.search(hash_padding_pattern, filepath)

    # If either pattern is found, there is frame padding
    return bool(percent_match or hash_match)


@callback_manager.bypass_pipeline_render_callbacks
def make_jpegs():
    """
    Make jpegs for each selected read. This is done by calling nuke.
    This function needs to bypass the AfterRender callbacks.
    """
    # Save script if the script is it's set.
    if nuke.root()["name"].getValue():
        nuke.scriptSave()

    reads = nuke.selectedNodes("Read")

    for read in reads:

        render_node_filepath = read["file"].value()
        file_name, _ = os.path.splitext(os.path.basename(render_node_filepath))

        # Returns the frame padding require if missing.
        if not has_frame_padding(render_node_filepath):
            padding = len(str(read["last"].value()))
            file_name = file_name + ".%0{}d".format(padding)

        # build the destination filepath
        write_fp = os.path.join(
            os.path.dirname(render_node_filepath), "jpegs", file_name + ".jpeg"
        )

        # create write and set knobs
        write = nuke.createNode("Write")
        write.setInput(0, read)
        write["use_limit"].setValue(True)
        write["first"].setExpression("[value input.first_frame]")
        write["last"].setExpression("[value input.last_frame]")
        write["file_type"].setValue("jpeg")
        write["file"].setValue(write_fp)

        # Set the preferred  colorspace to use for the write.
        prefered_colorspaces = ["review", "Output - Rec.709", "BT1886", "default"]
        for colorspace in prefered_colorspaces:
            if any(colorspace in s for s in write['colorspace'].values()):
                write["colorspace"].setValue(colorspace)
                break
            
        if bool(int(nuke.tcl("value {}.hasError".format(write.name())))):
            continue

        # Start rendering
        first = int(write["first"].getValue())
        last = int(write["last"].getValue())
        nuke.execute(write, first, last)

        nuke.delete(write)

    nuke.modified(False)

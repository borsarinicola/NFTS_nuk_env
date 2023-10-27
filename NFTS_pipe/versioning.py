"""
NFTS - National Film and Television School.
latest update by Nicola Borsari: 2023-10-16

The functions contained in this module handle the versioning of nodes and scripts.
Ideally a render's version should always match the script version that generated it
"""

import nuke  # pylint: disable=import-error
import nukescripts  # pylint: disable=import-error


def script_version():
    """
    Get the Nuke script version.
    @return the nuke version string (without token) if available. Otherwise False
    """
    script_filepath = nuke.root()["name"].value()
    try:
        version = nukescripts.version_get(script_filepath, "v")
        return version[1]
    except ValueError:
        return False


def get_node_version(node):
    """
    Get the version in the filepath of a node.
    @param node - The node object.
    @return the node filepath version string (without token) if available. Otherwise False
    """
    node_filepath = nuke.filename(node)
    try:
        version = nukescripts.version_get(node_filepath, "v")
        return version[1]
    except ValueError:
        return False


def set_node_version(node, version=script_version()):
    """
    Set the version of a node.
    @param node - The node object to change the version of.
    @param version - The version to set. Defaults to the script version
    """

    node_filepath = nuke.filename(node)
    # this excpetion ensures we can save a script for the first time
    try:
        new_filepath = node_filepath.replace(
            "v{}".format(get_node_version(node)), "v{}".format(version)
        )
        node["file"].setValue(new_filepath)
    except AttributeError:
        pass


def match_write_versions_to_script():
    """
    Match versions of Write and DeepWrite to the script.
    """
    write_nodes = nuke.allNodes("Write") + nuke.allNodes("DeepWrite")

    try:
        timeline_write = nuke.root()["timeline_write_node"].value()
        write_nodes.remove(nuke.toNode(timeline_write))
    except Exception:  # pylint: disable=broad-except
        pass

    for node in write_nodes:
        set_node_version(node, script_version())


def ask_to_version_script():
    """
    Asks to version up the script.
    """
    message = "Do you want to version up your script?"
    if nuke.ask(message):
        nukescripts.script_and_write_nodes_version_up()

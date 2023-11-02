"""
NFTS - National Film and Television School.
latest update by Nicola Borsari: 2023-10-16

The functions contained in this module handle the behavious of
artifacts. Artifacts are backup copies of the script to be generated
after the script has been rendered.
"""

import os
import shutil
import nuke  # pylint: disable=import-error

ARTIFACT_TOKEN = "_artifact"


def is_artifact():
    """
    Check if script is artifact. This is used to detect if
    the user is trying to run script with artifact token
    @return bool - True if artifact or False if not
    """
    script_filepath = nuke.root()["name"].value()
    script_name = os.path.basename(script_filepath)
    # Return true if script token is in script_name.
    if ARTIFACT_TOKEN in script_name:
        return True
    return False


def build_artifact_name():
    """
    Build artifact name from script name. This is used to determine
    the name of the artifact to be used when creating a new artifact.
    @return artifact name as a string.
    """
    script_filepath = nuke.root()["name"].value()
    script_name = os.path.basename(script_filepath)
    # The script name of the artifact.
    if not is_artifact():
        new_script_name = script_name.replace(".nk", ARTIFACT_TOKEN + ".nk")
        return new_script_name
    return script_name


def make_artifact():
    """
    Copy the artifact in the same directory. This is used to create a backup artifact
    """
    script_filepath = nuke.root()["name"].value()
    artifact_filepath = os.path.join(nuke.script_directory(), build_artifact_name())
    shutil.copy(script_filepath, artifact_filepath)


def artifact_warning():
    """
    Ask user to confirm they want to open the artifact.
    @return None
    """
    if not is_artifact():
        return

    error_message = """THIS SCRIPT IS AN ARTIFACT
     
This is a safe copy of this comp created when it was last rendered. it should not be edited, but rather used as a backup.
Are you sure you want to continue?
    """
    if not nuke.ask(error_message):
        nuke.scriptClose()

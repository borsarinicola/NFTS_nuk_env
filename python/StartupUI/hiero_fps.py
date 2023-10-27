"""
NFTS - National Film and Television School.
latest update by Nicola Borsari: 2023-10-24

This module contains functions to override clip's FPS interpretation.
"""

# pylint: disable=import-error
from PySide2 import QtWidgets

import hiero


def get_user_input():
    """
    Get user input FPS.
    This is a dialog to allow the user to enter the desired FPS
    @return str of user input
    """
    dialog = QtWidgets.QInputDialog()
    dialog.setInputMode(QtWidgets.QInputDialog.TextInput)
    dialog.setWindowTitle("Set Clips FPS")
    dialog.setLabelText("Please enter the desired FPS:")
    dialog.setTextValue("")  # Default input text

    result = dialog.exec_()

    # Return the user input from the dialog.
    if result == QtWidgets.QDialog.Accepted:
        user_input = dialog.textValue()
        return user_input
    else:
        return None


def set_fps():
    """
    Set framerate of selected clips. User input is used to set the framerate of the selected clips.
    @return None
    """
    view = hiero.ui.activeView()
    selection = view.getSelection()
    framerate = float(get_user_input())
    # apply framerate to all clip items
    for clip in selection:
        clip.activeItem().setFramerate(framerate)  # apply framerate
    return

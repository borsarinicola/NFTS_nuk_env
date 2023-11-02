"""
NFTS - National Film and Television School.
latest update by Nicola Borsari: 2023-10-24
"""

####################################

# Import standard Python modules.

import hiero # pylint: disable=import-error
import PySide2.QtGui # pylint: disable=import-error

####################################

# Import Custom Python scripts.

import hiero_presets
import hiero_fps

####################################

# Add custom calls to menus

def find_menu(name):
    """
    Find a menu by its name. This is used to find a menu item in the main menubar.
    If the menu is not found it gets added
    @param name - Name of the menu to find
    @return the menu object
    """
    # Returns the action that matches the name of the action.
    for action in hiero.ui.menuBar().actions():
        if action.text() == name:
            return action.menu()
    return hiero.ui.menuBar().addMenu(name)


nfts_menu = find_menu("NFTS")
ht_submenu = nfts_menu.addMenu("NFTS Hiero Tools")
presets_submenu = ht_submenu.addMenu("Presets")

change_fps_action = hiero.ui.createMenuAction("Change Clip FPS", hiero_fps.set_fps)
ht_submenu.addAction(change_fps_action)
change_fps_action.setShortcut(PySide2.QtGui.QKeySequence("Alt+Shift+F"))


reset_presets_action = hiero.ui.createMenuAction(
    "Reset Environment Presets", hiero_presets.reset_to_safe_presets
)
presets_submenu.addAction(reset_presets_action)


remove_user_presets_action = hiero.ui.createMenuAction(
    "Remove All User Presets", hiero_presets.remove_all_user_presets
)
presets_submenu.addAction(remove_user_presets_action)

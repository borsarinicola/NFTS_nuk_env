####################################

"""
NFTS - National Film and Television School.
latest update by Nicola Borsari: 2023-10-14
"""

####################################

import os
import nuke  # pylint: disable=import-error


def recursively_add_plugin_path(root_folder):
    """
    adds all the folders and subfolders in the Nuke plugin path
    Args:
        root_folder (string): the root folder to start the recursive add
    """
    for root, _, _ in os.walk(root_folder, topdown=False):
        nuke.pluginAddPath(root.replace("\\", "/"))

def create_gizmo_menu(gizmo_folder, menu=None):
    """
    Create a Nuke gizmo menu based on a folder structure.

    Traverses a specified folder and its subfolders to find Nuke gizmo
    (.gizmo and .nk) files and their corresponding PNG icons. It then creates a Nuke menu reflecting
    the folder hierarchy and assigns icons to the menu items.

    Usage:
    1. Specify the path to the main folder containing the gizmo files
    and icons in the 'main_folder_path' variable.
    2. Run the script in Nuke's Script Editor or execute it using the 'nuke.scriptSource' function.

    The script creates nested menus, where each subfolder becomes
    a submenu within its parent folder.
    Icons are assigned based on the assumption that they share the same
    name as their corresponding folders and gizmo files.

    Example:
        main_folder_path = '/path/to/your/main/folder'
        create_gizmo_menu(main_folder_path)
    """

    # Get the base name of the current folder
    folder_name = os.path.basename(gizmo_folder)

    # If menu is not provided, create a new menu in Nuke's toolbar
    if menu is None:
        menu = nuke.menu("Nodes").addMenu(
            folder_name, icon=os.path.join(gizmo_folder, folder_name + ".png")
        )
    else:
        # If menu is provided, create a submenu
        menu = menu.addMenu(folder_name)

        # Find the corresponding icon file for the submenu (assuming it has the same name)
        submenu_icon_file = os.path.join(gizmo_folder, folder_name + ".png")
        if os.path.exists(submenu_icon_file):
            menu.setIcon(submenu_icon_file)

    # Iterate through all files in the specified folder
    files = os.listdir(gizmo_folder)

    # Filter files to include only gizmo and nk files
    gizmo_files = [f for f in files if f.endswith((".gizmo", ".nk"))]

    # Iterate through each gizmo file
    for gizmo_file in gizmo_files:
        # Get the name of the gizmo (excluding the file extension)
        gizmo_name, _ = os.path.splitext(gizmo_file)

        # Create a menu item for each gizmo in the submenu
        menu_item = menu.addCommand(
            gizmo_name, 'nuke.createNode("{}")'.format(gizmo_name)
        )

        # Find the corresponding icon file for the menu item (assuming it has the same name)
        icon_file = os.path.join(gizmo_folder, gizmo_name + ".png")

        # Set the icon for the menu item if the icon file exists
        if os.path.exists(icon_file):
            menu_item.setIcon(icon_file)

    # Recursively process subfolders
    subfolders = [f for f in files if os.path.isdir(os.path.join(gizmo_folder, f))]
    for subfolder in subfolders:
        subfolder_path = os.path.join(gizmo_folder, subfolder)
        create_gizmo_menu(subfolder_path, menu)


# Specify the path to the main folder containing the gizmo file
NFTS_gizmos_root = os.path.join(os.getenv("NFTS_COMP_ENV_ROOT"), "NFTS_tools")
NFTS_gizmos_root = os.path.abspath(NFTS_gizmos_root)

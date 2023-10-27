"""
NFTS - National Film and Television School.
latest update by Nicola Borsari: 2023-10-24

This module contains functions to override clip's FPS interpretation.
"""

import os
import glob
import shutil


import hiero  # pylint: disable=import-error


HIERO_VERSION = "{}.{}".format(
    hiero.core.env["VersionMajor"], hiero.core.env["VersionMinor"]
)
HIERO_PLUGIN_PATH = os.getenv("HIERO_PLUGIN_PATH", "").replace("\\", "/")
PRESETS_PATH = os.path.join(
    os.getenv("NFTS_COMP_ENV_ROOT", HIERO_PLUGIN_PATH), "TaskPresets"
)
SAFE_PRESET = os.path.join(PRESETS_PATH, "NFTS_Safe_TaskPresets")
THIS_PRESET = os.path.join(PRESETS_PATH, HIERO_VERSION)


def check_missing_presets():
    """
    Check if presets are available for current Hiero version.
    if missing duplicate the presets of the latest versions.
    Falls back to the safe preset if none is available.
    """
    if HIERO_VERSION not in os.listdir(PRESETS_PATH):
        try:
            latest = glob.glob(os.path.join(PRESETS_PATH, "??.?"))[-1]
        except IndexError:
            latest = SAFE_PRESET
        shutil.copytree(latest, THIS_PRESET)


def reset_to_safe_presets():
    """
    Reset environment presets to safe presets.
    This useful as now users have RW access to presets, making them easily overwritten
    """
    shutil.rmtree(THIS_PRESET, ignore_errors=True)
    shutil.copytree(SAFE_PRESET, THIS_PRESET)


def remove_all_user_presets():
    """
    Remove all user presets sored in $HOME/.nuke/TaskPresets.
    """
    home = os.getenv("HOME")
    presets = os.path.join(home, ".nuke", "TaskPresets")
    shutil.rmtree(presets, ignore_errors=True)


# running this here makes this execute on Hiero start
check_missing_presets()

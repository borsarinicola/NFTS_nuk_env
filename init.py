####################################

"""
NFTS - National Film and Television School.
latest update by Nicola Borsari: 2023-11-02
"""

####################################

# Import standard Python modules.

import os
import glob
import nuke  # pylint: disable=import-error

####################################

# Import custom Python modules.

####################################

# Save env root in custom environment variable.

env_root = os.path.abspath(os.path.dirname(__file__)).replace("\\", "/")
os.environ["NFTS_COMP_ENV_ROOT"] = env_root

# Add plugin paths.

nuke.pluginAddPath("./NFTS_pipe")  # load NFTS pipe tools
nuke.pluginAddPath("./NukeSurvivalToolkit")
nuke.pluginAddPath("./gizmos")
nuke.pluginAddPath("./python")
nuke.pluginAddPath("./icons")
nuke.pluginAddPath("./3DE4")

# add 3DE4
import equalizer_version_check  # pylint: disable=import-error, unused-import, wrong-import-position, wrong-import-order

# recursively add folders in NFTS to the plugin path
import tools_loader  # pylint: disable=import-error, wrong-import-position, wrong-import-order

tools_loader.recursively_add_plugin_path(tools_loader.NFTS_gizmos_root)

# add 3DEqualizer

# recursively add keentools folders. version/platform management is done at the tool lever
for version in glob.glob(os.path.join(env_root, "KeenTools", "*_*.*")):
    if os.path.isdir(version):
        nuke.pluginAddPath(os.path.join(version))


####################################


# #Install Cryptomatte for Nuke 12 or Older
if nuke.NUKE_VERSION_MAJOR < 13:
    nuke.pluginAddPath("./cryptomatte")
    import cryptomatte_utilities  # pylint: disable=import-error

    cryptomatte_utilities.setup_cryptomatte()

####################################

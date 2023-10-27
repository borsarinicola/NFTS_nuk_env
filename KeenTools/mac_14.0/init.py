import os
import sys
# add KeenTools directory to python path to be able to import
# python files from KeenTools directory
current_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_directory)
from keentools_nuke_version_check import check_nuke_version_and_os, get_shared_lib_suffix


nuke.pluginAppendPath(
    os.path.join(current_directory, 'icons'))


# optional environment variable that can be set to specify the path to the data directory
# should be absolute or relative to the KeenTools library file (.so, .dll or .dylib)
# os.environ["KEENTOOLS_DATA_PATH"] = "../data"


def _keentools_get_load_plugin_lib(current_directory):
    def load_plugin_lib():
        # TODO load lib by full path not to change pluginPath
        nuke.pluginAppendPath(
            os.path.join(current_directory, 'plugin_libs'))
        try:
            nuke.load('KeenTools')
        except RuntimeError:
            error_message = 'Error! Failed to load KeenTools library. Please check KeenTools installation.'
            nuke.message(error_message)
            nuke.tprint(error_message)
    return load_plugin_lib


def _keentools_show_no_lib_warning(): 
    nuke.warning('No appropriate KeenTools installation '
                 'found. Can not create a KeenTools node')
    

if check_nuke_version_and_os('14.0', 'OSX', print_error_message=True):
    keentools_load_plugin_lib = _keentools_get_load_plugin_lib(
        current_directory)
else:
    print('KeenTools for Nuke14.0 OSX ignored')
    if 'keentools_load_plugin_lib' not in globals():
        keentools_load_plugin_lib = _keentools_show_no_lib_warning


# You may uncomment the next line to force KeenTools loading on Nuke startup
# Otherwise KeenTools loads on KeenTools nodes creation
# keentools_load_plugin_lib()

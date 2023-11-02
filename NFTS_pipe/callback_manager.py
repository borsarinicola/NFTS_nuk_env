"""
NFTS - National Film and Television School.
latest update by Nicola Borsari: 2023-10-16

Here we are collecting helper functions to deal with the
registration/unregistration of pipeline callbacks.
"""

import nuke  # pylint: disable=import-error

import versioning
import artifacting

####################################


# if you need to add a callback, add it to following dicrionary
# following the convention "callback type": function (case sensitive)
callback_dict = {
    "OnScriptSave": [versioning.match_write_versions_to_script],
    "OnScriptLoad": [artifacting.artifact_warning],
    "AfterRender": [artifacting.make_artifact, versioning.ask_to_version_script],
}


def register_pipeline_callbacks(callback_type):
    """
    Register callbacks for a given callback type.
    @param callback_type - The type of callback to
    """
    for call in callback_dict[callback_type]:
        callback_function_name = "add{}".format(callback_type)
        callback_registration_function = getattr(nuke, callback_function_name, None)
        if callback_registration_function:
            callback_registration_function(call)


def unregister_pipeline_callbacks(callback_type):
    """
    Unregister callbacks of a given type.
    @param callback_type - Type of callback to unregister ( string
    """
    for call in callback_dict[callback_type]:
        callback_function_name = "remove{}".format(callback_type)
        callback_unregistration_function = getattr(nuke, callback_function_name, None)
        if callback_unregistration_function:
            callback_unregistration_function(call)


def bypass_pipeline_render_callbacks(func):
    """
    Decorator to bypass AfterRender callbacks when doing something.
    @param func - The function to wrap. Must be a function that takes no arguments.
    """

    def wrapper():
        unregister_pipeline_callbacks("AfterRender")
        func()
        register_pipeline_callbacks("AfterRender")

    return wrapper


def bypass_pipeline_save_callbacks(func):
    """
    Decorator to bypass OnScriptSave callbacks when doing something.
    @param func - The function to wrap. Must be a function that takes no arguments.
    """

    def wrapper():
        unregister_pipeline_callbacks("OnScriptSave")
        func()
        register_pipeline_callbacks("OnScriptSave")

    return wrapper

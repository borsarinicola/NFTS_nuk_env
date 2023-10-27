import nuke


def current_nuke_version():
    return str(nuke.NUKE_VERSION_MAJOR) + '.' + str(nuke.NUKE_VERSION_MINOR)


def current_platform():
    from sys import platform
    if platform == "win32":
        return 'WIN'
    if platform == "linux" or platform == "linux2":
        return 'LINUX'
    if platform == "darwin":
        return 'OSX'
    assert(False)


def check_nuke_version_and_os(nuke_version, os_suffix, print_error_message=False):
    if current_platform() != os_suffix:
        if print_error_message:
            print('platform doesn\'t match')
        return False
    if current_nuke_version() != nuke_version:
        if print_error_message:
            print('nuke version doesn\'t match')
        return False
    return True


def get_shared_lib_suffix():
    platform = current_platform()
    if platform == 'WIN':
        return '.dll'
    if platform == 'LINUX':
        return '.so'
    if platform == 'OSX':
        return '.dylib'

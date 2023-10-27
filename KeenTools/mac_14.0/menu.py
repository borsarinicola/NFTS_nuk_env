from keentools_nuke_version_check import *
import nuke
import os


def _kt_add_node_to_menu(kt_menu, node_label, node_name=None, icon_path=None):
    if kt_menu is None:
        return

    if node_name is None:
        node_name = node_label
    if icon_path is None:
        icon_path = node_label + '.png'
    kt_menu.addCommand(node_label, 'nuke.createNode(\'%s\')' % node_name, icon=icon_path)


def _kt_add_node_to_menus(kt_menus, node_label, node_name=None, icon_path=None):
    for kt_menu in kt_menus:
        _kt_add_node_to_menu(kt_menu, node_label, node_name, icon_path)



def _kt_add_nodes_to_preferencies_color_class(node_names, color_class_name):
    preferences = nuke.toNode('preferences')
    assert(preferences)
    color_class = preferences.knob(color_class_name)
    if color_class is None:
        print('KeenTools: failed to add nodes to a color class')
        return
    current_class_nodes = set(color_class.getText().split())
    nodes_to_add = set(node_names) - current_class_nodes
    color_class.setText(color_class.getText() + ' ' + ' '.join(nodes_to_add))


def _kt_add_keentools_nodes_to_nodes_toolbar():
    toolbar = nuke.menu('Nodes')
    toolbar.removeItem('KeenTools')

    kt_menu = toolbar.addMenu('KeenTools', tooltip="""
        KeenTools v2023.2.0
        loaded from "{0}"
        """.format(_current_keentools_version[0]),
        icon='KeenTools.png')

    if nuke.env['NukeVersionMajor'] >= 14:
        about_3d = \
            'Nuke 14 introduced new 3D system that ' \
            'requires all 3D nodes to be reimplemented. ' \
            'We are going to reimplement all our Nodes to support ' \
            'new 3D system as 3D Classic nodes are still ' \
            'available.'
        kt_menu.addCommand('3D vs 3D Classic', lambda: nuke.message(about_3d))
        menu_3d = kt_menu.addMenu('3D')
        kt_menu = kt_menu.addMenu('3D Classic')
    else:
        menu_3d = None

    transform_like_nodes = []
    _kt_add_node_to_menu(kt_menu, 'GeoTracker')
    transform_like_nodes.append('GeoTracker')
    transform_like_nodes.append('TransformRiggedGeo')
    _kt_add_node_to_menu(kt_menu, 'PinTool')
    transform_like_nodes.append('PinTool')
    _kt_add_node_to_menu(kt_menu, 'ReadRiggedGeo')
    _kt_add_node_to_menu(kt_menu, 'FaceBuilder', 'FaceBuilder2')
    _kt_add_node_to_menu(kt_menu, 'FaceTracker')
    transform_like_nodes.append('FaceTracker')
    _kt_add_node_to_menu(kt_menu, 'FacialExpressions')
    transform_like_nodes.append('FacialExpressions')
    if 'ON' == 'ON':
        _kt_add_node_to_menus(
            [menu_3d, kt_menu], 'TextureBuilder',
            node_name='TextureBuilder',
            icon_path='TextureBuilder.png')
    blendshapes_menu = kt_menu.addMenu('Blendshapes', icon='Blendshapes.png')
    _kt_add_node_to_menu(blendshapes_menu, 'JoinBlendshapes')
    _kt_add_node_to_menu(blendshapes_menu, 'MixBlendshapes')
    _kt_add_node_to_menu(blendshapes_menu, 'FACS')
    if 'OFF' == 'ON':
        _kt_add_node_to_menu(kt_menu, 'View')
        _kt_add_node_to_menu(kt_menu, 'MultiviewGeoTracker')
        _kt_add_node_to_menu(kt_menu, 'ViewOut')
        
    _kt_add_nodes_to_preferencies_color_class(transform_like_nodes, 'NodeColourClass11')


def _kt_add_no_proper_keentools_warning_to_nodes_toolbar():
    toolbar = nuke.menu('Nodes')

    def keentools_version_to_str(keentools_version):
        path, nuke_v, os = keentools_version
        return '  - Nuke{0} {1} at \n    "{2}"'.format(nuke_v, os, path)

    available_keentools_versions_str = '\n'.join(
        [keentools_version_to_str(x) for x in available_keentools_versions])
    warning_text = ("You are using Nuke{0} on {1}\n"
                    "There is no KeenTools for that configuration installed\n"
                    "\n"
                    "Available KeenTools installations:\n"
                    "{2}").format(
                        current_nuke_version(), current_platform(),
                        available_keentools_versions_str)
    toolbar.removeItem('KeenTools')
    toolbar.addCommand('KeenTools', lambda: nuke.message(warning_text), icon='KeenTools.png')


if 'available_keentools_versions' not in globals():
    available_keentools_versions = []
    _proper_keentools_version_found = False

_current_keentools_version = (os.path.dirname(os.path.realpath(__file__)),
                             '14.0', 'OSX')
available_keentools_versions.append(_current_keentools_version)


if check_nuke_version_and_os(_current_keentools_version[1], _current_keentools_version[2]):
    _proper_keentools_version_found = True
    _kt_add_keentools_nodes_to_nodes_toolbar()


if not _proper_keentools_version_found:
    _kt_add_no_proper_keentools_warning_to_nodes_toolbar()

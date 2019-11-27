if 'available_keentools_versions' not in globals():
    available_keentools_versions = []
    proper_keentools_version_found = False

current_keentools_version = (os.path.dirname(os.path.realpath(__file__)),
                                '11.2', 'OSX')
available_keentools_versions.append(current_keentools_version)


toolbar = nuke.menu('Nodes')
if check_nuke_version_and_os(current_keentools_version[1], current_keentools_version[2]):
    proper_keentools_version_found = True

    # add KeenTools menu to Nodes toolbar
    toolbar.removeItem('KeenTools')
    kt_menu = toolbar.addMenu('KeenTools', tooltip="""
        KeenTools v1.4.7
        loaded from "{0}"
        """.format(current_keentools_version[0]),
        icon='KeenTools.png')
    kt_menu.addCommand('GeoTracker', lambda: nuke.createNode('GeoTracker'), icon='GeoTracker.png')
    kt_menu.addCommand('PinTool', lambda: nuke.createNode('PinTool'), icon='PinTool.png')
    kt_menu.addCommand('ReadRiggedGeo', lambda: nuke.createNode('ReadRiggedGeo'), icon='ReadRiggedGeo.png')
    if 'ON' == 'ON':
        kt_menu.addCommand('FaceBuilder', lambda: nuke.createNode('FaceBuilder'), icon='FaceBuilder.png')
    if 'ON' == 'ON':
        kt_menu.addCommand('FaceTracker (beta)', lambda: nuke.createNode('FaceTracker'), icon='FaceTracker.png')
    if 'OFF' == 'ON':
        kt_menu.addCommand('FlowEvaluationTool', lambda: nuke.createNode('FlowEvaluationTool'), icon='KeenTools.png')
    if 'ON' == 'ON':
        kt_menu.addCommand('TextureBuilder (beta)', lambda: nuke.createNode('TextureBuilder'), icon='TextureBuilder.png')
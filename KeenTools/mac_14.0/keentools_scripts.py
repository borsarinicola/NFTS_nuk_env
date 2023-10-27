import os.path
from collections import namedtuple
import nuke
import nukescripts


def _keentools_import_qapp():
    try:
        from PySide.QtGui import QApplication
    except ImportError:
        from PySide2.QtWidgets import QApplication
    return QApplication


_FrameRange = namedtuple('_FrameRange', ('first', 'last'))


if hasattr(nukescripts, 'PythonPanel'):  # False in render mode (for example)
    class _KeenTools_FrameRange_Dialog(nukescripts.PythonPanel):

        _INPUT = 'input'
        _GLOBAL = 'global'
        _CUSTOM = 'custom'
        _VIEWER_INOUT = 'in-out'
        _VIEWER_VISIBLE = 'visible'

        def __init__(self, title, input_node,
                     additional_front_range_sources=[],
                     additional_back_range_sources=[],
                     end_vspace=True):
            super(_KeenTools_FrameRange_Dialog, self).__init__(title)

            self._input_node = input_node
            input_range_source = [(self._INPUT, self._get_input_range)] \
                                 if self._input_node is not None else []
            default_range_sources = \
                [(self._GLOBAL, self._get_global_range),
                 (self._CUSTOM, self._get_custom_range)]

            viewer_range_sources = []
            for viewer in nuke.allNodes("Viewer", nuke.root()):
                viewer_range_sources.append(
                    (viewer.name() + '/' + self._VIEWER_INOUT,
                     lambda: self._get_viewer_in_out_range(viewer)))
                if nuke.NUKE_VERSION_MAJOR >= 12:
                    viewer_range_sources.append(
                        (viewer.name() + '/' + self._VIEWER_VISIBLE,
                         lambda: self._get_viewer_visible_range(viewer)))

            all_range_sources = additional_front_range_sources + \
                input_range_source + default_range_sources + \
                additional_back_range_sources + \
                viewer_range_sources
            self._range_sources = dict(all_range_sources)

            range_source_names = tuple(
                [source_name for source_name, _ in all_range_sources])
            self._range_source_name_knob = nuke.CascadingEnumeration_Knob(
                'range_source', 'Frame range', range_source_names
            )
            self.addKnob(self._range_source_name_knob)

            self._range_knob = nuke.String_Knob('range', ' ')
            self._range_knob.clearFlag(nuke.STARTLINE)
            self.addKnob(self._range_knob)

            self._set_frame_range(self._range_sources[range_source_names[0]]())

            if end_vspace:
                self.addKnob(nuke.Text_Knob('vspace', ' ', ' '))

        def knobChanged(self, knob):
            if knob is self._range_source_name_knob:
                source_name = self._range_source_name_knob.value()
                try:
                    current_range = self._range_sources[source_name]()
                    self._set_frame_range(current_range)
                except ValueError:
                    pass
                return

            if knob is self._range_knob:
                self._range_source_name_knob.setValue(self._CUSTOM)
                return

        def get_frame_range(self):
            input_str = self._range_knob.value()
            try:
                first, last = sorted(map(int, input_str.split('-')))
            except ValueError:
                raise
            return _FrameRange(first, last)

        def _get_input_range(self):
            return _FrameRange(self._input_node.firstFrame(),
                              self._input_node.lastFrame())

        def _get_viewer_in_out_range(self, viewer):
            r = viewer.playbackRange()
            return _FrameRange(r.first(), r.last())

        def _get_viewer_visible_range(self, viewer):
            r = viewer.visibleRange()
            return _FrameRange(r.first(), r.last())

        def _get_global_range(self):
            root = nuke.Root()
            return _FrameRange(root.firstFrame(), root.lastFrame())

        def _get_custom_range(self):
            return self.get_frame_range()

        def _set_frame_range(self, frame_range):
            if frame_range is None:
                self._range_knob.setValue('')
                return
            range_str = '%.0f-%.0f' % frame_range
            self._range_knob.setValue(range_str)


def keentools_run_analysis_with_dialog(kt_node):
    class KeenToolsAnalysis(object):
        _EXISTING_FILE_ERRMSG = 'Analysis file already exists. ' + \
            'Do you want to rewrite it? All data will be lost!'
        _EMPTY_FILE_ERRMSG = 'Please specify a file to save analysis data to.'
        _NON_EXISTING_FILE_ERRMSG = 'The target directory doesn\'t exist. ' + \
            'Turn on "create directories" checkbox and create the directory?'
        _INPUT_NAME = 'frames'
        _PANEL_TITLE = 'Run analysis'
        _CANCEL_IDX = 0

        def __init__(self, kt_node):
            self._node = kt_node
            self._input_node = self._node.input(0)

            self._first_frame_knob = self._node['_analysis_first_frame']
            self._last_frame_knob = self._node['_analysis_last_frame']

            self._set_error_combination()

        def _set_error_combination(self):
            self._first_frame_knob.setValue(0)
            self._last_frame_knob.setValue(-1)

        def _create_dialog(self):
            return _KeenTools_FrameRange_Dialog(
                self._PANEL_TITLE, self._input_node)

        def _run_precalc_dialog(self):
            dialog = self._create_dialog()
            while True:
                ok = dialog.showModalDialog()
                if not ok:
                    return
                try:
                    first, last = dialog.get_frame_range()
                    self._first_frame_knob.setValue(first)
                    self._last_frame_knob.setValue(last)
                    return
                except ValueError:
                    nuke.message('Invalid frame range')

        def _get_precalc_filename(self):
            return self._node['analysis_file_name'].evaluate()

        def _check_precalc_file(self, filename):
            if filename is None:
                nuke.message(self._EMPTY_FILE_ERRMSG)
                return False
            create_dir_knob = self._node['create_directories']
            dirname = os.path.dirname(filename)
            if not create_dir_knob.value() and dirname and not os.path.exists(dirname):
                if not nuke.ask(self._NON_EXISTING_FILE_ERRMSG):
                    return False
                create_dir_knob.setValue(True)
            if not os.path.exists(filename):
                return True
            return nuke.ask(self._EXISTING_FILE_ERRMSG)

        def _check_channels(self):
            ok = str(self._node['tracking_channels'].value()) != 'none'
            if not ok:
                nuke.message('All channels are disabled')
            return ok

        def _check_input_node(self):
            ok = self._input_node is not None
            if not ok:
                nuke.message('Video input node is not connected')
            return ok

        def run(self):
            filename = self._get_precalc_filename()

            if not self._check_input_node():
                return
            if not self._check_channels():
                return
            if not self._check_precalc_file(filename):
                return

            self._run_precalc_dialog()
            self._node['_run_analysis'].execute()

    KeenToolsAnalysis(kt_node).run()


def keentools_run_analysis(node, frame_from, frame_to, filepath):
    '''
    Executes analysis with specified parameters

        Parameters:
            node: a KeenTools node able to compute analysis (e.g. GeoTracker, FaceTracker)
            frame_from: analysis range `from` frame
            frame_to: analysis range `to` frame
            filepath: a path to a file where analysis will be saved.
                      WARNING: any existing file will be overwritten!
                      WARNING: .precalc extension is recommended!
    '''
    node.showControlPanel()
    node['_analysis_first_frame'].setValue(frame_from)
    node['_analysis_last_frame'].setValue(frame_to)
    node['analysis_file_name'].setValue(filepath)
    node['_run_analysis'].execute()


def keentools_create_exporting_utils():
    def create_node(node_creator, parent_position):
        node = node_creator()
        node.setXYpos(*parent_position)
        node.autoplace()
        return node


    def create_transform_geo(parent_position):
        transform_geo = create_node(nuke.nodes.TransformGeo, parent_position)
        transform_geo['rot_order'].setValue('XYZ')
        return transform_geo


    def create_axis(parent_position):
        axis = create_node(nuke.nodes.Axis, parent_position)
        axis['rot_order'].setValue('XYZ')
        return axis


    def create_transform_rigged_geo(parent_position):
        transform_geo = create_node(nuke.nodes.TransformRiggedGeo, parent_position)
        return transform_geo


    def create_camera(parent_position):
        cam = create_node(nuke.nodes.Camera, parent_position)
        cam['rot_order'].setValue('XYZ')
        return cam


    def create_facial_expressions(parent_position):
        fe = create_node(nuke.nodes.FacialExpressions, parent_position)
        return fe


    def create_default_camera(parent_position):
        cam = create_camera(parent_position)
        cam['haperture'].setValue(1.0)
        cam['vaperture'].setValue(1.0)
        cam['focal'].setValue(1.0)
        return cam


    def create_mix_blendshapes(ft_node):
        facs_node = create_node(nuke.nodes.FACS, get_position(ft_node))

        mix_blendshapes = create_node(nuke.nodes.MixBlendshapes, get_position(facs_node))
        mix_blendshapes.connectInput(0, facs_node)
        
        facs_node.connectInput(0, ft_node.input(1))

        return mix_blendshapes


    def is_camera(node):
        if not node.Class().startswith('Camera'):
            return False
        suffix = node.Class()[6:]
        return not suffix or suffix.isdigit()


    def get_input_camera(kt_node):
        cam = kt_node.input(2)
        while cam and not is_camera(cam):
            cam = cam.input(0)
        return cam


    def link_or_copy_knobs(link, src_node, dst_node, knob_names, knobs_vals={}):
        for n in knob_names:
            src_knob, dst_knob = n if isinstance(n, tuple) else (n, n)
            if link:
                expression = '%s.%s' % (src_node.name(), src_knob)
                dst_node[dst_knob].setExpression(expression)
            else:
                if dst_knob in knobs_vals:
                    dst_node[dst_knob].fromScript(knobs_vals[dst_knob])
                else:
                    dst_node[dst_knob].fromScript(src_node[src_knob].toScript())


    def link_or_copy_focal_length(link, kt_node, dst_cam):
        link_or_copy_knobs(link, kt_node, dst_cam,
                           (('focal_length', 'focal'),))


    def link_or_copy_camera_internal_params(link, src_cam, dst_cam):
        internal_params = ('haperture', 'vaperture', 'near', 'far',
                           'win_translate', 'win_scale', 'winroll', 'focal_point',
                           'fstop', 'projection_mode', 'focal')
        link_or_copy_knobs(link, src_cam, dst_cam, internal_params)


    def get_position(kt_node):
        return (kt_node.xpos(), kt_node.ypos())


    def uses_custom_focal_length(kt_node):
        return kt_node['focal_length_mode'].getValue() != 0


    def uses_ft_var_focal_length(kt_node):
        return kt_node['focal_length_mode'].getValue() == 2


    def uses_default_camera(kt_node):
        return get_input_camera(kt_node) is None


    def check_scale_and_export_transform_geo_if_needed(kt_node, link):
        if kt_node['scale'].value() == 1.0:
            return

        export_tg = \
            nuke.ask("You've changed the scale of the object, "
                     "the exported camera movement will align "
                     "only with a scaled object. Would you like "
                     "to export an additional TransformGeo node "
                     "with the appropriate scale settings?")

        if export_tg:
            export_transform_geo_impl(kt_node, link, with_scale=True, with_transforms=False)


    def link_or_copy_cam_views(link, kt_node, dst_cam):
        if link:
            link_or_copy_knobs(
                True,
                kt_node,
                dst_cam,
                (('cam_rotate', 'rotate'), ('cam_translate', 'translate'))
            )
            return

        src_rotate = kt_node['cam_rotate']
        src_translate = kt_node['cam_translate']
        dst_rotate = dst_cam['rotate']
        dst_translate = dst_cam['translate']

        dst_rotate.setAnimated()
        dst_translate.setAnimated()

        frames = set(kt_node['rotate'].getKeyList())
        frames |= set(kt_node['translate'].getKeyList())

        for frame in frames:
            rots = src_rotate.getValueAt(frame)
            trs = src_translate.getValueAt(frame)
            for channel, (rot, tr) in enumerate(zip(rots, trs)):
                dst_rotate.setValueAt(rot, frame, channel)
                dst_translate.setValueAt(tr, frame, channel)


    def export_transform_geo_impl(kt_node, link, with_scale, with_transforms):
        position = get_position(kt_node)
        transform_geo = create_transform_geo(position)

        export_knobs = []
        if with_scale:
            export_knobs += [('scale', 'uniform_scale')]
        if with_transforms:
            export_knobs += ['rotate', 'translate']

        link_or_copy_knobs(link, kt_node, transform_geo, export_knobs)


    class KeenToolsExportingUtils(object):
        @staticmethod
        def export_tracked_camera(kt_node, link):
            check_scale_and_export_transform_geo_if_needed(kt_node, link)
            cam = get_input_camera(kt_node)

            position = get_position(kt_node)
            if cam is None:
                new_cam = create_default_camera(position)
            else:
                new_cam = create_camera(position)
                link_or_copy_camera_internal_params(link, cam, new_cam)

            if uses_custom_focal_length(kt_node):
                link_or_copy_focal_length(link, kt_node, new_cam)

            link_or_copy_cam_views(link, kt_node, new_cam)


        @staticmethod
        def export_facial_expressions(kt_node, link):
            del link
            position = get_position(kt_node)
            facial_expressions = create_facial_expressions(position)

            is_facetracker = kt_node.Class() == 'FaceTracker'
            is_facebuilder = kt_node.Class() == 'FaceBuilder2'
            assert (is_facetracker + is_facebuilder == 1)


            if is_facebuilder:
                fb = kt_node
                facial_expressions.connectInput(0, fb)
                facial_expressions['use_expressions_from_source_geometry'].setValue(True)
                facial_expressions['use_transformations_from_expressions_input'].setValue(True)
            elif is_facetracker:
                ft = kt_node
                ft_fb_input = ft.input(1)
                facial_expressions.connectInput(0, ft_fb_input)
                facial_expressions.connectInput(1, ft)
                facial_expressions['use_transformations_from_expressions_input'].setValue(True)


        @staticmethod
        def export_camera(kt_node, link):
            position = get_position(kt_node)
            if uses_default_camera(kt_node):
                exported_camera = create_default_camera(position)
            else:
                exported_camera = create_camera(position)
                cam = get_input_camera(kt_node)
                link_or_copy_camera_internal_params(link, cam, exported_camera)
                link_or_copy_focal_length(link, kt_node, exported_camera)
                link_or_copy_knobs(link, cam, exported_camera, ('rotate', 'translate'))

            if uses_custom_focal_length(kt_node):
                link_or_copy_focal_length(link, kt_node, exported_camera)


        @staticmethod
        def export_transform_geo(kt_node, link):
            export_transform_geo_impl(kt_node, link, with_scale=True, with_transforms=True)


        @staticmethod
        def export_transform_geo_no_scale(kt_node, link):
            export_transform_geo_impl(kt_node, link, with_scale=False, with_transforms=True)


        @staticmethod
        def export_face_tracker(face_builder, link, knobs_vals):
            assert(not link)
            position = get_position(face_builder)
            face_tracker = create_node(nuke.nodes.FaceTracker, position)

            knobs_to_copy = ['rotate', 'translate', 'keyframes']
            if uses_ft_var_focal_length(face_builder):
                nuke.message('FaceTracker doesn\'t support varying '
                             'focal length which is selected in '
                             'FaceBuilder.\nThe default Focal Length '
                             'mode will be selected in FaceTracker, '
                             'hence the projection of the 3D model '
                             'may be inaccurate.')
            else:
                knobs_to_copy += ['focal_length_mode', 'focal_length']

            if face_builder['allow_facial_expressions'].value():
                knobs_to_copy.append('ModelEmotionsStorageKnob')
            link_or_copy_knobs(link, face_builder, face_tracker,
                               knobs_to_copy, knobs_vals)
            face_tracker.connectInput(0, face_builder.input(0))
            face_tracker.connectInput(1, face_builder)
            face_tracker.connectInput(2, face_builder.input(2))


        @staticmethod
        def export_axis(kt_node, link):
            position = get_position(kt_node)
            axis = create_axis(position)

            link_or_copy_knobs(link, kt_node, axis,
                               ('rotate', 'translate'))


        @staticmethod
        def export_transform_rigged_geo(kt_node, link):
            position = get_position(kt_node)
            transform_rigged_geo = create_transform_rigged_geo(position)

            link_or_copy_knobs(link, kt_node, transform_rigged_geo,
                               ('rotate', 'translate', 'scale'))


            # table knob won't be linked correctly unless it has the same 
            # structure. So we copy it by copying the values and then linking,
            # if required
            link_or_copy_knobs(False, kt_node, transform_rigged_geo,
                               ('bone_transformations', ))
            if link:
                link_or_copy_knobs(True, kt_node, transform_rigged_geo,
                                   ('bone_transformations', ))


        @staticmethod
        def export_transforms_as_transform_geo(kt_node, 
            translate_script, rotate_script, scale_script, skew_script):

            position = get_position(kt_node)
            transform_geo = create_transform_geo(position)

            transform_geo['translate'].setAnimated()
            transform_geo['translate'].fromScript(translate_script)

            transform_geo['rotate'].setAnimated()
            transform_geo['rotate'].fromScript(rotate_script)

            transform_geo['scaling'].setAnimated()
            transform_geo['scaling'].fromScript(scale_script)

            transform_geo['skew'].setAnimated()
            transform_geo['skew'].fromScript(skew_script)


        @staticmethod
        def export_ft_mods_as_facs_mix_blendshapes(ft_node, keyframes, all_values):
            mix_blendshapes = create_mix_blendshapes(ft_node)

            for bs_idx, bs_values in enumerate(all_values):
                bs_k = mix_blendshapes['blendshape_value_%d' % (bs_idx + 1)]
                bs_k.setAnimated()
                assert(len(keyframes) == len(bs_values))
                for keyframe, value in zip(keyframes, bs_values):
                    bs_k.setValueAt(value, keyframe)


        @staticmethod
        def export_ft_mods_as_facs_csv(ft_node):
            ExportSettings = namedtuple(
                'ExportSettings',
                ('frame_range', 'result_path', 'keyframes_only',
                 'use_framerate', 'framerate'))

            class Dialog(_KeenTools_FrameRange_Dialog):
                _FROM_KNOBS = 'tracked'

                def __init__(self, title, ft_node):
                    self._ft_node = ft_node
                    super(Dialog, self).__init__(
                        title, self._ft_node.input(0),
                        additional_front_range_sources=[(self._FROM_KNOBS, self._get_keyframes_range)],
                        end_vspace=False)

                    self._export_keyframes_only = nuke.Boolean_Knob(
                        'export_tracked_keyframes_only', 'tracked frames only')
                    self._export_keyframes_only.setFlag(nuke.STARTLINE)
                    self._export_keyframes_only.setTooltip(
                        'When on, only the frames with tracking information ' + \
                        '(incl. keyframes) are exported.')
                    self.addKnob(self._export_keyframes_only)


                    self._framerate = nuke.Double_Knob(
                        'framerate', 'Framerate')
                    self._framerate.setDefaultValue((nuke.root()['fps'].value(), ))
                    self._framerate.clearFlag(0x00000002) # disable slider
                    self.addKnob(self._framerate)

                    self._use_framerate = nuke.Boolean_Knob(
                        'write_timecode', 'write timecode', True)
                    self._use_framerate.setTooltip(
                        'The first column of the CSV file will contain ' + \
                        'not only the frame number, but also the calculated timestamp.')
                    self.addKnob(self._use_framerate)

                    self._result_csv_path = nuke.File_Knob('write_to_file', 'Write to')
                    self._result_csv_path.setFlag(nuke.STARTLINE)
                    self.addKnob(self._result_csv_path)

                def knobChanged(self, knob):
                    if knob is self._result_csv_path:
                        result_path = self._result_csv_path.value()
                        expected_extention = '.csv'
                        if not result_path.endswith(expected_extention):
                            self._result_csv_path.setValue(result_path + expected_extention)
                        return

                    if knob is self._use_framerate:
                        self._framerate.setEnabled(self._use_framerate.value())
                        return

                    super(Dialog, self).knobChanged(knob)

                def get_export_settings(self):
                    result_path = self._result_csv_path.value()
                    if result_path == '':
                        raise ValueError('Empty file path')

                    try:
                        return ExportSettings(
                            super(Dialog, self).get_frame_range(), 
                            result_path,
                            self._export_keyframes_only.value(),
                            self._use_framerate.value(),
                            self._framerate.value())
                    except ValueError:
                        raise ValueError('Invalid frame range')

                def _get_keyframes_range(self):
                    rotation_knob = self._ft_node['rotate']
                    rotation_knob_keys = rotation_knob.getKeyList()
                    if len(rotation_knob_keys) == 0:
                        return None
                    return _FrameRange(min(rotation_knob_keys), max(rotation_knob_keys))


            dialog = Dialog('Export as FACS animation', ft_node)
            while True:
                ok = dialog.showModalDialog()
                if not ok:
                    return
                try:
                    export_settings = dialog.get_export_settings()
                    ft_node['_export_ft_as_facs_frame_from'].setValue(export_settings.frame_range[0])
                    ft_node['_export_ft_as_facs_frame_to'].setValue(export_settings.frame_range[1])
                    ft_node['_export_ft_as_facs_file'].setValue(export_settings.result_path)
                    ft_node['_export_ft_as_facs_keyframes_only'].setValue(export_settings.keyframes_only)
                    ft_node['_export_ft_as_facs_use_framerate'].setValue(export_settings.use_framerate)
                    ft_node['_export_ft_as_facs_framerate'].setValue(export_settings.framerate)
                    ft_node['_export_ft_as_facs'].execute()
                    return
                except ValueError as e:
                    nuke.message(str(e))

    return KeenToolsExportingUtils


def keentools_create_keentools_utils_class():
    class KeenToolsUtils(object):
        @staticmethod
        def copy_expression(args):
            _keentools_import_qapp().clipboard().setText(args)

        @staticmethod
        def paste_expression():
            return _keentools_import_qapp().clipboard().text()

    return KeenToolsUtils


def keentools_create_ktl_utils_class():
    class KtlUtils(object):
        @staticmethod
        def copy_hardware_id():
            node = nuke.thisNode()
            hardware_id = node['hardware_id'].value()
            _keentools_import_qapp().clipboard().setText(hardware_id)

        @staticmethod
        def set_status_text(text):
            node = nuke.thisNode()
            node['license_status_text'].setValue(text)

        @staticmethod
        def clear_license_key():
            node = nuke.thisNode()
            node['license_key'].setValue('')

    return KtlUtils


def keentools_create_gpu_device_utils_class():
    class GpuDeviceUtils(object):
        @staticmethod
        def gpu_device():
            return nuke.toNode('preferences').knob('selectedGPUDeviceIndex').value()

    return GpuDeviceUtils


def keentools_run_mbs_load_csv_framerate_dialog():
    node = nuke.thisNode()

    framerate_knob = node['_load_csv_framerate']
    interpolate_knob = node['_load_csv_interpolate_frames']

    node['_do_preload_csv'].execute()
    if framerate_knob.getValue() == 0.0:
        # preload failed
        return

    
    class Dialog(nukescripts.PythonPanel):
        def __init__(self):
            super(Dialog, self).__init__('Import csv')
            self.framerate_knob = nuke.Double_Knob('fps', 'FPS')
            self.framerate_knob.setDefaultValue([framerate_knob.getValue()])
            self.framerate_knob.setRange(1, 120)
            self.framerate_knob.setTooltip(
                'Animation timecodes will be multiplied by ' + \
                'this value to transform seconds to frames.')
            self.addKnob(self.framerate_knob)
            self.interpolate_knob = nuke.Boolean_Knob('interpolate', 'Interpolate to whole frame numbers')
            self.interpolate_knob.setDefaultValue([interpolate_knob.getValue()])
            self.interpolate_knob.setFlag(nuke.STARTLINE)
            self.interpolate_knob.setTooltip(
                'If enabled the animation will be interpolated to integer frames.')
            self.addKnob(self.interpolate_knob)
            self.addKnob(nuke.Text_Knob('vspace', ' ', ' '))


    dialog = Dialog()
    if dialog.showModalDialog():
        framerate_knob.setValue(dialog.framerate_knob.getValue())
        interpolate_knob.setValue(dialog.interpolate_knob.getValue())
        node['_do_load_csv'].execute()

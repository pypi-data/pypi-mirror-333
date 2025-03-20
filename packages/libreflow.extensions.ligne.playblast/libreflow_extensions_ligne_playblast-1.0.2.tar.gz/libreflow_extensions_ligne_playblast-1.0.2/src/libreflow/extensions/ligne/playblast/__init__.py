import os

from kabaret import flow
from kabaret.flow.object import _Manager

import kabaret.app.resources as resources

from kabaret.flow_contextual_dict import get_contextual_dict

from libreflow.baseflow.file import RenderBlenderPlayblast,TrackedFile
from libreflow.baseflow.users import PresetSessionValue
from libreflow.utils.b3d import wrap_python_expr

class RenderBlenderPlayblastLigne(RenderBlenderPlayblast):
    _MANAGER_TYPE = _Manager

    render_lines = flow.SessionParam(True, PresetSessionValue).ui(
        tooltip="Render lines with Pencil+",
        editor='bool',
        )
    
    def check_default_values(self):
        super(RenderBlenderPlayblastLigne, self).check_default_values()
        self.render_lines.apply_preset()
    
    def update_presets(self):
        super(RenderBlenderPlayblastLigne, self).update_presets()
        self.render_lines.update_preset()
    
    def playblast_infos_from_revision(self, revision_name):
        filepath = self._file.path.get()
        filename = "_".join(self._file.name().split("_")[:-1])

        # Check if there is a AE compositing file
        if self._files.has_file('compositing', "aep"):
            playblast_filename = filename + "_movie_blend"
            playblast_revision_filename = self._file.complete_name.get() + "_movie_blend.mov"
        # Check if lines are disabled
        elif not self.render_lines.get():
            playblast_filename = filename + "_no_lines_movie"
            playblast_revision_filename = self._file.complete_name.get() + "_no_lines_movie.mov"
        else:
            playblast_filename = filename + "_movie"
            playblast_revision_filename = self._file.complete_name.get() + "_movie.mov"
        
        playblast_filepath = os.path.join(
            self.root().project().get_root(),
            os.path.dirname(filepath),
            playblast_filename + "_mov",
            revision_name,
            playblast_revision_filename
        )

        return playblast_filepath, playblast_filename, self._file.path_format.get()
    
    def extra_argv(self):
        file_settings = get_contextual_dict(
            self._file, "settings", ["sequence", "shot"]
        )
        project_name = self.root().project().name()
        revision = self._file.get_revision(self.revision_name.get())
        do_render = self.quality.get() == 'Final'
        python_expr = """import bpy
bpy.ops.lfs.playblast(do_render=%s, filepath='%s', studio='%s', project='%s', sequence='%s', scene='%s', quality='%s', version='%s', template_path='%s', do_autoplay=%s,render_lines=%s)""" % (
            str(do_render),
            self.output_path,
            self.root().project().get_current_site().name(),
            project_name,
            file_settings.get("sequence", "undefined"),
            file_settings.get("shot", "undefined"),
            'PREVIEW' if self.quality.get() == 'Preview' else 'FINAL',
            self.revision_name.get(),
            resources.get('mark_sequence.fields', 'default.json').replace('\\', '/'),
            self.auto_play_playblast.get(),
            self.render_lines.get(),
        )
        if not do_render:
            python_expr += "\nbpy.ops.wm.quit_blender()"
        
        args = [
            revision.get_path(),
            "--addons",
            "mark_sequence",
            "--python-expr",
            wrap_python_expr(python_expr),
        ]

        if do_render:
            args.insert(0, '-b')
        
        return args

    def run(self, button):
        if button == "Cancel":
            return
        elif button == "Submit job":
            self.update_presets()

            submit_action = self._file.submit_blender_playblast_job
            submit_action.revision_name.set(self.revision_name.get())
            submit_action.resolution_percentage.set(self.resolution_percentage.get())
            submit_action.use_simplify.set(self.use_simplify.get())
            submit_action.reduce_textures.set(self.reduce_textures.get())
            submit_action.target_texture_width.set(self.target_texture_width.get())
            
            return self.get_result(
                next_action=submit_action.oid()
            )
        
        self.update_presets()

        revision_name = self.revision_name.get()
        playblast_path, playblast_name, path_format = self.playblast_infos_from_revision(
            revision_name
        )

        # Get or create playblast file
        if not self._files.has_file(playblast_name, "mov"):
            tm = self.root().project().get_task_manager()
            df = next((
                file_data for file_name, file_data in tm.get_task_files(self._task.name()).items()
                if file_data[0] == f'{playblast_name}.mov'), None
            )
            playblast_file = self._files.add_file(
                name=playblast_name,
                extension="mov",
                base_name=playblast_name,
                tracked=True,
                default_path_format=path_format if df is None else df[1]
            )
            playblast_file.file_type.set('Outputs')
        else:
            playblast_file = self._files[playblast_name + "_mov"]
        
        playblast_file.source_file.set(self._file.oid())
        
        # Get or add playblast revision
        if playblast_file.has_revision(revision_name):
            playblast_revision = playblast_file.get_revision(
                revision_name
            )
        else:
            source_revision = self._file.get_revision(revision_name)
            playblast_revision = playblast_file.add_revision(
                name=revision_name,
                comment=source_revision.comment.get()
            )
        
        # Configure playblast revision
        playblast_revision.set_sync_status("Available")

        # Store revision path as playblast output path
        self.output_path = playblast_revision.get_path().replace("\\", "/")
        
        # Ensure playblast revision folder exists and is empty
        if not os.path.exists(self.output_path):
            os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        else:
            os.remove(self.output_path)

        result = GenericRunAction.run(self, button)
        self._files.touch()
        return result


def render_blender_playblast_ligne(parent):
    if isinstance(parent, TrackedFile):
        r = flow.Child(RenderBlenderPlayblastLigne)
        r.name = 'render_blender_playblast'
        r.index = 29
        return r


def install_extensions(session):
    return {
        "ligne_playblast": [
            render_blender_playblast_ligne,
        ]
    }


from . import _version
__version__ = _version.get_versions()['version']

import time
import os
import shutil
from kabaret import flow
from kabaret.flow.object import _Manager
from kabaret.flow_entities.entities import EntityCollection, Entity, Property
from libreflow.baseflow.file import GenericRunAction,TrackedFile
from libreflow.baseflow.task_manager import DefaultTaskFile


class DefaultTaskChoiceValue(flow.values.ChoiceValue):

    def choices(self):
        return [
            dft_task.display_name.get()
            for dft_task in self.root().project().get_default_tasks().mapped_items()
        ]


class DefaultFileChoiceValue(flow.values.ChoiceValue):

    _action = flow.Parent()

    def choices(self):
        if not self._action.task_name.get():
            return []

        _mgr = self.root().project().get_task_manager()

        return [
            file_name
            for n, (file_name, _, _, _, _, _, _, _, _, _, _, _) in _mgr.get_task_files(self._action.task_name.get().lower()).items()
        ]
    
    def revert_to_default(self):
        names = self.choices()
        self.set(names[0] if names else None)


class AddPublishRelation(flow.Action):

    task_name = flow.Param([], DefaultTaskChoiceValue).watched()
    file_name = flow.Param([], DefaultFileChoiceValue)

    _map = flow.Parent()

    def needs_dialog(self):
        return True

    def allow_context(self, context):
        return context

    def get_buttons(self):
        self.task_name.set('Animatic')
        return ['Create', 'Cancel']

    def child_value_changed(self, child_value):
        if child_value is self.task_name:
            self.file_name.revert_to_default()
    
    def run(self, button):
        if button == 'Cancel':
            return
        
        self._map.add_publish_relation(dict(
            name=f'relation_{str(int(time.time()))}',
            task_name=self.task_name.get(),
            file_name=self.file_name.get()
        ))


class RemovePublishRelation(flow.Action):

    ICON = ('icons.gui', 'remove-symbol')

    _relation = flow.Parent()
    _map = flow.Parent(2)

    def needs_dialog(self):
        return False

    def allow_context(self, context):
        return context

    def run(self, button):
        self._map.delete_publish_relation(self._relation.name())


class PublishRelation(Entity):

    task_name = Property()
    file_name = Property()

    remove = flow.Child(RemovePublishRelation)


class PublishRelations(EntityCollection):

    add_relation = flow.Child(AddPublishRelation)

    @classmethod
    def mapped_type(cls):
        return PublishRelation

    def add_publish_relation(self, data):
        c = self.get_entity_store().get_collection(
            self.collection_name())
        c.insert_one(data)
        self._document_cache = None
        self.touch()

    def delete_publish_relation(self, name):
        c = self.get_entity_store().get_collection(
            self.collection_name())
        c.delete_one(
            {'name': name}
        )
        self._document_cache = None
        self.touch()
    
    def get_publish_relation(self, task_name):
        match = [relation for relation in self.mapped_items() if relation.task_name.get() == task_name]
        return match[0] if match else None

    def columns(self):
        return ["Task", "File"]

    def _fill_row_cells(self, row, item):
        row["Task"] = item.task_name.get()
        row["File"] = item.file_name.get()


class PublishTaskChoiceValue(flow.values.ChoiceValue):

    _file = flow.Parent(2)
    _task = flow.Parent(4)

    def choices(self):
        _mgr = self.root().project().get_task_manager()
        _dft_file = None
        
        if _mgr.default_tasks.has_mapped_name(self._task.name()):
            _dft_task = _mgr.default_tasks[self._task.name()]
            
            if _dft_task.files.has_mapped_name(self._file.name()):
                _dft_file = _mgr.default_tasks[self._task.name()].files[self._file.name()]

                return [
                    relation.task_name.get()
                    for relation in _dft_file.publish_relations.mapped_items()
                ]
        
        return []
    
    def revert_to_default(self):
        choices = self.choices()
        if choices:
            self.set(choices[0])


class PublishNextTask(flow.Action):
    _MANAGER_TYPE = _Manager

    ICON = ("icons.libreflow", "publish")

    _file = flow.Parent()
    _task = flow.Parent(3)
    _tasks = flow.Parent(4)

    target_task = flow.Param([], PublishTaskChoiceValue)

    remove_animatic_layer = flow.BoolParam(False)
    keep_editing = flow.BoolParam(False)

    def get_buttons(self):
        self.message.set("<h2>Publish To Next Task</h2>")
        self.target_task.revert_to_default()
        self.remove_animatic_layer.revert_to_default()
        self.keep_editing.revert_to_default()

        return ['Publish', 'Cancel']

    def allow_context(self, context):
        return (
            context
            and self._file.get_revision_names(sync_status='Available', published_only=True) != []
            and self.target_task.choices() != []
        )

    def open_in_tvpaint(self,path):
        open_action = self._file.open_in_tvpaint
        open_action.file_path.set(path)
        open_action.run(None)

    def execute_remove_animatic_script(self, path, edit):
        exec_script = self._file.execute_remove_animatic_script
        exec_script.dest_path.set(path)
        exec_script.keep_editing.set(edit)
        exec_script.run(None)

    def _create_file(self, target_task, default_file):
        session = self.root().session()

        file_name = default_file.file_name.get()
        name, ext = os.path.splitext(file_name)
        target_file = None

        # Create default file
        if ext:
            if target_task.files.has_file(name, ext[1:]) is False:
                session.log_info(f'[Publish Next Task] Creating File {file_name}')
                target_file = target_task.files.add_file(
                    name, ext[1:],
                    display_name=file_name,
                    tracked=True,
                    default_path_format=default_file.path_format.get()
                )
                target_file.file_type.set(default_file.file_type.get())
                target_file.is_primary_file.set(default_file.is_primary_file.get())
            else:
                session.log_info(f'[Publish Next Task] File {file_name} exists')
                target_file = target_task.files[default_file.name()]
        else:
            if target_task.files.has_folder(name) is False:
                session.log_info(f'[Publish Next Task] Creating Folder {file_name}')
                target_file = target_task.files.add_folder(
                    name,
                    display_name=file_name,
                    tracked=True,
                    default_path_format=default_file.path_format.get()
                )
            else:
                session.log_info(f'[Publish Next Task] Folder {file_name} exists')
                target_file = target_task.files[default_file.name()]

        return target_file

    def publish_file(self, target_file):
        session = self.root().session()
        file_name = target_file.display_name.get()
        name, ext = os.path.splitext(file_name)

        source_revision = self._file.get_head_revision(sync_status='Available')

        if source_revision is not None and os.path.exists(source_revision.get_path()):

            if not self.remove_animatic_layer.get():
                if self.keep_editing.get():
                    r = target_file.create_working_copy()
                    session.log_info(f'[Publish Next Task] Creating Working Copy {target_file.display_name.get()} {r.name()}')
                
                else :
                    r = target_file.add_revision(comment=f'from {self._file.display_name.get()} {source_revision.name()}')
                    session.log_info(f'[Publish Next Task] Creating Revision {target_file.display_name.get()} {r.name()}')
                
                target_path = r.get_path()
                os.makedirs(os.path.dirname(target_path), exist_ok=True)
                
                session.log_info(f'[Publish Next Task] Copying Source Revision')

                if ext:
                    shutil.copy2(source_revision.get_path(), target_path)
                else:
                    shutil.copytree(source_revision.get_path(), target_path)

            else :
                r = target_file.create_working_copy()
                session.log_info(f'[Publish Next Task] Creating Working Copy {target_file.display_name.get()} {r.name()}')
                
                target_path = r.get_path()
                os.makedirs(os.path.dirname(target_path), exist_ok=True)
                
                session.log_info(f'[Publish Next Task] Removing Animatic')

                print(source_revision.get_path())
                print(target_path)

                self.open_in_tvpaint(source_revision.get_path())

                self.execute_remove_animatic_script(target_path, self.keep_editing.get())


    def run(self, button):
        if button == "Cancel":
            return

        # Get publish relation file name
        _mgr = self.root().project().get_task_manager()
        current_dft_file = _mgr.default_tasks[self._task.name()].files[self._file.name()]

        relation = current_dft_file.publish_relations.get_publish_relation(self.target_task.get())

        # Get default file data
        target_dft_file = _mgr.default_tasks[relation.task_name.get().lower()].files[relation.file_name.get().replace('.', '_')]
        
        # Get target task shot
        if self._tasks.has_mapped_name(relation.task_name.get().lower()):
            target_task_object = self._tasks[relation.task_name.get().lower()]

            # Create file
            target_file = self._create_file(target_task_object, target_dft_file)
            
            # Create revision
            self.publish_file(target_file)

class OpenInTvpaint(GenericRunAction):

    file_path = flow.Param()

    def allow_context(self, context):
        return context

    def runner_name_and_tags(self):
        return 'TvPaint', []

    def target_file_extension(self):
        return 'tvpp'

    def extra_argv(self):
        return [self.file_path.get()]


class ExecuteRemoveScript(GenericRunAction):

    dest_path = flow.Param()
    keep_editing = flow.BoolParam(False)

    def allow_context(self, context):
        return context
    
    def runner_name_and_tags(self):
        return 'PythonRunner', []

    def get_version(self, button):
        return None

    def get_run_label(self):
        return "Remove Animatic From Project"

    def extra_argv(self):
        current_dir = os.path.split(__file__)[0]
        script_path = os.path.normpath(os.path.join(current_dir,"scripts/remove_animatic.py"))
        return [script_path, '--destination', self.dest_path.get(), '--keep-editing', self.keep_editing.get()]


def publish_action(parent):
    if isinstance(parent, TrackedFile):
        r = flow.Child(PublishNextTask).ui(label='Publish to next task')
        r.name = 'publish_next_task'
        r.index = 28
        return r
    if isinstance(parent, DefaultTaskFile):
        r = flow.Child(PublishRelations)
        r.name = 'publish_relations'
        r.index = 13
        return r

def open_in_tvpaint(parent):
    if isinstance(parent, TrackedFile):
        r = flow.Child(OpenInTvpaint)
        r.name = 'open_in_tvpaint'
        r.index = None
        r.ui(hidden=True)
        return r

def execute_remove_animatic_script(parent):
    if isinstance(parent, TrackedFile):
        r = flow.Child(ExecuteRemoveScript)
        r.name = 'execute_remove_animatic_script'
        r.index = None
        r.ui(hidden=True)
        return r


def install_extensions(session):
    return {
        "2h14_publish": [
            publish_action,
            open_in_tvpaint,
            execute_remove_animatic_script,
        ]
    }


from . import _version
__version__ = _version.get_versions()['version']

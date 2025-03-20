import contextlib
from pathlib import Path
from unittest.mock import patch

import pytest

from automyte import Project
from automyte.config.base import Config
from automyte.discovery.explorers.base import ProjectExplorer
from automyte.discovery.explorers.local_files import LocalFilesExplorer
from automyte.vcs.base import VCS
from automyte.vcs.git import Git


class DummyExplorer(ProjectExplorer):
    def get_rootdir(self) -> str:
        return "smth"

    def set_rootdir(self, newdir: str):
        return "smth"

    def flush(self):
        self.flushed = True


class DummyVCS(VCS):
    def run(self, *args):
        return

    @contextlib.contextmanager
    def preserve_state(self, config):
        self.preserve_state_called = True
        yield "newdir"


class TestProjectInit:
    def test_requires_at_least_one_of_rootdir_or_explorer(self):
        with pytest.raises(ValueError):
            Project(project_id="proj1", vcs=Git(""))

    def test_uses_local_files_explorer_by_default(self, tmp_local_project):
        dir = tmp_local_project({})
        explorer = Project("proj1", rootdir=dir).explorer

        assert isinstance(explorer, LocalFilesExplorer)
        assert explorer.get_rootdir() == dir

    def test_assigns_roodir_from_explorer_if_no_rootdir_is_passed_in_init(self):
        explorer = DummyExplorer()

        proj = Project(project_id="proj1", explorer=explorer)

        assert proj.rootdir == "smth"

    def test_uses_git_vcs_with_correct_rootdir_by_default(self, tmp_local_project):
        dir = tmp_local_project({})
        vcs = Project(project_id="proj1", rootdir=dir).vcs

        assert isinstance(vcs, Git)
        assert vcs.original_rootdir == dir

    def test_validates_rootdir(self):
        with pytest.raises(ValueError):
            Project("proj1", rootdir="/some/definitely/not/existant/dir")


class TestProjectApplyChanges:
    def test_calls_explorer_flush(self):
        explorer = DummyExplorer()

        Project(project_id="proj1", explorer=explorer).apply_changes()

        assert explorer.flushed


class TestProjectInWorkingState:
    def test_calls_vcs_preserve_state(self, tmp_local_project):
        dir = tmp_local_project({})
        vcs = DummyVCS()

        with Project("proj1", rootdir=dir, vcs=vcs).in_working_state(Config.get_default()):
            ...

        assert vcs.preserve_state_called

    def test_sets_and_resets_own_rootdir_if_necessary(self, tmp_local_project):
        dir = tmp_local_project({})
        vcs = DummyVCS()
        project = Project("proj1", rootdir=dir, vcs=vcs)

        with project.in_working_state(Config.get_default()):
            assert project.rootdir == "newdir"
        assert project.rootdir == dir

    def test_updates_explorer_rootdir(self, tmp_local_project):
        dir = tmp_local_project({})
        vcs = DummyVCS()
        project = Project("proj1", rootdir=dir, vcs=vcs)

        with project.in_working_state(Config.get_default()):
            assert project.explorer.get_rootdir() == "newdir"
        assert project.explorer.get_rootdir() == dir


class TestProjectFromUri:
    def test_generates_correct_rootdir(self, tmp_local_project):
        dir = tmp_local_project({})
        assert Project.from_uri(dir).rootdir == dir

    def test_generates_unique_but_readable_project_id(self, tmp_local_project):
        dir = tmp_local_project({})
        with patch("automyte.project.project.random_hash", return_value="smth"):
            project = Project.from_uri(dir)

            assert project.project_id == f"smth_{Path(dir).name}"

    def test_sets_correct_explorer(self, tmp_local_project):
        dir = tmp_local_project({})
        explorer = Project.from_uri(dir).explorer

        assert isinstance(explorer, LocalFilesExplorer)
        assert explorer.get_rootdir() == dir

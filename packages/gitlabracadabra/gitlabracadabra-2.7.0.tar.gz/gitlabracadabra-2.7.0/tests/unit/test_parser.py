#
# Copyright (C) 2019-2025 Mathieu Parent <math.parent@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pytest

from gitlabracadabra.objects.group import GitLabracadabraGroup
from gitlabracadabra.objects.project import GitLabracadabraProject
from gitlabracadabra.parser import GitlabracadabraParser
from gitlabracadabra.tests import patch_open
from gitlabracadabra.tests.case import TestCase


class TestParser(TestCase):
    def test_from_yaml_file(self):
        contents_map = {
            "gitlabracadabra.yml": """
                message:
                  hello: world
                """,
        }
        with patch_open(contents_map):
            p = GitlabracadabraParser.from_yaml_file("gitlabracadabra.yml")
            assert dict(p._items()) == {"message": {"hello": "world"}}

    def test_include_str(self):
        contents_map = {
            "gitlabracadabra.yml": """
                include:
                  - included.yml
                """,
            "included.yml": """
                message:
                  hello: world
                """,
        }
        with patch_open(contents_map):
            p = GitlabracadabraParser.from_yaml_file("gitlabracadabra.yml")
            assert dict(p._items()) == {"message": {"hello": "world"}}

    def test_include_local(self):
        contents_map = {
            "gitlabracadabra.yml": """
                include:
                  - local: included.yml
                """,
            "included.yml": """
                message:
                  hello: world
                """,
        }
        with patch_open(contents_map):
            p = GitlabracadabraParser.from_yaml_file("gitlabracadabra.yml")
            assert dict(p._items()) == {"message": {"hello": "world"}}

    def test_include_recursion(self):
        contents_map = {
            "gitlabracadabra.yml": """
                include:
                  - included.yml
                """,
            "included.yml": """
                include:
                  - gitlabracadabra.yml
                """,
        }
        with patch_open(contents_map), pytest.raises(ValueError) as cm:
            GitlabracadabraParser.from_yaml_file("gitlabracadabra.yml")

        assert str(cm.value) == "gitlabracadabra.yml: nesting too deep in `include`"

    def test_include_forbidden_relative_path(self):
        contents_map = {
            "gitlabracadabra.yml": """
                include:
                  - ../included.yml
                """,
        }
        with patch_open(contents_map), pytest.raises(ValueError) as cm:
            GitlabracadabraParser.from_yaml_file("gitlabracadabra.yml")

        assert str(cm.value) == "gitlabracadabra.yml: forbidden path for `include`: ../included.yml"

    def test_include_forbidden_absolute_path(self):
        contents_map = {
            "gitlabracadabra.yml": """
                include:
                  - /included.yml
                """,
        }
        with patch_open(contents_map), pytest.raises(ValueError) as cm:
            GitlabracadabraParser.from_yaml_file("gitlabracadabra.yml")

        assert str(cm.value) == "gitlabracadabra.yml: forbidden path for `include`: /included.yml"

    def test_extend(self):
        p = GitlabracadabraParser.from_yaml(
            "-",
            """
            .hidden-key:
              param1: value1
              param2: value2
            shown-key:
              extends: .hidden-key
              param3: value3
            another-key:
              param4: value4
            """,
        )
        d = dict(p._items())

        assert ".hidden-key" not in d
        assert "shown-key" in d
        assert "another-key" in d
        assert d["another-key"] == {"param4": "value4"}

    def test_extend_not_found(self):
        p = GitlabracadabraParser.from_yaml(
            "-",
            """
            key2:
              extends:
                - key1
            """,
        )
        with pytest.raises(ValueError) as cm:
            dict(p._items())

        assert str(cm.value) == "- (`key1` from `key2`): key1 not found"

    def test_extend_recursion(self):
        p = GitlabracadabraParser.from_yaml(
            "-",
            """
            key1:
              extends: key3
              foo: bar
            key2:
              extends: key1
              foo2: bar2
            key3:
              extends: key2
              foo3: bar3
            """,
        )
        with pytest.raises(ValueError) as cm:
            dict(p._items())

        assert str(cm.value) == "- (key1): nesting too deep in `extends`"

    def test_extend_unknown_merge_strategy(self):
        p = GitlabracadabraParser.from_yaml(
            "-",
            """
            key1:
              hello: world
            key2:
              extends:
                - key1: keep-the-best
            """,
        )
        with pytest.raises(ValueError) as cm:
            dict(p._items())

        assert str(cm.value) == "- (`key1` from `key2`): Unknown merge strategy `keep-the-best`"

    def test_include_and_extend(self):
        contents_map = {
            "gitlabracadabra.yml": """
                group1/project1:
                  name: foo
                  extends: .e1
                  members:
                   baz: owner

                .e1:
                  branches:
                    - main
                    - develop
                  members:
                    bar: maintainer

                include:
                  - local: included.yml
                """,
            "included.yml": """
                .e1:
                  branches:
                    - main
                    - prod
                    - staging
                  members:
                    foo: developer
                """,
        }
        with patch_open(contents_map):
            p = GitlabracadabraParser.from_yaml_file("gitlabracadabra.yml")
            d = dict(p._items())

        assert ".e1" not in d
        assert "include" not in d
        assert d["group1/project1"] == {
            "name": "foo",
            "members": {"foo": "developer", "bar": "maintainer", "baz": "owner"},
            "branches": ["main", "develop"],
        }

    def test_extend_list(self):
        contents_map = {
            "gitlabracadabra.yml": """
                group1/project1:
                  name: foo
                  extends:
                    - .e1
                    - .e2: replace
                    - .e3
                  members:
                   foo: owner

                .e1:
                  branches:
                    - main1
                    - develop1
                  members:
                    bar: maintainer

                .e2:
                  branches:
                    - main2
                    - develop2
                  members:
                    baz: developer

                .e3:
                  branches:
                    - main3
                    - develop3
                  members:
                    bar: developer # override .e1 maintainer
                """,
        }
        with patch_open(contents_map):
            p = GitlabracadabraParser.from_yaml_file("gitlabracadabra.yml")
            d = dict(p._items())

        assert ".e1" not in d
        assert "include" not in d
        assert d["group1/project1"] == {
            "name": "foo",
            "members": {"foo": "owner", "bar": "developer"},
            "branches": ["main3", "develop3"],
        }

    def test_extend_list_aggregate(self):
        contents_map = {
            "gitlabracadabra.yml": """
                group1/project1:
                  name: foo
                  extends:
                    - .e1
                    - .e2: aggregate
                    - .e3
                  members:
                   foo: owner

                .e1:
                  branches:
                    - main1
                    - develop1
                  members:
                    bar: maintainer

                .e2:
                  branches:
                    - main2
                    - develop2
                  members:
                    baz: developer

                .e3:
                  branches:
                    - main3
                    - develop3
                  members:
                    bar: developer # override .e1 maintainer
                """,
        }
        with patch_open(contents_map):
            p = GitlabracadabraParser.from_yaml_file("gitlabracadabra.yml")
            d = dict(p._items())

        assert ".e1" not in d
        assert "include" not in d
        assert d["group1/project1"] == {
            "name": "foo",
            "members": {"foo": "owner", "bar": "developer", "baz": "developer"},
            "branches": ["main2", "develop2", "main3", "develop3"],
        }

    def test_objects(self):
        p = GitlabracadabraParser.from_yaml(
            "-",
            """
            .project-template:
              wiki_enabled: true
              issues_enabled: true
            group1/:
              description: My group
            group1/project1:
              extends: .project-template
              wiki_enabled: false
              description: My project
              buggy_param: Oh no!
            """,
        )
        d = p.objects()

        assert ".project-template" not in d

        assert "group1" in d
        group1 = d["group1"]
        assert isinstance(group1, GitLabracadabraGroup)
        assert group1._errors == []
        assert group1._content == {"description": "My group"}

        assert "group1/project1" in d
        project1 = d["group1/project1"]
        assert isinstance(project1, GitLabracadabraProject)
        assert len(project1._errors) == 1
        assert project1._errors[0].message == "Additional properties are not allowed " "('buggy_param' was unexpected)"
        assert project1._content == {
            "buggy_param": "Oh no!",
            "description": "My project",
            "issues_enabled": True,
            "wiki_enabled": False,
        }

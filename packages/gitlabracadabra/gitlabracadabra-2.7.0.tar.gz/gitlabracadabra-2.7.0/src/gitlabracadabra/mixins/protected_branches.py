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

from __future__ import annotations

import logging
from json import dumps as json_dumps
from time import sleep
from types import MethodType

from gitlab.exceptions import GitlabCreateError, GitlabParsingError, GitlabUpdateError
from gitlab.mixins import CRUDMixin, NoUpdateMixin, SaveMixin
from gitlab.v4.objects import ProjectProtectedBranch, ProjectProtectedBranchManager

from gitlabracadabra.gitlab.access_levels import access_level_value
from gitlabracadabra.objects.object import GitLabracadabraObject

ALLOWED_TO_PREFIX = "allowed_to_"
ALLOWED_TO_MERGE = "allowed_to_merge"
ALLOWED_TO_PUSH = "allowed_to_push"
ACCESS_LEVELS_SUFFIX = "_access_levels"
ACCESS_LEVEL = "access_level"
USER_ID = "user_id"
GROUP_ID = "group_id"
DEPLOY_KEY_ID = "deploy_key_id"

logger = logging.getLogger(__name__)


# Before https://github.com/python-gitlab/python-gitlab/commit/a867c48 (v4.5.0)
if SaveMixin not in ProjectProtectedBranch.__bases__:
    ProjectProtectedBranch.__bases__ = (SaveMixin, *ProjectProtectedBranch.__bases__)
if NoUpdateMixin in ProjectProtectedBranchManager.__bases__:
    ProjectProtectedBranchManager.__bases__ = tuple(
        [CRUDMixin if base == NoUpdateMixin else base for base in ProjectProtectedBranchManager.__bases__]
    )

    # https://github.com/python-gitlab/python-gitlab/commit/f711d9e (v3.14)
    def _http_patch(self, path, *, query_data=None, post_data=None, **kwargs):
        query_data = query_data or {}
        post_data = post_data or {}

        response = self.http_request(
            "patch",
            path,
            query_data=query_data,
            post_data=post_data,
            **kwargs,
        )
        try:
            return response.json()
        except Exception as err:
            raise GitlabParsingError(
                error_message="Failed to parse the server message",
            ) from err

    # https://github.com/python-gitlab/python-gitlab/commit/7073a2d (v4.0)
    def _get_update_method(self):
        return MethodType(_http_patch, self.gitlab)

    ProjectProtectedBranchManager._get_update_method = _get_update_method  # type: ignore # noqa: SLF001


class ProtectedBranchesMixin(GitLabracadabraObject):
    """Object with protected branches."""

    def _process_protected_branches(self, param_name, param_value, *, dry_run=False, skip_save=False):
        """Process the protected_branches param.

        Args:
            param_name: "protected_branches".
            param_value: target protected branches.
            dry_run: Dry run.
            skip_save: False.
        """
        assert param_name == "protected_branches"  # noqa: S101
        assert not skip_save  # noqa: S101
        current_protected_branches = self._get_current_protected_branches()
        self._create_or_update_protected_branches(param_value, dry_run, current_protected_branches)
        self._remove_unknown_protected_branches(param_value, dry_run, current_protected_branches)

    def _get_current_protected_branches(self):
        current_protected_branches = dict(
            [
                [protected_branch.name, protected_branch]
                for protected_branch in self._obj.protectedbranches.list(all=True)
            ]
        )
        if not self._just_created:
            return current_protected_branches
        for _ in range(10):
            if current_protected_branches:
                break
            logger.debug("[%s] Waiting one second before retrieving protected branches again", self._name)
            sleep(1)
            current_protected_branches = dict(
                [
                    [protected_branch.name, protected_branch]
                    for protected_branch in self._obj.protectedbranches.list(all=True)
                ]
            )
        return current_protected_branches

    def _create_or_update_protected_branches(self, param_value, dry_run, current_protected_branches):
        for protected_name, target_config_str in sorted(param_value.items()):
            if protected_name in current_protected_branches:
                self._update_protected_branch(protected_name, target_config_str, dry_run, current_protected_branches)
            else:
                self._create_protected_branch(protected_name, target_config_str, dry_run, current_protected_branches)

    def _update_protected_branch(self, protected_name, target_config_str, dry_run, current_protected_branches):
        target_config = self._target_protected_branch_config(protected_name, target_config_str)
        current_config = self._current_protected_branch_config(current_protected_branches, protected_name)
        for current_k, current_v in current_config.items():
            if current_k not in target_config:
                target_config[current_k] = current_v
        if current_config == target_config:
            return
        # CE compatibility
        can_use_allowed_to = "code_owner_approval_required" in current_config
        if not can_use_allowed_to:
            self._create_protected_branch(protected_name, target_config_str, dry_run, current_protected_branches)
            return
        if dry_run:
            logger.info(
                "[%s] NOT Changing protected branch %s: %s -> %s (dry-run)",
                self._name,
                protected_name,
                json_dumps(current_config, sort_keys=True),
                json_dumps(target_config, sort_keys=True),
            )
            return
        logger.info(
            "[%s] Changing protected branch %s: %s -> %s",
            self._name,
            protected_name,
            json_dumps(current_config, sort_keys=True),
            json_dumps(target_config, sort_keys=True),
        )
        protected_branch = current_protected_branches.get(protected_name)
        for target_config_key, target_config_value in target_config.items():
            current_config_value = current_config.get(target_config_key)
            if target_config_value == current_config_value:
                continue
            if target_config_key.startswith(ALLOWED_TO_PREFIX):
                self._update_protected_branch_access_levels(
                    protected_branch,
                    current_config_value,
                    target_config_key,
                    target_config_value,
                )
            else:
                setattr(protected_branch, target_config_key, target_config_value)
        try:
            protected_branch.save()
        except GitlabUpdateError as err:
            logger.warning(
                "[%s] Unable to change protected branch %s: %s",
                self._name,
                protected_name,
                err.error_message,
            )

    def _update_protected_branch_access_levels(
        self,
        protected_branch,
        current_config_value,
        target_config_key,
        target_config_value,
    ):
        changes = []
        for target_config_value_item in target_config_value:
            if target_config_value_item in current_config_value:
                continue
            changes.append(target_config_value_item)
        for current_config_value_item in getattr(protected_branch, self._received_attribute_name(target_config_key)):
            current_access_level = self._current_access_level(current_config_value_item)
            if current_access_level in target_config_value:
                target_config_value.remove(current_access_level)
                continue
            changes.append({"id": current_config_value_item.get("id"), "_destroy": True})
        setattr(protected_branch, target_config_key, changes)

    def _received_attribute_name(self, attribute_name):
        if attribute_name.startswith(ALLOWED_TO_PREFIX):
            return attribute_name.removeprefix(ALLOWED_TO_PREFIX) + ACCESS_LEVELS_SUFFIX
        return attribute_name

    def _create_protected_branch(self, protected_name, target_config_str, dry_run, current_protected_branches):
        target_config = self._target_protected_branch_config(protected_name, target_config_str)
        # CE compatibility
        target_allowed_to_push = target_config.get(ALLOWED_TO_PUSH)
        if len(target_allowed_to_push or []) == 1:
            target_config["push_access_level"] = target_allowed_to_push[0][ACCESS_LEVEL]
        target_allowed_to_merge = target_config.get(ALLOWED_TO_MERGE)
        if len(target_allowed_to_merge or []) == 1:
            target_config["merge_access_level"] = target_allowed_to_merge[0][ACCESS_LEVEL]
        if dry_run:
            logger.info(
                "[%s] NOT Creating protected branch %s: %s (dry-run)",
                self._name,
                protected_name,
                json_dumps(target_config, sort_keys=True),
            )
            return
        logger.info(
            "[%s] Creating protected branch %s: %s",
            self._name,
            protected_name,
            json_dumps(target_config, sort_keys=True),
        )
        try:
            if protected_name in current_protected_branches:
                # GitLab CE can't update push/merge access level
                self._obj.protectedbranches.delete(protected_name)
            self._obj.protectedbranches.create(target_config)
        except GitlabCreateError as err:
            logger.warning(
                "[%s] Unable to create protected branch %s: %s",
                self._name,
                protected_name,
                err.error_message,
            )

    def _target_protected_branch_config(self, protected_name, target_config_str):
        target_config_int = {
            "name": protected_name,
        }
        for target_config_key, target_config_value in target_config_str.items():
            if target_config_key.endswith("_access_level"):
                target_config_int[target_config_key] = access_level_value(target_config_value)
            elif target_config_key.startswith(ALLOWED_TO_PREFIX):
                target_config_int[target_config_key] = self._target_access_levels(target_config_value)
            else:
                target_config_int[target_config_key] = target_config_value
        if "merge_access_level" in target_config_int:
            if ALLOWED_TO_MERGE not in target_config_int:
                target_config_int[ALLOWED_TO_MERGE] = []
            target_config_int[ALLOWED_TO_MERGE].append(
                {
                    ACCESS_LEVEL: target_config_int.pop("merge_access_level"),
                }
            )
        if "push_access_level" in target_config_int:
            if ALLOWED_TO_PUSH not in target_config_int:
                target_config_int[ALLOWED_TO_PUSH] = []
            target_config_int[ALLOWED_TO_PUSH].append(
                {
                    ACCESS_LEVEL: target_config_int.pop("push_access_level"),
                }
            )
        return target_config_int

    def _target_access_levels(self, access_levels_str):
        target_access_levels = []
        for access_level_str in access_levels_str:
            if "role" in access_level_str:
                target_access_levels.append(
                    {
                        ACCESS_LEVEL: access_level_value(access_level_str.get("role")),
                    }
                )
            elif "user" in access_level_str:
                target_access_levels.append(
                    {
                        USER_ID: self.connection.user_cache.id_from_username(access_level_str.get("user")),
                    }
                )
            elif "group" in access_level_str:
                target_access_levels.append(
                    {
                        GROUP_ID: self.connection.group_cache.id_from_full_path(access_level_str.get("group")),
                    }
                )
            elif "deploy_key" in access_level_str:
                target_access_levels.append(
                    {
                        DEPLOY_KEY_ID: self.connection.deploy_key_cache.id_from_title(
                            self._obj.id,
                            access_level_str.get("deploy_key"),
                        ),
                    }
                )
        return sorted(
            target_access_levels,
            key=lambda access_level: json_dumps(access_level, sort_keys=True),
        )

    def _current_protected_branch_config(self, current_protected_branches, protected_name):
        if protected_name in current_protected_branches:
            current_protected_branch = current_protected_branches.get(protected_name)
            current_config = {}
            for param_k, param_v in current_protected_branch.attributes.items():
                if param_k in {"push_access_levels", "merge_access_levels", "unprotect_access_levels"}:
                    current_config[self._sent_attribute_name(param_k)] = self._current_access_levels(param_v)
                elif param_k in {"name", "allow_force_push", "code_owner_approval_required"}:
                    current_config[param_k] = param_v
            return current_config
        return {}

    def _current_access_levels(self, access_levels):
        return sorted(
            [self._current_access_level(access_level) for access_level in access_levels],
            key=lambda access_level: json_dumps(access_level, sort_keys=True),
        )

    def _current_access_level(self, access_level):
        if access_level.get(USER_ID):
            return {USER_ID: access_level.get(USER_ID)}
        if access_level.get(GROUP_ID):
            return {GROUP_ID: access_level.get(GROUP_ID)}
        if access_level.get(DEPLOY_KEY_ID):
            return {DEPLOY_KEY_ID: access_level.get(DEPLOY_KEY_ID)}
        return {ACCESS_LEVEL: access_level.get(ACCESS_LEVEL)}

    def _sent_attribute_name(self, attribute_name):
        if attribute_name.endswith(ACCESS_LEVELS_SUFFIX):
            return ALLOWED_TO_PREFIX + attribute_name.removesuffix(ACCESS_LEVELS_SUFFIX)
        return attribute_name

    def _remove_unknown_protected_branches(self, param_value, dry_run, current_protected_branches):
        # Remaining protected branches
        unknown_protected_branches = self._content.get("unknown_protected_branches", "warn")
        if unknown_protected_branches in {"ignore", "skip"}:
            return
        for current_protected_name in current_protected_branches:
            if current_protected_name in param_value:
                continue
            if unknown_protected_branches in {"delete", "remove"} and dry_run:
                logger.info(
                    "[%s] NOT Deleting unknown protected branch: %s (dry-run)",
                    self._name,
                    current_protected_name,
                )
            elif unknown_protected_branches in {"delete", "remove"}:
                logger.info(
                    "[%s] Deleting unknown protected branch: %s",
                    self._name,
                    current_protected_name,
                )
                self._obj.protectedbranches.delete(current_protected_name)
            else:
                logger.warning(
                    "[%s] NOT Deleting unknown protected branch: %s (unknown_protected_branches=%s)",
                    self._name,
                    current_protected_name,
                    unknown_protected_branches,
                )

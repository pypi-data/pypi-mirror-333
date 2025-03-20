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

from gitlabracadabra.containers.blob import Blob
from gitlabracadabra.containers.const import (
    DOCKER_MANIFEST_SCHEMA1,
    DOCKER_MANIFEST_SCHEMA1_SIGNED,
    DOCKER_MANIFEST_SCHEMA2,
    DOCKER_MANIFEST_SCHEMA2_LIST,
    OCI_IMAGE_INDEX,
    OCI_IMAGE_MANIFEST,
)
from gitlabracadabra.containers.manifest_base import ManifestBase


class Manifest(ManifestBase):
    """Retrieve Manifest or Manifest list."""

    def manifests(self) -> list[Manifest]:
        """Get manifests of the manifest list.

        Returns:
            A list of manifests.

        Raises:
            ValueError: Unsupported manifest list type.
        """
        if self.mime_type in {DOCKER_MANIFEST_SCHEMA2_LIST, OCI_IMAGE_INDEX}:
            return self._manifests_v2()
        msg = f"Unsupported manifest list type {self.mime_type}"
        raise ValueError(msg)

    def tag_list(self) -> list[str]:
        """Get tags of the manifest.

        Returns:
            A list of tags (strings).

        Raises:
            ValueError: Expected list got something else.
        """
        response = self._registry.request(
            "get",
            f"/v2/{self.manifest_name}/tags/list",
            scopes={self.scope()},
        )
        tags = response.json().get("tags")
        if not isinstance(tags, list):
            msg = f"Expected list got {type(tags)}"
            raise TypeError(msg)
        return tags

    def blobs(self) -> list[Blob]:
        """Get blobs of the manifest.

        Returns:
            A list of blobs.

        Raises:
            ValueError: Unsupported media type.
        """
        if self.mime_type in {DOCKER_MANIFEST_SCHEMA2, OCI_IMAGE_MANIFEST}:
            return [
                Blob(
                    self.registry,
                    self.manifest_name,
                    layer_json["digest"],
                    size=layer_json["size"],
                    mime_type=layer_json["mediaType"],
                )
                for layer_json in self.json.get("layers")
            ]
        if self.mime_type in {DOCKER_MANIFEST_SCHEMA1, DOCKER_MANIFEST_SCHEMA1_SIGNED}:
            return [
                Blob(
                    self.registry,
                    self.manifest_name,
                    fs_layer_json["blobSum"],
                    mime_type="application/octet-stream",
                )
                for fs_layer_json in self.json.get("fsLayers")
            ]
        msg = f"Unsupported media type: {self.mime_type}"
        raise ValueError(msg)

    def _manifests_v2(self) -> list[Manifest]:
        json = dict(self.json)
        if json["mediaType"] not in {DOCKER_MANIFEST_SCHEMA2_LIST, OCI_IMAGE_INDEX}:
            msg = "Unexpected manifest list type {}".format(json["mediaType"])
            raise ValueError(msg)
        if json["schemaVersion"] != 2:  # noqa: PLR2004
            msg = "Unexpected manifest schema version {}".format(json["schemaVersion"])
            raise ValueError(msg)
        manifests = []
        for manifest_json in json["manifests"]:
            manifest = Manifest(
                self.registry,
                self.manifest_name,
                digest=manifest_json["digest"],
                size=manifest_json["size"],
                mime_type=manifest_json["mediaType"],
                tag=self.tag,
            )
            manifest.platform = manifest_json["platform"]
            manifests.append(manifest)
        return manifests

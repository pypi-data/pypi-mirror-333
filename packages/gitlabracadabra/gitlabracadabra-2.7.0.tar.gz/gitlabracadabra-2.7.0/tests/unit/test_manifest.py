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
from requests import HTTPError, codes

from gitlabracadabra.containers.const import DOCKER_MANIFEST_SCHEMA1_SIGNED, DOCKER_MANIFEST_SCHEMA2
from gitlabracadabra.containers.manifest import Manifest
from gitlabracadabra.containers.registry import Registry
from gitlabracadabra.tests import my_vcr
from gitlabracadabra.tests.case import TestCase


class TestManifest(TestCase):
    """Test Manifest class."""

    @my_vcr.use_cassette
    def test_tag_list(self, cass):
        """Test tag_list method.

        Args:
            cass: VCR cassette.
        """
        registry = Registry("docker.io")
        manifest = Manifest(registry, "library/debian")
        assert isinstance(manifest, Manifest)
        tag_list = manifest.tag_list()
        assert isinstance(tag_list, list)
        assert "buster" in tag_list
        assert cass.all_played

    @my_vcr.use_cassette
    def test_not_found(self, cass):
        """Test proper 404 handling.

        Args:
            cass: VCR cassette.
        """
        registry = Registry("docker.io")
        for attr in "digest", "size", "mime_type":
            with self.subTest(attr=attr):
                manifest = Manifest(registry, "library/debian", tag="not_found")
                with pytest.raises(HTTPError) as cm:
                    getattr(manifest, attr)
                assert cm.value.response.status_code == codes["not_found"]
        assert not Manifest(registry, "library/debian", tag="not_found").exists()
        assert cass.all_played

    @my_vcr.use_cassette
    def test_blobs(self, cass):
        """Test blobs method.

        Args:
            cass: VCR cassette.
        """
        registry = Registry("registry.developers.crunchydata.com")
        manifest = Manifest(registry, "crunchydata/pgo-apiserver", None, tag="centos8-4.6.2")
        assert manifest.mime_type == DOCKER_MANIFEST_SCHEMA2
        blobs = manifest.blobs()
        assert len(blobs) == 17
        blob0 = blobs[0]
        assert blob0.manifest_name == manifest.manifest_name
        assert blob0.mime_type == "application/vnd.docker.image.rootfs.diff.tar.gzip"
        assert blob0.size == 75181999
        assert blob0.digest == "sha256:7a0437f04f83f084b7ed68ad9c4a4947e12fc4e1b006b38129bac89114ec3621"
        assert cass.all_played

    @my_vcr.use_cassette
    def test_blobs_manifest_v1(self, cass):
        """Test blobs method with a manifest v1.

        Args:
            cass: VCR cassette.
        """
        registry = Registry("quay.io")
        manifest = Manifest(registry, "jetstack/cert-manager-controller", None, tag="v0.1.0")
        assert manifest.mime_type == DOCKER_MANIFEST_SCHEMA1_SIGNED
        blobs = manifest.blobs()
        assert len(blobs) == 7
        assert blobs[0].manifest_name == manifest.manifest_name
        assert blobs[0].mime_type == "application/octet-stream"
        assert cass.play_count == 3
        assert blobs[0].size == 32
        assert cass.play_count == 4
        assert blobs[0].digest == "sha256:a3ed95caeb02ffe68cdd9fd84406680ae93d633cb16422d00e8a7c22955b46d4"
        assert cass.all_played

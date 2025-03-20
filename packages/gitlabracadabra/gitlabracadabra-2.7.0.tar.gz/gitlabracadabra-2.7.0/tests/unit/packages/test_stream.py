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

from random import randint
from unittest.mock import MagicMock, call

from requests import Response
from requests.sessions import Session

from gitlabracadabra.packages.destination import Stream
from gitlabracadabra.tests.case import TestCase
from gitlabracadabra.tests.vcrfuncs import my_vcr


class TestStream(TestCase):
    """Test Stream class."""

    def test_bool(self):
        """Test __bool__ method."""
        response = MagicMock()
        stream = Stream(response)
        assert (stream or False) == stream
        assert response.mock_calls == []

    def test_len_without_content_length(self):
        """Test __len__ method, when there is no Content-Length."""
        response = Response()
        stream = Stream(response)

        assert len(stream) == 0

    def test_len_with_content_length(self):
        """Test __len__ method, when there is a Content-Length header."""
        size = randint(1, 10000)
        response = Response()
        response.headers["Content-Length"] = size
        stream = Stream(response)

        assert len(stream) == size

    def test_iter(self):
        """Test __iter__ method."""
        chunksize = randint(1, 10000)
        response = Response()
        response.raw = MagicMock()
        response.raw.stream.return_value = ["a" * chunksize].__iter__()
        stream = Stream(response, chunksize)

        assert [chunk for chunk in stream] == ["a" * chunksize]  # noqa: C416
        assert response.raw.mock_calls == [call.stream(chunksize)]

    def test_read(self):
        """Test read method."""
        size = randint(1, 10000)
        response = Response()
        response.raw = MagicMock()
        response.raw.read.return_value = "a" * size
        stream = Stream(response)

        assert stream.read(size) == "a" * size
        assert response.raw.mock_calls == [call.read(size)]

    @my_vcr.use_cassette
    def test_e2e(self, cass):
        """Test Stream class.

        Args:
            cass: VCR cassette.
        """
        source_url = "http://httpbin.org/stream-bytes/200"
        destination_url = "http://httpbin.org/put"

        session = Session()
        download_response = session.request(
            "GET",
            source_url,
            stream=True,
        )

        upload_response = session.request(
            "PUT",
            destination_url,
            data=Stream(download_response),
        )
        assert upload_response.status_code == 200
        assert cass.all_played

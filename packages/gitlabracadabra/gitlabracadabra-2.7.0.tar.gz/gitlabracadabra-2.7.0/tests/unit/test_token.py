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

from unittest.mock import patch

from gitlabracadabra.containers.authenticated_session import Token
from gitlabracadabra.tests.case import TestCase


class TestToken(TestCase):
    """Test Token class."""

    def test_simple(self) -> None:
        """Test simple token."""
        current_time = 42.42
        one_hour = 3600
        with patch("gitlabracadabra.containers.authenticated_session.time") as mocked_time:
            mocked_time.return_value = current_time
            token = Token("abc", one_hour)
            assert token.token == "abc"
            assert token.expiration_time == current_time + one_hour
            assert not token.is_expired()

            mocked_time.return_value = current_time + one_hour - 1
            assert not token.is_expired()

            mocked_time.return_value = current_time + one_hour
            assert token.is_expired()

    def test_short_lifetime(self) -> None:
        """Test token with too short expires_in."""
        current_time = 42.42
        one_minute = 60
        with patch("gitlabracadabra.containers.authenticated_session.time") as mocked_time:
            mocked_time.return_value = current_time
            token = Token("def", 1)
            assert token.token == "def"
            assert token.expiration_time == current_time + one_minute
            assert not token.is_expired()

            mocked_time.return_value = current_time + one_minute - 1
            assert not token.is_expired()

            mocked_time.return_value = current_time + one_minute
            assert token.is_expired()

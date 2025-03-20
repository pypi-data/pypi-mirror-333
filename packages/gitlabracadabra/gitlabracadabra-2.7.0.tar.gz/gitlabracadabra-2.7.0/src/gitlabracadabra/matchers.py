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

from logging import getLogger
from re import IGNORECASE, Pattern
from re import compile as re_compile
from re import error as re_error
from typing import TYPE_CHECKING

try:
    from semantic_version import NpmSpec
except ImportError:
    # semantic_version < 2.7
    from semantic_version import Spec as NpmSpec
from semantic_version import Version

if TYPE_CHECKING:
    from collections.abc import Callable
    from re import Match

    InputData = list[str] | Callable[[], list[str]]
    Patterns = list[str | Pattern[str]]


logger = getLogger(__name__)


class Matcher:
    """Matcher."""

    def __init__(
        self,
        patterns: str | list[str],
        semver: str | None,
        limit: int | None = None,
        *,
        log_prefix: str = "",
    ) -> None:
        """Initialize a matcher.

        Args:
            patterns: A pattern or list of patterns.
            semver: Semantic versioning.
            limit: Keep at most n latest versions.
            log_prefix: Log prefix.
        """
        self._log_prefix = log_prefix
        if not isinstance(patterns, list):
            patterns = [patterns]
        self._patterns: Patterns = []
        for pattern in patterns:
            parsed = self._parse_pattern(pattern)
            if parsed is not None:
                self._patterns.append(parsed)
        self._semver = None
        if semver:
            self._semver = NpmSpec(semver)
        self._limit = limit

    def match(
        self,
        input_data: InputData,
    ) -> list[Match]:
        """Filer.

        Args:
            input_data: Either a list of string or an input function, called only when needed (and at most once).

        Returns:
            List of matches.
        """
        has_regex = any(isinstance(pattern, Pattern) for pattern in self._patterns)
        if not isinstance(input_data, list) and has_regex:
            input_data = input_data()
        if isinstance(input_data, list):
            return self._limiter(self._match_list(input_data))
        return self._limiter(self._match_all())

    def _match_list(self, input_data: list[str]) -> list[Match[str]]:
        matched_items: list[Match[str]] = []
        for current_item in input_data:
            match = self._match_item(current_item)
            if match:
                matched_items.append(match)
        return matched_items

    def _match_item(self, current_item: str) -> Match[str] | None:
        if current_item in self._patterns:
            return re_compile("^.*$").match(current_item)
        for pattern in self._patterns:
            if isinstance(pattern, Pattern):
                match = pattern.match(current_item)
                if match and self._match_semver(current_item):
                    return match
        return None

    def _match_semver(self, current_item: str) -> bool:
        if not self._semver:
            return True
        return self._safe_version(current_item) in self._semver

    def _match_all(self) -> list[Match[str]]:
        matched_items: list[Match[str]] = []
        for pattern in self._patterns:
            if not isinstance(pattern, Pattern):
                match = re_compile("^.*$").match(pattern)
                if match:
                    matched_items.append(match)
        return matched_items

    def _parse_pattern(self, pattern: str) -> None | str | Pattern[str]:
        """Parse a pattern.

        Args:
            pattern: The pattern as string.

        Returns:
            A string for exact match or a pattern.
        """
        if pattern.startswith("/"):
            flags_str = pattern.rsplit("/", 1).pop()
            flags = 0
            for flag in flags_str:
                if flag == "i":
                    flags |= IGNORECASE
                else:
                    logger.warning(
                        "%sInvalid regular expression flag %s in %s. Flag ignored.",
                        self._log_prefix,
                        flag,
                        pattern,
                    )
            try:
                return re_compile(
                    "^{}$".format(pattern[1 : pattern.rindex("/")]),
                    flags,
                )
            except re_error as err:
                logger.warning(
                    "%sInvalid regular expression %s: %s. Skipping pattern.",
                    self._log_prefix,
                    pattern,
                    str(err),
                )
                return None
        return pattern

    def _limiter(self, matches: list[Match[str]]) -> list[Match[str]]:
        if self._limit is None:
            return matches
        indexed_matches = {self._safe_version(match[0]): match for match in matches}
        sorted_matches = [match for (_, match) in sorted(indexed_matches.items(), reverse=True)]
        return sorted_matches[: self._limit]

    def _safe_version(self, version_str: str) -> Version | None:
        if version_str.startswith("v"):
            version_str = version_str[1:]
        try:
            return Version.coerce(version_str)
        except ValueError as err:
            logger.warning(
                "%s%s for %s",
                self._log_prefix,
                str(err),
                str(version_str),
            )
        return Version("0.0.0-0")

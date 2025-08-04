import re
from functools import total_ordering
from typing import Tuple

PATCH_REGEX = re.compile(r"(\d+)([a-zA-Z][\w\-\.]*)?")


@total_ordering
class Version:

    def __init__(self, version):
        parts = version.split("-", 1)
        core_version = parts[0]
        self.prerelease = parts[1] if len(parts) > 1 else ""
        self.major, self.minor, self.patch = self._process_version(
            core_version
        )
        self.prerelease_parts = (
            self.prerelease.split(".") if self.prerelease else []
        )

    def __lt__(self, other: "Version") -> bool:
        if (self.major, self.minor, self.patch) != (
            other.major,
            other.minor,
            other.patch,
        ):
            return (self.major, self.minor, self.patch) < (
                other.major,
                other.minor,
                other.patch,
            )
        return self._compare_prereleases(other)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Version):
            return NotImplemented
        return (
            self.major,
            self.minor,
            self.patch,
            self.prerelease_parts,
        ) == (
            other.major,
            other.minor,
            other.patch,
            other.prerelease_parts,
        )

    def _process_version(self, version: str) -> Tuple[int, int, int]:
        core = version.split(".")
        if len(core) != 3:
            raise ValueError("Version must have major.minor.patch format")

        try:
            major = int(core[0])
            minor = int(core[1])
        except ValueError:
            raise ValueError("Major and minor must be integers")

        match = PATCH_REGEX.match(core[2])
        if not match:
            raise ValueError("Invalid patch segment")

        patch = int(match.group(1))
        return major, minor, patch

    def _compare_prereleases(self, other: "Version") -> bool:
        if not self.prerelease and not other.prerelease:
            return False
        if not self.prerelease:
            return False
        if not other.prerelease:
            return True

        for self_part, other_part in zip(
            self.prerelease_parts, other.prerelease_parts
        ):
            s_is_num = self_part.isdigit()
            o_is_num = other_part.isdigit()
            if s_is_num and not o_is_num:
                return True
            if not s_is_num and o_is_num:
                return False
            if s_is_num and o_is_num:
                if int(self_part) != int(other_part):
                    return int(self_part) < int(other_part)
            else:
                if self_part != other_part:
                    return self_part < other_part
        return len(self.prerelease_parts) < len(other.prerelease_parts)

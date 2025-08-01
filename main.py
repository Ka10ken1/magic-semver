import re


class Version:

    def __init__(self, version):
        parts = version.split("-", 1)

        core_version = parts[0]

        self.prerelease = parts[1] if len(parts) > 1 else ""

        self.major, self.minor, self.patch = self._process_version(core_version)

        self.prerelease_parts = self.prerelease.split(".") if self.prerelease else []

    def __lt__(self, other) -> bool:
        if (self.major, self.minor, self.patch) != (other.major,other.minor,other.patch):
            return (self.major, self.minor, self.patch) < (other.major,other.minor,other.patch)

        return self._compare_prereleases(other)

    def __gt__(self, other) -> bool:
        return other < self

    def __eq__(self, other) -> bool:
        return (self.major, self.minor, self.patch, self.prerelease_parts) == (
            other.major,
            other.minor,
            other.patch,
            other.prerelease_parts,
        )

    def __ne__(self, other) -> bool:
        return not self == other

    def _process_version(self, version: str) -> tuple[int, int, int]:
        core = version.split(".")
        if len(core) != 3:
            raise ValueError("Version must have major.minor.patch format")

        try:
            major = int(core[0])
            minor = int(core[1])
        except ValueError:
            raise ValueError("Major and minor must be integers")

        # start with one or more digits
        # optionally some string like (1b)
        # optinally something like alpha-beta
        m = re.match(r"(\d+)([a-zA-Z][\w\-\.]*)?", core[2])
        if not m:
            raise ValueError("Invalid patch segment")

        patch = int(m.group(1))
        return major, minor, patch
     
    def _compare_prereleases(self, other) -> bool:
        if not self.prerelease and not other.prerelease:
            return False
        if not self.prerelease:
            return False
        if not other.prerelease:
            return True

        for s, o in zip(self.prerelease_parts, other.prerelease_parts):
            s_is_num = s.isdigit()
            o_is_num = o.isdigit()
            if s_is_num and not o_is_num:
                return True
            if not s_is_num and o_is_num:
                return False
            if s_is_num and o_is_num:
                if int(s) != int(o):
                    return int(s) < int(o)
            else:
                if s != o:
                    return s < o
        return len(self.prerelease_parts) < len(other.prerelease_parts)


def main():
    to_test = [
        ("1.0.0", "2.0.0"),
        ("1.0.0", "1.42.0"),
        ("1.2.0", "1.2.42"),
        ("1.1.0-alpha", "1.2.0-alpha.1"),
        ("1.0.1b", "1.0.10-alpha.beta"),
        ("1.0.0-rc.1", "1.0.0"),
    ]

    for left, right in to_test:
        assert Version(left) < Version(right), "le failed"
        assert Version(right) > Version(left), "ge failed"
        assert Version(right) != Version(left), "neq failed"


if __name__ == "__main__":
    main()

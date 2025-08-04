import unittest
from magic_semvar.version import Version


class TestVersion(unittest.TestCase):

    def test_basic_comparisons(self):
        self.assertTrue(Version("1.0.0") < Version("2.0.0"))
        self.assertTrue(Version("1.0.0") < Version("1.42.0"))
        self.assertTrue(Version("1.2.0") < Version("1.2.42"))
        self.assertTrue(Version("1.0.0") == Version("1.0.0"))
        self.assertFalse(Version("1.0.0") != Version("1.0.0"))

    def test_prerelease_comparisons(self):
        self.assertTrue(Version("1.0.0-alpha") < Version("1.0.0-beta"))
        self.assertTrue(Version("1.0.0-alpha.1") < Version("1.0.0-alpha.2"))
        self.assertTrue(Version("1.0.0-alpha") < Version("1.0.0"))
        self.assertFalse(Version("1.0.0") < Version("1.0.0-alpha"))

    def test_patch_with_suffix(self):
        self.assertTrue(Version("1.0.1b") < Version("1.0.10-alpha.beta"))
        self.assertTrue(Version("1.0.1b") == Version("1.0.1b"))

    def test_invalid_versions(self):
        with self.assertRaises(ValueError):
            Version("1.0")  # missing patch
        with self.assertRaises(ValueError):
            Version("1.a.0")  # invalid minor
        with self.assertRaises(ValueError):
            Version("1.0.x")  # invalid patch segment

    def test_equality_and_inequality(self):
        v1 = Version("1.0.0-alpha.1")
        v2 = Version("1.0.0-alpha.1")
        v3 = Version("1.0.0-alpha.2")
        self.assertEqual(v1, v2)
        self.assertNotEqual(v1, v3)


if __name__ == "__main__":
    unittest.main()

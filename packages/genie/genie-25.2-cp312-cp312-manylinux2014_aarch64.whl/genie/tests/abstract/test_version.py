import unittest

versions = {
    "17.18.20250210:004817": {"release": (17, 18, "20250210:004817")},
    "12.2.20100719_0104est": {"release": (12, 2, 201007190104)},
    "24.1.1": {"release": (24, 1, 1)},
    "12.0.5wc3b": {"release": (12, 0, 5)},
    "25.1.1b0.dev0": {"release": (25, 1, 1), "pre": ("b", 0), "dev": 0},
    "10.5(2)": {"release": (10, 5, 2)},
    "12.2(20100719_0104)EST": {"release": (12, 2, 201007190104)},
    "17.7.1(20210101:01234)": {"release": (17, 7, 1, "20210101:01234")},
    "12.0.4T": {"release": (12, 0, 4)},
    "12.0.4.1": {"release": (12, 0, 4, 1)},
}


class TestVersion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global Version
        global packaging_version
        from genie.abstract import Version
        from packaging import version as packaging_version

    def test_version_negative(self):
        with self.assertRaises(packaging_version.InvalidVersion):
            Version("a.b.c")

    def test_version_pre(self):
        version = Version("12.0.4.a")
        self.assertEqual(str(version), "12.0.4a0")
        self.assertEqual(version.major, 12)
        self.assertEqual(version.minor, 0)
        self.assertEqual(version.micro, 4)
        self.assertEqual(version.pre, ("a", 0))

    def test_version_special(self):
        version = Version("12.0.4.1")
        self.assertEqual(str(version), "12.0.4.1")
        self.assertEqual(version.major, 12)
        self.assertEqual(version.minor, 0)
        self.assertEqual(version.micro, 4)
        self.assertEqual(version.pre, None)
        self.assertEqual(version.post, None)

    def test_versions(self):
        for ver, kv in versions.items():
            version = Version(ver)
            for k, v in kv.items():
                self.assertEqual(getattr(version, k), v)

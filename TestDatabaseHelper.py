import unittest
from Classes.DatabaseHelper import DatabaseHelper


class TestStringMethods(unittest.TestCase):
    def test_DatabaseHelperOnlyFirstRegex(self):
        testdatabasehelper = DatabaseHelper.UseOnlyFirstRegex(417, 'Aerospace Engineering')
        self.assertIsNotNone(testdatabasehelper)
        self.assertEqual(True, DatabaseHelper.UseOnlyFirstRegex(417, 'Aerospace Engineering'))
        self.assertEqual(False, DatabaseHelper.UseOnlyFirstRegex(417, 'Cats'))

    def test_DatabaseHelperOnlyFirstRegexHelper(self):
        self.assertEqual(True, DatabaseHelper.useOnlyOneRegexHelper(417, 'Aerospace Engineering'))
        self.assertEqual(False, DatabaseHelper.useOnlyOneRegexHelper(417, 'Cats'))

    def test_UseOnlyFirstRegexAndRegexHelper(self):
        self.assertEqual(True, DatabaseHelper.useOnlyFirstRegexAndRegexHelper(417, 'Aerospace Engineering'))

    def test_UseAllRegex(self):
        self.assertEqual(True, DatabaseHelper.useAllRegex(417, 'Aerospace Engineering'))

    def test_UseAllRegexHelper(self):
        self.assertEqual(True, DatabaseHelper.useAllRegexHelper(417, 'Aerospace Engineering'))

    def test_UseAllRegexAndRegexHelper(self):
        self.assertEqual(True, DatabaseHelper.useAllRegexAndRegexHelper(417, 'Aerospace Engineering'))

if __name__ == '__main__':
    unittest.main()

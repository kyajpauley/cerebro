import SamsLogins.FastWebClass as FWR
import unittest


class TestStringMethods(unittest.TestCase):

  def test_upper(self):
      self.assertEqual('foo'.upper(), 'FOO')

  def test_isupper(self):
      self.assertTrue('FOO'.isupper())
      self.assertFalse('Foo'.isupper())

  def test_classPutInCorrectVariables(self):
      testObject=FWR.FastWebClass("nameTest")
      self.assertEqual(testObject.name,"nameTest")







if __name__ == '__main__':
    unittest.main()
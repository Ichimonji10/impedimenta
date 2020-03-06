from unittest import TestCase


class MyTestCase(TestCase):
    def test_math(self):
        self.assertEqual(1 + 1, 2)

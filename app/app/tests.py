from django.test import TestCase

from app.calc import sum, sub


class CalcTests(TestCase):

    def test_add_numbers(self):
        """Testing add function"""
        self.assertEqual(sum(3, 5), 8)

    def test_subs_numbers(self):
        """Testing subtracting two numbers"""
        self.assertEqual(sub(5, 3), 2)
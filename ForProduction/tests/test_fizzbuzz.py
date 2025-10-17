# temporary tests to check unittest implementation, to be deleted

import unittest
from ForProduction.fizzbuzz import fizzbuzz

class TestFizzBuzz(unittest.TestCase):
    def test_fizz(self):
        for i in [3, 6, 9, 18]:
            print('testing', i)
            assert fizzbuzz(i) == 'Fizz'


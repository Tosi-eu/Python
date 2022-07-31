import unittest
from numbers import arithmetic_arranger

# the test case
class UnitTests(unittest.TestCase):

    def test_arrangement(self):
        test_now = arithmetic_arranger( ["3 + 855", "3801 - 2", "45 + 43", "123 + 49"])

        test_expected = "    3      3801      45      123\n+ 855    -    2    + 43    +  49\n-----    ------    ----    -----"
        self.assertEqual( test_now, test_expected,'Expected different output when calling "arithmetic_arranger()" with ["3 + 855", "3801 - 2", "45 + 43", "123 + 49"]')

        actual = arithmetic_arranger(["11 + 4", "3801 - 2999", "1 + 2", "123 + 49", "1 - 9380"])
        expected = "  11      3801      1      123         1\n+  4    - 2999    + 2    +  49    - 9380\n----    ------    ---    -----    ------"
        self.assertEqual(actual, expected,'Expected different output when calling "arithmetic_arranger()" with ["11 + 4", "3801 - 2999", "1 + 2", "123 + 49", "1 - 9380"]')

    def test_more_than5_problems(self):
        test_now = arithmetic_arranger(["44 + 815", "909 - 2", "45 + 43", "123 + 49", "888 + 40", "653 + 87"])
        test_expected = "Error: Too many problems."
        self.assertEqual(test_now, test_expected,'Expected calling "arithmetic_arranger()" with more than five problems to return "Error: Too many problems."')

    def test_valid_operators(self):
        test_now = arithmetic_arranger(["3 / 855", "3801 - 2", "45 + 43", "123 + 49"])
        test_expected = "Error: Operator must be '+' or '-'."
        self.assertEqual(test_now, test_expected, '''Expected calling "arithmetic_arranger()" with a problem that uses the "/" operator to return "Error: Operator must be '+' or '-'."''')

    def test_amount_of_digits(self):
        test_now = arithmetic_arranger(["24 + 85215", "3801 - 2", "45 + 43", "123 + 49"])
        test_expected = "Error: Numbers cannot be more than four digits."
        self.assertEqual(test_now, test_expected, 'Expected calling "arithmetic_arranger()" with a problem that has a number over 4 digits long to return "Error: Numbers cannot be more than four digits."')

    def test_valid_digits(self):
        test_now = arithmetic_arranger(["98 + 3g5", "3801 - 2", "45 + 43", "123 + 49"])
        test_expected = "Error: Numbers must only contain digits."
        self.assertEqual(test_now, test_expected, 'Expected calling "arithmetic_arranger()" with a problem that contains a letter character in the number to return "Error: Numbers must only contain digits."')

    def test_solutions(self):
        test_now = arithmetic_arranger(["32 - 698", "1 - 3801", "45 + 43", "123 + 49"], True)
        test_expected = "   32         1      45      123\n- 698    - 3801    + 43    +  49\n-----    ------    ----    -----\n -666     -3800      88      172"
        self.assertEqual(test_now, test_expected, 'Expected solutions to be correctly displayed in output when calling "arithmetic_arranger()" with arithemetic problems and a second argument of `True`.')

if __name__ == "__main__":
    unittest.main()
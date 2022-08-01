import unittest
import budget
from budget import MoneySpentGraphic


class UnitTests(unittest.TestCase):
    def setUp(self):
        self.__Food = budget.Category("Food")
        self.__Entertainment = budget.Category("Entertainment")
        self.__Business = budget.Category("Business")

    def test_deposit(self):
        self.__Food.DepositMoney(900, "deposit")
        actual = self.__Food.Ledger[0]
        expected = {"amount": 900, "description": "deposit"}
        self.assertEqual(actual, expected, 'Expected `deposit` method to create a specific object in the ledger instance variable.')

    def test_deposit_no_description(self):
        self.__Food.deposit(45.56)
        actual = self.__Food.Ledger[0]
        expected = {"amount": 45.56, "description": ""}
        self.assertEqual(actual, expected, 'Expected calling `deposit` method with no description to create a blank description.')

    def test_withdraw(self):
        self.__Food.DepositMoney(900, "deposit")
        self.__Food.WithDrawMoney(45.67, "milk, cereal, eggs, bacon, bread")
        actual = self.__Food.Ledger[1]
        expected = {"amount": -45.67, "description": "milk, cereal, eggs, bacon, bread"}
        self.assertEqual(actual, expected, 'Expected `withdraw` method to create a specific object in the ledger instance variable.')

    def test_withdraw_no_description(self):
        self.__Food.deposit(900, "deposit")
        good_withdraw = self.__Food.WithDrawMoney(45.67)
        actual = self.__Food.Ledger[1]
        expected = {"amount": -45.67, "description": ""}
        self.assertEqual(actual, expected, 'Expected `withdraw` method with no description to create a blank description.')
        self.assertEqual(good_withdraw, True, 'Expected `transfer` method to return `True`.')

    def test_get_balance(self):
        self.__Food.DepositMoney(900, "deposit")
        self.__Food.WithDrawMoney(45.67, "milk, cereal, eggs, bacon, bread")
        actual = self.__Food.MoneyBalance()
        expected = 854.33
        self.assertEqual(actual, expected, 'Expected balance to be 854.33')

    def test_transfer(self):
        self.__Food.DepositMoney(900, "deposit")
        self.__Food.WithDrawMoney(45.67, "milk, cereal, eggs, bacon, bread")
        good_transfer = self.__Food.TransferMoney(20, self.__Entertainment)
        actual = self.__Food.Ledger[2]
        expected = {"amount": -20, "description": "Transfer to Entertainment"}
        self.assertEqual(actual, expected, 'Expected `transfer` method to create a specific ledger item in food object.')
        self.assertEqual(good_transfer, True, 'Expected `transfer` method to return `True`.')
        actual = self.__Entertainment.Ledger[0]
        expected = {"amount": 20, "description": "Transfer from Food"}
        self.assertEqual(actual, expected, 'Expected `transfer` method to create a specific ledger item in entertainment object.')

    def test_check_funds(self):
        self.__Food.DepositMoney(10, "deposit")
        actual = self.__Food.CheckDisponibleMoney(20)
        expected = False
        self.assertEqual(actual, expected, 'Expected `check_funds` method to be False')
        actual = self.__Food.CheckDisponibleMoney(10)
        expected = True
        self.assertEqual(actual, expected, 'Expected `check_funds` method to be True')

    def test_withdraw_no_funds(self):
        self.__Food.DepositMoney(100, "deposit")
        good_withdraw = self.__Food.WithDrawMoney(100.10)
        self.assertEqual(good_withdraw, False, 'Expected `withdraw` method to return `False`.')

    def test_transfer_no_funds(self):
        self.__Food.DepositMoney(100, "deposit")
        good_transfer = self.__Food.TransferMoney(200, self.__Entertainment)
        self.assertEqual(good_transfer, False, 'Expected `transfer` method to return `False`.')

    def test_to_string(self):
        self.__Food.DepositMoney(900, "deposit")
        self.__Food.WithDrawMoney(45.67, "milk, cereal, eggs, bacon, bread")
        self.__Food.TransferMoney(20, self.__Entertainment)
        actual = str(self.__Food)
        expected = f"*************Food*************\ndeposit                 900.00\nmilk, cereal, eggs, bac -45.67\nTransfer to Entertainme -20.00\nTotal: 834.33"
        self.assertEqual(actual, expected, 'Expected different string representation of object.')

    def test_create_spend_chart(self):
        self.__Food.DepositMoney(900, "deposit")
        self.__Entertainment.DepositMoney(900, "deposit")
        self.__Business.DepositMoney(900, "deposit")
        self.__Food.WithDrawMoney(105.55)
        self.__Entertainment.WithDrawMoney(33.40)
        self.__Business.WithDrawMoney(10.99)
        actual = MoneySpentGraphic([self.__Business, self.__Food, self.__Entertainment])
        expected = "Percentage spent by category\n100|          \n 90|          \n 80|          \n 70|    o     \n 60|    o     \n 50|    o     \n 40|    o     \n 30|    o     \n 20|    o  o  \n 10|    o  o  \n  0| o  o  o  \n    ----------\n     B  F  E  \n     u  o  n  \n     s  o  t  \n     i  d  e  \n     n     r  \n     e     t  \n     s     a  \n     s     i  \n           n  \n           m  \n           e  \n           n  \n           t  "
        self.assertEqual(actual, expected, 'Expected different chart representation. Check that all spacing is exact.')

if __name__ == "__main__":
    unittest.main()
class Category:
  
    def __init__(self, ProductDescription):
        self.Describe = ProductDescription
        self.Ledger = []
        self.__Balance = 0.0

    def __repr__(self):
        HeaderOrnament = self.Describe.center(30, "*") + "\n"
        Ledger = ""
        for item in self.Ledger:
            line_description = "{:<23}".format(item["Description"])
            line_amount = "{:>7.2f}".format(item["Amount"])
            Ledger += "{}{}\n".format(line_description[:23], line_amount[:7])

        TotalCast = "Total: {:.2f}".format(self.__Balance)
        return HeaderOrnament + Ledger + TotalCast

    def DepositMoney(self, Amount, ProductDescription=""):
        self.Ledger.append({"Amount": Amount, "Description": ProductDescription})
        self.__Balance += Amount

    def WithDrawMoney(self, Amount, ProductDescription=""):
        if self.__Balance - Amount >= 0:
            self.Ledger.append({"Amount": -1 * Amount, "Description": ProductDescription})
            self.__Balance -= Amount
            return True
        else:
            return False

    def MoneyBalance(self):
        return self.__Balance

    def TransferMoney(self, Amount, SpecificCategory):
        if self.WithDrawMoney(Amount, "Transfer to {}".format(SpecificCategory.Describe)):
            SpecificCategory.DepositMoney(Amount, "Transfer from {}".format(self.Describe))
            return True
        else:
            return False

    def CheckDisponibleMoney(self, amount):
        if self.__Balance >= amount:
            return True
        else:
            return False


def MoneySpentGraphic(categories):
    Spent = []
    for SpecificItem in categories:
        MoneySpent = 0
        for Item in SpecificItem.Ledger:
            if Item["Amount"] < 0:
                MoneySpent += abs(Item["Amount"])
        Spent.append(round(MoneySpent, 2))

    Total = round(sum(Spent), 2)
    SpentPercent = list(map(lambda amount: int((((amount / Total) * 10) // 1) * 10), Spent))
    
    PercentageHeader = "\nPercentage spent by category:\n"

    PercentageGraphic = ""
    for Value in reversed(range(0, 101, 10)):
        PercentageGraphic += str(Value).rjust(3) + '|'
        for Percent in SpentPercent:
            if Percent >= Value:
                PercentageGraphic += " o "
            else:
                PercentageGraphic += "   "
        PercentageGraphic += " \n"

    BaseBoard = "    " + "-" * ((3 * len(categories)) + 1) + "\n"
    CategoryDescription = list(map(lambda category: category.Describe, categories))
    Max = max(map(lambda description: len(description), CategoryDescription))
    CategoryDescription = list(map(lambda description: description.ljust(Max), CategoryDescription))
    for x in zip(*CategoryDescription):
        BaseBoard += "    " + "".join(map(lambda s: s.center(3), x)) + " \n"

    return (PercentageHeader + PercentageGraphic + BaseBoard).rstrip("\n")

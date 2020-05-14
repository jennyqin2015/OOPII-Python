class Portfolio(object):
    '''
        This portfolio contains account, stocks, and real estate information.
    '''
    def __init__(self, name):
        self.name = name
        self.stocks = {}
        self.realEstate = {}
        self.account = Account(0)

    def addFund(self, money):
        self.account.deposit(money)

    def minusFund(self, money):
        self.account.withdraw(money)


    def buyStock(self, symbol, shares, price):
        totalCost = price * shares
        try:
            if totalCost > self.account.balance:
                raise NoFundError
            else:
                self.stocks[symbol] = Stock(symbol, shares, totalCost)
                self.account.balance -= totalCost
        except NoFundError:
            print("There is not enough fund in your accound.")

    def sellStock(self, symbol, shares):
        price = self.stocks[symbol].totalCost / self.stocks[symbol].shares
        received_money = price * shares
        self.stocks[symbol].shares -= shares
        self.account.balance += received_money

    def buyReal(self,id, marketValue):
        try:
            if marketValue > self.account.balance:
                raise NoFundError
            else:
                self.realEstate[id] = RealEstate(id, marketValue)
                self.account.balance -= marketValue
        except NoFundError:
            print("There is not enough fund in your accound.")
    def sellReal(self,id, sellPrice):
        self.account.balance += sellPrice
        del self.realEstate[id]

    def transferFund(self, portB, money):
        self.addFund(money)
        portB.minusFund(money)

    def transferStock(self, portB, symbol, shares):
        '''

        if symbol does not exist in portB's stock list
        '''
        price = self.stocks[symbol].totalCost / self.stocks[symbol].shares
        totalCost = price * shares
        if symbol in portB.stocks.keys():
            self.stocks[symbol].minusShares(shares, totalCost)
            self.stocks[symbol].addShares(shares, totalCost)
        else:
            self.stocks[symbol].minusShares(shares, totalCost)
            stock = Stock(symbol,shares, totalCost)
            portB.stocks[symbol] = stock

    def transferReal(self, portB, id):
        portB.realEstate[id] = self.realEstate[id]
        del self.realEstate[id]



    def writeToFile(self, filename):
        with open(filename, 'a') as f:
            f.write(self.name+"\n")
            f.write(self.account.__str__())

            for i in self.stocks:
                f.write(self.stocks[i].__str__())
            for i in self.realEstate:
                f.write(self.realEstate[i].__str__())



class NoFundError(Exception):
    pass

class Account(object):
    def __init__(self, balance):
        self.balance = balance
    def deposit(self, money):
        self.balance += money
    def withdraw(self, money):
        self.balance -= money

    def __str__(self):
        return "Your account balance is {} \n".format(self.balance)

class RealEstate(object):
    def __init__(self, id, marketvalue):
        self.id = id
        self.marketValue = marketvalue
    def __str__(self):
        return "You own property {0} which worths {1} \n".format(self.id, self.marketValue)

class Stock(object):
    def __init__(self, symbol, shares, totalCost):
        self.symbol = symbol
        self.shares = shares
        self.totalCost = totalCost

    def addShares(self,shares, totalCost):
        self.shares += shares
        self.totalCost+=totalCost

    def minusShares(self,shares, totalCost):
        self.shares -= shares
        self.totalCost -= totalCost

    def __str__(self):
        return "You hold stock {0} {1} shares, and they cost {2}\n".format(self.symbol, self.shares,self.totalCost)









def mergePorts(portfolioA, portfolioB, newPortName):
    new = Portfolio(newPortName)
    fund = portfolioA.account.balance + portfolioB.account.balance
    account = Account(fund)
    new.account = account
    new.realEstate = {**portfolioA.realEstate, **portfolioB.realEstate}
    for symbol in portfolioA.stocks.keys():
        if symbol in portfolioB.stocks.keys():
            shares = portfolioA.stocks[symbol].shares + portfolioB.stocks[symbol].shares
            totalCost = portfolioA.stocks[symbol].totalCost + portfolioB.stocks[symbol].totalCost
            new.stocks[symbol] = Stock(symbol, shares, totalCost)
        else:
            shares = portfolioA.stocks[symbol].shares
            totalCost = portfolioA.stocks[symbol].totalCost
            new.stocks[symbol] = Stock(symbol, shares, totalCost)
    for symbol in portfolioB.stocks.keys():
        if symbol not in new.stocks.keys():
            shares = portfolioB.stocks[symbol].shares
            totalCost = portfolioB.stocks[symbol].totalCost
            new.stocks[symbol] = Stock(symbol, shares, totalCost)
    return new



if __name__ == "__main__":
    '''
    port_a = Portfolio("jenny")
    port_a.setAccount(10000)
    port_a.buyRealEstate("abba",100000)
    port_a.buyStocks("appl",10,200)
    print(port_a.account.balance)
    '''

    '''
    read in an input file with commands
    create portfolios and complete the operations specified in the input file
    output the portfolio information to a new file output.txt
    '''
    portfolios = {}
    arg_list = []
    with open("/Users/jennyqin/Desktop/oop2/hw/HW3/input","r") as file:
        for line in file:
            line = line.rstrip('\n')
            print(line)

            args = line.split(',')
            args = [i.lstrip(" ") for i in args]
            arg_list.append(args)
    print(arg_list)
    # perform operations
    # convert string type user input to float type variables
    for i in arg_list:
        operation = i[0]
        args = i[1:]
        for j in range(len(args)):
            if args[j].isdigit():
                args[j] = float(args[j])
        if operation =="Cp":
            portfolios[args[0]] = Portfolio(args[0])
            print(len(portfolios))
        if operation == "Bs":
            print(type(args[1]))
            print(type(args[2]))
            portfolios[args[-1]].buyStock(args[0],args[1],float(args[2]))
        if operation == "Ss":
            portfolios[args[-1]].sellStock(args[0], float(args[1], float(args[2])))
        if operation == "Br":
            portfolios[args[-1]].buyReal(args[0],args[1])
        if operation == "Sr":
            portfolios[args[-1]].sellReal(args[0], args[1])
        if operation == "Xs":
            portfolios[args[0]].transferStock(portfolios[args[1]], args[2], float(args[3]))

        if operation == "Xr":
            portfolios[args[0]].transferReal(portfolios[args[1]], args[2])
        if operation == "Xf":
            portfolios[args[0]].transferFund(portfolios[args[1]], float(args[2]))
        if operation == "Dp":
            portfolios[args[0]].addFund(args[1])
        if operation == "Wd":
            portfolios[args[0]].minusFund(args[1])
        if operation == "Mg":
            portfolios[args[2]] = mergePorts(portfolios[args[0]], portfolios[args[1]],args[2])

    for k in portfolios.keys():
        portfolios[k].writeToFile("output")
    # write portfolios to an output file

'''
    A = Portfolio("michael")
    A.addFund(1000)
    A.minusFund(500)
    
    A.buyReal("id",400)
    #A.sellReal("id")
    A.display()

'''

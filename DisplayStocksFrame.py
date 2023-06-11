import tkinter as tk
from PIL import ImageTk, Image
import yfinance as yf
import DBHandler
import threading
import time
import pandas as pd
import matplotlib.pyplot as plt
import sys 


class DispalyStocksFrame(tk.Frame) :
    """
        A class representing a frame to display stocks and interact with a database.

    Attributes:
        dbh (DBHandler.DatabaseHandler): An instance of the database handler.
        user (str): The username associated with the frame.
        stocks (list): A list of stock symbols.
        user_id (int): The user ID associated with the frame.
        stock_name_label (tk.Label): A label for the stock names.
        stock_price_label (tk.Label): A label for the stock prices.
        owned_stock_amount (tk.Label): A label for the owned stock amounts.
        owned_res_var (tk.StringVar): A string variable for displaying owned resources.
        owned_resources (tk.Label): A label for displaying owned resources.
        open (bool): A flag indicating if the frame is open.

    Methods:
        __init__(self, parent, dbh:DBHandler.DatabaseHandler, user:str): Initializes the DisplayStocksFrame instance.
        inset_stick_data_to_db(self, name, ticker): Inserts stock data into the database.
        __generate_row__(self, i): Generates a row in the frame for a stock.
        __update_labels__(self): Updates the stock labels with the latest prices.
        buy_stock(self, userid, stockid, stock_name): Buys a stock for the user.
        sell_stock(self, userid, stockid, stock_name): Sells a stock for the user.
        on_close(self): Closes the frame.
        __display_graph__(self, stock): Displays a graph for the stock data.
    """


    def __init__(self, parent, dbh:DBHandler.DatabaseHandler , user :str) :
        tk.Frame.__init__(self, parent)
        self.dbh = dbh
        self.user = user
        self.stocks = ["AAPL", "MSFT" , "GOOG" , "META" ,"TSLA", "MCD", "T", "S", "SOFI"]
        self.user_id = dbh.get_user_id(user)
        
        self.stock_name_label = tk.Label(self ,text="code")
        self.stock_price_label = tk.Label(self , text ="price")
        self.owned_stock_amount = tk.Label(self , text="owned")
        
        self.stock_name_label.grid(row=3, column=0)
        self.stock_name_label.grid(row=3 , column= 1)
        self.owned_stock_amount.grid(row= 3 , column= 2)
        self.owned_res_var = tk.StringVar()
        self.owned_res_var.set(f"owned resoutces: {dbh.get_user_resources(self.user_id)}")
        self.owned_resources = tk.Label(self , textvariable=self.owned_res_var).grid(row =3 , column= 3 )
        
        self.open = True
        
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)
        
        ticker_list = list()
        self.label_list = list()
        
        self.stockPrices= dict()    
        
        self.stockAmount = dict()
        #get acces to db and get how many of given stock user have
        for stock in self.stocks:
            ticker = yf.Ticker(stock)
            sv = tk.StringVar()
            th = threading.Thread(target=self.inset_stick_data_to_db(stock , ticker))
            th.start()
            sv.set(ticker.info["currentPrice"])
            self.stockPrices[stock] = sv
            
            self.label_list.append(tk.Label(self,text=stock))
            self.label_list.append(tk.Label(self, textvariable=sv ))    
        
        for i in range(0, len(self.label_list)//2):
            self.__generate_row__(i )
            
        label_update_thread = threading.Thread(target=self.__update_labels__)
        label_update_thread.start()
        
        

    def inset_stick_data_to_db(self , name ,ticker: yf.Ticker):
        """
        Inserts stock data into the database.

        Args:
            name (str): The stock symbol.
            ticker (yfinance.Ticker): The Ticker object for the stock.
        """
        ticker_data = ticker.history()
        self.dbh.inset_to_stock_table(name , ticker_data)
        
    def __generate_row__(self , i: int , ):
        """
        Generates a row in the frame for a stock.

        Args:
            i (int): The index of the stock.
        """
        
        k=i*2
        self.label_list[k].grid(row = 4+ k , column = 0)
        self.label_list[k+1].grid(row = 4+ k , column = 1)
        st = self.stocks[i]
        amount = self.dbh.get_stock_amount(self.user , st)

        strVar = tk.StringVar()
        strVar.set(amount)
        self.stockAmount[st] = strVar
        st_id = self.dbh.get_stock_id(st)
        l = tk.Label(self, textvariable=strVar).grid( row = 4 + k , column= 2 )
        buy_button = tk.Button(self , text= "buy" , command=lambda : self.buy_stock(self.user_id ,st_id , st )).grid( row = 4 + k , column= 3 )
        buy_button = tk.Button(self , text="sell" , command=lambda : self.sell_stock(self.user_id , st_id , st) ).grid( row = 4 + k , column= 4 )
        details_button = tk.Button(self , text="graphs" , command= lambda : self.__display_graph__(st) ).grid( row = 4 + k , column= 5 )
        
    
    def __update_labels__(self):
        """
        Updates the stock string variables with the latest prices.
        """
        while(True):
            time.sleep(5)
            if(not self.open):
                return
            for stock in self.stocks:
                ticker = yf.Ticker(stock)
                self.stockPrices[stock].set( ticker.info["currentPrice"])

                
                
    def buy_stock(self , userid , stockid , stock_name ):
        """
        Buys a stock for the user.

        Args:
            userid (int): The user ID.
            stockid (int): The stock ID.
            stock_name (str): The stock symbol.
        """
        price = float(self.stockPrices[stock_name].get())
        self.dbh.buy_stock(self.user_id , stockid , price)
        amount = self.dbh.get_stock_amount(self.user , stock_name)
        self.stockAmount[stock_name].set(amount)
        res = self.dbh.get_user_resources(userid)
        self.owned_res_var.set(res)
        
        
    def sell_stock(self ,  userid , stockid , stock_name ):
        """
        Sells a stock for the user.

        Args:
            userid (int): The user ID.
            stockid (int): The stock ID.
            stock_name (str): The stock symbol.
        """
        price = float(self.stockPrices[stock_name].get())
        self.dbh.sell_stock(self.user_id , stockid , price)
        amount = self.dbh.get_stock_amount(self.user , stock_name)
        self.stockAmount[stock_name].set(amount)
        res = self.dbh.get_user_resources(userid)
        self.owned_res_var.set(res)

    
    def on_close(self):
        """
        Closes the frame.
        """
        self.open = False
        self.master.destroy()
        sys.exit()
        
    def __display_graph__(self , stock ):
        """
        Displays a graph for the stock data.

        Args:
            stock (str): The stock symbol.
        """
        df = self.dbh.get_stock_data(stock)

        plt.plot(df['Date'], df['Open'], label='Open')
        plt.plot(df['Date'], df['Close'], label='Close')
        plt.plot(df['Date'], df['High'], label='High')
        plt.plot(df['Date'], df['Low'], label='Low')
        
        plt.xlabel('Date')
        plt.ylabel('Value')
        plt.title('Stock Data')
        plt.legend()
        plt.grid(True)
        
        plt.show()
        

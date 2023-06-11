from sqlalchemy import Column, Integer, String, ForeignKey, Float, desc, select, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, inspect, MetaData, Table
import pandas as pd

engine = create_engine("sqlite:///usersdatabase.db")
Base = declarative_base()


class User(Base):
    """
    Represents the User table in the database.

    Attributes:
        id (Column): The primary key column for the user ID.
        name (Column): The column for the user's name.
        password (Column): The column for the user's password.
        resources (Column): The column for the user's resources.

    """
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    password = Column(String(50))
    resources = Column(Float)



class Instrument(Base):
    """
    Represents the Instrument table in the database.

    Attributes:
        id (Column): The primary key column for the user ID.
        name (Column): The column for the stkocks's name.
        

    """
    __tablename__ = 'instrument'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))


class UserInstrument(Base):
    """
    Represents the join table between user and instrument.

    Attributes:
        user_id The column for the user's id.
        instrument_id column for instuments id
        amount column for amounmt of given stock by given user

    """
    __tablename__ = 'user_instrument'

    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    instrument_id = Column(Integer, ForeignKey('instrument.id'), primary_key=True)
    amount = Column(Float)
    
    user = relationship("User", backref="user_instrument")
    instrument = relationship("Instrument", backref="user_instrument")

class StockBase(Base):
    """
    Abstract base class representing stock data in the database.

    Attributes:
        Date (sqlalchemy.sql.schema.Column): The column for the date of the stock data (primary key).
        Open (sqlalchemy.sql.schema.Column): The column for the opening price of the stock.
        Close (sqlalchemy.sql.schema.Column): The column for the closing price of the stock.
        High (sqlalchemy.sql.schema.Column): The column for the highest price of the stock.
        Low (sqlalchemy.sql.schema.Column): The column for the lowest price of the stock.

    Args:
        Base (type): The declarative base class for the SQLAlchemy model.
    """
    __abstract__ = True
    Date = Column(String   ,primary_key=True)
    Open = Column(Float)
    Close = Column(Float)
    High = Column(Float)
    Low = Column(Float)    

class DatabaseHandler():
    """
    A class for handling database operations.

    Attributes:
        engine (sqlalchemy.engine.Engine): The database engine.
        session (sqlalchemy.orm.Session): The database session.
        user_id (int): The user ID associated with the database handler.

    Methods:
        __init__(self, engine: sqlalchemy.engine.Engine): Initializes the DatabaseHandler instance.
        verify_user(self, username: str, password: str) -> bool: Verifies if a user exists with the given username and password.
        draw_graph(self, stock: str) -> pd.DataFrame: Retrieves stock data from the database and returns it as a DataFrame.
        insert_to_stock_table(self, stock: str, pd_frame: pd.DataFrame): Inserts stock data into the specified stock table in the database.
        get_stock_id(self, stock: str) -> int: Retrieves the ID of the given stock from the database.
        get_last_date(self, stock: str) -> str: Retrieves the latest date from the specified stock table in the database.
        get_user_id(self, user: str) -> int: Retrieves the ID of the given user from the database.
        get_stock_amount(self, user: str, stock: str) -> float: Retrieves the amount of the specified stock owned by the user from the database.
        get_user_resources(self, user_id: int) -> float: Retrieves the resources of the specified user from the database.
        buy_stock(self, user_id: int, stock_id: int, price: float): Buys a stock for the user and updates the database.
        sell_stock(self, user_id: int, stock_id: int, price: float): Sells a stock for the user and updates the database.
    """
    stock_list = ["AAPL", "MSFT" , "GOOG" , "META" ,"TSLA", "MCD", "T", "S", "SOFI"]
    def __init__(self, engine: engine ):
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.user_id = int()
        self.mtdata = MetaData()
        self.mtdata.reflect(bind = engine)
        self.engine = engine

    def verivy_user(self , username:str() , password:str()):
        """
        Verifies if a user with the given username and password exists in the database.

        Args:
            username (str): The username.
            password (str): The password.

        Returns:
            bool: True if the user exists, False otherwise.
        """

        correct = self.session.query(User).filter(User.name == username , User.password == password).count()
        return correct == 1
    
    def get_stock_data(self , stock):
        """
        Retrieves stock data from the database and returns it as a DataFrame.

        Args:
            stock (str): The stock symbol.

        Returns:
            pd.DataFrame: The stock data.
        """
        query = f'select * from {stock}'
        return pd.read_sql(query , self.engine)


    def inset_to_stock_table(self, stock, pdFrame: pd.DataFrame):
        """
        Inserts stock data into the specified stock table in the database.

        Args:
            stock (str): The stock symbol.
            pdFrame (pd.DataFrame): The stock data as a DataFrame.
        """
        pdFrame = pdFrame.reset_index()

        query = f'select * from {stock}'
        query_df = pd.read_sql(query, self.engine)

        selected_cols = ["Date" , "Open" , "Close" , "High" , "Low"] 
        pdFrame = pdFrame[selected_cols]
        new_records = pdFrame[~pdFrame['Date'].isin(query_df['Date'])]

        res = pd.concat([query_df, new_records])

        res.sort_values('Date', inplace=True)
        
        res['Date'] = res['Date'].astype(str)

        res.to_sql(stock, self.engine, if_exists="replace", index=False)
        

            
    def get_stock_id(self , stock):
        """
        Retrieves the ID of the given stock from the database.

        Args:
            stock (str): The stock symbol.

        Returns:
            int: The stock ID.
        """
        s = self.session.query(Instrument).filter(Instrument.name == stock).limit(1).all()
        for el in s :
            return el.id
    
    def __last_date__(self, stock):
        """
        Retrieves the latest date from the specified stock table in the database.

        Args:
            stock (str): The stock symbol.

        Returns:
            str: The latest date.
        """
        table = self.mtdata.tables(stock)
        latest_date_query = table.select().order_by(desc(table.c.date_column)).limit(1)
        result = engine.execute(latest_date_query)
        latest_row = result.fetchone()
        latest_date = latest_row.Date  

        return latest_date
    
    def get_user_id(self , user:str):
        """
        Retrieves the ID of the given user from the database.

        Args:
            user (str): The username.

        Returns:
            int: The user ID.
        """
        u = self.session.query(User).filter(User.name == user ).limit(1).all()
        self.user_id = 1
        return self.user_id
    
    def get_stock_amount(self , user: str , stock:str):
        """
        Retrieves the amount of the specified stock owned by the user from the database.

        Args:
            user (str): The username.
            stock (str): The stock symbol.

        Returns:
            float: The amount of the stock owned by the user.
        """
        stock_id = self.get_stock_id(  stock)    
        for e in (self.session.query(UserInstrument)
                .filter(UserInstrument.user_id == self.user_id , UserInstrument.instrument_id == stock_id)
                .limit(1)
                .all()):
            return e.amount
        
    def get_user_resources(self , user_id ) :
        """
        Retrieves the resources (e.g., money) of the specified user from the database.

        Args:
            user_id (int): The user ID.

        Returns:
            float: The user's resources.
        """
        query = self.session.query(User).filter(User.id == user_id).all()
        for u in query:
            return u.resources
        

    def buy_stock(self , userid , stockid , price ):
        """
        Buys a stock for the specified user and updates the user's resources and stock amount in the database.

        Args:
            userid (int): The ID of the user.
            stockid (int): The ID of the stock.
            price (float): The price of the stock.
        """
        query_user = self.session.query(User).filter(User.id == userid ).all()
        query_join = self.session.query(UserInstrument).filter(UserInstrument.user_id == userid , UserInstrument.instrument_id == stockid).all()
        if query_user[0].resources - price >=0 :
            query_user[0].resources = query_user[0].resources - price 
            query_join[0].amount = query_join[0].amount +1 
            self.session.commit()
            
    def sell_stock(self , userid , stockid , price ):
        """
        Sells a stock for the specified user and updates the user's resources and stock amount in the database.

        Args:
            userid (int): The ID of the user.
            stockid (int): The ID of the stock.
            price (float): The price of the stock.
        """
        query_user = self.session.query(User).filter(User.id == userid ).all()
        query_join = self.session.query(UserInstrument).filter(UserInstrument.user_id == userid , UserInstrument.instrument_id == stockid).all()
        if query_join[0].amount -1  >= 0 :
            query_user[0].resources = query_user[0].resources + price
            query_join[0].amount = query_join[0].amount -1 
            self.session.commit()
        
class AAPL(StockBase):
    __tablename__  ="AAPL"

class MSFT(StockBase):
    __tablename__  ="MSFT"

class GOOG(StockBase):
    __tablename__  ="GOOG"

class META(StockBase):
    __tablename__  ="META"

class TSLA(StockBase):
    __tablename__  ="TSLA"

class MCD(StockBase):
    __tablename__  ="MCD"

class T(StockBase):
    __tablename__  ="T"

class S(StockBase):
    __tablename__  ="S"

class SOFI(StockBase):
    __tablename__  ="SOFI"


# initialises database
inspector = inspect(engine)
dbh = DatabaseHandler(engine)

table_names = inspector.get_table_names()
if 'user' in table_names:
    print("The table exists.")
else:
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    stock_list = ["AAPL", "MSFT" , "GOOG" , "META" ,"TSLA", "MCD", "T", "S", "SOFI"]
    
    for s in stock_list:
        session.add(Instrument(name = s))
    

    user = User(name="admin", password="1234", resources=10000)
    session.add(user)
    
    session.commit()
    st = session.query(Instrument).all()
    
    for s in st:
        user_st = UserInstrument(user_id = dbh.get_user_id("admin")  , instrument_id = s.id , amount =1)
        session.add(user_st)

    session.commit()








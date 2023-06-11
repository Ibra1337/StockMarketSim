# StockMarketSim
this aplication is simple stock market simaltor
-prices are updated almoust in real time 
-allows user to simulate buying/selling stocks of fiew selected companys

```bash
pip install -r requirements.txt
```

## Starting the app
In order to start the program user needs to simply either run the ***main.py*** file from file explorer or run following command in command line:

- **Windows**
```bash
py main.py
```

## Feautures
***Stock market sim***
alow user to login
buy/sell invest on stock market
collect data about stocks 
display OHCLgrap for each stock 

### Module breakdown
-** DBHandler **: module responsible for handling operations connected with database 
-**LoginFrame** : frame responsible for login part
-**StartFrame** : welcoming frame
-**DisplayStockFrame** : frame responsible for buying/selling stocks displaying graphs and displaying prices

## Challenges during development
-making background to adjust to window size 
-making stock prices update 
-not inserting unnecesary data to database

## Learned lessons
- panda frame can be easly inseted to database
- making images adjusting to widnow size 
- how to  plot graphs using matholillib.pyplot

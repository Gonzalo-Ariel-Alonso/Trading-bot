# Trading strategy test

The main objetive of this proyect is to create and teset trading strategy, for this porpose we need four thing: 
- A data base with price history 
- A trading strategy.
- A program who backtest who test strategy.
- A program that comunicate with an exchange to execute the strategy.
Let's expand this topics:

### Data base with price history: ###
In order to backteset a strategy first we need the data of historical prices of the asset with which we want to test the strategy. To archive this we are going
to use an API of an exchange to send a request with all the information of a japanse candle and store this information in a local data base. The info that we need
from a japanese calnde is:
- Date of the candle (YYYY-MM-DD)
- Start time (HH-MM-SS)
- End time (HH-MM-SS)
- [Low , High , Open , Close] price
- % variation between High and Low
- Time stamp
- Operated volume

Note: Some of this data comes directly from the API and some other need to be caluclated. Depending on the strategy it migth be needed more or less information.

### Trading strategy ###
There are a lots of trading strategy, some of them are very simple and some of them are very complex. For this proyect
we are going to use a simple one: 
    Some tradeers belibe that market move by inertia, in phisics a body only moves if 
an external force is applied to it, in the market case our body will be the price and our force the aggresive buying/selling of smarth mony (entitis with big amounts of money that can move the suply and demand curve). So if we detect that the price move to a direction with a lot of variation in a sigle candle its means that smarth money it is interested in the price moves to that direction. So when we detect that the price move a cenrtain % in a certain amount of time we are going to open a trade to join the smarth money in his intention.

### Back Testing Strategy ###
If we do not ensure that our strategy will be profitable it going to drain our money, so in order to avoid this we need to backtest the strategy, it can be do manualy, but this will take a lot of time and we will be expose to the human error. Insted we can use the Data Base to simulite every posible trade that we would it take it with our strategy. This methot allow us to not only backtest a strategy but figure it out what is the most profitable move price % to open a trade.

Note: NOBODY can predict what is the market going to do, all strategy have wins and loses, but if we keep the odds in our side, our profit it is going to be bigger than our loses.

### Execuintg the strategy ###
we crate a strategy, we backtested and polish all numbers to get the most profits, now we need to put it into operation.
As equal to backtesting, we can do this manulay, but this will require somone to be seat in front of the computer to open and close the operation, this by itslef would be very inefitien and we dont even take in count the big pyscologial presure that humans take when money is risked. So we can create a bot that do all the diry stuff for use: this bot will make sure that every trade open and closes in the exact moment that our strategy tell us to do. To do this we need to comunicate with and exchange via API telling our bot this things our bot need to monitore the price in real time so we can tell him:
- When open a trade
- How much money goes in to the trade
- Leverage
- Price of stop loss
- Price if take profit
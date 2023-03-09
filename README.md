# Trading bot

Trading is not an easy thing to do, and everyone who has tried knows the rule of 90: 90% of traders lose 90% of their capital within the first 90 days. There are three reasons why this happens:

- Finding a good strategy that suits the trader.
- Being at the computer to execute that strategy.
- Controlling the emotions of the possibility (and being ready for it, because it will happen) of losing money.

Perhaps it seems like there are only three reasons that sound like they could be mastered very fast, but most people just can't handle their emotions when they see their money disappearing. Sooner rather than later, they quit (just like me).

Don't get me wrong, if you keep studying, trying, and learning from your mistakes, you will become a successful trader. However, if you, like me, feel like you're stuck, I believe I found a better solution to easily resolve those problems. If you think about it, all barriers are caused because of the human factor. So, I have the idea of removing this fact by creating a trading bot. This is how it works:

This trading bot is divided into three main parts:

- A database with price history.
- A coded trading strategy and backtesting.
- Automated execution of a strategy.

Let's expand on these topics:

## Data base with price history: 
In order to backtest a strategy, we first need the data of historical prices of an asset with which we want to test the strategy. To achieve this, we are going to use an API of an exchange to request all the information of a Japanese candle that will be stored in a local database. The info that we need from a Japanese candle is:

   - Date of the candle (YYYY-MM-DD)
   - Start time (HH-MM-SS)
   - End time (HH-MM-SS)
   - [Low, High, Open, Close] price
   - Time stamp (This will function as a primary key)
   - Operated volume

Note: This data comes directly from the API, but in order to execute some strategies, we may need to calculate some indicators.

## Trading strategy and backtesting
There are a lots of trading strategy, some of them are very simple, and some are very complex. For this proyect,
we are going to use a simple one: 

### Big candle strategy:
Some traders believe that the market moves by inertia. In physics, a body only moves if an external force is applied to it. In the market case, our body will be the price, and our force the aggressive buying/selling of smart money (entities with big amounts of money that can move the supply and demand curve). So, if we detect that the price moves in a direction with a lot of variation in a single candle, it means that smart money is interested in the price moving to that direction. Therefore, when we detect that the price moves a certain percentage in a certain amount of time, we are going to open a trade to join the smart money in their intention.

If we do not ensure that our strategy will be profitable, it will drain our money. Therefore, to avoid this, we need to backtest the strategy. It can be done manually, but this will take a lot of time, and we will be exposed to human error. Instead, we can use the database to simulate every possible trade that we would take with our strategy. This method allows us to not only backtest a strategy but also figure out what is the most profitable move price percentage to open a trade.

Note: NOBODY can predict what the market is going to do. All strategies have wins and losses, but if we keep the odds in our favor, in the long term, our profit will be bigger than our

## Automating our strategy
Now that we have created a strategy, backtested it, and polished all the numbers to get the most profits, it's time to put it into operation.
Just like with backtesting, we could do this manually, but that would require someone to sit in front of the computer and open and close all trades. This would be very inefficient, and we don't even take into account the significant psychological pressure that humans experience when risking money. So, we can create a bot that does all the repetitive work for us. This bot will ensure that every trade is opened and closed at the exact moment that our strategy tells us to do so. To do this, our bot needs to communicate with the exchange via API. To automate a strategy, we will need three things:

- Monitor the price in real-time (API)
- All signals of our strategy (when to open and close a trade) plus the money and leverage of the trade (hard-coded)
- Send these signals to the exchange to execute the trade (API)

In case this text sounds hard to understand, inside the project, there is a .jpeg that contains a flowchart of how each part of the program communicates with each other.

## DISCLAIMER
Everything in this project has been made for academic purposes only. This is not financial advice, and you should be responsible for what you do with your own money. I will not be responsible for any losses. As you will see in the project, the Big Candle strategy is not profitable and is still a work in progress so I sugest to code your own strategy.
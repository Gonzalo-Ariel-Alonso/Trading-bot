# Trading strategy test

The main objetive of this proyect is to create and teset trading strategy, for this porpose we need four thing: a data base with price history, a program
who test a given trading strategy and a programr that comunicate with an exchange to execute the strategy.
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

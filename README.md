# ETF Invest Simulation

[![Python Powered](https://www.python.org/static/community_logos/python-powered-w-100x40.png)](https://www.python.org)

ETF Invest Simulation is a Python-based application for performing investment ratings on ETFs. The application has a set of rating methods which can be used or furthered developed by the user.

## Installation

Install [Python 3.5.4](https://www.python.org/downloads/release/python-354/) and confirm the successful installation by running (in cmd):
```
py -3.5 --version
>>> Python 3.5.4
```

Open cmd, go to the project folder, and install the libraries by running:
```
py -3.5 -m pip install -r requirements.txt
```

## How to Run the Program

All commands described below can be ran from cmd. Be aware that the first time the program is running, it has to update the database, since it is too large (170MB+) for Github.

### Running main.py
```
py -3.5 main.py <ticker> <method> <update>
```

**Parameters**

```<ticker>``` must be stated as a parameter since it defines which ETF to perform rating on.
 
```<method>``` must be stated as a parameter since it defines which rating method use. Available methods: 'trade_days', 'weekends', 'average_more'.

```<update>``` is optional and updates the database with newest data entries.

**Examples**
```
py -3.5 main.py EO-NORDS trade_days upd
py -3.5 main.py EO-NORDN weekends
py -3.5 main.py EO-NORDD average_more
```

## Run Result Examples

**X-axis** is defined between 1 and 31 to represent all potential days in the month.

**Y-axis** defines how many ETF-stocks you are able to purchase for 500/month in average, for each specific day. 

**Blue line** shows the average line for all values.

### EO-NORDN : Trade Days Rating

Rates are only based on that the specific date is a trade day. If the date is a weekend or vacation (not a trade day), then the results will not be included.

```
py -3.5 main.py EO-NORDN trade_days
```

![Trade_days rating for EO-NORDN](https://github.com/FredrikBakken/etf-invest-simulation/blob/master/data/results/trade_days/EO_NORDN.png)

Results shows that you get the most ETF-stocks in total by investing on the 15th day of the month.

### EO-NORDN : Weekends Rating

Rates are based on that the specific date is a trade day. If the date is a weekend or vacation (not a trade day), then the results will use the values for the next trading day. 

```
py -3.5 main.py EO-NORDN weekends
```

![Weekends rating for EO-NORDN](https://github.com/FredrikBakken/etf-invest-simulation/blob/master/data/results/weekends/EO_NORDN.png)

Results shows that you get the most ETF-stocks in total by investing on the 16th day of the month and the next available trading day if the 16th is a weekend/vacation day.
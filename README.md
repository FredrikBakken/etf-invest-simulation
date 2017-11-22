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

All commands described below can be ran from cmd.

### Running main.py
```
py -3.5 main.py <ticker> <method> <update>
```

**Parameters**

```<ticker>``` must be stated as a parameter since it defines which ETF to perform rating on.
 
```<method>``` must be stated as a parameter since it defines which rating method use. Available methods: 'trade_days', 'weekends'.

```<update>``` is optional and updates the database with newest data entries.

**Examples**
```
py -3.5 main.py EO-NORDS trade_days
py -3.5 main.py EO-NORDN weekends
py -3.5 main.py EO-NORDD weekends upd
```

## Results

### EO-NORDN : Trade Days Rating

```
py -3.5 main.py EO-NORDN trade_days
```

![Trade_days rating for EO-NORDN](https://github.com/FredrikBakken/etf-invest-simulation/blob/master/data/results/trade_days/EO_NORDN.png)

### EO-NORDN : Weekends Rating

```
py -3.5 main.py EO-NORDN weekends
```

![Weekends rating for EO-NORDN](https://github.com/FredrikBakken/etf-invest-simulation/blob/master/data/results/weekends/EO_NORDN.png)
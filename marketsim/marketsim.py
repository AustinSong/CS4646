"""MC2-P1: Market simulator.  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		   	  			    		  		  		    	 		 		   		 		  
Atlanta, Georgia 30332  		   	  			    		  		  		    	 		 		   		 		  
All Rights Reserved  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
Template code for CS 4646/7646  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
Georgia Tech asserts copyright ownership of this template and all derivative  		   	  			    		  		  		    	 		 		   		 		  
works, including solutions to the projects assigned in this course. Students  		   	  			    		  		  		    	 		 		   		 		  
and other users of this template code are advised not to share it with others  		   	  			    		  		  		    	 		 		   		 		  
or to make it available on publicly viewable websites including repositories  		   	  			    		  		  		    	 		 		   		 		  
such as github and gitlab.  This copyright statement should not be removed  		   	  			    		  		  		    	 		 		   		 		  
or edited.  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
We do grant permission to share solutions privately with non-students such  		   	  			    		  		  		    	 		 		   		 		  
as potential employers. However, sharing with other current or future  		   	  			    		  		  		    	 		 		   		 		  
students of CS 7646 is prohibited and subject to being investigated as a  		   	  			    		  		  		    	 		 		   		 		  
GT honor code violation.  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
-----do not edit anything above this line---  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
Student Name: Pranshav Thakkar (replace with your name)
GT User ID: pthakkar7 (replace with your User ID)
GT ID: 903079725 (replace with your GT ID)
"""  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
import pandas as pd  		   	  			    		  		  		    	 		 		   		 		  
import numpy as np  		   	  			    		  		  		    	 		 		   		 		  
import datetime as dt  		   	  			    		  		  		    	 		 		   		 		  
import os  		   	  			    		  		  		    	 		 		   		 		  
from util import get_data, plot_data  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
def compute_portvals(orders_file = "./orders/orders.csv", start_val = 1000000, commission=9.95, impact=0.005):  		   	  			    		  		  		    	 		 		   		 		  
    # this is the function the autograder will call to test your code  		   	  			    		  		  		    	 		 		   		 		  
    # NOTE: orders_file may be a string, or it may be a file object. Your  		   	  			    		  		  		    	 		 		   		 		  
    # code should work correctly with either input  		   	  			    		  		  		    	 		 		   		 		  
    # TODO: Your code here  		   	  			    		  		  		    	 		 		   		 		  
    orders = pd.read_csv(orders_file)
    orders.sort_values(by=['Date'])
    start_date = orders.iloc[0,0]
    end_date = orders.iloc[-1, 0]
    dates = pd.date_range(start_date, end_date)

    symbols = []
    for sym in orders['Symbol']:
        if sym not in symbols:
            symbols.append(sym)

    prices = get_data(symbols, dates)
    prices = prices[symbols]
    prices['CASH'] = 1.0
    trades = prices.copy()
    trades[:] = 0

    for index, row in orders.iterrows():
        date = row['Date']
        sym = row['Symbol']
        ord = row['Order']
        shares = row['Shares']
        if ord == "BUY":
            trades[sym][date] += shares
            trades['CASH'][date] -= (prices[sym][date] * shares * (1 + impact)) + commission
        elif ord == "SELL":
            trades[sym][date] -= shares
            trades['CASH'][date] += (prices[sym][date] * shares * (1 - impact)) - commission

    holdings = trades.copy()
    holdings['CASH'][start_date] += start_val
    holdings = holdings.cumsum()

    value = prices * holdings

    portval = value.sum(axis=1)

    return portval

def author():
    return 'pthakkar7'
  		   	  			    		  		  		    	 		 		   		 		  
def test_code():  		   	  			    		  		  		    	 		 		   		 		  
    # this is a helper function you can use to test your code  		   	  			    		  		  		    	 		 		   		 		  
    # note that during autograding his function will not be called.  		   	  			    		  		  		    	 		 		   		 		  
    # Define input parameters  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
    of = "./orders/orders-09.csv"
    sv = 1000000  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
    # Process orders  		   	  			    		  		  		    	 		 		   		 		  
    portvals = compute_portvals(orders_file = of, start_val = sv)  		   	  			    		  		  		    	 		 		   		 		  
    if isinstance(portvals, pd.DataFrame):  		   	  			    		  		  		    	 		 		   		 		  
        portvals = portvals[portvals.columns[0]] # just get the first column  		   	  			    		  		  		    	 		 		   		 		  
    else:  		   	  			    		  		  		    	 		 		   		 		  
        "warning, code did not return a DataFrame"  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
    # Get portfolio stats  		   	  			    		  		  		    	 		 		   		 		  
    # Here we just fake the data. you should use your code from previous assignments.  		   	  			    		  		  		    	 		 		   		 		  
    start_date = dt.datetime(2008,1,1)  		   	  			    		  		  		    	 		 		   		 		  
    end_date = dt.datetime(2008,6,1)  		   	  			    		  		  		    	 		 		   		 		  
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [0.2,0.01,0.02,1.5]  		   	  			    		  		  		    	 		 		   		 		  
    cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = [0.2,0.01,0.02,1.5]  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
    # Compare portfolio against $SPX  		   	  			    		  		  		    	 		 		   		 		  
    print "Date Range: {} to {}".format(start_date, end_date)  		   	  			    		  		  		    	 		 		   		 		  
    print  		   	  			    		  		  		    	 		 		   		 		  
    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)  		   	  			    		  		  		    	 		 		   		 		  
    print "Sharpe Ratio of SPY : {}".format(sharpe_ratio_SPY)  		   	  			    		  		  		    	 		 		   		 		  
    print  		   	  			    		  		  		    	 		 		   		 		  
    print "Cumulative Return of Fund: {}".format(cum_ret)  		   	  			    		  		  		    	 		 		   		 		  
    print "Cumulative Return of SPY : {}".format(cum_ret_SPY)  		   	  			    		  		  		    	 		 		   		 		  
    print  		   	  			    		  		  		    	 		 		   		 		  
    print "Standard Deviation of Fund: {}".format(std_daily_ret)  		   	  			    		  		  		    	 		 		   		 		  
    print "Standard Deviation of SPY : {}".format(std_daily_ret_SPY)  		   	  			    		  		  		    	 		 		   		 		  
    print  		   	  			    		  		  		    	 		 		   		 		  
    print "Average Daily Return of Fund: {}".format(avg_daily_ret)  		   	  			    		  		  		    	 		 		   		 		  
    print "Average Daily Return of SPY : {}".format(avg_daily_ret_SPY)  		   	  			    		  		  		    	 		 		   		 		  
    print  		   	  			    		  		  		    	 		 		   		 		  
    print "Final Portfolio Value: {}".format(portvals[-1])  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		   	  			    		  		  		    	 		 		   		 		  
    test_code()  		   	  			    		  		  		    	 		 		   		 		  

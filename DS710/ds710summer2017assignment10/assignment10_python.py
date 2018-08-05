# Author: Brian Pankau
# Class: UWLAX DS 710
# Assignment: 10 Python

import time
import pandas as pd
import numpy as np
from pandas import Series, DataFrame

#--- FUNCTIONS --------------------------------------------------------------

# Problem 1(a)). Unionized workers.
# create a function to determine the wage of union workers using control flow
# input:  a data frame of the cps.csv file
# output: the mean wage for all union workers, zero if there are no union workers
def mean_union_wage_control_flow(df):
  union_wage_sum = 0
  r = 0
  w = 0
  while (r < df.shape[0]):
    if (df.loc[r, "union"] == "Union"):
      union_wage_sum = union_wage_sum + df.loc[r, "wage"]
      w = w + 1
    r = r + 1
    
  # return the mean wage of all union workers
  if (w == 0):
    return (0)
  else:
    return(union_wage_sum / w)

    
# Problem 1(b). More unionized workers.
# input:  a row of a cps data frame
# output: returns the worker's hourly wage if the worker is unionized, or returns 0 if a worker is not unionized
def union_wage(a_df_row):
  if (a_df_row.union == "Union"):
    return a_df_row.wage
  else:
    return 0

    
# Problem 1(c). Selecting and analyzing unionized workers.
# input:  a data frame of the cps.csv file
# output: the mean wage for all union workers, zero if there are no union workers
def mean_union_wage(df):
  # find wages for all union workers and return the mean for the wages
  union_wage_list = []
  union_wage_list = df.loc[df.union == "Union", "wage"]
  
  # return the mean wage of all union workers
  if (len(union_wage_list) == 0):
    return(0)
  else:
    return(union_wage_list.mean())


#--- MAIN -------------------------------------------------------------------

# read the file into memory and store the contents as a frame
cps_df = pd.read_csv("C:/Temp10/cps.csv")

# Problem 1(a)). Unionized workers.
# Create a pandas data frame to hold the CPS data. 
# Write a function that computes the average hourly wage of a 
# unionized worker by using control flow to iterate through each row 
# of the data frame.
# output mean wage for union workers
print("Mean wage for union workers using control flow  = %3.3f" % (mean_union_wage_control_flow(cps_df)))


# Problem 1(b). More unionized workers.
# Write a function that takes a row of a data frame as input. 
# Your function should return 0 if a worker is not unionized, and the worker's hourly wage if the worker is unionized. 
# Apply this function to your data frame, then use the resulting series to compute the average hourly wage of a unionized worker.
wage_list = []
for n in range(0,cps_df.shape[0]):
  wage_list.append(union_wage(cps_df.loc[n]))
wage_list_series = Series(wage_list)
print("Mean wage for union workers using row selection = %3.3f" % (wage_list_series[wage_list_series > 0].mean()))


# Problem 1(c). Selecting and analyzing unionized workers.
# Write code that selects the unionized workers, then computes the average hourly wage of the resulting subset.
print("Mean wage for union workers using indexing      = %3.3f" % (mean_union_wage(cps_df)))


# Problem 1(d). Timing.
# Use the %time or %timeit magic commands to compare your code from 1(a), 1(b), and 1(c). 
# Create a markdown cell which explains the results of your comparison, 
# including which is fastest and which is slowest. 
# Can you explain what makes the fastest code fastest?

print("1a time: ")
%timeit by_1_a = mean_union_wage_control_flow(cps_df)

print("1b time: ")
%timeit by_1_b = wage_list_series[wage_list_series > 0].mean()

print("1c time: ")
%timeit by_1_c = mean_union_wage(cps_df)

"""
RESULTS:
1a time: 
10000 loops, best of 3: 176 µs per loop
1b time: 
1000 loops, best of 3: 589 µs per loop
1c time: 
1000 loops, best of 3: 596 µs per loop


# Results Explaination:
The method used in problem 1a had the shortest time.
The method used in problem 1b had the next shortest time.
The method used in problem 1c had the longest time.

In the method used in problem 1a, the fastest method, we are itterating through the data frame using a while loop 
in which each row is tested against the "Union" condition, upon true the row's wages are added to the total wage sum.

In method 1b, we are generating a list of wages to average by appending the list, which is expensive in time.

Likewise, in the method used in problem 1c, we are creating a subset of wages from the entire data frame by applying a 
filter against each row is also expensive in time.


#!/usr/bin/env python3
"""
Program name: self_isolation_dates.py
Student number: 

Given a string and a duration in days, check if the string contains a valid date and compute date when isolation ends by adding the duration specified.
"""
def DaysMonth(m):
  """Function to get days for corresponding month no 
  
  Paramters: 
  m (int) : month 
  
  return:
   days(int): number days in month """
  days_30_months = [2,4,6,9,11] 
  #  months which has 30 days
  days_31_months = [1, 3, 5, 7, 8, 10, 12]  
  #  months which has 31 days
  if m==2:  
    #  if is feb then return 28 days
    return 28
  elif m in days_30_months: 
    #  if it is 30 days month, return 30
    return 30
  elif m in days_31_months:
    #  if it is 31 days month, return 31
    return 31

def self_isolation_end_date(date, n_days):
  lst = []
  if "-" in date: 
    #  if there is - in date, then split by - 
    lst = date.split("-")
  elif "/" in date:
    #  if there is / in date, then split by / 
    lst = date.split("/")  

  for i in lst:  
    # checking that if no digit, then return error  
    if not i.isdigit():
      return (0,0,0)  
  if len(lst)>3: 
    # if list having more entries than format, then consider it error  
    return (0,0,0)
  if not len(lst[2]) in [2,4]:  
    # if year lenght is not correct, then consider it error 
    return (0,0,0)
  # Getting days, month, year from list
  days, month, year =int(lst[0]) , int(lst[1]), int(lst[2])
  if (days<0 or days>31) or (month<1 or month>12) :  # Checks for days and months
    return (0,0,0)
  days_in_month= DaysMonth(month) # Getting days for a month 
  for i in range(n_days):
    days+=1
    if days>days_in_month: # boundry condition checking, if days are more than current days of month, then reset it to 1 and increase month
      days=1
      if month>12:  # If months are more than 12, then reset it to 1 and increase year  
        month = 1 
        year +=1
      else:
        month+=1
  return (days, month, year)
def main():
    ######################################################################################################
    # WARNING: An error will be raised by this code until you define the function self_isolation_end_date 
    ######################################################################################################
    
    # Example cases (dates, duration assumed to lways be 10 days)
    correct_dates = ["28/02/2022", "28/2/2022", "28-02-2022", "28/2/22"]
    incorrect_dates = ["128/02/2022", "28/0/2022", "28-02-022", "28/2/22001", "2a/1/19", "1/1/2022/2"]
    
    # Check test cases (i.e., compute end of isolation for these dates)
    for date in correct_dates : 
        result = self_isolation_end_date (date, 10)
        if (result [0] == 0 or result [1] == 0 or result [2] == 0 ) :
            print("Incorrect date")
        else :
            print(f'End isolation in {result [0]} of month {result [1]} of {result[2]}')       
    for date in incorrect_dates : 
        result = self_isolation_end_date (date, 10)
        if (result [0] == 0 or result [1] == 0 or result [2] == 0 ) :
            print("Incorrect date")
        else :
            print(f'End isolation in {result [0]} of month {result [1]} of {result[2]}')   

    
if __name__ == "__main__":
    main()
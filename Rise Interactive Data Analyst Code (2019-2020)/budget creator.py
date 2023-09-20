# MARCOS FROM 2023: this was one of my first scripts created in a professional setting. I'd correct
# the numerous inefficiencies but I'd like to keep it reflective of my journey in Python so far.

# This modified version of the creator uses static budgets and a time period range

import time

print("Hello! The purpouse of this script is to generate a file containing a massive number of possible different budget allocations for different channels. \n")

#time.sleep(3)

print("For those familiar with Python, this script uses the pandas and numpy modules, so please install it if you don't have it already. You will know if you don't have pandas because you will receive an error message as soon as these introductory texts finish. \n")

#time.sleep(3)

print("The end result of this script is a csv which gets saved in the same folder the file for this script is located in. \n")

#time.sleep(3)

import pandas as pd
import numpy as np
import sys
import itertools
from itertools import repeat
import datetime
import math

all_months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

def basic():

    run_again = True

    while run_again == True:

        budget = int(input("Let's get started. What is your budget? "))

        number_of_channels = int(input("How many regions are you predicting for? "))

        # defining month and year to project for
        current_month = input("What is the month you're projecting for? Please enter the month in it's full name, with first letter capitalized. ")

        if number_of_channels <= 3:
            channel_step = 1
        #elif number_of_channels <= 4:
        #    print("Slightly lowering precision of distribution due to large number of channels")
        #    channel_step = 4
        elif number_of_channels <= 6:
            print("Moderately lowering precision of distribution due to large number of channels")
            channel_step = 5
        elif number_of_channels <= 8:
            print("Dramatically lowering precision of distribution due to large number of channels")
            channel_step = 10
        else:
            sys.exit("Please enter a lower number of channels, as this will likely cause a memory error")

        all_channels_names = []

        for i in range(number_of_channels):
            channel_name = input(("What is the name of channel", i+1, "? "))
            all_channels_names.append(channel_name)

        all_channels_numbers = []

        for z in (all_channels_names):
            z = list([x / 100.0 for x in range(0, 101, channel_step)])
            all_channels_numbers.append(z)
            
        # permuting all viable ratio combinations between given ratios for PLA/PPC/Social    
        viables = []
        for r in itertools.product(*all_channels_numbers):
            if math.fsum(r) == 1:
                viables.append(r)
            else:
                pass
            
        # Selecting current date (for file naming)
        now = datetime.datetime.now().strftime("%Y-%m-%d")



        print("Please wait while the csv gets created, this may take a few seconds.")

        # Make sure to change this as needed, set default to 2020 for simplicity
        current_year = 2020

        # defining amount of days in a given month
        number_of_days = 0
        if current_month.lower() in ['january', 'march', 'may', 'july', 'august', 'october', 'december']:
            number_of_days = 31
        elif current_month.lower() in ['april', 'june', 'september', 'november']:
            number_of_days = 30
        elif current_month.lower() == 'february' and current_year % 4 == 0:
            number_of_days = 29
        elif current_month.lower() == 'february' and current_year % 4 != 0:
            number_of_days = 28
        else:
            sys.exit("Please enter the month in it's full name, with first letter capitalized")

        # shrinking month down to a daily budget scale
        daily_budgets = [x/number_of_days for x in budget]

        # Creating all possible permutations between daily budgets and viable ratios
        full_combos = []

        for r in itertools.product(daily_budgets, viables):
            full_combos.append([r[0], r[1]])
            
        budgets_final = []
        channel_budgets = [[] for _ in range(number_of_channels)]

        for i in range(len(full_combos)):
            budgets_final.append(full_combos[i][0])
            for y in range(len(all_channels_names)):
                z = full_combos[i][1][y]
                channel_budgets[int(y)].append(z)

                
        # Creating dataframe and assigning values to columns

        columns=['Month', 'Daily Budget']
        df = pd.DataFrame(0, index = np.arange(len(budgets_final)), columns=columns)
        df['Month'] = current_month
        df['Daily Budget'] = budgets_final
        for i in all_channels_names:
            # constantly adding the same value, need to access all values in channel_budgets
            df[i + ' Share of Cost'] = channel_budgets[all_channels_names.index(i)]
            df[i + ' Budget'] = df[i + ' Share of Cost'] * df['Daily Budget']
        #df.head()
        #df['a Share of Cost'].value_counts()
        df.to_csv((r'Model_Ready_data_' + now + current_month +'.csv'))

        print("\nSuccess!")

        yes_no = input("\nWould you like to run this again? Please type yes or no").lower()

        if yes_no == 'yes':
            pass
        if yes_no != 'yes':
            run_again = False


basic()

time.sleep(1)

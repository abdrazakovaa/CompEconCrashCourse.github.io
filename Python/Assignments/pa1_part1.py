'''
Programming Assignment 1
'''
#%%
import random

TEST_SEED = 20170217

def count_ever_infected(city):
    '''
    Given a city, return the number of infected plus the number of recovered people in that city.

    Arguments:
        city (list of str): city of individuals and their current infection status

    Returns:
        (int): number of infected + number of recovered in the city
    '''
    count = 0

    for person in city:
        if person[0] in ['I', 'R']: # if ((person[0] == 'I') or (person[0] == 'R'))
            count += 1

    return count

# %%
count_ever_infected(['I0', 'I0', 'I2', 'S', 'R']) # Should be 4

# %%

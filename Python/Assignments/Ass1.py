#%%
def count_ever_infected(city):
    # Count the number of people who have ever been infected
    inf = 0
    ind = 'I'
    # for each element in the city
    for i in city:
        # my mistake was to look in city.[i]
        if ind in ['I', 'R']:
            # print(i, inf) 
            inf += 1
    return inf 

# Adam's solution

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

#%%
# Task # 1
city1 = ['I0', 'I0', 'I2', 'S', 'R']
city2 = ['S', 'S', 'S', 'S']
city3 = ['I1', 'R', 'R', 'R']

lst = [city1, city2, city3]

for i, city in enumerate(lst):
    # print(i,city)
    count = count_ever_infected(city)
    print(f'For a city number {i+1} count of infected people: {count_ever_infected(city)}')
    
#%%

def has_an_infected_neighbor(city,pid):
    """
    compute the positions of the specified person's left and right
    neighbors in the city, if they exist, and 
    determine whether either one is in an infected state.
    """
    ind = 'I'
    lefn = pid - 1
    rightn = pid + 1
    # print(pid-1, pid, pid+1)
    if lefn < 0:
        if ind in city[pid+1]:
            return True
        else:
            return False 
        # return city[1][0] = 'I
    elif rightn > len(city)-1:
        if ind in city[pid-1]:
            return True
        else:
            return False 
    elif ind in city[pid-1] or ind in city[pid+1]:
        # print(city[pid-1],city[pid+1])
        return True
    else:
        return False
    

#%%
# Task # 2

print(city3)
pid = 1
has_an_infected_neighbor(city3, 1)

#%%
import random
import copy

#%%
# Task 3
def gets_infected_at_position(city,pid,rate):
    """
    determine whether the person at the specified position in the city
    becomes infected, based on the specified infection rate.
    """
    ind = 'I'
    if has_an_infected_neighbor(city,pid) == True:
        if random.random() < rate:
            return True
        else:
            return False
    else:
        return False
    # I could just write instead of else: return False
    # return False

#%%
test_seed = 20170217
random.seed(test_seed)

print(city3,city3[0][1])
# print(has_an_infected_neighbor(city3, 1))
gets_infected_at_position(city3, 1, 0.5)

#%%
# Task 4
def advance_person_at_position(city, pid, rate, c):
    """
    advance the state of the person at the specified position in the city
    by one time step, based on the specified infection rate and recovery rate.
    """
    cityv = copy.deepcopy(city)
    ind = 'I'
    if cityv[pid] == 'S':
        if gets_infected_at_position(cityv,pid, rate) == True:
            if random.random() < rate:
                cityv[pid] = 'I0'
    elif ind in cityv[pid]:
        # print(city[pid])
        x = int(cityv[pid][1])
        if x+1 < c:
            cityv[pid] = 'I' + str(x+1)
        else:
            cityv[pid] = 'R'
    return cityv[pid]

#%%
random.seed(test_seed)
advance_person_at_position(['I0', 'I1', 'R'], 0, 0.3, 2)
advance_person_at_position(['I0', 'I1', 'R'], 1, 0.3, 2)
advance_person_at_position(['I0', 'I1', 'R'], 2, 0.3, 2)

#%% 
#%%
# Task 5

def simulate_one_day(city, rate, c):
    """
    simulate one time step of the spread of infection in the city,
    based on the specified infection rate and recovery rate.
    """
    cityv = copy.deepcopy(city)
    # create an empty list instead for shorter cities
    for i in range(len(city)):
#         print(i)
        cityv[i] = advance_person_at_position(city, i, rate, c)
    return cityv

#%%
random.seed(test_seed)

simulate_one_day(['S', 'I0', 'S'], 0.3, 2)

# advance_person_at_position(['S', 'I0', 'S'], 2, 0.3, 2)

#%%
# Task 6

def run_simulation(city, seed, max_num_days, rate, c):
    """
    run a full simulation of the spread of infection in the city
    over the specified number of days, based on the specified infection rate and recovery rate.
    """
    test_seed = seed
    random.seed(test_seed)
    time = 0
    
    for j in range(max_num_days):
        city_tomo = simulate_one_day(city, rate, c)
        time += 1
        
        if city == city_tomo:
            print(f'City has reached a steady state at day {time}')
            break
        else:
            city = city_tomo
            print(f'Day number: {time}')
            print(f'State of the city: {city}')

    return (city, time)

#%%
run_simulation(['S', 'S', 'I1'], 20170217, 10, 0.4, 3)


#%%
def calc_avg_num_newly_infected(city, seed, max_num_days, rate, c, num_trials):
    '''
    computes the average number of newly infected people over num_trials trials for a given city, 
    infection rate, and number of days contagious.
    '''
    for t in range(num_trials):
        seed += 1
        cityv, timev = run_simulation(city, seed, max_num_days, rate, c)


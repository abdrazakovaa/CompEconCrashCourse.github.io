'''
Programming Assignment 1
'''
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
        if person[0] in ['I', 'R']:
            count += 1

    return count

def has_an_infected_neighbor(city, position):
    '''
    Determine whether a susceptible person at a given position in a city has at least one neighbor who is infected.

    Arguments:
        city (list of str): city of individuals and their current infection status
        position (int): position of the susceptible person to check

    Returns:
        (bool): True if the susceptible person has at least one neighbor who is infected; False otherwise
    '''
    if len(city) == 1:
        # If there's only one person in the city, they have no neighbors
        return False

    if position == 0:
        # At position 0, only neighbor is to the right
        return city[1][0] == 'I'

    if position == (len(city) - 1):
        # At position (len(city) - 1), only neighbor is to the left
        return city[-2][0] == 'I'

    # Interior positions
    return (city[position - 1][0] == 'I') or (city[position + 1][0] == 'I')

def gets_infected_at_position(city, position, r):
    '''
    Determine whether someone at a given position in a city will become infected on the next day of the simulation.

    Arguments:
        city (list of str): city of individuals and their current infection status
        position (int): position of the susceptible person to check
        r (float): infection rate (in [0, 1])

    Returns:
        (bool): True if the person becomes infected on the next day of the simulation; False otherwise
    '''
    if has_an_infected_neighbor(city, position):
        # If the person has an infected neighbor
        if random.random() < r:
            # Become infected with probability r
            return True

    # Return False otherwise
    return False

def advance_person_at_position(city, position, r, c):
    '''
    Determine the state of someone at a given position in a city for the next day of the simulation.

    Arguments:
        city (list of str): city of individuals and their current infection status
        position (int): position of the person to advance
        r (float): infection rate (in [0, 1])
        c (int): the number of days (>= 1) the infection is contagious

    Returns:
        (str): state of the person in the next day
    '''
    state_today = city[position]
    if state_today == 'S':
        # If susceptible
        if gets_infected_at_position(city, position, r):
            # If gets infected
            return 'I0'
        # If doesn't get infected
        return 'S'

    if state_today[0] == 'I':
        # If currently infected
        days_infected = int(state_today[1:])
        if days_infected + 1 < c:
            # If still infected tomorrow
            return 'I' + str(days_infected + 1)
        # If recovered tomorrow
        return 'R'

    # If recovered
    return 'R'

def simulate_one_day(city, r, c):
    '''
    Model one day in a simulation.

    Arguments:
        city (list of str): city of individuals and their current infection status
        r (float): infection rate (in [0, 1])
        c (int): the number of days (>= 1) the infection is contagious
    '''
    city_tomorrow = []

    for position in range(len(city)):
        city_tomorrow.append(advance_person_at_position(city, position, r, c))

    return city_tomorrow

def run_simulation(city, seed, max_num_days, r, c):
    '''
    Simulate the infected city over time.

    Arguments:
        city (list of str): city of individuals and their initial infection status
        r (float): infection rate (in [0, 1])
        c (int): the number of days (>= 1) the infection is contagious

    Returns:
        (tuple of list of str, int): the final state of the city and the number days simulated
    '''
    random.seed(seed)
    iters = 0
    for _ in range(max_num_days):
        # Update iters
        iters += 1

        # Simulate one day
        city_tomorrow = simulate_one_day(city, r, c)

        if city == city_tomorrow:
            # If city doesn't change between today and tomorrow, stop
            break

        # If city does change, update city to become city_tomorrow
        city = city_tomorrow

    return (city, iters)

def calc_avg_num_newly_infected(city, seed, max_num_days, r, c, num_trials):
    '''
    Compute the average number of newly infected people over a specified number of trials.

    Arguments:
        city (list of str): city of individuals and their initial infection status
        r (float): infection rate (in [0, 1])
        c (int): the number of days (>= 1) the infection is contagious
        num_trials (int): the number of trials (>= 1) to run

    Returns:
        (float): the average number of newly infected people over the trials
    '''
    # How many people started infected or recovered
    baseline_infected = count_ever_infected(city)

    # List where we will store how many newly infected are in each city
    newly_infected = []
    for trial_n in range(num_trials):
        # Run simulation n
        city_n, iters_n = run_simulation(city, seed + trial_n, max_num_days, r, c)

        # Count number of infected or recovered in city n
        infected_n = count_ever_infected(city_n)

        # Store the number of newly infected
        newly_infected.append(infected_n - baseline_infected)

    # Return the average number of newly infected people over the trials
    return sum(newly_infected) / len(newly_infected)

# Test:
# calc_avg_num_newly_infected(['S', 'S', 'I1', 'I1', 'I1', 'I1', 'I1', 'S'], 20170217, 2, 0.8, 2, 1)
# Expected result:
# 3.0

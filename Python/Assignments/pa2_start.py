'''
Programming Assignment 2
'''
#%%
import copy 
#%%
M =  [
     ['M', 'M', 'O', 'M', 'M'],
     ['O', 'B', 'B', 'B', 'O'],
     ['M', 'M', 'M', 'M', 'B'],
     ['B', 'B', 'B', 'O', 'B'],
     ['B', 'M', 'M', 'M', 'O']
 ]


#%%
def find_opens(grid):
    '''
    Take an occupancy grid and return a list of open locations in that grid.

    Arguments:
        grid (list of lists of str): occupancy grid

    Returns:
        (list of tuples): open locations
    '''
    ## Unpack parameters ##
    N = len(grid)

    ## Values to compute ##
    open_locs = []

    for i in range(N):
        ## Iterate over rows ##
        for j in range(N):
            ## Iterate over columns ##
            if grid[i][j] == 'O':
                # If location is open
                open_locs.append((i, j))

    return open_locs

def calc_min_dist(grid, i, j, opens):
    # calculate distance to each open location
    dist = []
    for n_locs, open_locs in enumerate(opens):
        man = man_dist(i, j, open_locs[0], open_locs[1])
        dist.append(man)
    return dist


def find_mismatch(grid0, grid1):
    '''
    Take two occupancy grids and return the first location where they differ, or None if the grids are the same.

    Arguments:
        grid0 (list of lists of str): occupancy grid
        grid1 (list of lists of str): occupancy grid

    Returns:
        (tuple or None): tuple of the first location where they differ, or None if the grids are the same
    '''
    ## Unpack parameters ##
    N = len(grid0)

    for i in range(N):
        ## Iterate over rows ##
        for j in range(N):
            ## Iterate over columns ##
            if grid0[i][j] != grid1[i][j]:
                # If locations don't match
                return (i, j)

    return None

#%%
man_dist = lambda a, b, c, d: abs(a - c) + abs(b - d)



#%% 
def find_neighbors(grid,radius, i, j):
    neighbors = []
    rows = len(grid)
    cols = len(grid[0])
    
    for x in range(max(0,i-radius), min(i+radius+1,rows)):
        for y in range(max(0,j-radius), min(j+radius+1,cols)):
            if x == i and y == j:
                continue  # Skip the current cell
            if 0 <= x < rows and 0 <= y < cols:
                neighbors.append((x, y))
    
    return neighbors

def count_occupied(grid, neighbors):
    count = 0 # count the current location
    # print(neighbors)
    for neighbor in neighbors:
        # print(neighbor)
        if grid[neighbor[0]][neighbor[1]] != 'O':
            count += 1
    return count

def count_similar(grid, i, j, neighbors):
    count = 0 # count the current location
    for neighbor in neighbors:
        # print(f'Neighbor: {neighbor}')
        # print(grid[neighbor[0]][neighbor[1]])
        # print(grid[i][j])
        if grid[neighbor[0]][neighbor[1]] == grid[i][j]:
            count += 1
    return count

def is_satisfied(grid,R,i,j,simil_threshold,occup_threshold):
    N = len(grid)
    # first, find neighbors
    neighbors = find_neighbors(grid, R, i, j)
    # second, find the number of occupied neighbors, H
    num_occupied = count_occupied(grid, neighbors)
    # third, find the number of similar neighbors, S
    num_similar = count_similar(grid, i, j, neighbors)
    # find T: total number of locations around
    T = len(neighbors)+1
    # similarity score = S/H
    # occupancy score = H/T
    
    print(f'Neighbors {neighbors}')
    print(f'Number of neighbors: {T}')
    print(f'Number of occupied: {num_occupied}')
    print(f'Number of similar: {num_similar}')

    occup_score = num_occupied/T
    simil_score = num_similar/num_occupied

    print(f'occup_score is {occup_score}, simil_score is {simil_score}')
    return [True if num_occupied/T >= occup_threshold and num_similar/num_occupied >= simil_threshold else False]

#%%
def find_satisfied_opens(grid, R, opens, i, j, simil_threshold, occup_threshold):
    N = len(grid)
    satisfied_opens = []
    for open_loc in opens:
        print(open_loc)
        # print(is_satisfied(grid, R, open_loc[0], open_loc[1], simil_threshold, occup_threshold))
        print(is_satisfied(grid, R, open_loc[0], open_loc[1], simil_threshold, occup_threshold)[0])
        if is_satisfied(grid, R, open_loc[0], open_loc[1], simil_threshold, occup_threshold)[0]:
            satisfied_opens.append(open_loc)
    return satisfied_opens

#%%
print(find_opens(M))
print(find_mismatch(M, M))
print(M)

#%%
'''
AA: I dont think I can do this
To recap: a visit to a particular home will trigger a relocation in a given step if, at the time of the visit:

    the home is occupied;
    the homeowner is unsatisfied with their location; and
    there is an open location that meets the satisfaction criteria, and there is more than one choice available.

Stopping conditions: Your simulation should stop when:

    it has executed a specified maximum number of steps or
    no relocations occur in a step.

Sample simulation: Step 1

'''
#%%
def is_moving(grid,R, simil_threshold,occup_threshold):
    '''
    See where the person is moving.
    Return should be equal to a moving location tuple.
    If empty, person is not moving anywhere.
    '''
    N = len(grid)

    reallocations = 0

    for i in range(N):
        ## Iterate over rows ##
        for j in range(N):
            ## Iterate over columns ##
            if grid[i][j] == 'O':
                # If location is open
                continue
            
            # Goal is to get people how people think about their functions
            opens = find_opens(grid) # cannot be called inside the function

            # Find the neighbors of the current location
            neighbors = find_neighbors(grid, R, i, j)

            # Find the number of neighbors that are occupied
            num_occupied = count_occupied(grid, neighbors) 

            # Find the number of neighbors that are similar
            num_similar = count_similar(grid, i, j, neighbors) 

            T = len(neighbors) + 1 ## Total number of locations around

            if num_occupied/T >= occup_threshold and num_similar/num_occupied >= simil_threshold:
                continue

            # Find the open locations that meet the satisfaction criteria
            open_locs = find_satisfied_opens(grid, R, opens, i, j, simil_threshold, occup_threshold)

            if len(open_locs) < 2:
                print(f'HH number ({i},({j}) is not satisfied but cannot move due to number of locations < 1')
                # If there are no open locations that meet the satisfaction criteria
                continue
            else:
                # calculate distance to each open location
                reallocations += 1
                dist = calc_min_dist(grid, i, j, open_locs)
                # find a home that minimizes distance
                min_dist = min(dist)
                # best location to which this hh wants to move
                bsf = open_locs[dist.index(min_dist)] # best so far
                print(f'Place to move, minimum location: {bsf}')
                # update a list of available space
                opens.remove(bsf) 
                # opens.append(bsf) # append the current location

                # Update the grid
                grid[bsf[0]][bsf[1]] = grid[i][j]
                grid[i][j] = 'O'

    return (grid, reallocations)

#%%
def do_simulation(grid, R, simil_threshold, occup_threshold, max_steps):
    '''
    Simulate the relocation of homeowners in a city.

    Arguments:
        grid (list of lists of str): occupancy grid
        R (int): maximum number of relocations in a step
        simil_threshold (int): similarity threshold
        occup_threshold (int): occupancy threshold
        max_steps (int): maximum number of steps
        opens (list of tuples): open locations

    Returns:
        (list of lists of str): final occupancy grid
    '''
    ## Unpack parameters ##
    N = len(grid)

    ## Values to compute ##
    step = 0

    while step < max_steps:
        ## Iterate over steps ##
        step += 1

        (tomo_grid, reallocations) = is_moving(grid,R,simil_threshold,occup_threshold)
                
        match = find_mismatch(tomo_grid, grid)
        
        if match is None:
            print('No relocations occur in a step')
            break
    
    return (grid, reallocations)


#%%
do_simulation(M, 1, 0.44, 0.5, 1)



#%%
occ_threshold = 0.44
simil_threshold = 0.5
hh = (1,1)
R = 1
p = find_neighbors(M, R, hh[0], hh[1])
print(f'Neighbors of this person: {p}')
print(len(p))
o = count_occupied(M, p)
print(f'Count occupied homes in the neighborhood: {o}')
#%%
s = count_similar(M, 0, 0, p)
print(s)
#%%

print(f'Count similar homes in the neighborhood: {s}')
S = is_satisfied(M, R, hh[0], hh[1], simil_threshold, occ_threshold)
print(f'Is hh satisfied?: {S}')

#%%
opens = find_satisfied_opens(M, R, find_opens(M), hh[0], hh[1], simil_threshold, occ_threshold)
print(f'Find open locations?: {opens}')
mindist = calc_min_dist(M, hh[0], hh[1], opens)
print(f'Minimum distance to open locations: {mindist}')
# minmindist = mindist.index(min(mindist))
# print(f'Index of the location with min distance: {minmindist}')
# print(f'Print location with minimum distance: {opens[minmindist]}')

#%%
S = is_satisfied(M, R, hh[0], hh[1], simil_threshold, occ_threshold)
print(S)
wheremoves = is_moving(M, R, hh[0], hh[1], simil_threshold, occ_threshold)
opens = find_satisfied_opens(M, R, find_opens(M), hh[0], hh[1], simil_threshold, occ_threshold)

print(f'Find open locations?: {opens}')
print(len(opens))
print(wheremoves)

#%%
'''
1) check if the person is satisfied
2) if yes: move to the next person
3) if not: find a list of open locations
4) iterate over a list of open locations and run `is_satisfied` function, creating a list of booleans
5) convert them to integers and count its length
6) if the length is 1 move on, otherwise calculate distance for each satisfactory home
7) this is all happening within a list of open locations, so find a home that minimizes distance
8) 
'''


#%%
i = 0
j = 2 
N = len(M)
for k in range(i-1-R,i+1+R):
    for m in range(j-1-R,j+1+R):
        if k >= 0 and k < N and m >= 0 and m < N:
            print(k,m)

#%%
# Example usage
grid = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

i, j, radius = 1, 1, 1  # Position and radius for which to find neighbors
print(find_neighbors(grid, i, j, radius))  # Output for radius=1: [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)]

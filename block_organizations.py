import numpy as np
import sys
def minimize_grid(grid):
    """
    Takes a grid from its full size to just the 
    bit that contains 0s

    turns 1 1 0 0 1 0
          1 0 1 1 0 0
          1 0 0 1 0 0
          1 1 1 1 1 1

    into
          1 0 0 1 0
          0 1 1 0 0
          0 0 1 0 0

    This will make it so that if the same pattern of remaining blocks
    occurs anywhere in the grid, it will recognize them
    """
    nz_locs = np.array(np.nonzero(grid==0))
    if nz_locs.size==0:
        return None
    x_min = min(nz_locs[0,:]);
    x_max = max(nz_locs[0,:]);
    y_min = min(nz_locs[1,:]);
    y_max = max(nz_locs[1,:]);
    return grid[x_min:x_max+1, y_min:y_max+1]

def all_rotations(grid):
    """
    returns all rotations of the grid, plus both 'flips'
    """
    rot1 = np.rot90(grid)
    rot2 = np.rot90(rot1)
    rot3 = np.rot90(rot2)
    flip1 = np.fliplr(grid)
    flip2 = np.flipud(grid)
    return (grid, rot1, rot2, rot3, flip1, flip2)

def num_combos(grid, loc, grid_dict):
    """
    Calculates the number of combinations of blocks
    that can fill a grid. The grid is a numpy array of 
    boolean values, where 'True's show that the spot has
    already been filled
    """
    # If the spot you're trying to place is already full, 
    # Nothing can be placed
    # (Should never happen)
    if grid[loc[0],loc[1]]:
        return 0
    # Organizations of blocks to fill with
    blocks = ((1,1),(1,2),(2,1))
    # Number of possible placements of blocks
    placements = 0
    for block in blocks:
        # Make a copy of the grid
        new_grid = np.copy(grid)
        # Check to make sure that the block can fit in with the other blocks
        if not np.any(grid[loc[0]:loc[0]+block[0], loc[1]:loc[1]+block[1]]):
            # check to make sure the blocks don't push it off the side 
            if not(loc[0]+block[0]<=grid.shape[0] and loc[1]+block[1]<=grid.shape[1]):
                continue
            # Set the values to a unique value
            new_grid[loc[0]:loc[0]+block[0], loc[1]:loc[1]+block[1]] = np.max(new_grid)+1
            # Find the next location that a block can be placed in
            new_loc = find_next_open(new_grid, loc)

            # If there's nowhere to place a new block, increment the number of 
            # placements. Also print if you want
            if new_loc==None:
                ####
                # UNCOMMENT NEXT TWO LINES TO PRINT
                ####
                #print new_grid
                #print ''
                placements +=1
                continue

            min_grid = minimize_grid(new_grid)

            # Have to tuple the grid, because np arrays are not hashable
            tupled_grid = tuple([tuple(x) for x in min_grid])

            if tupled_grid in grid_dict:
                # If it already exists, you don't have to calculate it
                # Huzzah!
                placements += grid_dict[tupled_grid]
            else:
                # Otherwise, calculate the number of combinations with
                # that grid remaining
                combos = num_combos(new_grid, new_loc, grid_dict)
                # Get all of the rotations
                rotations = all_rotations(min_grid)
                
                # Make a dictionary that points all of the rotations to the number
                # of placements 
                rot_dict = dict([(tuple([tuple(x) for x in r]), combos) for r in rotations])
                grid_dict.update(rot_dict)
                placements += combos
    return placements

def find_next_open(grid, loc):
    """
    Finds the next open spot in the grid to place the next block in
    """
    # Probably not necessary
    loc = loc[:]

    # If the y-loc is greater than the size of the grid, you know
    # that there's no spots left
    if loc[1]>=grid.shape[1]:
        return None
    # if the spot is open, return that spot
    if not grid[loc[0],loc[1]]:
        return loc
    # If the spot was full, increment x
    loc[0] +=1
    # If X is over the edge, reset and increment
    if loc[0]>=grid.shape[0]:
        loc[0] =0
        loc[1] +=1
    return find_next_open(grid, loc)

def run(x_len, y_len):
    grid = np.zeros((x_len, y_len))
    return num_combos(grid, [0,0],{})

def run_arbitrary(gridfile):
    a = [[int(x.strip()) for x in y.split()] for y in open(gridfile).readlines()]
    grid = np.array(a)
    initial_spot = find_next_open(grid, [0,0])
    return num_combos(grid, initial_spot, {})


if __name__=='__main__':
    print 'starting'
    if len(sys.argv)==3:
        x_len = int(sys.argv[1])
        y_len = int(sys.argv[2])
        grid = np.zeros((x_len, y_len))
        print num_combos(grid, [0,0], {})
    elif len(sys.argv)==2:
        print run_arbitrary(sys.argv[1])

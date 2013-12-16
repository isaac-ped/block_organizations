import numpy as np
import sys

def num_combos(grid, loc):
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
            placements += num_combos(new_grid, new_loc)   
    return placements

import pdb 

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


if __name__=='__main__':
    print 'starting'
    x_len = int(sys.argv[1])
    y_len = int(sys.argv[2])
    grid = np.zeros((x_len, y_len))
    print num_combos(grid, [0,0])

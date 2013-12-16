import numpy as np
import sys

def num_combos(grid, loc):
    if np.all(grid[loc[0],loc[1]]):
        return 0
    blocks = ((1,1),(1,2),(2,1))
    placements = 0
    for block in blocks:
        #print 'b',block
        new_grid = np.copy(grid)
        if not np.any(grid[loc[0]:loc[0]+block[0], loc[1]:loc[1]+block[1]]):
            if not(loc[0]+block[0]<=grid.shape[0] and loc[1]+block[1]<=grid.shape[1]):
                #print loc, block, grid.shape
                #print grid
                #print 'NO SPACE'
                continue
            new_grid[loc[0]:loc[0]+block[0], loc[1]:loc[1]+block[1]] = np.max(new_grid)+1
            new_loc = find_next_open(new_grid, loc)
            if new_loc==None:

                #print new_grid
                #print ''
                placements +=1
                continue
            placements += num_combos(new_grid, new_loc)   
    return placements

import pdb 

def find_next_open(grid, loc):
    """
    Finds the next open spot in the grid to place it on
    """
    loc = loc[:]
    if loc[1]>=grid.shape[1]:
        return None
    if not grid[loc[0],loc[1]]:
        return loc
    loc[0] +=1
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

import time
from block_organizations import run
for i in range(1,10):
    start_time = time.time()
    run(i,i)
    end_time = time.time()
    print end_time-start_time


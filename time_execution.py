import time
from block_organizations import run
for i in range(1,50):
    start_time = time.time()
    run(6,i)
    end_time = time.time()
    print end_time-start_time


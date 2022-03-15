import time
import math
import numpy as np

t1 = time.time()
r = 1
total = 10000000
count = 0
bestpi = 3.14
diff = 5
bestdiff = 5
# METHOD USING ONLY THE LOOP

for i in range(total):
    x = np.random.random()
    y = np.random.random()
    if x*x + y*y <= 1:  
        count+=1

    pi = (4*(count/(i+1)))
    diff = abs(pi - math.pi)
    if diff < bestdiff:
        bestpi = pi
        bestdiff = diff
        print("best Pi approx is", bestpi)
        print()


t2 = time.time()
print(t2-t1)




import time
import math
from turtle import circle
import numpy as np
import matplotlib.pyplot as plt

t1 = time.time()

r = 1
fig, ax = plt.subplots(figsize = (7,7),frameon = False)
ax.set_facecolor('darkslategrey')
ax.margins(x=0,y=0)
circle = plt.Circle((0,0),r,color = 'black')
ax.add_artist(circle)

total = 5000
count = 0

# METHOD USING ONLY THE LOOP

for i in range(1,total+1):
    x = np.random.uniform(-1.0,1.0)
    y = np.random.uniform(-1.0,1.0)
    if math.sqrt(x*x + y*y) <= r:
        plt.scatter(x,y,color = 'blue',s=5)
        count+=1
    else:
        plt.scatter(x,y,color = 'lime',s=5)
    print(4*(count/i))

t2 = time.time()
print(t2-t1)
plt.show()
exit()
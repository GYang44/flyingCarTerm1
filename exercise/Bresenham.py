
# coding: utf-8

# ## Bresenham 

# In[3]:


import numpy as np
import matplotlib.pyplot as plt

def bres(p1, p2): 

    x1, y1 = p1
    x2, y2 = p2
    cells = []
    if x1 == x2:
        min = np.minimum(y1,y2)
        max = np.maximum(y1,y2)
        for y in range (min,max):
            cells.append([x1, y])
    elif y1 == y2:
        min = np.minimum(x1,x2)
        max = np.maximum(x1,x2)
        for x in range (min,max):
            cells.append([x, y1])
    else:
        slop = (y2 - y1)/(x2 - x1)
        x = 0
        y = 0
        if x1 < x2 and y1 < y2:
            while x + x1 != x2 or y + y1 != y2:
                cells.append([x1 + x, y1 + y])
                if slop * (x + 1) > y + 1:
                    y += 1
                else:
                    x += 1
        elif x1 < x2 and y1 > y2:
            while x + x1 != x2 or y + y1 != y2:
                cells.append([x1 + x, y1 + y])
                if slop * (x + 1) < y - 1:
                    y -= 1
                else:
                    x += 1
        elif x1 > x2 and y1 > y2:
            while x + x1 != x2 or y + y1 != y2:
                cells.append([x1 + x, y1 + y])
                if slop * (x - 1) < y - 1:
                    y -= 1
                else:
                    x -= 1
        elif x1 > x2 and y1 < y2:
            while x + x1 != x2 or y + y1 != y2:
                cells.append([x1 + x, y1 + y])
                if slop * (x - 1) > y + 1:
                    y += 1
                else:
                    x -= 1
    
    # Done: Determine valid grid cells
        
    return np.array(cells)

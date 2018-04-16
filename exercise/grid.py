
# coding: utf-8

# ## Confguration Space
#
# In this notebook you'll create a configuration space given a map of the world and setting a particular altitude for your drone. You'll read in a `.csv` file containing obstacle data which consists of six columns $x$, $y$, $z$ and $\delta x$, $\delta y$, $\delta z$.
#
# You can look at the `.csv` file [here](/edit/colliders.csv). The first line gives the map center coordinates and the file is arranged such that:
#
# * $x$ -> NORTH
# * $y$ -> EAST
# * $z$ -> ALTITUDE (positive up, note the difference with NED coords)
#
# Each $(x, y, z)$ coordinate is the center of an obstacle. $\delta x$, $\delta y$, $\delta z$ are the half widths of the obstacles, meaning for example that an obstacle with $(x = 37, y = 12, z = 8)$ and $(\delta x = 5, \delta y = 5, \delta z = 8)$ is a 10 x 10 m obstacle that is 16 m high and is centered at the point $(x, y) = (37, 12)$ at a height of 8 m.
#
# Given a map like this, the free space in the $(x, y)$ plane is a function of altitude, and you can plan a path around an obstacle, or simply fly over it! You'll extend each obstacle by a safety margin to create the equivalent of a 3 dimensional configuration space.
#
# Your task is to extract a 2D grid map at 1 metre resolution of your configuration space for a particular altitude, where each value is assigned either a 0 or 1 representing feasible or infeasible (obstacle) spaces respectively.

# The end result should look something like this ... (colours aren't important)
#
# ![title](grid_map.png)

# In[1]:


import numpy as np
import matplotlib.pyplot as plt

def create_grid(data, drone_altitude, safe_distance):
 """
 Returns a grid representation of a 2D configuration space
 based on given obstacle data, drone altitude and safety distance
 arguments.
 """

 # minimum and maximum north coordinates
 north_min = np.floor(np.amin(data[:, 0] - data[:, 3]))
 north_max = np.ceil(np.amax(data[:, 0] + data[:, 3]))

 # minimum and maximum east coordinates
 east_min = np.floor(np.amin(data[:, 1] - data[:, 4]))
 east_max = np.ceil(np.amax(data[:, 1] + data[:, 4]))

 # given the minimum and maximum coordinates we can
 # calculate the size of the grid.
 north_size = int(np.ceil(north_max - north_min))
 east_size = int(np.ceil(east_max - east_min))
 # Initialize an empty grid
 grid = np.zeros((north_size, east_size))
 # Center offset for grid
 north_min_center = np.min(data[:, 0])
 east_min_center = np.min(data[:, 1])
 grid = np.zeros((north_size,east_size))

 # Populate the grid with obstacles
 for i in range(data.shape[0]):
     north, east, alt, d_north, d_east, d_alt = data[i, :]
     if ((drone_altitude <= alt + d_alt + safe_distance) and (drone_altitude >= alt - d_alt - safe_distance)):
         n = (north + d_north + safe_distance) - north_min
         if n > north_size: n = int(north_size)
         else: n = int(np.ceil(n))
         s = (north - d_north - safe_distance) - north_min
         if s < 0: s = int(0)
         else: s = int(np.floor(s))

         w = (east - d_east - safe_distance) - east_min
         if w < 0: w = int(0)
         else: w = int(np.floor(w))
         e = (east + d_east + safe_distance) - east_min
         if e > east_size: e = int(east_size)
         else: e = int(np.ceil(e))


         for y in range(s, n):
             for x in range (w, e):
                 grid[y,x] = 1


     # TODO: Determine which cells contain obstacles
     # and set them to 1.
     #
     # Example:
     #
     #    grid[north_coordinate, east_coordinate] = 1

 return grid

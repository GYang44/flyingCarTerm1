
# coding: utf-8

# # Voronoi Graphs

# Make the relevant imports including Voronoi methods
import numpy as np
from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt
from Bresenham import bres

def create_grid_and_edges(data, drone_altitude, safety_distance):
    """
    Returns a grid representation of a 2D configuration space
    along with Voronoi graph edges given obstacle data and the
    drone's altitude.
    """

    # minimum and maximum north coordinates
    north_min = np.floor(np.min(data[:, 0] - data[:, 3]))
    north_max = np.ceil(np.max(data[:, 0] + data[:, 3]))

    # minimum and maximum east coordinates
    east_min = np.floor(np.min(data[:, 1] - data[:, 4]))
    east_max = np.ceil(np.max(data[:, 1] + data[:, 4]))

    # given the minimum and maximum coordinates we can
    # calculate the size of the grid.
    north_size = int(np.ceil((north_max - north_min)))
    east_size = int(np.ceil((east_max - east_min)))
    
    print(north_size, east_size)

    # Initialize an empty grid
    grid = np.zeros((north_size, east_size))
    # Center offset for grid
    north_min_center = np.min(data[:, 0])
    east_min_center = np.min(data[:, 1])

    # Define a list to hold Voronoi points
    points = []
    
    # Populate the grid with obstacles
    for i in range(data.shape[0]):
        north, east, alt, d_north, d_east, d_alt = data[i, :]


        if alt + d_alt + safety_distance > drone_altitude:
            obstacle = [
                int(north - d_north - safety_distance - north_min_center),
                int(north + d_north + safety_distance - north_min_center),
                int(east - d_east - safety_distance - east_min_center),
                int(east + d_east + safety_distance - east_min_center),
            ]
            grid[obstacle[0]:obstacle[1]+1, obstacle[2]:obstacle[3]+1] = 1
            
            # add center of obstacles to points list
            points.append([north - north_min, east - east_min])

    # Done: create a voronoi graph based on
    # location of obstacle centres
    graph = Voronoi(points)
    voronoi_plot_2d(graph)
    plt.show()
    
    # Done: check each edge from graph.ridge_vertices for collision
    edges = []
    for v in graph.ridge_vertices:
        p1 = graph.vertices[v[0]]
        p1 = (int(p1[0]), int(p1[1]))
        p2 = graph.vertices[v[1]]
        p2 = (int(p2[0]), int(p2[1]))
        
        if int(p1[0]) > -1 and int(p1[0]) < north_size and int(p1[1]) > -1 and int(p1[1]) < east_size and int(p2[0]) > -1 and int(p2[0]) < north_size and int(p2[1]) > -1 and int(p2[1]) < east_size:
            cells = bres(p1, p2)
            in_collision = False
            for cell in cells:
                if grid[cell[0], cell[1]] == 1:
                    in_collision = True
                    break
            if not in_collision:
                edges.append((p1,p2))
        

    return grid, edges


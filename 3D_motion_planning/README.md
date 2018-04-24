# 1. Explain the Starter Code

## 1.1 planning_utils.py
This file contains basic functions that we've explored through lectures.

### 1.1.1 'create_grid'
This function take inputs including data extracted from the CSV file discribing obstacles, altitude drons is crusing and safety_distance. Then the function will use such infomation create an grid mark cell occupied by obstacles as "1" and space as "0". The function also return the lower_left corner of the grid.

### 1.1.2 Action enumerator class
This class define all possible move of the dron at any given status. In addition to that, there is a funtion that returns the movement 'delta'  and a function that returns cost of step 'cost'. 

### 1.1.3 valid_actions function
This function return all possible actions in a status by looking at grid and current_node.

### 1.1.4 a_star function
This function use find paths using breath first search, and verify the end of each branch using *valid_action*. Then using heuristic (potentially) to estimate cost.

### 1.1.5 heuristic fucntion
This function estimate the euclidian distance from any given position to goal.

## 1.2 motion_planning.py
### 1.2.1 'States'
The enumerator class creates a list of all possible states of the drone.

### 1.2.2 MotionPlanning class
This class handles the control of drone.

#### 1.2.2.1 __init__ function 
This function is the constructor of the class. It sets the initial status of an instance of the class.

#### 1.2.2.2 local_position_callback function
This fucntion will be executed when the position of the drone is updated. In takeoff procedure, when drone ascend to 0.95 of target altitude, the drone will start following waypoints. Once the drone reaches the last waypoint, it will land it self. 

#### 1.2.2.3 velocity_callback function
This function will be executed when speed of the drone is changed. In landing procedure, once the drone is touches the ground, it will be disarmed.

#### 1.2.2.4 state_callback function
This function will be executed when states of the drone is changed. In this function the sequence of transition is specified.

#### 1.2.2.5 arming_transition function
This function transit the drone from disarmed to armed and take over the control. This fucntion will be called from the state_callback function. After arming the drone will start planning a path.

#### 1.2.2.6 takeoff_transition function
Shoot the drone into the sky.

#### 1.2.2.7 waypoint_transition function
Fly the drone to waypoints one by one, local_position_callback will trigger the transition to next waypoint.

#### 1.2.2.8 landing_transition function 
Bring the drone back to ground. 

#### 1.2.2.9 disarming_transition function
Release control.

#### 1.2.2.10 manual_transition function
End the mission.

#### 1.2.2.11 send_waypoints function
Visualize waypoints in simulator.

#### 1.2.2.12 plan_path function
This function plan the path with known grid and start goal information. In the starter code, the path is hardcoded to fly 10$\times \sqrt{2}$ meter to north east. Using functions in planning *utils.py*, *a_start* will find the path. Then waypoints will be loaded to the drone.

#### 1.2.2.13 start function
Start the connection, logging and etc.

#### 1.2.3 main function
Create an instance of drone and initialize it properly.

# 2. Implementation of home position extraction
This function is implemented in the *plan_path* function in class *MotionPlanning* in file *motion_planning.py*. By parsing the first line of the csv file, the latitude and longtitude of home position can be retrieved easily.

# 3. Implementation of start position extraction
This is achieved by checking the global position of the drone upon path planning, the global position is then be converted to coordinated in local frame then adjusted by the offset of the grid.

# 4. Implementation of goal position extraction
The latitude and longtitude position of the goal position will be hardcoded, then been converted to grid coordinate using similar method as start position.

# 5. Implementation of the diagnal move 
Diagnal movements can be easiliy added by adding 4 differenct entries in the enumerate class. In valid actions add conditions regarding diagnal moves as well.

# 6. Collinear check
For collinear check, it take the list of path, then re-exame each entry and eliminate thoes collinear. To be more specific, it requires the path has at least 3 entries. For each point in the path, the algorithm will exame if they collinear, if yes, the second and third pointer will be incremented. Otherwise all pointer increment, and the seond pointer will be presever to a new list of path. Finally the new path will replace the old one.

![Quad Image](./Untitled.png)
Drone cutting corners after checking collineary.
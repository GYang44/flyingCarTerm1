#The Writeup for Controller implementation

In this project I took most of the time trying to port the python code I've implemented in different exercises to C++.

##Scenario 1
This part was compiled and run to check if my IDE was properly configured. I was trying to let the drone hover only to discovered most parameters were masked later.

##Scenario 2
This part was tested after the pitch roll controll was implemented. After little bit of tunning the response of the drone can be harnessed with little ocallation.

##Scenario 3
This part was implemented after all functions were implemented. This was the part I figuered I have to use negative gain in for P and D controller for location and speed in X Y direction. Couldn't figure out the reason.

##Scenario 4
This part was tested then discovered the integrator was not been used previously. Three drones was able to proceed to the target location, however, the error seem exceeded the requirement on simulator. Based on my understanding, the error remaining when drones are stablized could not eliminated just by changing gain in P and D. I even tried to create a child class for quadcontroller in order to have integrator on X,Y positions.

##Scenario 5
The drone can follow the trajectory, not as perfect as in exercises in python.
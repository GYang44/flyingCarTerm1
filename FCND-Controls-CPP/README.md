# he Writeup for Controller implementation #

In this project I took most of the time trying to port the python code I've implemented in different exercises to C++. Then spend most of the time check the modeling. Finaly spend some time try to add limitations on ascent descent and tilt rate.

## Scenario 1 ##
This part was compiled and run to check if my IDE was properly configured. I was trying to let the drone hover only to discovered most parameters were masked.

## Scenario 2 ##
This part was tested after the pitch roll controll was implemented. After little bit of tunning the response of the drone can be harnessed with little ocallation.

## Scenario 3 ##
This part was tested after all functions were implemented. At the begining I had to use negative gain in for P and D controller for location and speed in X Y direction.

Later I figured although the thrusts for all motors are defined in the opposite direction as drone body frame, that was causing the drone accelerate in oppsite direciton, and the control loop with positive feedback was created.

## Scenario 4 ##
This part was tested then discovered the integrator was not been used previously. Three drones was able to proceed to the target location, however, the error seem exceeded the requirement on simulator. Based on my understanding, the error remaining when drones are stablized could not eliminated just by changing gain in P and D. I even tried to create a child class for quadcontroller in order to have integrator on X,Y positions.

Later by cheking the local control inputs in stacks, I figured, in order to get faster responses, the system need to have very large gain, however control inputs should be capped, so that the drone won't go crazy.

## Scenario 5 ##
The drone can follow the trajectory.
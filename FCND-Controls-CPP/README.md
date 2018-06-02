# The Writeup for Controller implementation #

In this project I took most of the time trying to port the python code I've implemented in different exercises to C++. Then spend most of the time check the modeling. Finaly spend some time try to add limitations on ascent descent and tilt rate.

## Scenario 1 ##
This part was compiled and run to check if my IDE was properly configured. I was trying to let the drone hover only to discovered most parameters were masked. After increasing the mass, the simulation can be conducted sucessfully.

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

# Rubric Requirements #

## Implement body rate controller ##
This is implemented as BodyRateControl in class QuadControl. This member function take desired angular speed and actual angular speed, using a P controller return angular accelerations to control four motors.

To be more specific, the controller controls how quick the drone can roll or pitch. This affect the acceleration of the drone. By looking at the difference in angular rate and inertial of the drone, the controller can generate proper momentenm in order to allow motors to take proper action. With a large P can accelerate and decelerate more quickly, however, the drone may flip over due to high angular acceleration.

## Implement roll pitch controller ##
This is implemented as RollPitchControl in class QuadControl. This member function take desired acceleration in X,Y world frame and convert thoes accelerations into angular speeds in drone body frame. This was achieved by a P controller.

The challenging part is convert world frame acceleration into body angular acceleration. First the desired acceleration in world frame was converted into world frame roll pitch by findng the cosine component of the thrust at current attitude. As shown in class exercise, using rotation matrix angular rotation in world frame can be converted into body frame. In this function, the P controller is in act of the calculating desired angle rate by looking at the difference between actual acceleration in body frame and desired acceleration in body frame. This controller controls how quickly the drone is able change its speed in X and Y

## Implement altitude controller ##
This is implemented as AltitudeControl in class QuadControl. This member function take desired position velocity and acceleration; actual position velocity and acceleration; attitude; time constant as inputs, and use a PID controller generate collective thrust of the drone. All inputs are for vertical direction in world frame. acceleration in vertical direction was used as feed forward.

This pid controller generate the overall thrust based on vertical acceleration and position of the drone. Using the attitude information and desired acceleration in vertical direction, the thrust can be calculated. Using P and D controller, the drone can react change in position and speed more quickly. Due to inprecise modeling and interference from environements, the thrust calculated by PD controller may never eliminate error in position or speed, by introducing I controller, the accumulated error can compensate such error.

## Implement lateral position control ##
This is implemented as LateralControl in class QuadControl. This member function take desired position; speed in horizental plane and generate accelerations in horizental plane, feed forward for acceleration was also used when been provided. This is achieved by a PD controller.

By looking at position and speed PD controller generate acceleration in horizental plane to control the drone. P controls the speed of reacting while D is in charge of the overshoot. However, in practice Kp and Kd was set to large values, then by constrain the calculated acceleration command, the drone alway accelerate in full throttle (with out flip over) then slow down with a slam on the break.

## Implement yaw control ##
This is implemented as YawControl in class QuadControl. This member function take desired yaw angle and generate angular around Z axie. This is achieved by implemented a P controller.

The torque created by all motors can turn the dronw in very predictable way, there for the gain in this P controller was easily tuned.

## Implement calculating the motor commands given commanded thrust and moments ##
This is implemented as GenerateMotorCommands in class QuadControl. This member function take desired moment of the drone(body frame) and desired collective thrust of motors and generate thrust of each motor. 

# Tunning process #
This was conducted with developing simultaneously. 

## Scenario 1 ##
By increase the drone mass by 10%, the drone was able to fall as desired.

## Scenario 2 ##
In this step, the KpBank and KpPQR were tunned, first was the KpPQR, it controls the angular rate, with proper gain, the drone can eliminate the angular acceleration. Then by tunning the KpBank, the drone can counter move and eliminate the acceleration in horizontal plane create by the angular acceleration.

## Scenario 3 ##
In this simulation, kpPosXY, kpPosZ, kpVelXY, kpVelZ, was tuned, mostly with KpPosXY and KpVelXY. These two controls how quickly the drone can move and stop. KpYaw was increasedd in order for the drone to yaw within the time been provided.

after setting the limitation on angular velocity kpBank was increased. 

## Scenario 4 ##
In this simulation, KiPosZ was tuned to eliminate error on vertical direction of the drone. KpPosXY KpPosZ, kpPQR was furthur tuned.

## Scenario 5 ##
In this simulation, I furthur examed code constraining angular rate; acceleration. Then run previous simulations with larger gains on pretty all parameters. with only KiPosZ decreased.

Final parameter is shown in QuadPControlParams.txt


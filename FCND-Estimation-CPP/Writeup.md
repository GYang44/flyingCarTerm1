# Project Writeup #

## 1.Determine the standard deviation ##
I finished this step using excel from microsoft office, simply by seperate the time from data, the standard deviation can be easily caculated using built in function from excel.

Standard deviation of postion X from GPS and acceleration X from IMU are calculated as 0.713633 and 0.488362 respectivly.

## 2.Attitude Estimation ##
This part is implemented as suggested in the comment of QuadEstimatorEKF.cpp UpdateFromIMU.

First, a Quaternion instance is created using estimated attitude from previous step. Then the quaternion were integrated with bodyrates measured by gyro. Finally the integrated quaternion were converted back to Euler angles. Then after applying the complementary filter, we have estimated attitude.
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from scipy.interpolate import splprep, splev
from scipy.optimize import minimize
import time


class LateralController:
    '''
    Lateral control using the Stanley controller

    functions:
        stanley 

    init:
        gain_constant (default=5)
        damping_constant (default=0.5)
    '''


    def __init__(self, gain_constant=5, damping_constant=0.6):

        self.gain_constant = gain_constant
        self.damping_constant = damping_constant
        self.previous_steering_angle = 0


    def stanley(self, waypoints, speed):
        '''
        ##### TODO #####
        one step of the stanley controller with damping
        args:
            waypoints (np.array) [2, num_waypoints]
            speed (float)
        '''
        k = self.gain_constant
        
        # derive orientation error as the angle of the first path segment to the car orientation
        dx = waypoints[0,1] - waypoints[0,0]
        dy = waypoints[1,1] - waypoints[1,0]
        heading_error = np.arctan(dx/dy)
        
                                
        # derive stanley control law
        # derive cross track error as distance between desired waypoint at spline parameter equal zero ot the car position
        e = waypoints[0,0] - 48
        
        # prevent division by zero by adding as small epsilon
        epsilon = 1E-9
        delta = heading_error + np.arctan(k * e / (speed+epsilon))
        # derive damping
        damping = self.damping_constant * (delta - self.previous_steering_angle)
        # clip to the maximum stering angle (0.4) and rescale the steering action space
        a =0
        b=0
        if delta <0 :
            a = delta
            b = -1 * delta
        else :
            a = -1 * delta
            b = delta
        
        damping = np.clip(damping, a - 0.1* delta, b + 0.1*delta)
        steering_angle = delta - damping
        steering_angle = np.clip(steering_angle, -0.4, 0.4) 

        self.previous_steering_angle = steering_angle

        return steering_angle
        """
        crosstrack error : waypoints의 맨 처음값 - (48,0)
        heading error : waypoints의 첫 번째 인덱스 값과 그 다음 인덱스에 해당되는 값 사용
        """

        

        






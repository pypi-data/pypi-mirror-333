import numpy as np
from filterpy.kalman import KalmanFilter
from ..config.settings import *

class LandmarkKalmanFilter:
    def __init__(self):
        self.kf = KalmanFilter(dim_x=9, dim_z=3)  # State: [x, y, z, vx, vy, vz, ax, ay, az]
        dt = 1.0/30.0  # Assuming 30 fps
        
        # State transition matrix
        self.kf.F = np.array([
            [1., 0., 0., dt, 0., 0., 0.5*dt**2, 0., 0.],
            [0., 1., 0., 0., dt, 0., 0., 0.5*dt**2, 0.],
            [0., 0., 1., 0., 0., dt, 0., 0., 0.5*dt**2],
            [0., 0., 0., 1., 0., 0., dt, 0., 0.],
            [0., 0., 0., 0., 1., 0., 0., dt, 0.],
            [0., 0., 0., 0., 0., 1., 0., 0., dt],
            [0., 0., 0., 0., 0., 0., 1., 0., 0.],
            [0., 0., 0., 0., 0., 0., 0., 1., 0.],
            [0., 0., 0., 0., 0., 0., 0., 0., 1.]
        ])
        
        # Measurement matrix
        self.kf.H = np.array([
            [1., 0., 0., 0., 0., 0., 0., 0., 0.],
            [0., 1., 0., 0., 0., 0., 0., 0., 0.],
            [0., 0., 1., 0., 0., 0., 0., 0., 0.]
        ])
        
        # Initialize noise matrices
        self.kf.Q *= KALMAN_PROCESS_NOISE
        self.kf.R *= KALMAN_MEASUREMENT_NOISE
        
        # Additional tracking parameters
        self.velocity_history = []
        self.initialized = False

    def update(self, measurement, visibility=1.0):
        measurement = np.array(measurement).reshape(-1, 1)
        
        if not self.initialized:
            self.kf.x[:3] = measurement
            self.initialized = True
            return measurement.flatten()
        
        # Predict next state
        self.kf.predict()
        
        # Combine measurement with motion model based on visibility
        if visibility > VISIBILITY_THRESHOLD:
            # Good visibility - trust the measurement more
            self.kf.R *= (2.0 - visibility)  # Adjust measurement noise
            self.kf.update(measurement)
            return self.kf.x[:3].flatten()
        else:
            # Poor visibility - trust motion model more
            motion_prediction = self.kf.x[:3].copy()
            
            # If we have some measurement, blend it with motion model
            if visibility > 0.1:
                # Weighted blend between measurement and motion model
                blended_measurement = (MOTION_MODEL_WEIGHT * motion_prediction + 
                                    (1-MOTION_MODEL_WEIGHT) * measurement)
                self.kf.update(blended_measurement)
            
            return self.kf.x[:3].flatten()

    def get_velocity(self):
        """Return current velocity estimate."""
        return self.kf.x[3:6].flatten()

    def get_acceleration(self):
        """Return current acceleration estimate."""
        return self.kf.x[6:9].flatten()

    def reset(self):
        """Reset the filter state."""
        self.initialized = False
        self.kf.x = np.zeros((9, 1))
        self.velocity_history.clear()
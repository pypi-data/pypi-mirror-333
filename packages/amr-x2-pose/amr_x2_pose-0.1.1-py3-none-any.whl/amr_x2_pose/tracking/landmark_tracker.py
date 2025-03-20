import numpy as np
from filterpy.kalman import KalmanFilter
from ..config.settings import *
from ..tracking.kalman_filter import LandmarkKalmanFilter
from ..tracking.multi_hypothesis import MultiHypothesisTracker

class LandmarkTracker:
    def __init__(self, landmark_id):
        self.landmark_id = landmark_id
        self.kalman_filter = LandmarkKalmanFilter()
        self.multi_hypothesis = MultiHypothesisTracker()
        self.last_reliable_position = None
        self.frames_since_reliable = 0
        self.max_frames_to_track = 30  # Stop tracking after this many frames without reliable detection
        
    def update(self, measurement, visibility):
        """Update the tracker with a new measurement."""
        # Update frame counter for tracking reliability
        if visibility > VISIBILITY_THRESHOLD:
            self.last_reliable_position = measurement
            self.frames_since_reliable = 0
        else:
            self.frames_since_reliable += 1
            
        # If we've lost track for too long, consider resetting
        if self.frames_since_reliable > self.max_frames_to_track:
            if visibility > 0.1:  # If we have any measurement at all
                self.kalman_filter.reset()
                self.multi_hypothesis.clear_hypotheses()
                self.frames_since_reliable = 0
        
        # Update Kalman filter
        kalman_position = self.kalman_filter.update(measurement, visibility)
        
        # Add both the raw measurement and Kalman-filtered position as hypotheses
        if visibility > 0.1:
            self.multi_hypothesis.update(measurement, visibility)
        
        # Add Kalman prediction as a hypothesis with confidence based on motion model
        motion_confidence = max(0.2, 1.0 - (self.frames_since_reliable / self.max_frames_to_track))
        self.multi_hypothesis.update(kalman_position, motion_confidence)
        
        # Merge similar hypotheses
        self.multi_hypothesis.merge_hypotheses(distance_threshold=0.05)
        
        # Get best position from hypotheses
        best_position, confidence = self.multi_hypothesis.update(kalman_position, motion_confidence)
        
        return best_position if best_position is not None else kalman_position, confidence
        
    def get_velocity(self):
        """Return current velocity estimate."""
        return self.kalman_filter.get_velocity()
        
    def get_acceleration(self):
        """Return current acceleration estimate."""
        return self.kalman_filter.get_acceleration()
        
    def reset(self):
        """Reset the tracker state."""
        self.kalman_filter.reset()
        self.multi_hypothesis.clear_hypotheses()
        self.last_reliable_position = None
        self.frames_since_reliable = 0
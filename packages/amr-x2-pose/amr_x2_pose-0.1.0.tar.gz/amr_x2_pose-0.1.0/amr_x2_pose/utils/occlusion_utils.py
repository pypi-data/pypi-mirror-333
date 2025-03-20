import numpy as np
from ..config.settings import *  # This will import MAX_MOVEMENT_RATIO
def detect_temporal_inconsistencies(current_landmarks, previous_landmarks, velocity_estimates=None):
    """
    Detect landmarks that show unrealistic movement between frames.
    
    Args:
        current_landmarks: Current frame landmarks
        previous_landmarks: Previous frame landmarks
        velocity_estimates: Optional velocity estimates from Kalman filter
        
    Returns:
        List of visibility scores adjusted for temporal consistency
    """
    if not previous_landmarks or not current_landmarks:
        return [lm.visibility for lm in current_landmarks]
    
    adjusted_visibility = []
    
    for i, (curr, prev) in enumerate(zip(current_landmarks, previous_landmarks)):
        # Calculate movement distance
        # Check if prev is a dictionary (from pose_history) or an object with attributes
        if isinstance(prev, dict):
            # Handle dictionary format from pose_history
            movement = np.linalg.norm([curr.x - prev['x'], curr.y - prev['y'], curr.z - prev['z']])
        else:
            # Handle object format
            movement = np.linalg.norm([curr.x - prev.x, curr.y - prev.y, curr.z - prev.z])
        
        # Get expected movement from velocity if available
        expected_movement = 0
        if velocity_estimates and i < len(velocity_estimates):
            vel = velocity_estimates[i]
            expected_movement = np.linalg.norm(vel) * (1.0/30.0)  # Assuming 30fps
        
        # If movement is much larger than expected, reduce visibility confidence
        movement_ratio = movement / max(expected_movement, 0.001)
        
        if movement_ratio > MAX_MOVEMENT_RATIO and curr.visibility > 0.3:
            # Suspicious movement - might be a false detection
            adjusted_vis = curr.visibility * (MAX_MOVEMENT_RATIO / movement_ratio)
        else:
            adjusted_vis = curr.visibility
            
        adjusted_visibility.append(adjusted_vis)
    
    return adjusted_visibility

def apply_temporal_smoothing(current_landmarks, landmark_history, alpha=0.7):
    """
    Apply temporal smoothing to landmark positions to reduce jitter.
    
    Args:
        current_landmarks: Current frame landmarks
        landmark_history: List of previous frame landmarks
        alpha: Smoothing factor (higher = more weight to current frame)
        
    Returns:
        Smoothed landmarks
    """
    if not landmark_history:
        return current_landmarks
    
    # Get the most recent history entry
    prev_landmarks = landmark_history[-1]
    
    # Apply exponential smoothing
    for i, (curr, prev) in enumerate(zip(current_landmarks, prev_landmarks)):
        # Only smooth if current landmark is somewhat visible
        if curr.visibility > 0.1:
            # Weighted average between current and previous position
            curr.x = alpha * curr.x + (1 - alpha) * prev['x']
            curr.y = alpha * curr.y + (1 - alpha) * prev['y']
            curr.z = alpha * curr.z + (1 - alpha) * prev['z']
    
    return current_landmarks
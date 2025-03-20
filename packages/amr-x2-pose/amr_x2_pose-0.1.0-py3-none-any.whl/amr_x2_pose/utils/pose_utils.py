import mediapipe as mp
import numpy as np
# Add this at the top of the file
mp_pose = mp.solutions.pose

def copy_landmarks(landmarks):
    landmark_list = []
    for landmark in landmarks:
        landmark_data = {
            'x': landmark.x,
            'y': landmark.y,
            'z': landmark.z,
            'visibility': landmark.visibility
        }
        landmark_list.append(landmark_data)
    return landmark_list
from ..config.settings import VISIBILITY_THRESHOLD, OCCLUSION_CONFIDENCE_BOOST

def apply_symmetry_constraints(landmarks):
    """Apply body symmetry constraints to improve occluded landmark estimation."""
    if not landmarks:
        return landmarks
    
    # Define symmetric landmark pairs (left-right pairs)
    symmetric_pairs = [
        (mp_pose.PoseLandmark.LEFT_SHOULDER.value, mp_pose.PoseLandmark.RIGHT_SHOULDER.value),
        (mp_pose.PoseLandmark.LEFT_ELBOW.value, mp_pose.PoseLandmark.RIGHT_ELBOW.value),
        (mp_pose.PoseLandmark.LEFT_WRIST.value, mp_pose.PoseLandmark.RIGHT_WRIST.value),
        (mp_pose.PoseLandmark.LEFT_HIP.value, mp_pose.PoseLandmark.RIGHT_HIP.value),
        (mp_pose.PoseLandmark.LEFT_KNEE.value, mp_pose.PoseLandmark.RIGHT_KNEE.value),
        (mp_pose.PoseLandmark.LEFT_ANKLE.value, mp_pose.PoseLandmark.RIGHT_ANKLE.value),
        (mp_pose.PoseLandmark.LEFT_EYE.value, mp_pose.PoseLandmark.RIGHT_EYE.value),
        (mp_pose.PoseLandmark.LEFT_EAR.value, mp_pose.PoseLandmark.RIGHT_EAR.value),
    ]
    
    # Apply symmetry constraints
    for left_idx, right_idx in symmetric_pairs:
        left_lm = landmarks[left_idx]
        right_lm = landmarks[right_idx]
        
        # If one side is occluded but the other is visible
        if left_lm.visibility < VISIBILITY_THRESHOLD and right_lm.visibility >= VISIBILITY_THRESHOLD:
            # Mirror the right landmark to estimate left position
            # Note: x-coordinate needs to be mirrored around the body's midline
            midline_x = landmarks[mp_pose.PoseLandmark.NOSE.value].x
            mirror_offset_x = 2 * (midline_x - right_lm.x)
            
            left_lm.x = right_lm.x + mirror_offset_x
            left_lm.y = right_lm.y  # y-coordinate stays the same
            left_lm.z = right_lm.z  # z-coordinate stays the same (depth)
            left_lm.visibility = right_lm.visibility * 0.8  # Slightly lower confidence
            
        elif right_lm.visibility < VISIBILITY_THRESHOLD and left_lm.visibility >= VISIBILITY_THRESHOLD:
            # Mirror the left landmark to estimate right position
            midline_x = landmarks[mp_pose.PoseLandmark.NOSE.value].x
            mirror_offset_x = 2 * (midline_x - left_lm.x)
            
            right_lm.x = left_lm.x + mirror_offset_x
            right_lm.y = left_lm.y
            right_lm.z = left_lm.z
            right_lm.visibility = left_lm.visibility * 0.8
    
    return landmarks

# Define the apply_anatomical_constraints function
def apply_anatomical_constraints(landmarks):
    # Now OCCLUSION_CONFIDENCE_BOOST can be used
    """Apply anatomical constraints to improve occluded landmark estimation."""
    if not landmarks:
        return landmarks
    
    # Define body segments with fixed lengths (normalized)
    body_segments = {
        # Torso
        (mp_pose.PoseLandmark.LEFT_SHOULDER.value, mp_pose.PoseLandmark.RIGHT_SHOULDER.value): 0.25,
        (mp_pose.PoseLandmark.LEFT_HIP.value, mp_pose.PoseLandmark.RIGHT_HIP.value): 0.25,
        (mp_pose.PoseLandmark.LEFT_SHOULDER.value, mp_pose.PoseLandmark.LEFT_HIP.value): 0.5,
        (mp_pose.PoseLandmark.RIGHT_SHOULDER.value, mp_pose.PoseLandmark.RIGHT_HIP.value): 0.5,
        
        # Arms
        (mp_pose.PoseLandmark.LEFT_SHOULDER.value, mp_pose.PoseLandmark.LEFT_ELBOW.value): 0.3,
        (mp_pose.PoseLandmark.LEFT_ELBOW.value, mp_pose.PoseLandmark.LEFT_WRIST.value): 0.25,
        (mp_pose.PoseLandmark.RIGHT_SHOULDER.value, mp_pose.PoseLandmark.RIGHT_ELBOW.value): 0.3,
        (mp_pose.PoseLandmark.RIGHT_ELBOW.value, mp_pose.PoseLandmark.RIGHT_WRIST.value): 0.25,
        
        # Legs
        (mp_pose.PoseLandmark.LEFT_HIP.value, mp_pose.PoseLandmark.LEFT_KNEE.value): 0.45,
        (mp_pose.PoseLandmark.LEFT_KNEE.value, mp_pose.PoseLandmark.LEFT_ANKLE.value): 0.4,
        (mp_pose.PoseLandmark.RIGHT_HIP.value, mp_pose.PoseLandmark.RIGHT_KNEE.value): 0.45,
        (mp_pose.PoseLandmark.RIGHT_KNEE.value, mp_pose.PoseLandmark.RIGHT_ANKLE.value): 0.4,
    }
    
    # Apply constraints for occluded landmarks
    for (start_idx, end_idx), expected_length in body_segments.items():
        start_lm = landmarks[start_idx]
        end_lm = landmarks[end_idx]
        
        # If one point is occluded but the other is visible
        if start_lm.visibility < VISIBILITY_THRESHOLD and end_lm.visibility >= VISIBILITY_THRESHOLD:
            # Estimate position based on expected length and direction
            direction = np.array([
                end_lm.x - start_lm.x,
                end_lm.y - start_lm.y,
                end_lm.z - start_lm.z
            ])
            
            if np.linalg.norm(direction) > 0:
                unit_direction = direction / np.linalg.norm(direction)
                start_lm.x = end_lm.x - unit_direction[0] * expected_length
                start_lm.y = end_lm.y - unit_direction[1] * expected_length
                start_lm.z = end_lm.z - unit_direction[2] * expected_length
                start_lm.visibility += OCCLUSION_CONFIDENCE_BOOST
                
        elif end_lm.visibility < VISIBILITY_THRESHOLD and start_lm.visibility >= VISIBILITY_THRESHOLD:
            # Estimate position based on expected length and direction
            direction = np.array([
                end_lm.x - start_lm.x,
                end_lm.y - start_lm.y,
                end_lm.z - start_lm.z
            ])
            
            if np.linalg.norm(direction) > 0:
                unit_direction = direction / np.linalg.norm(direction)
                end_lm.x = start_lm.x + unit_direction[0] * expected_length
                end_lm.y = start_lm.y + unit_direction[1] * expected_length
                end_lm.z = start_lm.z + unit_direction[2] * expected_length
                end_lm.visibility += OCCLUSION_CONFIDENCE_BOOST
    
    return landmarks
import cv2
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import mediapipe as mp
from ..config.settings import *

class PoseVisualizer:
    def __init__(self):
        self.fig = plt.figure(figsize=(10, 8))
        self.ax = self.fig.add_subplot(111, projection='3d')
        plt.ion()
        
        # Initialize MediaPipe drawing utilities
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        
        # Define drawing specifications
        self.visible_landmark_spec = self.mp_drawing.DrawingSpec(
            color=(0, 255, 0), thickness=2, circle_radius=2)
        self.occluded_landmark_spec = self.mp_drawing.DrawingSpec(
            color=(0, 0, 255), thickness=3, circle_radius=4)
        self.connection_spec = self.mp_drawing.DrawingSpec(
            color=(0, 255, 255), thickness=2)

    def update_3d_plot(self, landmarks, visibility):
        self.ax.cla()
        
        x, y, z = [], [], []
        colors = []
        sizes = []
        
        for i, landmark in enumerate(landmarks):
            x.append(landmark.x)
            y.append(landmark.y)
            z.append(landmark.z)
            
            if visibility[i] < VISIBILITY_THRESHOLD:
                colors.append('red')
                sizes.append(20)
            else:
                colors.append('green')
                sizes.append(50 * visibility[i] + 10)
        
        # Plot landmarks
        self.ax.scatter(x, y, z, c=colors, s=sizes, marker='o', alpha=0.7)
        
        # Draw connections
        for connection in self.mp_pose.POSE_CONNECTIONS:
            start_idx = connection[0]
            end_idx = connection[1]
            if visibility[start_idx] > VISIBILITY_THRESHOLD/2 and visibility[end_idx] > VISIBILITY_THRESHOLD/2:
                self.ax.plot([x[start_idx], x[end_idx]], 
                           [y[start_idx], y[end_idx]], 
                           [z[start_idx], z[end_idx]], 
                           'gray', alpha=0.5)
        
        # Set plot limits and labels
        self.ax.set_xlim([0, 1])
        self.ax.set_ylim([0, 1])
        self.ax.set_zlim([-0.5, 0.5])
        
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.ax.set_title('3D Pose with Occlusion Detection')
        
        # Add statistics
        occluded_count = sum(1 for v in visibility if v < VISIBILITY_THRESHOLD)
        self.ax.text(0.1, 0.1, 0.4, f'Occluded points: {occluded_count}/{len(visibility)}')
        
        plt.pause(0.001)

    def draw_pose_landmarks(self, image, landmarks, connections):
        annotated_image = image.copy()
        occlusion_overlay = np.zeros_like(annotated_image)
        
        if landmarks:
            # Draw landmarks and connections
            for idx, landmark in enumerate(landmarks.landmark):  # Access the landmark attribute
                is_occluded = landmark.visibility < VISIBILITY_THRESHOLD
                drawing_spec = self.occluded_landmark_spec if is_occluded else self.visible_landmark_spec
                
                # Get pixel coordinates
                cx = int(landmark.x * image.shape[1])
                cy = int(landmark.y * image.shape[0])
                
                # Draw landmark point
                circle_radius = drawing_spec.circle_radius * (3 if is_occluded else 2)
                cv2.circle(annotated_image, (cx, cy), circle_radius, 
                          drawing_spec.color, drawing_spec.thickness)
                
                # Draw confidence visualization
                confidence_radius = int(30 * (0.5 if is_occluded else landmark.visibility))
                circle_color = (0, 0, 255) if is_occluded else (0, int(255 * landmark.visibility), 0)
                cv2.circle(occlusion_overlay, (cx, cy), confidence_radius, 
                          circle_color, -1)
            
            # Draw skeleton connections
            self.mp_drawing.draw_landmarks(
                annotated_image,
                landmarks,
                connections,
                landmark_drawing_spec=None,
                connection_drawing_spec=self.connection_spec
            )
            
            # Blend overlay with main image
            alpha = 0.3
            annotated_image = cv2.addWeighted(annotated_image, 1, occlusion_overlay, alpha, 0)
        
        return annotated_image

    def add_processing_stats(self, image, settings_dict):
        """Add image processing statistics to the frame."""
        y_pos = 30
        cv2.putText(image, "Image Enhancement:", 
                    (10, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        y_pos += 30
        for setting, value in settings_dict.items():
            if isinstance(value, bool) and value:
                cv2.putText(image, f"{setting}: ON", 
                           (10, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
                y_pos += 25
            elif isinstance(value, float):
                cv2.putText(image, f"{setting}: {value:.1f}", 
                           (10, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
                y_pos += 25
        
        return image
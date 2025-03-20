import cv2
import mediapipe as mp
import numpy as np
import time  # Add this import
from .config.settings import *
from .processing.image_enhancement import enhance_image
from .tracking.kalman_filter import LandmarkKalmanFilter
from .tracking.multi_hypothesis import MultiHypothesisTracker
from .utils.pose_utils import copy_landmarks, apply_anatomical_constraints, apply_symmetry_constraints
from .utils.occlusion_utils import detect_temporal_inconsistencies, apply_temporal_smoothing
from .tracking.landmark_tracker import LandmarkTracker
from .visualization.pose_visualizer import PoseVisualizer

def occluded_landmarks_handler(
    use_webcam=True, 
    camera_index=0, 
    show_controls=True, 
    show_comparison=True, 
    show_pose=True,
    device='cpu',  # 'cpu' or 'gpu'
    video_path=None,  # Path to video file if not using webcam
    target_fps=30,  # Target FPS for processing
    enable_adaptive_preprocessing=True,  # Enable/disable image preprocessing
    output_video_path=None,  # Path to save output video (None = don't save)
    extract_landmarks=False,  # Extract landmarks for each frame
    save_landmarks_to_file=None  # Path to save landmarks to file (None = don't save)
):
    # Initialize MediaPipe Pose with device selection
    mp_pose = mp.solutions.pose
    
    # Set device options based on parameter
    if device.lower() == 'gpu':
        # Enable GPU acceleration if available
        try:
            import tensorflow as tf
            physical_devices = tf.config.list_physical_devices('GPU')
            if len(physical_devices) > 0:
                tf.config.experimental.set_memory_growth(physical_devices[0], True)
                print("GPU acceleration enabled")
            else:
                print("No GPU found, falling back to CPU")
                device = 'cpu'
        except:
            print("Failed to enable GPU acceleration, falling back to CPU")
            device = 'cpu'
    
    pose = mp_pose.Pose(
        static_image_mode=False,
        model_complexity=2,
        enable_segmentation=True,
        smooth_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )

    # Initialize visualization
    visualizer = PoseVisualizer()
    
    # Initialize pose history list
    pose_history = []
    
    # Initialize video source
    if use_webcam:
        cap = cv2.VideoCapture(camera_index)
    else:
        # Use provided video path or fallback to camera_index if it's a string path
        video_source = video_path if video_path else camera_index
        cap = cv2.VideoCapture(video_source)
    
    # Get video properties
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    original_fps = cap.get(cv2.CAP_PROP_FPS)
    
    # Setup video writer if output path is provided
    video_writer = None
    if output_video_path:
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        video_writer = cv2.VideoWriter(
            output_video_path, 
            fourcc, 
            target_fps, 
            (frame_width, frame_height)
        )
    
    # Create windows based on parameters
    if show_controls:
        cv2.namedWindow('Controls')
        # Create trackbars
        cv2.createTrackbar('CLAHE', 'Controls', int(APPLY_CLAHE), 1, 
                        lambda x: globals().update({'APPLY_CLAHE': bool(x)}))
        cv2.createTrackbar('Bilateral Filter', 'Controls', int(APPLY_BILATERAL_FILTER), 1, 
                        lambda x: globals().update({'APPLY_BILATERAL_FILTER': bool(x)}))
        cv2.createTrackbar('Gamma Correction', 'Controls', int(APPLY_GAMMA_CORRECTION), 1, 
                        lambda x: globals().update({'APPLY_GAMMA_CORRECTION': bool(x)}))
        cv2.createTrackbar('Gamma Value x10', 'Controls', int(GAMMA_VALUE*10), 30, 
                        lambda x: globals().update({'GAMMA_VALUE': x/10.0}))
        cv2.createTrackbar('Sharpening', 'Controls', int(APPLY_SHARPENING), 1, 
                        lambda x: globals().update({'APPLY_SHARPENING': bool(x)}))
        cv2.createTrackbar('Sharpen Strength x10', 'Controls', int(SHARPEN_STRENGTH*10), 10, 
                        lambda x: globals().update({'SHARPEN_STRENGTH': x/10.0}))
        cv2.createTrackbar('Adaptive Lighting', 'Controls', int(ADAPTIVE_LIGHTING), 1, 
                        lambda x: globals().update({'ADAPTIVE_LIGHTING': bool(x)}))
        cv2.createTrackbar('Target Brightness x100', 'Controls', int(TARGET_BRIGHTNESS*100), 100, 
                        lambda x: globals().update({'TARGET_BRIGHTNESS': x/100.0}))
        cv2.createTrackbar('Enable Preprocessing', 'Controls', int(enable_adaptive_preprocessing), 1, 
                        lambda x: globals().update({'enable_adaptive_preprocessing': bool(x)}))
    
    if show_comparison:
        cv2.namedWindow('Original vs Enhanced')
    
    if show_pose:
        cv2.namedWindow('BlazePose 3D Pose Estimation with Occlusion Handling')

    # FPS control variables
    prev_frame_time = 0
    new_frame_time = 0
    frame_interval = 1.0 / target_fps if target_fps > 0 else 0
    
    # Initialize data structure for extracted landmarks if enabled
    extracted_landmarks = [] if extract_landmarks else None
    
    while cap.isOpened():
        # FPS control - skip frames if processing too fast
        if target_fps > 0:
            new_frame_time = time.time()
            elapsed = new_frame_time - prev_frame_time
            if elapsed < frame_interval:
                time.sleep(frame_interval - elapsed)
        
        ret, frame = cap.read()
        if not ret:
            break

        # Convert to RGB (MediaPipe requirement)
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image_height, image_width, _ = image.shape
        
        # Create a copy of the original for side-by-side comparison
        original_rgb = image.copy()
        
        # Apply image enhancement techniques if enabled
        if enable_adaptive_preprocessing:
            enhanced_image = enhance_image(image)
        else:
            enhanced_image = image.copy()
        
        # Process the enhanced image with MediaPipe Pose
        results = pose.process(enhanced_image)
        
        # Prepare images for display
        original_bgr = cv2.cvtColor(original_rgb, cv2.COLOR_RGB2BGR)
        enhanced_bgr = cv2.cvtColor(enhanced_image, cv2.COLOR_RGB2BGR)
        
        # Initialize landmark trackers
        landmark_trackers = [LandmarkTracker(i) for i in range(33)]  # 33 landmarks in MediaPipe Pose
        
        # Inside your main loop where you process pose landmarks
        if results.pose_landmarks:
            # Update pose history
            if len(pose_history) >= HISTORY_LENGTH:
                pose_history.pop(0)
            pose_history.append(copy_landmarks(results.pose_landmarks.landmark))
            
            # Get raw landmarks
            raw_landmarks = results.pose_landmarks.landmark
            
            # Check for temporal inconsistencies
            if ENABLE_TEMPORAL_CONSISTENCY and len(pose_history) > 1:
                # Get velocity estimates from trackers
                velocity_estimates = [tracker.get_velocity() for tracker in landmark_trackers]
                
                # Adjust visibility based on temporal consistency
                adjusted_visibility = detect_temporal_inconsistencies(
                    raw_landmarks, 
                    [pose_history[-2][i] for i in range(len(raw_landmarks))],
                    velocity_estimates
                )
                
                # Update landmark visibility with adjusted values
                for i, vis in enumerate(adjusted_visibility):
                    raw_landmarks[i].visibility = vis
            
            # Update trackers and get improved positions
            improved_landmarks = []
            for i, landmark in enumerate(raw_landmarks):
                position = [landmark.x, landmark.y, landmark.z]
                improved_position, confidence = landmark_trackers[i].update(
                    position, landmark.visibility
                )
                
                # Create a new landmark with improved position
                improved_landmark = type(landmark)()
                improved_landmark.x = improved_position[0]
                improved_landmark.y = improved_position[1]
                improved_landmark.z = improved_position[2]
                improved_landmark.visibility = max(landmark.visibility, confidence * 0.8)
                improved_landmarks.append(improved_landmark)
            
            # Apply temporal smoothing if enabled
            if ENABLE_TEMPORAL_CONSISTENCY:
                improved_landmarks = apply_temporal_smoothing(improved_landmarks, pose_history)
            
            # Apply additional constraints
            if SYMMETRY_CONSTRAINTS:
                improved_landmarks = apply_symmetry_constraints(improved_landmarks)
            if ANATOMICAL_CONSTRAINTS_ENABLED:
                improved_landmarks = apply_anatomical_constraints(improved_landmarks)
            
            # Update visualization with improved landmarks
            visibility = [lm.visibility for lm in improved_landmarks]
            visualizer.update_3d_plot(improved_landmarks, visibility)
            
            # Create a new landmark collection for drawing
            # The error is here - PoseLandmarkList doesn't exist
            # Instead, we need to use the correct MediaPipe structure
            from mediapipe.framework.formats import landmark_pb2
            
            improved_results_landmarks = landmark_pb2.NormalizedLandmarkList()
            for landmark in improved_landmarks:
                improved_results_landmarks.landmark.add(
                    x=landmark.x,
                    y=landmark.y,
                    z=landmark.z,
                    visibility=landmark.visibility
                )
            
            # Draw 2D visualization with improved landmarks
            annotated_image = visualizer.draw_pose_landmarks(
                enhanced_bgr, 
                improved_results_landmarks,
                mp_pose.POSE_CONNECTIONS
            )
            
            # Add processing stats
            settings_dict = {
                'CLAHE': APPLY_CLAHE,
                'Bilateral': APPLY_BILATERAL_FILTER,
                'Gamma': GAMMA_VALUE,
                'Sharpening': SHARPEN_STRENGTH,
                'Device': device,
                'Preprocessing': enable_adaptive_preprocessing
            }
            annotated_image = visualizer.add_processing_stats(annotated_image, settings_dict)
        else:
            annotated_image = enhanced_bgr

        # Calculate and display FPS
        new_frame_time = time.time()
        fps = 1 / (new_frame_time - prev_frame_time) if prev_frame_time > 0 else 0
        prev_frame_time = new_frame_time
        
        # Display FPS on the right side of the frame
        fps_text = f"FPS: {fps:.1f}"
        fps_text_size = cv2.getTextSize(fps_text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
        fps_x = annotated_image.shape[1] - fps_text_size[0] - 10  # 10 pixels from right edge
        cv2.putText(annotated_image, fps_text, (fps_x, 70), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Display frames based on parameters
        if show_comparison:
            # Combine original and enhanced images side by side
            combined_view = np.hstack((original_bgr, enhanced_bgr))
            cv2.putText(combined_view, "Original", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(combined_view, "Enhanced", (image_width + 10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.imshow('Original vs Enhanced', combined_view)
        
        if show_pose:
            cv2.imshow('BlazePose 3D Pose Estimation with Occlusion Handling', annotated_image)
        
        # Write frame to output video if enabled
        if video_writer:
            video_writer.write(annotated_image)

        # Exit on 'q' press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Clean up resources
    cap.release()
    if video_writer:
        video_writer.release()
    cv2.destroyAllWindows()

    # Save landmarks to file if path is provided
    if save_landmarks_to_file and extracted_landmarks:
        import json
        with open(save_landmarks_to_file, 'w') as f:
            json.dump(extracted_landmarks, f)
    
    # Return both the pose processor and extracted landmarks
    return (None, extracted_landmarks)

def main():
    """Entry point for the application when installed as a package."""
    import argparse
    import time
    
    # Create argument parser
    parser = argparse.ArgumentParser(description='3D Pose Estimation with BlazePose')
    parser.add_argument('--use-webcam', type=bool, default=True, help='Use webcam as input source')
    parser.add_argument('--camera-index', type=int, default=0, help='Camera index for webcam')
    parser.add_argument('--show-controls', type=bool, default=True, help='Show control window')
    parser.add_argument('--show-comparison', type=bool, default=True, help='Show comparison window')
    parser.add_argument('--show-pose', type=bool, default=True, help='Show pose estimation window')
    parser.add_argument('--device', type=str, default='cpu', choices=['cpu', 'gpu'], help='Device to use for processing')
    parser.add_argument('--video-path', type=str, default=None, help='Path to video file if not using webcam')
    parser.add_argument('--target-fps', type=int, default=30, help='Target FPS for processing')
    parser.add_argument('--enable-preprocessing', type=bool, default=True, help='Enable adaptive preprocessing')
    parser.add_argument('--output-video', type=str, default=None, help='Path to save output video')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Call occluded_landmarks_handler with parsed arguments
    occluded_landmarks_handler(
        use_webcam=args.use_webcam,
        camera_index=args.camera_index,
        show_controls=args.show_controls,
        show_comparison=args.show_comparison,
        show_pose=args.show_pose,
        device=args.device,
        video_path=args.video_path,
        target_fps=args.target_fps,
        enable_adaptive_preprocessing=args.enable_preprocessing,
        output_video_path=args.output_video
    )

if __name__ == "__main__":
    import time  # Add time import for FPS control
    
    # Call the main function
    main()
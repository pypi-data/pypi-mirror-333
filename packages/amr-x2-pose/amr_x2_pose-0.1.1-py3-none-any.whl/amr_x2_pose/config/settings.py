# Image processing parameters
APPLY_CLAHE = True
APPLY_BILATERAL_FILTER = True
APPLY_GAMMA_CORRECTION = True
GAMMA_VALUE = 1.0
APPLY_SHARPENING = True
SHARPEN_STRENGTH = 0.5
SHARPEN_KERNEL_SIZE = 3
VISIBILITY_THRESHOLD = 0.5  # Keep only one instance
HISTORY_LENGTH = 30        # Keep only one instance
# Adaptive lighting parameters
ADAPTIVE_LIGHTING = True
MIN_GAMMA = 0.5
MAX_GAMMA = 2.0
TARGET_BRIGHTNESS = 0.45
BRIGHTNESS_TOLERANCE = 0.1

# Tracking parameters
INTERPOLATION_THRESHOLD = 0.3
KALMAN_PROCESS_NOISE = 0.1
KALMAN_MEASUREMENT_NOISE = 0.1
OCCLUSION_CONFIDENCE_BOOST = 0.2
TEMPORAL_WINDOW_SIZE = 7
ANATOMICAL_CONSTRAINTS_ENABLED = True
VELOCITY_CONSISTENCY_CHECK = True
MAX_VELOCITY_THRESHOLD = 0.1

# Multi-hypothesis tracking parameters
MULTI_HYPOTHESIS_TRACKING = True
MAX_HYPOTHESES = 3
SYMMETRY_CONSTRAINTS = True
CONFIDENCE_DECAY_RATE = 0.8
MOTION_MODEL_WEIGHT = 0.7

# Occlusion handling parameters
# Add this line to your settings file (along with your other constants)
MAX_MOVEMENT_RATIO = 0.2  # Adjust this value as needed for your application
TEMPORAL_SMOOTHING_ALPHA = 0.7  # Smoothing factor for temporal filtering
ENABLE_TEMPORAL_CONSISTENCY = True  # Enable temporal consistency checks
ENABLE_MULTI_HYPOTHESIS = True  # Enable multi-hypothesis tracking
CONFIDENCE_DECAY_RATE = 0.9  # Rate at which hypothesis confidence decays
MAX_HYPOTHESES = 5  # Maximum number of hypotheses to track per landmark
MOTION_MODEL_WEIGHT = 0.7  # Weight given to motion model vs measurement for occluded points
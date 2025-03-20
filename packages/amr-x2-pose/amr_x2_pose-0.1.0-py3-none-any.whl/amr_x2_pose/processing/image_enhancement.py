import cv2
import numpy as np
from ..config.settings import *

def enhance_image(image):
    """Apply image processing techniques with adaptive lighting adjustment."""
    enhanced = image.copy()
    
    if ADAPTIVE_LIGHTING:
        # Calculate current frame brightness
        gray = cv2.cvtColor(enhanced, cv2.COLOR_RGB2GRAY)
        current_brightness = np.mean(gray) / 255.0
        
        # Dynamically adjust gamma based on brightness
        global GAMMA_VALUE
        if abs(current_brightness - TARGET_BRIGHTNESS) > BRIGHTNESS_TOLERANCE:
            if current_brightness < TARGET_BRIGHTNESS:
                GAMMA_VALUE = max(MIN_GAMMA, 1.0 + (TARGET_BRIGHTNESS - current_brightness))
            else:
                GAMMA_VALUE = max(MIN_GAMMA, 1.0 - (current_brightness - TARGET_BRIGHTNESS))
        
        # Adjust CLAHE parameters based on lighting
        if current_brightness < 0.3:  # Dark scene
            clip_limit = 3.0
            grid_size = (6, 6)
        elif current_brightness > 0.7:  # Bright scene
            clip_limit = 1.5
            grid_size = (10, 10)
        else:  # Normal lighting
            clip_limit = 2.0
            grid_size = (8, 8)
    else:
        clip_limit = 2.0
        grid_size = (8, 8)
    
    # Convert to LAB color space for better processing
    if APPLY_CLAHE:
        lab = cv2.cvtColor(enhanced, cv2.COLOR_RGB2LAB)
        l, a, b = cv2.split(lab)
        
        # Apply adaptive CLAHE
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=grid_size)
        l = clahe.apply(l)
        
        lab = cv2.merge((l, a, b))
        enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)
    
    if APPLY_BILATERAL_FILTER:
        enhanced = cv2.bilateralFilter(enhanced, 9, 75, 75)
    
    if APPLY_GAMMA_CORRECTION:
        lookUpTable = np.empty((1, 256), np.uint8)
        for i in range(256):
            lookUpTable[0, i] = np.clip(pow(i / 255.0, 1.0 / GAMMA_VALUE) * 255.0, 0, 255)
        
        r, g, b = cv2.split(enhanced)
        r = cv2.LUT(r, lookUpTable)
        g = cv2.LUT(g, lookUpTable)
        b = cv2.LUT(b, lookUpTable)
        enhanced = cv2.merge((r, g, b))
    
    if APPLY_SHARPENING:
        # Adjust sharpening based on brightness
        if ADAPTIVE_LIGHTING:
            global SHARPEN_STRENGTH
            SHARPEN_STRENGTH = max(0.3, min(0.7, 1.0 - current_brightness))
        
        blur = cv2.GaussianBlur(enhanced, (SHARPEN_KERNEL_SIZE, SHARPEN_KERNEL_SIZE), 0)
        enhanced = cv2.addWeighted(enhanced, 1.0 + SHARPEN_STRENGTH, blur, -SHARPEN_STRENGTH, 0)
    
    return enhanced
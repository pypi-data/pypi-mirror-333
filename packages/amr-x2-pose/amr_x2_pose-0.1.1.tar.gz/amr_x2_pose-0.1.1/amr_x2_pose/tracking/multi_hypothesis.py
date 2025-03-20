import numpy as np
from ..config.settings import *

class MultiHypothesisTracker:
    def __init__(self, max_hypotheses=MAX_HYPOTHESES):
        self.max_hypotheses = max_hypotheses
        self.hypotheses = []  # List of (position, confidence) tuples
        self.best_hypothesis = None
        self.last_update_time = 0
        
    def update(self, measurement, confidence):
        # Add new measurement as a hypothesis
        if confidence > 0.1:  # Only add if it has some minimal confidence
            self.hypotheses.append((measurement, confidence))
        
        # Decay confidence of existing hypotheses
        self.hypotheses = [(pos, conf * CONFIDENCE_DECAY_RATE) for pos, conf in self.hypotheses]
        
        # Keep only the top hypotheses
        self.hypotheses.sort(key=lambda x: x[1], reverse=True)
        self.hypotheses = self.hypotheses[:self.max_hypotheses]
        
        # Select best hypothesis
        if self.hypotheses:
            self.best_hypothesis = self.hypotheses[0]
            return self.best_hypothesis[0], self.best_hypothesis[1]
        return None, 0.0
    
    def get_all_hypotheses(self):
        """Return all current hypotheses and their confidences."""
        return self.hypotheses.copy()
    
    def clear_hypotheses(self):
        """Clear all current hypotheses."""
        self.hypotheses.clear()
        self.best_hypothesis = None
    
    def merge_hypotheses(self, distance_threshold=0.1):
        """Merge similar hypotheses to reduce redundancy."""
        if not self.hypotheses:
            return
        
        merged = []
        used = set()
        
        for i, (pos1, conf1) in enumerate(self.hypotheses):
            if i in used:
                continue
                
            similar_positions = []
            similar_confidences = []
            
            for j, (pos2, conf2) in enumerate(self.hypotheses):
                if j in used:
                    continue
                    
                distance = np.linalg.norm(np.array(pos1) - np.array(pos2))
                if distance < distance_threshold:
                    similar_positions.append(pos2)
                    similar_confidences.append(conf2)
                    used.add(j)
            
            if similar_positions:
                # Weighted average of positions
                weights = np.array(similar_confidences)
                weights = weights / np.sum(weights)
                avg_pos = np.average(similar_positions, weights=weights, axis=0)
                max_conf = max(similar_confidences)
                merged.append((avg_pos, max_conf))
        
        self.hypotheses = merged
        if self.hypotheses:
            self.best_hypothesis = max(self.hypotheses, key=lambda x: x[1])
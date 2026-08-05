import numpy as np
from sklearn.tree import DecisionTreeClassifier


class AIResourceAllocator:
    def __init__(self):
        self.model = DecisionTreeClassifier()
        self._train_initial_model()

    def _train_initial_model(self):
        # Features: [CPU Usage %, RAM Usage %, Page Fault Count, Wait Time (s)]
        X_train = np.array([
            [10, 15, 2, 1],    # Light process
            [85, 90, 50, 12],  # Memory leak / Rogue process
            [95, 30, 5, 20],   # CPU Bound heavy job
            [40, 50, 10, 3],   # Standard balanced process
            [90, 95, 80, 25],  # Critical resource hog
            [5, 5, 0, 0]       # Idle process
        ])
        # Targets: 0: MAINTAIN, 1: THROTTLE, 2: TERMINATE, 3: ALLOCATE_MORE
        y_train = np.array([0, 2, 3, 0, 2, 0])
        self.model.fit(X_train, y_train)

    def evaluate_process(self, cpu_pct, ram_pct, page_faults, wait_time):
        """Classifies process status and returns automated action recommendation."""
        action_map = {
            0: "MAINTAIN: Process operating within normal thresholds.",
            1: "THROTTLE: High resource consumption. Reducing CPU priority (renice).",
            2: "TERMINATE: Dangerously high memory/faults. Kill process to avoid crash.",
            3: "ALLOCATE_MORE: Bottlenecked CPU bound job. Increasing core allocation."
        }
        
        sample = np.array([[cpu_pct, ram_pct, page_faults, wait_time]])
        pred = self.model.predict(sample)[0]
        return action_map[pred]


if __name__ == "__main__":
    allocator = AIResourceAllocator()
    # Test a heavy process (90% CPU, 88% RAM, 45 faults, 15s wait)
    result = allocator.evaluate_process(90, 88, 45, 15)
    print("AI Decision:", result)
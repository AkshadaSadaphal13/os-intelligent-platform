import numpy as np


class BankerAlgorithm:
    def __init__(self, total_resources, allocation_matrix, max_matrix):
        """
        :param total_resources: 1D array of total available resources [R1, R2, ...]
        :param allocation_matrix: 2D array of current allocated resources (Processes x Resources)
        :param max_matrix: 2D array of max resource demands (Processes x Resources)
        """
        self.allocation = np.array(allocation_matrix, dtype=int)
        self.max = np.array(max_matrix, dtype=int)
        self.need = self.max - self.allocation
        
        # Available = Total System Resources - Sum of Currently Allocated Resources
        self.available = np.array(total_resources, dtype=int) - np.sum(self.allocation, axis=0)
        self.num_processes, self.num_resources = self.allocation.shape

    def check_safety_state(self):
        """
        Determines if the system is in a safe state and returns a valid execution sequence.
        """
        work = np.copy(self.available)
        finish = [False] * self.num_processes
        safe_sequence = []

        while len(safe_sequence) < self.num_processes:
            found_candidate = False
            
            for p in range(self.num_processes):
                if not finish[p] and np.all(self.need[p] <= work):
                    work += self.allocation[p]
                    finish[p] = True
                    safe_sequence.append(f"P{p}")
                    found_candidate = True
                    break

            # If no process could be safely executed, the system is in an UNSAFE state
            if not found_candidate:
                return False, [], "System is in an UNSAFE state (Potential Deadlock Detected)."

        return True, safe_sequence, "System is in a SAFE state."

    def request_resources(self, process_id, request_vector):
        """
        Simulates allocating resources to a process and checks safety.
        """
        req = np.array(request_vector, dtype=int)
        
        if np.any(req > self.need[process_id]):
            return False, f"Error: Process P{process_id} exceeded its declared maximum claim."
        
        if np.any(req > self.available):
            return False, f"Process P{process_id} must wait. Resources unavailable."

        # Pre-allocate resources speculatively
        self.available -= req
        self.allocation[process_id] += req
        self.need[process_id] -= req

        # Check safety state with new allocation
        is_safe, sequence, msg = self.check_safety_state()

        if is_safe:
            return True, f"Request GRANTED. Safe Sequence: {' -> '.join(sequence)}"
        else:
            # Rollback allocation if unsafe
            self.available += req
            self.allocation[process_id] -= req
            self.need[process_id] += req
            return False, f"Request DENIED. Granting request leads to Deadlock. {msg}"


# Quick Test/Standalone Execution
if __name__ == "__main__":
    # Example: 5 processes (P0-P4) and 3 resource types (A, B, C)
    total_res = [10, 5, 7]
    alloc = [
        [0, 1, 0],
        [2, 0, 0],
        [3, 0, 2],
        [2, 1, 1],
        [0, 0, 2]
    ]
    max_claim = [
        [7, 5, 3],
        [3, 2, 2],
        [9, 0, 2],
        [2, 2, 2],
        [4, 3, 3]
    ]

    banker = BankerAlgorithm(total_res, alloc, max_claim)
    is_safe, seq, status = banker.check_safety_state()
    print(f"Safety Check: {status} | Sequence: {seq}")
    
    # Simulate a request from Process 1 requesting [1, 0, 2]
    granted, res_msg = banker.request_resources(process_id=1, request_vector=[1, 0, 2])
    print(f"Resource Request Result: {res_msg}")
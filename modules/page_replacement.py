class PageReplacementSimulator:
    def __init__(self, reference_string, frame_capacity):
        """
        :param reference_string: List of page numbers requested by OS (e.g., [7, 0, 1, 2, 0, 3])
        :param frame_capacity: Number of available physical memory frames
        """
        self.pages = reference_string
        self.capacity = frame_capacity

    def fifo(self):
        """First-In, First-Out (FIFO) Page Replacement"""
        frames = []
        page_faults = 0
        hits = 0
        frame_history = []

        for page in self.pages:
            if page in frames:
                hits += 1
            else:
                page_faults += 1
                if len(frames) < self.capacity:
                    frames.append(page)
                else:
                    frames.pop(0)  # Evict oldest page
                    frames.append(page)
            frame_history.append(list(frames))

        return self._format_results("FIFO", page_faults, hits, frame_history)

    def lru(self):
        """Least Recently Used (LRU) Page Replacement"""
        frames = []
        page_faults = 0
        hits = 0
        frame_history = []

        for page in self.pages:
            if page in frames:
                hits += 1
                frames.remove(page)
                frames.append(page)  # Move accessed page to end (most recently used)
            else:
                page_faults += 1
                if len(frames) < self.capacity:
                    frames.append(page)
                else:
                    frames.pop(0)  # Evict least recently used page (front of list)
                    frames.append(page)
            frame_history.append(list(frames))

        return self._format_results("LRU", page_faults, hits, frame_history)

    def optimal(self):
        """Optimal Page Replacement Algorithm"""
        frames = []
        page_faults = 0
        hits = 0
        frame_history = []

        for i, page in enumerate(self.pages):
            if page in frames:
                hits += 1
            else:
                page_faults += 1
                if len(frames) < self.capacity:
                    frames.append(page)
                else:
                    # Find page that will not be used for longest duration in future
                    farthest_idx = -1
                    page_to_replace = None

                    for frame in frames:
                        if frame not in self.pages[i + 1:]:
                            page_to_replace = frame
                            break
                        else:
                            next_use = self.pages[i + 1:].index(frame)
                            if next_use > farthest_idx:
                                farthest_idx = next_use
                                page_to_replace = frame

                    frames.remove(page_to_replace)
                    frames.append(page)
            frame_history.append(list(frames))

        return self._format_results("Optimal", page_faults, hits, frame_history)

    def _format_results(self, algo_name, faults, hits, history):
        total_requests = len(self.pages)
        return {
            "algorithm": algo_name,
            "page_faults": faults,
            "hits": hits,
            "hit_ratio": round((hits / total_requests) * 100, 2) if total_requests > 0 else 0,
            "fault_ratio": round((faults / total_requests) * 100, 2) if total_requests > 0 else 0,
            "frame_snapshots": history
        }


# Quick Test/Standalone Execution
if __name__ == "__main__":
    ref_str = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1]
    frames_count = 3

    sim = PageReplacementSimulator(ref_str, frames_count)
    
    print("FIFO Result:", sim.fifo())
    print("LRU Result:", sim.lru())
    print("Optimal Result:", sim.optimal())
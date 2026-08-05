import pandas as pd


class CPUScheduler:
    def __init__(self, processes):
        """
        :param processes: List of dicts, e.g., [{'pid': 'P1', 'burst': 6, 'arrival': 0}]
        """
        self.processes = processes

    def fcfs(self):
        """First-Come, First-Served"""
        procs = sorted(self.processes, key=lambda x: x['arrival'])
        time = 0
        wait_times, turnaround_times = [], []

        for p in procs:
            if time < p['arrival']:
                time = p['arrival']
            wait = time - p['arrival']
            tat = wait + p['burst']
            time += p['burst']
            
            wait_times.append(wait)
            turnaround_times.append(tat)

        return {
            "algorithm": "FCFS",
            "avg_wait": round(sum(wait_times) / len(procs), 2),
            "avg_tat": round(sum(turnaround_times) / len(procs), 2)
        }

    def sjf(self):
        """Shortest Job First (Non-Preemptive)"""
        procs = [p.copy() for p in self.processes]
        time = 0
        completed = 0
        n = len(procs)
        visited = [False] * n
        wait_times, turnaround_times = [0] * n, [0] * n

        while completed < n:
            idx = -1
            min_burst = float('inf')

            for i in range(n):
                if procs[i]['arrival'] <= time and not visited[i]:
                    if procs[i]['burst'] < min_burst:
                        min_burst = procs[i]['burst']
                        idx = i

            if idx == -1:
                time += 1
            else:
                wait_times[idx] = time - procs[idx]['arrival']
                turnaround_times[idx] = wait_times[idx] + procs[idx]['burst']
                time += procs[idx]['burst']
                visited[idx] = True
                completed += 1

        return {
            "algorithm": "SJF",
            "avg_wait": round(sum(wait_times) / n, 2),
            "avg_tat": round(sum(turnaround_times) / n, 2)
        }

    def recommend_best(self):
        results = [self.fcfs(), self.sjf()]
        best = min(results, key=lambda x: x['avg_wait'])
        return results, f"Recommended Algorithm: {best['algorithm']} (Lowest Avg Wait: {best['avg_wait']}s)"


if __name__ == "__main__":
    sample_procs = [
        {'pid': 'P1', 'burst': 6, 'arrival': 0},
        {'pid': 'P2', 'burst': 2, 'arrival': 1},
        {'pid': 'P3', 'burst': 8, 'arrival': 2}
    ]
    scheduler = CPUScheduler(sample_procs)
    results, recommendation = scheduler.recommend_best()
    print("Results:", results)
    print("Recommendation:", recommendation)
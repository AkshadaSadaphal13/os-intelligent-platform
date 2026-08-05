import psutil
import pandas as pd


class ProcessMonitor:
    @staticmethod
    def get_system_summary():
        """Returns high-level system usage metrics."""
        return {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "memory_used_gb": round(psutil.virtual_memory().used / (1024**3), 2),
            "memory_total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
            "disk_percent": psutil.disk_usage('/').percent
        }

    @staticmethod
    def get_process_list(top_n=10):
        """Fetches active processes sorted by memory usage."""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
            try:
                info = proc.info
                info['memory_percent'] = round(info['memory_percent'] or 0, 2)
                info['cpu_percent'] = round(info['cpu_percent'] or 0, 2)
                processes.append(info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        df = pd.DataFrame(processes)
        if not df.empty:
            df = df.sort_values(by="memory_percent", ascending=False).head(top_n)
        return df


if __name__ == "__main__":
    mon = ProcessMonitor()
    print("System Summary:", mon.get_system_summary())
    print("\nTop Processes:\n", mon.get_process_list(5))
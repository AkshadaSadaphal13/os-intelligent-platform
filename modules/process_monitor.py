import psutil
import pandas as pd


class ProcessMonitor:
    @staticmethod
    def get_system_summary():
        """Returns high-level system usage metrics safely inside Docker/Linux."""
        try:
            return {
                "cpu_percent": psutil.cpu_percent(interval=0.1),
                "memory_percent": psutil.virtual_memory().percent,
                "memory_used_gb": round(psutil.virtual_memory().used / (1024**3), 2),
                "memory_total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
                "disk_percent": psutil.disk_usage('/').percent
            }
        except Exception:
            return {
                "cpu_percent": 0.0,
                "memory_percent": 0.0,
                "memory_used_gb": 0.0,
                "memory_total_gb": 0.0,
                "disk_percent": 0.0
            }

    @staticmethod
    def get_process_list(top_n=10):
        """Fetches active processes with broad exception handling for containers."""
        processes = []
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
                try:
                    info = proc.info
                    info['memory_percent'] = round(info.get('memory_percent') or 0, 2)
                    info['cpu_percent'] = round(info.get('cpu_percent') or 0, 2)
                    processes.append(info)
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess, KeyError, Exception):
                    continue
        except Exception:
            pass
        
        df = pd.DataFrame(processes)
        if not df.empty:
            df = df.sort_values(by="memory_percent", ascending=False).head(top_n)
        else:
            df = pd.DataFrame(columns=['pid', 'name', 'cpu_percent', 'memory_percent', 'status'])
        return df


def get_system_metrics():
    try:
        cpu = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory().percent
        return cpu, memory
    except Exception:
        return 0.0, 0.0


if __name__ == "__main__":
    mon = ProcessMonitor()
    print("System Summary:", mon.get_system_summary())
    print("\nTop Processes:\n", mon.get_process_list(5))
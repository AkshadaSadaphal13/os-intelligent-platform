import re
import pandas as pd


class LogAnalyzer:
    @staticmethod
    def parse_logs(log_text):
        """
        Parses raw log strings formatted like:
        '2026-08-05 10:15:30 [ERROR] Out of Memory Exception'
        """
        pattern = r"(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\s\[(INFO|WARN|ERROR|CRITICAL)\]\s(.+)"
        matches = re.findall(pattern, log_text)

        parsed_data = []
        for match in matches:
            parsed_data.append({
                "timestamp": match[0],
                "level": match[1],
                "message": match[2]
            })

        df = pd.DataFrame(parsed_data)
        if df.empty:
            return df, {"INFO": 0, "WARN": 0, "ERROR": 0, "CRITICAL": 0}

        summary = df['level'].value_counts().to_dict()
        return df, summary


if __name__ == "__main__":
    sample_logs = """
    2026-08-05 10:00:01 [INFO] System booted successfully.
    2026-08-05 10:05:12 [WARN] High Memory usage detected (>80%).
    2026-08-05 10:10:45 [ERROR] Process 4022 terminated unexpectedly.
    2026-08-05 10:15:00 [CRITICAL] Kernel Panic - Deadlock state achieved.
    """
    analyzer = LogAnalyzer()
    df_logs, log_summary = analyzer.parse_logs(sample_logs)
    print("Parsed Log Data:\n", df_logs)
    print("\nLog Severity Summary:", log_summary)
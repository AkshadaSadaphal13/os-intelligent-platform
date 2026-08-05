import streamlit as st
import pandas as pd
import plotly.express as px

# Import custom platform modules
from modules.process_monitor import ProcessMonitor
from modules.cpu_scheduler import CPUScheduler
from modules.memory_predictor import MemoryPredictor
from modules.deadlock_detector import BankerAlgorithm
from modules.page_replacement import PageReplacementSimulator
from modules.log_analyzer import LogAnalyzer
from modules.ai_allocator import AIResourceAllocator

st.set_page_config(page_title="Intelligent OS Platform", layout="wide")
st.title("🖥️ Intelligent OS Analytics & Resource Management Platform")

# Sidebar Navigation
st.sidebar.header("Navigation")
page = st.sidebar.radio(
    "Select Module",
    [
        "Process Monitor", 
        "CPU Scheduler", 
        "Memory Predictor", 
        "Deadlock Detector", 
        "Page Replacement", 
        "Log Analyzer", 
        "AI Resource Allocation"
    ]
)

# -------------------------------------------------------------
# Module 1: Process Monitor
# -------------------------------------------------------------
if page == "Process Monitor":
    st.header("📊 Live Process & System Monitor")
    
    summary = ProcessMonitor.get_system_summary()
    col1, col2, col3 = st.columns(3)
    col1.metric("CPU Usage", f"{summary['cpu_percent']}%")
    col2.metric("RAM Usage", f"{summary['memory_percent']}% ({summary['memory_used_gb']} GB / {summary['memory_total_gb']} GB)")
    col3.metric("Disk Usage", f"{summary['disk_percent']}%")

    st.subheader("Top Active Processes")
    df_procs = ProcessMonitor.get_process_list(top_n=10)
    st.dataframe(df_procs, use_container_width=True)

# -------------------------------------------------------------
# Module 2: CPU Scheduler
# -------------------------------------------------------------
elif page == "CPU Scheduler":
    st.header("⚡ CPU Scheduling Optimizer")
    st.write("Compare scheduling algorithms and find the lowest Average Waiting Time.")

    processes = [
        {'pid': 'P1', 'burst': 6, 'arrival': 0},
        {'pid': 'P2', 'burst': 2, 'arrival': 1},
        {'pid': 'P3', 'burst': 8, 'arrival': 2},
        {'pid': 'P4', 'burst': 3, 'arrival': 3}
    ]
    
    st.dataframe(pd.DataFrame(processes))
    scheduler = CPUScheduler(processes)
    results, recommendation = scheduler.recommend_best()
    
    st.success(recommendation)
    st.json(results)

# -------------------------------------------------------------
# Module 3: Memory Predictor
# -------------------------------------------------------------
elif page == "Memory Predictor":
    st.header("📈 Memory Usage Forecast")
    
    history_str = st.text_input("Enter Historical RAM % (comma-separated):", "35, 38, 42, 45, 52, 58, 64")
    history_data = [float(x.strip()) for x in history_str.split(",") if x.strip()]

    if st.button("Predict Future RAM"):
        predictor = MemoryPredictor()
        preds = predictor.train_and_predict(history_data, future_steps=5)
        
        full_series = history_data + preds
        df_chart = pd.DataFrame({
            "Time Index": list(range(len(full_series))),
            "RAM %": full_series,
            "Type": ["Historical"] * len(history_data) + ["Predicted"] * len(preds)
        })
        
        fig = px.line(df_chart, x="Time Index", y="RAM %", color="Type", markers=True, title="RAM Usage Trend & Prediction")
        st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------------------
# Module 4: Deadlock Detector
# -------------------------------------------------------------
elif page == "Deadlock Detector":
    st.header("🔒 Deadlock Detection (Banker's Algorithm)")
    
    total_res = [10, 5, 7]
    alloc = [[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]]
    max_claim = [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]]

    banker = BankerAlgorithm(total_res, alloc, max_claim)
    is_safe, seq, msg = banker.check_safety_state()

    if is_safe:
        st.success(f"{msg}\nSafe Sequence: {' -> '.join(seq)}")
    else:
        st.error(msg)

# -------------------------------------------------------------
# Module 5: Page Replacement
# -------------------------------------------------------------
elif page == "Page Replacement":
    st.header("📄 Page Replacement Simulator")
    
    ref_str = st.text_input("Page Reference String:", "7, 0, 1, 2, 0, 3, 0, 4, 2, 3")
    frames = st.slider("Number of Frames:", 1, 7, 3)
    
    pages = [int(x.strip()) for x in ref_str.split(",") if x.strip()]
    sim = PageReplacementSimulator(pages, frames)

    col1, col2, col3 = st.columns(3)
    col1.metric("FIFO Page Faults", sim.fifo()['page_faults'])
    col2.metric("LRU Page Faults", sim.lru()['page_faults'])
    col3.metric("Optimal Page Faults", sim.optimal()['page_faults'])

# -------------------------------------------------------------
# Module 6: Log Analyzer
# -------------------------------------------------------------
elif page == "Log Analyzer":
    st.header("📜 System Log Parser")
    
    raw_logs = st.text_area("Paste System Logs:", """2026-08-05 10:00:01 [INFO] System booted.
2026-08-05 10:05:12 [WARN] High RAM usage (>80%).
2026-08-05 10:10:45 [ERROR] Process 4022 terminated.
2026-08-05 10:15:00 [CRITICAL] Potential Deadlock state.""", height=150)

    if st.button("Parse Logs"):
        df_logs, summary = LogAnalyzer.parse_logs(raw_logs)
        st.subheader("Severity Distribution")
        st.bar_chart(pd.Series(summary))
        st.dataframe(df_logs, use_container_width=True)

# -------------------------------------------------------------
# Module 8: AI Resource Allocation
# -------------------------------------------------------------
elif page == "AI Resource Allocation":
    st.header("🤖 AI Process Policy Engine")
    
    cpu = st.slider("Target Process CPU %:", 0, 100, 85)
    ram = st.slider("Target Process RAM %:", 0, 100, 90)
    faults = st.number_input("Page Faults / sec:", 0, 200, 50)
    wait = st.number_input("Wait Time (seconds):", 0, 100, 12)

    if st.button("Evaluate Process with AI Model"):
        allocator = AIResourceAllocator()
        decision = allocator.evaluate_process(cpu, ram, faults, wait)
        st.info(decision)
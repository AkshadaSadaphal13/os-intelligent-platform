import time
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Custom Platform Modules
from modules.ai_allocator import AIResourceAllocator
from modules.cpu_scheduler import CPUScheduler
from modules.deadlock_detector import BankerAlgorithm
from modules.log_analyzer import LogAnalyzer
from modules.memory_predictor import MemoryPredictor
from modules.page_replacement import PageReplacementSimulator
from modules.process_monitor import ProcessMonitor

# Dashboard Configuration
st.set_page_config(
    page_title="Intelligent OS Platform",
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🖥️ Intelligent OS Analytics & Resource Management Platform")

# Sidebar Setup
st.sidebar.title("🎛️ Control Panel")
page = st.sidebar.radio(
    "Modules",
    [
        "Process Monitor",
        "CPU Scheduler Engine",
        "Memory Forecast ML",
        "Deadlock Prevention Matrix",
        "Page Replacement Simulator",
        "System Log Parser",
        "AI Policy Engine",
    ],
)

# -------------------------------------------------------------
# Module 1: Dynamic Process Monitor
# -------------------------------------------------------------
if page == "Process Monitor":
    st.header("📊 Live System Telemetry & Process Monitor")

    # Interactive Controls
    col_ctrl1, col_ctrl2, col_ctrl3 = st.columns([1, 1, 2])
    with col_ctrl1:
        auto_refresh = st.checkbox("Enable Auto Refresh", value=False)
    with col_ctrl2:
        refresh_interval = st.slider("Interval (sec)", 1, 10, 2)
    with col_ctrl3:
        search_query = st.text_input("🔍 Search Process Name or PID", "")

    placeholder = st.empty()

    def render_process_monitor():
        summary = ProcessMonitor.get_system_summary()
        df_procs = ProcessMonitor.get_process_list(top_n=50)

        if search_query and not df_procs.empty:
            df_procs = df_procs[
                df_procs["name"].str.contains(search_query, case=False, na=False)
                | df_procs["pid"].astype(str).str.contains(search_query)
            ]

        with placeholder.container():
            # High-Level Metrics
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("CPU Load", f"{summary['cpu_percent']}%")
            m2.metric(
                "RAM Usage",
                f"{summary['memory_percent']}%",
                f"{summary['memory_used_gb']} / {summary['memory_total_gb']} GB",
            )
            m3.metric("Disk Storage", f"{summary['disk_percent']}%")
            m4.metric("Tracked Processes", len(df_procs))

            st.divider()

            # Interactive Process Data Table
            col_tbl, col_chart = st.columns([3, 2])
            with col_tbl:
                st.subheader("Active System Processes")
                st.dataframe(
                    df_procs,
                    use_container_width=True,
                    height=350,
                    column_config={
                        "memory_percent": st.column_config.ProgressColumn(
                            "RAM %", min_value=0, max_value=100, format="%.1f%%"
                        ),
                        "cpu_percent": st.column_config.NumberColumn(
                            "CPU %", format="%.1f%%"
                        ),
                    },
                )

            with col_chart:
                st.subheader("Memory Breakdown (Top 5)")
                if not df_procs.empty:
                    fig = px.pie(
                        df_procs.head(5),
                        values="memory_percent",
                        names="name",
                        hole=0.4,
                        color_discrete_sequence=px.colors.qualitative.Pastel,
                    )
                    st.plotly_chart(fig, use_container_width=True)

    if auto_refresh:
        while True:
            render_process_monitor()
            time.sleep(refresh_interval)
    else:
        render_process_monitor()

# -------------------------------------------------------------
# Module 2: Interactive CPU Scheduler
# -------------------------------------------------------------
elif page == "CPU Scheduler Engine":
    st.header("⚡ Interactive CPU Scheduling Engine")

    st.markdown("Add custom workload processes to evaluate scheduling strategies.")

    # Dynamic Process Creation
    if "custom_processes" not in st.session_state:
        st.session_state.custom_processes = [
            {"pid": "P1", "burst": 6, "arrival": 0},
            {"pid": "P2", "burst": 2, "arrival": 1},
            {"pid": "P3", "burst": 8, "arrival": 2},
            {"pid": "P4", "burst": 3, "arrival": 3},
        ]

    with st.expander("➕ Configure Workload Queue"):
        c1, c2, c3 = st.columns(3)
        new_pid = c1.text_input("Process ID", f"P{len(st.session_state.custom_processes) + 1}")
        new_burst = c2.number_input("Burst Time (ms)", min_value=1, value=4)
        new_arrival = c3.number_input("Arrival Time (ms)", min_value=0, value=0)

        if st.button("Add Process to Queue"):
            st.session_state.custom_processes.append(
                {"pid": new_pid, "burst": new_burst, "arrival": new_arrival}
            )
            st.rerun()

        if st.button("Reset Default Processes"):
            st.session_state.custom_processes = [
                {"pid": "P1", "burst": 6, "arrival": 0},
                {"pid": "P2", "burst": 2, "arrival": 1},
                {"pid": "P3", "burst": 8, "arrival": 2},
            ]
            st.rerun()

    st.dataframe(pd.DataFrame(st.session_state.custom_processes), use_container_width=True)

    scheduler = CPUScheduler(st.session_state.custom_processes)
    results, recommendation = scheduler.recommend_best()

    st.success(f"🏆 {recommendation}")

    # Comparative Metrics Visualization
    df_res = pd.DataFrame(results)
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        fig_wait = px.bar(
            df_res,
            x="algorithm",
            y="avg_wait",
            title="Average Waiting Time (Lower is Better)",
            color="algorithm",
            text_auto=True,
        )
        st.plotly_chart(fig_wait, use_container_width=True)
    with col_g2:
        fig_tat = px.bar(
            df_res,
            x="algorithm",
            y="avg_tat",
            title="Average Turnaround Time (Lower is Better)",
            color="algorithm",
            text_auto=True,
        )
        st.plotly_chart(fig_tat, use_container_width=True)

# -------------------------------------------------------------
# Module 3: Memory Predictor Engine
# -------------------------------------------------------------
elif page == "Memory Forecast ML":
    st.header("📈 Predictive Machine Learning Memory Analysis")

    col_m1, col_m2 = st.columns([1, 2])

    with col_m1:
        st.subheader("Historical Data Input")
        default_ram = "35.5, 38.0, 42.1, 45.0, 52.3, 58.0, 64.2, 70.1"
        raw_input = st.text_area("RAM Usage Timeline (%)", default_ram, height=100)
        future_horizon = st.slider("Prediction Horizon (Steps Ahead)", 1, 10, 5)

        history_data = [float(x.strip()) for x in raw_input.split(",") if x.strip()]

    with col_m2:
        if st.button("Generate ML Forecast") or len(history_data) > 0:
            predictor = MemoryPredictor()
            preds = predictor.train_and_predict(history_data, future_steps=future_horizon)

            time_hist = list(range(1, len(history_data) + 1))
            time_pred = list(range(len(history_data) + 1, len(history_data) + future_horizon + 1))

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=time_hist, y=history_data, mode="lines+markers", name="Observed RAM"))
            fig.add_trace(
                go.Scatter(
                    x=[time_hist[-1]] + time_pred,
                    y=[history_data[-1]] + preds,
                    mode="lines+markers",
                    name="ML Forecast",
                    line=dict(dash="dash", color="orange"),
                )
            )

            fig.update_layout(
                title="RAM Usage Trajectory & Forecast",
                xaxis_title="Time Interval",
                yaxis_title="RAM Usage (%)",
            )
            st.plotly_chart(fig, use_container_width=True)

            if max(preds) > 85:
                st.warning("⚠️ Critical Threshold Warning: Predicted memory demand exceeds 85%!")

# -------------------------------------------------------------
# Module 4: Interactive Deadlock Matrix (Banker's)
# -------------------------------------------------------------
elif page == "Deadlock Prevention Matrix":
    st.header("🔒 Banker's Algorithm Safe State Evaluator")

    st.write("Modify allocation and maximum claim matrices to simulate safety checks.")

    # Editable Matrices
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.subheader("Allocation Matrix")
        alloc_data = pd.DataFrame(
            [[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]],
            columns=["R1", "R2", "R3"],
            index=["P0", "P1", "P2", "P3", "P4"],
        )
        edited_alloc = st.data_editor(alloc_data, key="alloc_ed")

    with col_d2:
        st.subheader("Maximum Demand Matrix")
        max_data = pd.DataFrame(
            [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]],
            columns=["R1", "R2", "R3"],
            index=["P0", "P1", "P2", "P3", "P4"],
        )
        edited_max = st.data_editor(max_data, key="max_ed")

    total_sys = [10, 5, 7]

    banker = BankerAlgorithm(total_sys, edited_alloc.values, edited_max.values)
    is_safe, seq, msg = banker.check_safety_state()

    st.divider()

    if is_safe:
        st.success(f"✅ {msg}")
        st.info(f"Execution Order: {' ➡️ '.join(seq)}")
    else:
        st.error(f"❌ {msg}")

# -------------------------------------------------------------
# Module 5: Interactive Page Replacement Simulator
# -------------------------------------------------------------
elif page == "Page Replacement Simulator":
    st.header("📄 Memory Frame Page Replacement Simulator")

    c_pg1, c_pg2 = st.columns([3, 1])
    with c_pg1:
        ref_str = st.text_input("Memory Page Reference Sequence", "7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3")
    with c_pg2:
        frame_capacity = st.slider("Frame Capacity Slots", 2, 6, 3)

    pages = [int(x.strip()) for x in ref_str.split(",") if x.strip()]
    sim = PageReplacementSimulator(pages, frame_capacity)

    res_fifo = sim.fifo()
    res_lru = sim.lru()
    res_opt = sim.optimal()

    # Metric Row
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("FIFO Faults", res_fifo["page_faults"], f"Hit Rate: {res_fifo['hit_ratio']}%")
    col_m2.metric("LRU Faults", res_lru["page_faults"], f"Hit Rate: {res_lru['hit_ratio']}%")
    col_m3.metric("Optimal Faults", res_opt["page_faults"], f"Hit Rate: {res_opt['hit_ratio']}%")

    # Hit/Fault Comparative Plot
    df_compare = pd.DataFrame(
        [
            {"Algo": "FIFO", "Page Faults": res_fifo["page_faults"], "Hits": res_fifo["hits"]},
            {"Algo": "LRU", "Page Faults": res_lru["page_faults"], "Hits": res_lru["hits"]},
            {"Algo": "Optimal", "Page Faults": res_opt["page_faults"], "Hits": res_opt["hits"]},
        ]
    )

    fig_page = px.bar(
        df_compare,
        x="Algo",
        y=["Page Faults", "Hits"],
        title="Page Faults vs Hits Comparison",
        barmode="group",
    )
    st.plotly_chart(fig_page, use_container_width=True)

# -------------------------------------------------------------
# Module 6: Log File Analyzer
# -------------------------------------------------------------
elif page == "System Log Parser":
    st.header("📜 Interactive System Log Parser")

    log_option = st.radio("Log Source", ["Sample Text", "Upload .log File"], horizontal=True)

    if log_option == "Sample Text":
        log_text = st.text_area(
            "Kernel Output",
            """2026-08-05 10:00:01 [INFO] Kernel initialized successfully.
2026-08-05 10:02:14 [WARN] Memory pressure threshold exceeded (>80%).
2026-08-05 10:05:00 [ERROR] Out of Memory: Killed process 2041 (chrome).
2026-08-05 10:06:12 [INFO] Swappiness adjusted dynamically.
2026-08-05 10:10:00 [CRITICAL] Deadlock state detected on resource R2.""",
            height=150,
        )
    else:
        uploaded_file = st.file_uploader("Choose a log file", type=["log", "txt"])
        if uploaded_file is not None:
            log_text = uploaded_file.getvalue().decode("utf-8")
        else:
            log_text = ""

    if log_text:
        df_logs, summary = LogAnalyzer.parse_logs(log_text)

        col_l1, col_l2 = st.columns([1, 2])
        with col_l1:
            st.subheader("Severity Breakdown")
            st.json(summary)
        with col_l2:
            st.subheader("Parsed Events")
            st.dataframe(df_logs, use_container_width=True)

# -------------------------------------------------------------
# Module 8: AI Policy Decision Engine
# -------------------------------------------------------------
elif page == "AI Policy Engine":
    st.header("🤖 Autonomous AI Resource Allocator")

    st.write("Adjust live process metrics to test automated system actions.")

    col_ai1, col_ai2 = st.columns(2)
    with col_ai1:
        cpu = st.slider("Target CPU Consumption (%)", 0, 100, 85)
        ram = st.slider("Target RAM Allocation (%)", 0, 100, 92)
    with col_ai2:
        faults = st.slider("Page Fault Frequency / sec", 0, 100, 60)
        wait = st.slider("Process Queue Wait Time (sec)", 0, 30, 15)

    allocator = AIResourceAllocator()
    decision = allocator.evaluate_process(cpu, ram, faults, wait)

    st.divider()

    st.subheader("Automated OS Mitigation Policy")
    if "TERMINATE" in decision:
        st.error(f"🛑 {decision}")
    elif "THROTTLE" in decision:
        st.warning(f"⚠️ {decision}")
    elif "ALLOCATE_MORE" in decision:
        st.info(f"⚡ {decision}")
    else:
        st.success(f"✅ {decision}")
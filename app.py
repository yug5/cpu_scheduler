import streamlit as st
from scheduler.fcfs import fcfs
from scheduler.sjf import sjf
from scheduler.round_robin import round_robin

st.set_page_config(page_title="CPU Scheduler", layout="wide")
st.markdown("""
    <h1 style='text-align: center; color: #2c3e50; padding: 20px; 
    background: linear-gradient(45deg, #f8f9fa, #e9ecef); 
    border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); 
    margin-bottom: 30px; border: 1px solid #dee2e6;'>
    CPU Scheduling Algorithms Comparison
    </h1>
""", unsafe_allow_html=True)

# Custom CSS for the timeline
st.markdown("""
<style>
body {
    background-color: #1a1a1a;
    color: #ffffff;
}
.stApp {
    background-color: #1a1a1a;
}
.algorithm-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    margin-bottom: 30px;
    background-color: #1a1a1a;
    width: 100%;
}
.algorithm-container {
    background-color: #1a1a1a;
    border: none;
    padding: 20px;
    display: flex;
    flex-direction: column;
    width: 100%;
    overflow: hidden;
}
.algorithm-title {
    font-size: 1.3em;
    font-weight: bold;
    margin-bottom: 15px;
    color: #4a9eff;
    text-align: center;
    padding-bottom: 10px;
    border-bottom: 1px solid #333;
}
.timeline-scroll {
    overflow-x: auto;
    width: 100%;
    white-space: nowrap;
    border: 2px solid #444;
    border-radius: 8px;
    padding: 15px;
    background-color: #1a1a1a;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}
.timeline-wrapper {
    display: inline-block;
    min-width: 100%;
    padding: 10px 0;
}
.timeline {
    display: table;
    width: 100%;
    border-collapse: separate;
    border-spacing: 1px;
}
.time-header, .process-row {
    display: table-row;
    white-space: nowrap;
}
.time-header {
    font-weight: bold;
    margin-bottom: 12px;
    border-bottom: 2px solid #444;
}
.process-row {
    margin-bottom: 8px;
}
.time-unit, .process-label, .execution-block, .waiting-block {
    display: table-cell;
    min-width: 40px;
    height: 30px;
    vertical-align: middle;
    border: 1px solid #333;
}
.time-unit {
    text-align: center;
    color: #ffffff;
    background-color: #1a1a1a;
    border-bottom: 2px solid #444;
}
.process-label {
    min-width: 80px;
    padding-right: 10px;
    font-weight: bold;
    color: #ffffff;
    background-color: #1a1a1a;
    border-right: 2px solid #444;
}
.execution-block {
    background-color: #4CAF50;
    border: 1px solid #45a049;
}
.waiting-block {
    background-color: #333;
    border: 1px solid #444;
}
.legend {
    display: flex;
    gap: 20px;
    justify-content: center;
    margin-top: 20px;
    padding: 10px;
    background-color: #1a1a1a;
}
.legend-item {
    display: flex;
    align-items: center;
    gap: 10px;
    color: #ffffff;
}
.metrics {
    margin-top: 20px;
    padding: 15px;
    background-color: #242424;
    border-radius: 5px;
    color: #ffffff;
}
.comparison-summary {
    margin-top: 30px;
    padding: 20px;
    background-color: #242424;
    border-radius: 10px;
    color: #ffffff;
}
.comparison-summary h3 {
    color: #ffffff;
    text-align: center;
    margin-bottom: 20px;
    font-size: 1.4em;
    border-bottom: 1px solid #333;
    padding-bottom: 10px;
}
.metric-value {
    font-weight: bold;
    color: #4CAF50;
}
.waiting-time {
    color: #ff6b6b;
}
.turnaround-time {
    color: #4a9eff;
}
.best-algorithm {
    color: #4CAF50;
    font-weight: bold;
}
/* Scrollbar styling */
.timeline-scroll::-webkit-scrollbar {
    height: 8px;
}
.timeline-scroll::-webkit-scrollbar-track {
    background: #1a1a1a;
    border-radius: 4px;
}
.timeline-scroll::-webkit-scrollbar-thumb {
    background: #333;
    border-radius: 4px;
}
.timeline-scroll::-webkit-scrollbar-thumb:hover {
    background: #444;
}
</style>
""", unsafe_allow_html=True)

# Sidebar for input
st.sidebar.header("Process Input")
num_processes = st.sidebar.number_input("Number of Processes", min_value=1, max_value=10, value=3)

processes = []
for i in range(num_processes):
    st.sidebar.subheader(f"Process {i+1}")
    pid = st.sidebar.text_input(f"Process ID {i+1}", value=f"P{i+1}")
    arrival = st.sidebar.number_input(f"Arrival Time {i+1}", min_value=0, value=i)
    burst = st.sidebar.number_input(f"Burst Time {i+1}", min_value=1, value=3)
    processes.append((pid, arrival, burst))

# Time quantum input
time_quantum = st.sidebar.number_input("Time Quantum for Round Robin", min_value=1, value=2)

def create_timeline(processes, total_time, execution_sequence=None):
    timeline_html = """
    <div class="timeline-scroll">
        <div class="timeline-wrapper">
            <div class="timeline">
                <div class="time-header">
                    <div class="process-label">Time</div>
    """
    
    # Add time units
    for t in range(total_time + 1):
        timeline_html += f'<div class="time-unit">{t}</div>'
    timeline_html += "</div>"
    
    # Add process rows
    for pid, arrival, burst in processes:
        timeline_html += f'<div class="process-row"><div class="process-label">P{pid}</div>'
        for t in range(total_time + 1):
            if execution_sequence:
                if any(p == pid and s <= t < s + d for p, s, d in execution_sequence):
                    timeline_html += '<div class="execution-block"></div>'
                else:
                    timeline_html += '<div class="waiting-block"></div>'
            else:
                if t >= arrival and t < arrival + burst:
                    timeline_html += '<div class="execution-block"></div>'
                else:
                    timeline_html += '<div class="waiting-block"></div>'
        timeline_html += "</div>"
    
    timeline_html += """
            </div>
        </div>
    </div>
    """
    return timeline_html

def visualize_algorithm(processes, algorithm_name, time_quantum=None):
    # Calculate total time and prepare processes
    total_time = max([arrival + burst for _, arrival, burst in processes])
    
    # Create container
    st.markdown(f'<div class="algorithm-container">', unsafe_allow_html=True)
    st.markdown(f'<div class="algorithm-title">{algorithm_name}</div>', unsafe_allow_html=True)
    
    if algorithm_name == "Round Robin":
        current_time = 0
        execution_sequence = []
        
        # Sort processes by arrival time and create process state tracking
        sorted_processes = sorted(processes, key=lambda x: x[1])
        remaining_time = {pid: burst for pid, _, burst in processes}
        ready_queue = []
        
        # Find first arrival time
        current_time = min(arrival for _, arrival, _ in processes)
        
        # Add initially available processes to ready queue
        for pid, arrival, _ in sorted_processes:
            if arrival <= current_time:
                ready_queue.append(pid)
        
        while ready_queue or any(remaining_time.values()):
            if not ready_queue:
                # Jump to next arrival time
                next_arrivals = [(pid, arrival) for pid, arrival, _ in sorted_processes 
                               if arrival > current_time and remaining_time[pid] > 0]
                if next_arrivals:
                    current_time = min(arrival for _, arrival in next_arrivals)
                    # Add newly arrived processes to ready queue
                    for pid, arrival in next_arrivals:
                        if arrival <= current_time and remaining_time[pid] > 0:
                            ready_queue.append(pid)
                    continue
            
            if ready_queue:
                current_pid = ready_queue.pop(0)
                if remaining_time[current_pid] > 0:
                    # Execute for time quantum or remaining time
                    exec_time = min(time_quantum, remaining_time[current_pid])
                    execution_sequence.append((current_pid, current_time, exec_time))
                    remaining_time[current_pid] -= exec_time
                    current_time += exec_time
                    
                    # Add newly arrived processes that came during this execution
                    for pid, arrival, _ in sorted_processes:
                        if (arrival > current_time - exec_time and 
                            arrival <= current_time and 
                            remaining_time[pid] > 0 and 
                            pid not in ready_queue):
                            ready_queue.append(pid)
                    
                    # If process not finished, add it back to ready queue
                    if remaining_time[current_pid] > 0:
                        ready_queue.append(current_pid)
    
    else:
        # Keep existing FCFS and SJF logic
        execution_sequence = []
        if algorithm_name == "First-Come, First-Serve (FCFS)":
            sorted_processes = sorted(processes, key=lambda x: x[1])
            current_time = 0
            for pid, arrival, burst in sorted_processes:
                start_time = max(current_time, arrival)
                execution_sequence.append((pid, start_time, burst))
                current_time = start_time + burst
        else:  # SJF
            remaining_processes = [(pid, arrival, burst) for pid, arrival, burst in processes]
            current_time = 0
            while remaining_processes:
                available = [(pid, arrival, burst) for pid, arrival, burst in remaining_processes if arrival <= current_time]
                if available:
                    chosen = min(available, key=lambda x: x[2])
                    pid, arrival, burst = chosen
                    execution_sequence.append((pid, current_time, burst))
                    current_time += burst
                    remaining_processes.remove(chosen)
                else:
                    current_time = min([arrival for _, arrival, _ in remaining_processes])
    
    # Calculate final timeline width
    max_end_time = max([start + duration for _, start, duration in execution_sequence])
    total_time = max(total_time, max_end_time) + 1
    
    # Create timeline HTML
    timeline_html = create_timeline(processes, total_time, execution_sequence)
    st.markdown(timeline_html, unsafe_allow_html=True)
    
    # Calculate metrics correctly
    waiting_times = {}
    turnaround_times = {}
    completion_times = {}
    
    # First calculate completion times for each process
    for pid, _, _ in processes:
        process_blocks = [(s, d) for p, s, d in execution_sequence if p == pid]
        if process_blocks:
            completion_times[pid] = process_blocks[-1][0] + process_blocks[-1][1]
    
    # Then calculate waiting and turnaround times
    for pid, arrival, burst in processes:
        if pid in completion_times:
            # Turnaround time = completion time - arrival time
            turnaround_times[pid] = completion_times[pid] - arrival
            
            # Calculate total execution time for this process
            total_exec_time = sum(d for p, _, d in execution_sequence if p == pid)
            
            # Waiting time = turnaround time - total execution time
            waiting_times[pid] = turnaround_times[pid] - total_exec_time
    
    # Calculate averages
    avg_waiting = sum(waiting_times.values()) / len(processes)
    avg_turnaround = sum(turnaround_times.values()) / len(processes)
    
    # Display metrics with more detail
    st.markdown(f"""
    <div class="metrics">
        <p>Average <span class="waiting-time">Waiting Time</span>: <span class="metric-value">{avg_waiting:.2f}</span></p>
        <p>Average <span class="turnaround-time">Turnaround Time</span>: <span class="metric-value">{avg_turnaround:.2f}</span></p>
        <div class="metrics-details">
            <p><strong>Process Details:</strong></p>
            {''.join(f'<p>P{pid}: Waiting={waiting_times[pid]:.2f}, Turnaround={turnaround_times[pid]:.2f}</p>' 
                    for pid in sorted(waiting_times.keys()))}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    return avg_waiting, avg_turnaround

if st.sidebar.button("Run Comparison"):
    st.markdown('<div class="algorithm-row">', unsafe_allow_html=True)
    
    # Create three columns for the algorithms
    col1, col2, col3 = st.columns(3)
    
    # Visualize each algorithm
    with col1:
        fcfs_waiting, fcfs_turnaround = visualize_algorithm(processes, "First-Come, First-Serve (FCFS)")
    
    with col2:
        sjf_waiting, sjf_turnaround = visualize_algorithm(processes, "Shortest Job First (SJF)")
    
    with col3:
        rr_waiting, rr_turnaround = visualize_algorithm(processes, "Round Robin", time_quantum)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Find best algorithm
    algorithms = {
        "FCFS": (fcfs_waiting, fcfs_turnaround),
        "SJF": (sjf_waiting, sjf_turnaround),
        "Round Robin": (rr_waiting, rr_turnaround)
    }
    
    best_waiting = min(algorithms.items(), key=lambda x: x[1][0])
    best_turnaround = min(algorithms.items(), key=lambda x: x[1][1])
    
    # Display comparison summary
    st.markdown("""
    <div class="comparison-summary">
        <h3>Algorithm Comparison Summary</h3>
        <p>Best for <span class="waiting-time">Waiting Time</span>: <span class="best-algorithm">{}</span> (Average: {:.2f})</p>
        <p>Best for <span class="turnaround-time">Turnaround Time</span>: <span class="best-algorithm">{}</span> (Average: {:.2f})</p>
    </div>
    """.format(
        best_waiting[0], best_waiting[1][0],
        best_turnaround[0], best_turnaround[1][1]
    ), unsafe_allow_html=True)
    
    # Show process details
    st.subheader("Process Details")
    for pid, arrival, burst in processes:
        st.write(f"{pid}: Arrival Time = {arrival}, Burst Time = {burst}") 
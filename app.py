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
.timeline {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin: 20px 0;
}
.process-row {
    display: flex;
    align-items: center;
    gap: 5px;
}
.time-header {
    display: flex;
    gap: 5px;
    margin-bottom: 5px;
}
.time-unit {
    width: 30px;
    text-align: center;
    font-weight: bold;
}
.process-label {
    width: 50px;
    font-weight: bold;
}
.execution-block {
    width: 30px;
    height: 20px;
    background-color: #4CAF50;
    border: 1px solid #45a049;
}
.waiting-block {
    width: 30px;
    height: 20px;
    background-color: #f0f0f0;
    border: 1px solid #ddd;
}
.legend {
    display: flex;
    gap: 20px;
    margin-top: 20px;
}
.legend-item {
    display: flex;
    align-items: center;
    gap: 5px;
}
.algorithm-container {
    border: 1px solid #ddd;
    padding: 20px;
    border-radius: 5px;
    margin-bottom: 20px;
}
.algorithm-title {
    font-size: 1.2em;
    font-weight: bold;
    margin-bottom: 10px;
    color: #2c3e50;
}
.metrics {
    margin-top: 20px;
    padding: 15px;
    background-color: #f8f9fa;
    border-radius: 5px;
    border-left: 4px solid #4CAF50;
}
.metric-value {
    font-weight: bold;
    color: #2c3e50;
}
.waiting-time {
    color: #e74c3c;
}
.turnaround-time {
    color: #3498db;
}
.comparison-summary {
    margin-top: 30px;
    padding: 20px;
    background-color: #f8f9fa;
    border-radius: 5px;
    border-left: 4px solid #f1c40f;
}
.best-algorithm {
    font-weight: bold;
    color: #27ae60;
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
    timeline_html = f"""
    <div class="timeline">
        <div class="time-header">
            <div class="process-label">Time</div>
    """
    
    # Add time units
    for t in range(total_time + 1):
        timeline_html += f'<div class="time-unit">{t}</div>'
    timeline_html += "</div>"
    
    for pid, arrival, burst in processes:
        timeline_html += f'<div class="process-row"><div class="process-label">P{pid}</div>'
        for t in range(total_time + 1):
            if execution_sequence:
                if t < arrival:
                    timeline_html += '<div class="waiting-block"></div>'
                elif any(p == pid and s <= t < s + d for p, s, d in execution_sequence):
                    timeline_html += '<div class="execution-block"></div>'
                else:
                    timeline_html += '<div class="waiting-block"></div>'
            else:
                if t < arrival:
                    timeline_html += '<div class="waiting-block"></div>'
                elif t < arrival + burst:
                    timeline_html += '<div class="execution-block"></div>'
                else:
                    timeline_html += '<div class="waiting-block"></div>'
        timeline_html += "</div>"
    
    return timeline_html

def visualize_algorithm(processes, algorithm_name, time_quantum=None):
    # Calculate total time
    total_time = max([arrival + burst for _, arrival, burst in processes])
    
    # Create container
    st.markdown(f'<div class="algorithm-container">', unsafe_allow_html=True)
    st.markdown(f'<div class="algorithm-title">{algorithm_name}</div>', unsafe_allow_html=True)
    
    if algorithm_name == "First-Come, First-Serve (FCFS)":
        # Sort by arrival time
        sorted_processes = sorted(processes, key=lambda x: x[1])
        timeline_html = create_timeline(sorted_processes, total_time)
        
        # Calculate metrics
        waiting_time = sum([max(0, sum(p[2] for p in sorted_processes[:i]) - arrival) 
                          for i, (_, arrival, _) in enumerate(sorted_processes)])
        turnaround_time = sum([sum(p[2] for p in sorted_processes[:i+1]) - arrival 
                             for i, (_, arrival, _) in enumerate(sorted_processes)])
        
    elif algorithm_name == "Shortest Job First (SJF)":
        # Sort by burst time
        sorted_processes = sorted(processes, key=lambda x: x[2])
        timeline_html = create_timeline(sorted_processes, total_time)
        
        # Calculate metrics
        waiting_time = sum([max(0, sum(p[2] for p in sorted_processes[:i]) - arrival) 
                          for i, (_, arrival, _) in enumerate(sorted_processes)])
        turnaround_time = sum([sum(p[2] for p in sorted_processes[:i+1]) - arrival 
                             for i, (_, arrival, _) in enumerate(sorted_processes)])
        
    else:  # Round Robin
        remaining_processes = [(pid, arrival, burst) for pid, arrival, burst in processes]
        current_time = 0
        execution_sequence = []
        
        while remaining_processes:
            for i, (pid, arrival, burst) in enumerate(remaining_processes):
                if arrival <= current_time:
                    if burst <= time_quantum:
                        execution_sequence.append((pid, current_time, burst))
                        current_time += burst
                        remaining_processes.pop(i)
                    else:
                        execution_sequence.append((pid, current_time, time_quantum))
                        current_time += time_quantum
                        remaining_processes[i] = (pid, arrival, burst - time_quantum)
                    break
            else:
                current_time += 1
        
        timeline_html = create_timeline(processes, total_time, execution_sequence)
        
        # Calculate metrics
        waiting_time = sum([start - arrival for pid, arrival, _ in processes 
                          for p, start, _ in execution_sequence if p == pid])
        turnaround_time = sum([(start + duration) - arrival for pid, arrival, _ in processes 
                             for p, start, duration in execution_sequence if p == pid])
    
    # Add legend
    timeline_html += """
    <div class="legend">
        <div class="legend-item">
            <div class="execution-block"></div>
            <span>Executing</span>
        </div>
        <div class="legend-item">
            <div class="waiting-block"></div>
            <span>Waiting/Completed</span>
        </div>
    </div>
    </div>
    """
    
    # Display timeline
    st.markdown(timeline_html, unsafe_allow_html=True)
    
    # Display metrics
    st.markdown(f"""
    <div class="metrics">
        <p>Average <span class="waiting-time">Waiting Time</span>: <span class="metric-value">{waiting_time/len(processes):.2f}</span></p>
        <p>Average <span class="turnaround-time">Turnaround Time</span>: <span class="metric-value">{turnaround_time/len(processes):.2f}</span></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return waiting_time/len(processes), turnaround_time/len(processes)

if st.sidebar.button("Run Comparison"):
    # Create three columns for the algorithms
    col1, col2, col3 = st.columns(3)
    
    # Visualize each algorithm
    with col1:
        fcfs_waiting, fcfs_turnaround = visualize_algorithm(processes, "First-Come, First-Serve (FCFS)")
    
    with col2:
        sjf_waiting, sjf_turnaround = visualize_algorithm(processes, "Shortest Job First (SJF)")
    
    with col3:
        rr_waiting, rr_turnaround = visualize_algorithm(processes, "Round Robin", time_quantum)
    
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
        <h3 style="color: black;">Algorithm Comparison Summary</h3>
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
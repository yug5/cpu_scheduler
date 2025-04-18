import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
import os

def create_gantt_chart(processes, title):
    try:
        # Create figure and axis
        plt.figure(figsize=(10, 6))
        ax = plt.gca()
        
        # Set up the y-axis with process IDs
        y_ticks = []
        y_labels = []
        for i, (pid, arrival, burst) in enumerate(processes):
            y_ticks.append(i)
            y_labels.append(f'P{pid}')
        
        # Plot each process as a rectangle
        for i, (pid, arrival, burst) in enumerate(processes):
            ax.add_patch(Rectangle((arrival, i-0.4), burst, 0.8, 
                                 facecolor=f'C{i}', 
                                 edgecolor='black',
                                 label=f'P{pid}'))
        
        # Customize the plot
        ax.set_yticks(y_ticks)
        ax.set_yticklabels(y_labels)
        ax.set_xlabel('Time')
        ax.set_title(title)
        ax.grid(True, axis='x')
        
        # Add legend
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        # Adjust layout to prevent label cutoff
        plt.tight_layout()
        
        # Create output directory if it doesn't exist
        os.makedirs('output', exist_ok=True)
        
        # Save the plot
        filename = f'output/{title.lower().replace(" ", "_")}.png'
        plt.savefig(filename)
        print(f"Graph saved as {filename}")
        plt.close()
        
    except Exception as e:
        print(f"Error creating graph: {str(e)}")
        plt.close()

def create_timeline(processes, title):
    print(f"\n{title}")
    print("=" * 50)
    
    # Find total execution time
    total_time = max([arrival + burst for _, arrival, burst in processes])
    
    # Create timeline header
    header = "Time:  "
    for t in range(total_time + 1):
        header += f"{t:3d}"
    print(header)
    print("-" * len(header))
    
    # Create timeline for each process
    for pid, arrival, burst in processes:
        timeline = f"P{pid}:   "
        for t in range(total_time + 1):
            if t < arrival:
                timeline += "   "  # Before arrival
            elif t < arrival + burst:
                timeline += "███"  # During execution
            else:
                timeline += "   "  # After completion
        print(timeline)
    
    print("\nLegend:")
    print("███ - Process executing")
    print("   - Process waiting or completed")
    print("=" * 50)

def visualize_fcfs(processes):
    # Sort processes by arrival time
    sorted_processes = sorted(processes, key=lambda x: x[1])
    create_timeline(sorted_processes, "First Come First Serve (FCFS) Timeline")

def visualize_sjf(processes):
    # Sort processes by burst time
    sorted_processes = sorted(processes, key=lambda x: x[2])
    create_timeline(sorted_processes, "Shortest Job First (SJF) Timeline")

def visualize_rr(processes, time_quantum):
    print("\nRound Robin Timeline")
    print("=" * 50)
    print(f"Time Quantum: {time_quantum}")
    
    # Find total execution time
    total_time = sum([burst for _, _, burst in processes])
    
    # Create timeline header
    header = "Time:  "
    for t in range(total_time + 1):
        header += f"{t:3d}"
    print(header)
    print("-" * len(header))
    
    # Initialize process states
    process_states = {pid: (arrival, burst) for pid, arrival, burst in processes}
    current_time = 0
    
    # Create timeline for each process
    while any(burst > 0 for _, burst in process_states.values()):
        for pid, (arrival, burst) in process_states.items():
            if arrival <= current_time and burst > 0:
                # Execute process for time quantum or remaining burst time
                execute_time = min(time_quantum, burst)
                process_states[pid] = (arrival, burst - execute_time)
                current_time += execute_time
                
                # Print execution
                timeline = f"P{pid}:   "
                for t in range(total_time + 1):
                    if t < arrival:
                        timeline += "   "  # Before arrival
                    elif t < current_time:
                        timeline += "███"  # During execution
                    else:
                        timeline += "   "  # After completion
                print(timeline)
    
    print("\nLegend:")
    print("███ - Process executing")
    print("   - Process waiting or completed")
    print("=" * 50) 
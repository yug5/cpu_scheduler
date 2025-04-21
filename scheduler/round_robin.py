def round_robin(processes, time_quantum):
    print("\nRound Robin Scheduling:")
    print("---------------------")
    print(f"Time Quantum: {time_quantum}")
    
    # Sort processes by arrival time
    processes = sorted(processes, key=lambda x: x[1])  # Sort by arrival time
    
    # Initialize variables
    current_time = 0
    waiting_time = 0
    turnaround_time = 0
    ready_queue = []
    remaining_processes = processes.copy()
    
    # Stores the start and end times for each process to calculate turnaround and waiting times
    process_times = {pid: {"start_time": None, "end_time": None, "burst_left": burst} for pid, arrival, burst in processes}
    
    print("\nProcess Execution Order:")
    print("Process ID | Arrival Time | Burst Time | Start Time | End Time | Waiting Time | Turnaround Time")
    print("-" * 85)
    
    while remaining_processes or ready_queue:
        # Add processes that have arrived to ready queue
        while remaining_processes and remaining_processes[0][1] <= current_time:
            pid, arrival, burst = remaining_processes.pop(0)
            ready_queue.append((pid, arrival, burst))
        
        if ready_queue:
            # Get next process from ready queue
            pid, arrival, burst = ready_queue.pop(0)
            
            # Track the remaining burst time for each process
            remaining_burst = process_times[pid]["burst_left"]
            execute_time = min(time_quantum, remaining_burst)
            start_time = current_time
            end_time = current_time + execute_time
            
            # Assign start and end time
            if process_times[pid]["start_time"] is None:
                process_times[pid]["start_time"] = start_time  # First time the process starts
            
            process_times[pid]["end_time"] = end_time  # Final end time for the process
            
            # Update current time
            current_time = end_time
            
            # If process is not finished, add it back to ready queue with updated burst time
            if remaining_burst - execute_time > 0:
                process_times[pid]["burst_left"] -= execute_time
                ready_queue.append((pid, arrival, remaining_burst - execute_time))
            
            # Process is completed, calculate waiting time and turnaround time
            else:
                waiting_time += (start_time - arrival)
                turnaround_time += (end_time - arrival)
            
            # Print process execution
            print(f"{pid:^10} | {arrival:^12} | {burst:^10} | {start_time:^10} | {end_time:^8} | "
                  f"{start_time - arrival:^12} | {end_time - arrival:^14}")
        else:
            # If no processes are ready, increment time
            current_time += 1
    
    # Calculate averages
    avg_waiting_time = waiting_time / len(processes)
    avg_turnaround_time = turnaround_time / len(processes)
    
    print("\nAverage Waiting Time:", avg_waiting_time)
    print("Average Turnaround Time:", avg_turnaround_time)
    
    return processes

def round_robin(processes, time_quantum):
    print("\nRound Robin Scheduling:")
    print("---------------------")
    print(f"Time Quantum: {time_quantum}")
    
    # Sort processes by arrival time
    processes = sorted(processes, key=lambda x: x[1])
    
    # Initialize variables
    current_time = 0
    waiting_time = 0
    turnaround_time = 0
    ready_queue = []
    remaining_processes = processes.copy()
    
    print("\nProcess Execution Order:")
    print("Process ID | Arrival Time | Burst Time | Start Time | End Time | Waiting Time | Turnaround Time")
    print("-" * 85)
    
    while remaining_processes or ready_queue:
        # Add processes that have arrived to ready queue
        while remaining_processes and remaining_processes[0][1] <= current_time:
            ready_queue.append(remaining_processes.pop(0))
        
        if ready_queue:
            # Get next process from ready queue
            pid, arrival, burst = ready_queue.pop(0)
            
            # Calculate execution time
            execute_time = min(time_quantum, burst)
            start_time = current_time
            end_time = current_time + execute_time
            
            # Print process execution
            print(f"{pid:^10} | {arrival:^12} | {burst:^10} | {start_time:^10} | {end_time:^8} | {start_time - arrival:^12} | {end_time - arrival:^14}")
            
            # Update current time
            current_time = end_time
            
            # If process is not finished, add it back to ready queue
            if burst > time_quantum:
                ready_queue.append((pid, arrival, burst - time_quantum))
            else:
                # Process is completed
                waiting_time += (start_time - arrival)
                turnaround_time += (end_time - arrival)
        else:
            # If no processes are ready, increment time
            current_time += 1
    
    # Calculate averages
    avg_waiting_time = waiting_time / len(processes)
    avg_turnaround_time = turnaround_time / len(processes)
    
    print("\nAverage Waiting Time:", avg_waiting_time)
    print("Average Turnaround Time:", avg_turnaround_time)
    
    return processes


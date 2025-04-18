def sjf(processes):
    print("\nShortest Job First (SJF) Scheduling:")
    print("-----------------------------------")
    
    # Sort processes by arrival time first
    processes = sorted(processes, key=lambda x: x[1])
    
    # Initialize variables
    current_time = 0
    waiting_time = 0
    turnaround_time = 0
    completed_processes = []
    ready_queue = []
    
    print("\nProcess Execution Order:")
    print("Process ID | Arrival Time | Burst Time | Start Time | End Time | Waiting Time | Turnaround Time")
    print("-" * 85)
    
    while processes or ready_queue:
        # Add processes that have arrived to ready queue
        while processes and processes[0][1] <= current_time:
            ready_queue.append(processes.pop(0))
        
        if ready_queue:
            # Sort ready queue by burst time
            ready_queue.sort(key=lambda x: x[2])
            pid, arrival, burst = ready_queue.pop(0)
            
            # Calculate times
            start_time = current_time
            end_time = current_time + burst
            process_waiting_time = start_time - arrival
            process_turnaround_time = end_time - arrival
            
            # Update total times
            waiting_time += process_waiting_time
            turnaround_time += process_turnaround_time
            
            # Print process details
            print(f"{pid:^10} | {arrival:^12} | {burst:^10} | {start_time:^10} | {end_time:^8} | {process_waiting_time:^12} | {process_turnaround_time:^14}")
            
            # Update current time
            current_time = end_time
            completed_processes.append((pid, arrival, burst))
        else:
            # If no processes are ready, increment time
            current_time += 1
    
    # Calculate averages
    avg_waiting_time = waiting_time / len(completed_processes)
    avg_turnaround_time = turnaround_time / len(completed_processes)
    
    print("\nAverage Waiting Time:", avg_waiting_time)
    print("Average Turnaround Time:", avg_turnaround_time)
    
    return completed_processes

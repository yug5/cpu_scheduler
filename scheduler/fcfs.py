def fcfs(processes):
    print("\nFirst Come First Serve (FCFS) Scheduling:")
    print("----------------------------------------")
    
    # Sort processes by arrival time
    processes = sorted(processes, key=lambda x: x[1])
    
    # Initialize variables
    current_time = 0
    waiting_time = 0
    turnaround_time = 0
    
    print("\nProcess Execution Order:")
    print("Process ID | Arrival Time | Burst Time | Start Time | End Time | Waiting Time | Turnaround Time")
    print("-" * 85)
    
    for pid, arrival, burst in processes:
        # If current time is less than arrival time, wait until process arrives
        if current_time < arrival:
            current_time = arrival
        
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
    
    # Calculate averages
    avg_waiting_time = waiting_time / len(processes)
    avg_turnaround_time = turnaround_time / len(processes)
    
    print("\nAverage Waiting Time:", avg_waiting_time)
    print("Average Turnaround Time:", avg_turnaround_time)
    
    return processes

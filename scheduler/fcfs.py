def fcfs(processes):
    print()
    print("For First come first serve")
    print()
    processes.sort(key=lambda x: x[1])  
    time = 0
    for pid, arrival, burst in processes:
        if time < arrival:
            time = arrival
        print(f"Process {pid} executed from {time} to {time + burst}")
        time += burst

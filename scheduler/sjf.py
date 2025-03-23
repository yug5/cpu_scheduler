
def sjf(processes):
    print()
    print("For SJF")
    print()
    processes.sort(key=lambda x: x[2])  
    time = 0
    for pid, arrival, burst in processes:
        if time < arrival:
            time = arrival
        print(f"Process {pid} executed from {time} to {time + burst}")
        time += burst

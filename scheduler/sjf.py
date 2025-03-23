
def sjf(processes):
    processes.sort(key=lambda x: x[2])  
    time = 0
    for pid, arrival, burst in processes:
        if time < arrival:
            time = arrival

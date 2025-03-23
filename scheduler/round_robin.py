
def round_robin(processes, time_quantum):
    print()
    print("For Round Robin")
    print()
    queue = processes[:]
    time = 0
    while queue:
        pid, arrival, burst = queue.pop(0)
        execute_time = min(time_quantum, burst)
        print(f"Process {pid} executed from {time} to {time + execute_time}")
        time += execute_time
        if burst > time_quantum:
            queue.append((pid, arrival, burst - time_quantum))


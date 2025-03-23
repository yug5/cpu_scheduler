
def round_robin(processes, time_quantum):
    queue = processes[:]
    time = 0
    while queue:
        pid, arrival, burst = queue.pop(0)
        execute_time = min(time_quantum, burst)

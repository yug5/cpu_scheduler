from scheduler.fcfs import fcfs
from scheduler.sjf import sjf
from scheduler.round_robin import round_robin
from scheduler.utils import get_process_input
from visualization import visualize_fcfs, visualize_sjf, visualize_rr

if __name__ == "__main__":
    print("Choose CPU Scheduling Algorithm:")
    print("1. First-Come, First-Serve (FCFS)")
    print("2. Shortest Job First (SJF)")
    print("3. Round Robin (RR)")
    print("4. All")
 
    choice = int(input("Enter choice (1/2/3/4): "))
    processes = get_process_input()
    
    if choice == 1:
        fcfs(processes)
        visualize_fcfs(processes)
    elif choice == 2:
        sjf(processes)
        visualize_sjf(processes)
    elif choice == 3:
        time_quantum = int(input("Enter Time Quantum for RR: "))
        round_robin(processes, time_quantum)
        visualize_rr(processes, time_quantum)
    elif choice == 4:
        time_quantum = int(input("Enter Time Quantum for RR: "))
        fcfs(processes)
        visualize_fcfs(processes)
        sjf(processes)
        visualize_sjf(processes)
        round_robin(processes, time_quantum)
        visualize_rr(processes, time_quantum)
    else:
        print("Invalid choice.")
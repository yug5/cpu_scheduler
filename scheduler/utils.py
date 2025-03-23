def get_process_input():
    n = int(input("Enter number of processes: "))
    processes = []
    for _ in range(n):
        pid = input("Enter Process ID: ")
        arrival = int(input("Enter Arrival Time: "))

# CPU Scheduling Algorithms Visualizer

A web-based visualization tool for CPU scheduling algorithms implemented using Streamlit. This application helps users understand and compare different CPU scheduling algorithms through interactive visualizations.

## Features

- Interactive visualization of three CPU scheduling algorithms:
  - First-Come, First-Serve (FCFS)
  - Shortest Job First (SJF)
  - Round Robin (RR)
- Side-by-side comparison of algorithms
- Dynamic timeline visualization with scrolling
- Performance metrics calculation:
  - Average Waiting Time
  - Average Turnaround Time
- Process-specific metrics display
- Customizable process input:
  - Process ID
  - Arrival Time
  - Burst Time
- Adjustable time quantum for Round Robin

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/cpu_scheduler.git
cd cpu_scheduler
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the Streamlit application:
```bash
streamlit run app.py
```

2. Use the sidebar to:
   - Set the number of processes
   - Input process details (ID, arrival time, burst time)
   - Set time quantum for Round Robin
   - Click "Run Comparison" to visualize

## Project Structure

```
cpu_scheduler/
├── app.py              # Main Streamlit application
├── scheduler/          # Scheduling algorithms implementation
│   ├── __init__.py
│   ├── fcfs.py        # First-Come, First-Serve implementation
│   ├── sjf.py         # Shortest Job First implementation
│   └── round_robin.py # Round Robin implementation
├── requirements.txt    # Project dependencies
└── README.md          # Project documentation
```

## Contributing

Feel free to contribute to this project by:
1. Forking the repository
2. Creating a new branch for your feature
3. Submitting a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

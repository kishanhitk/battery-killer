# Battery Killer

A sophisticated battery stress testing tool for macOS with both GUI and CLI interfaces. This tool helps test battery life under heavy CPU load while monitoring system metrics in real-time.

![Battery Killer GUI](screenshots/gui.png)

## Features

- **Real-time System Monitoring**
  - CPU usage per core
  - CPU temperature
  - Battery level and status
  - Memory usage
  - System temperature protection

- **Interactive GUI**
  - Live performance graphs
  - Real-time metric updates
  - Easy control interface
  - Temperature and CPU core configuration

- **CLI Interface**
  - ASCII graphs for performance metrics
  - Detailed logging
  - Configuration file support
  - Command-line arguments

- **Safety Features**
  - Automatic shutdown on high temperature
  - Minimum battery level protection
  - Graceful process handling
  - Configurable safety limits

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/battery-killer.git
   cd battery-killer
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install system dependencies (for temperature monitoring):
   ```bash
   brew install osx-cpu-temp
   ```

## Usage

### GUI Version

Run the graphical interface:
```bash
python battery_killer_gui.py
```

The GUI provides:
- Start/Stop button for stress testing
- CPU core count selector
- Maximum temperature limit
- Real-time performance graphs
- System status indicators

### CLI Version

Run the command-line interface:
```bash
python battery_killer.py [options]
```

Available options:
- `--config`: Path to configuration file
- `--min-battery`: Minimum battery percentage (default: 5)
- `--interval`: Check interval in seconds (default: 10)
- `--cores`: Number of CPU cores to stress
- `--max-temp`: Maximum temperature in Celsius (default: 90)
- `--no-temp-check`: Disable temperature monitoring

### Configuration

Create a `config.json` file to customize settings:
```json
{
    "min_battery": 10,
    "check_interval": 10,
    "num_cores": 8,
    "enable_gpu": false,
    "gpu_test_path": "",
    "monitor_temp": true,
    "max_temp_celsius": 90
}
```

## Project Structure

```
battery-killer/
├── README.md
├── requirements.txt
├── battery_killer/
│   ├── __init__.py
│   ├── core.py           # Core stress testing functionality
│   ├── gui.py           # GUI implementation
│   └── utils.py         # Utility functions
├── config.json          # Default configuration
└── scripts/
    ├── battery_killer.py     # CLI entry point
    └── battery_killer_gui.py # GUI entry point
```

## Development

### Prerequisites
- Python 3.8+
- macOS (tested on macOS Monterey and later)
- Homebrew (for installing osx-cpu-temp)

### Setting up development environment
1. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

2. Run tests:
   ```bash
   python -m pytest tests/
   ```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Technical Deep Dive

### How Battery Killer Works

Battery Killer leverages fundamental principles of computer architecture to create controlled CPU stress, resulting in power consumption that accelerates battery drain. Let's explore the technical details of how each component works:

#### CPU Stress Mechanism

The core stress testing strategy uses a compute-intensive algorithm that forces the CPU into high-utilization states:

1. **Floating-Point Operations**: The stress algorithm repeatedly performs CPU-intensive floating-point operations (multiplication and square root calculations) which:
   - Activate the FPU (Floating Point Unit) of the CPU
   - Force higher power states due to complex calculations
   - Prevent CPU optimization by ensuring results are used in subsequent calculations
   - Maximize heat generation and energy consumption

2. **Multi-Core Utilization**: 
   - Each physical CPU core runs its own independent Python process
   - Process isolation prevents the OS from optimizing workloads across cores
   - Ensures all cores are stressed evenly, maximizing power draw
   - Avoids inter-process communication overhead

3. **Infinite Loop Pattern**:
   ```python
   def stress_cpu():
       while True:
           x = 1234.5678
           for _ in range(1000000):
               x = x ** 2
               x = x ** 0.5
   ```
   - The value computation is mathematically designed to prevent compiler optimizations
   - The large iteration count (1,000,000) creates sustained CPU load
   - Results of calculations are fed back into the loop to prevent dead code elimination
   - The infinite outer loop ensures continuous operation until externally terminated

#### Temperature Monitoring System

Temperature monitoring uses a multi-layered approach:

1. **Primary Method**: Uses Apple's `powermetrics` tool to access the SMC (System Management Controller):
   ```python
   cmd = ['sudo', 'powermetrics', '--samplers', 'thermal', '-i1', '-n1']
   ```
   - Accesses low-level temperature sensors directly from hardware
   - Requires elevated privileges due to hardware access
   - Parses the output to extract CPU die temperature values
   - Provides accurate, real-time temperature readings

2. **Fallback Method**: Utilizes the `osx-cpu-temp` utility:
   ```python
   result = subprocess.run(['osx-cpu-temp'], capture_output=True, text=True)
   ```
   - Offers a simplified interface to temperature data
   - Works even when powermetrics fails or isn't available
   - More reliable on older macOS versions

3. **Safety Monitoring**:
   - Continuously compares measured temperatures against defined thresholds
   - Implements graceful shutdown of stress processes if temperature exceeds safe limits
   - Logs all temperature events for post-run analysis

#### Battery Level Monitoring

Battery monitoring leverages the `psutil` library to:

1. **Track Battery State**:
   ```python
   battery = psutil.sensors_battery()
   ```
   - Monitors charge percentage in real-time
   - Detects charging state (plugged in vs. battery power)
   - Calculates discharge rate by comparing sequential readings

2. **Safety Controls**:
   - Prevents battery from discharging below a configurable minimum level
   - Automatically pauses stress tests if battery gets too low
   - Resumes testing when charger is connected

#### GUI Architecture

The GUI is built using a Model-View-Controller pattern:

1. **Threading Model**:
   - Uses `QThread` to separate UI from system monitoring
   - Prevents UI freezing during intensive operations
   - Ensures responsive controls even under system stress
   - Implements proper thread synchronization with PyQt signals

2. **Real-time Graphing**:
   - Utilizes circular buffers (`collections.deque`) to store time-series data
   - Maintains fixed-size history (60 data points) for each metric
   - Updates graphs at regular intervals (every second)
   - Properly scales axis ranges to visualize trends

3. **Signal Flow**:
   ```
   Worker Thread ---> Signal Emission ---> UI Update Slots
   ```
   - Temperature and system stats are emitted as signals from the worker thread
   - UI components connect to these signals and update when data changes
   - This event-driven architecture ensures thread safety

### Why This Approach Works

1. **Power Consumption Physics**:
   - Modern CPUs follow the power equation: P = C × V² × f
   - Where:
     - P: Power consumption (watts)
     - C: Capacitance (determined by chip design)
     - V: Voltage (increases with CPU frequency/turbo)
     - f: Operating frequency
   - By maximizing CPU utilization, the voltage and frequency increase
   - Higher voltage has a squared effect on power consumption
   - This creates maximum battery drain in the shortest time

2. **Thermal Management**:
   - CPUs increase power draw when computational load rises
   - This generates heat as a byproduct of computation
   - The cooling system must work harder, drawing additional power
   - Battery Killer monitors this thermal envelope to:
     - Maximize power consumption without thermal throttling
     - Prevent damage by staying under critical thermal limits
     - Optimize for sustained high power draw

3. **Process Isolation Benefits**:
   - Running separate processes prevents the OS scheduler from optimizing
   - Each core must independently execute its workload
   - Memory is not shared between processes, requiring more cache usage
   - This circumvents CPU efficiency features, maximizing energy use

4. **Cross-Platform Considerations**:
   - macOS employs sophisticated power management
   - The approach uses direct hardware access when possible
   - Fallback mechanisms ensure compatibility across macOS versions
   - The architecture respects Apple's security model while still accessing necessary metrics

## Scientific Background

The stress test is based on several computing principles:

1. **Amdahl's Law**: By distributing work across all available cores, we maximize parallel execution and power consumption.

2. **Thermal Dynamics**: CPU power consumption follows an approximately cubic relationship with frequency, which means even small increases in clock speed result in significantly higher power draw.

3. **DVFS (Dynamic Voltage and Frequency Scaling)**: By creating sustained workloads, we force the CPU to maintain higher voltage and frequency states, preventing power-saving mechanisms from engaging.

## Effective Battery Testing

This tool provides a realistic battery stress test because:

1. It simulates actual computational workloads rather than artificial power drain
2. It exercises all major system components (CPU, memory, thermal)
3. It provides real-time monitoring of critical metrics
4. It implements safety measures to prevent damage

By combining these approaches, Battery Killer creates a controlled, measurable, and safe environment for testing battery performance under load.

## Safety Warning

⚠️ **Use this tool responsibly!**

- This tool is designed to stress test your system
- Extended use may cause battery wear
- Monitor temperature to prevent overheating
- Not recommended for production machines
- Use at your own risk

## Acknowledgments

- [psutil](https://github.com/giampaolo/psutil) for system monitoring
- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) for the GUI
- [pyqtgraph](http://www.pyqtgraph.org/) for real-time plotting
- [osx-cpu-temp](https://github.com/lavoiesl/osx-cpu-temp) for temperature monitoring

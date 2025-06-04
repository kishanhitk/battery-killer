# Battery Killer

A comprehensive battery stress testing tool for macOS with CLI-based real-time monitoring.

## Features

- Intelligent CPU stress testing with temperature monitoring
- Real-time statistics monitoring including:
  - Battery discharge rate
  - CPU temperature and usage
  - Memory usage
  - Fan speed (RPM)
  - Power consumption (Watts)
  - Disk and network I/O
  - System uptime and test duration
- Terminal-based interface with ASCII performance graphs
- Automatic throttling based on temperature thresholds
- Safety measures to prevent overheating

## Installation & Usage

### Step 1: Setup Environment

1. Clone the repository:
   ```bash
   git clone https://github.com/kishanhitk/battery-killer.git
   cd battery-killer
   ```

2. Create and activate virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Step 2: Run the Application

```bash
python3 battery_killer/scripts/battery_killer.py [options]
```

#### Command Line Options

```bash
usage: battery_killer.py [-h] [--cores CORES] [--max-temp MAX_TEMP] [--duration DURATION] [--verbose]

Battery Killer - A CPU stress testing tool

options:
  -h, --help            show this help message and exit
  --cores CORES         Number of CPU cores to use (default: all physical cores)
  --max-temp MAX_TEMP   Maximum CPU temperature in Celsius (default: 90°C)
  --duration DURATION   Duration of stress test in minutes (default: 0 = run until stopped)
  --verbose, -v         Show verbose output
```

#### Examples

```bash
# Basic usage - run until stopped
python3 battery_killer/scripts/battery_killer.py

# Run for 10 minutes with verbose output
python3 battery_killer/scripts/battery_killer.py --duration 10 --verbose

# Use 4 cores with 85°C temperature limit
python3 battery_killer/scripts/battery_killer.py --cores 4 --max-temp 85
```

## Requirements

- macOS 10.14 or higher
- Python 3.8 or higher
- Administrative privileges (for temperature monitoring)

### Dependencies

- psutil
- asciichartpy

## Project Structure

```
battery-killer/
├── README.md
├── requirements.txt
├── battery_killer/
│   ├── __init__.py
│   ├── core.py           # Core stress testing functionality
│   ├── utils.py         # Utility functions
│   └── scripts/
│       └── battery_killer.py     # Main CLI script
└── venv/                 # Virtual environment (created during setup)
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

#### Terminal Interface Architecture

The application uses a simple, efficient terminal-based architecture:

1. **Real-time Statistics Display**:
   - Clean, formatted output with live system metrics
   - Tabular format showing CPU, temperature, memory, battery, etc.
   - Updates every few seconds with current system state

2. **ASCII Chart Generation**:
   - Historical data visualization using ASCII characters
   - Circular buffers to maintain recent data points
   - Automatic scaling for optimal chart display

3. **Responsive Monitoring**:
   - Non-blocking system monitoring
   - Graceful shutdown with Ctrl+C
   - Real-time temperature safety checks

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
- [asciichartpy](https://github.com/kroitor/asciichart) for ASCII charts
- [osx-cpu-temp](https://github.com/lavoiesl/osx-cpu-temp) for temperature monitoring

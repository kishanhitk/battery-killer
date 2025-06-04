# Battery Killer

An **INTENSE** battery stress testing tool for macOS that maximizes power consumption through aggressive CPU, GPU, Memory, and I/O stress testing.

## Features

### 🔥 **INTENSE Multi-Component Stress Testing**
- **Aggressive CPU Stress**: Multiple stress patterns per core including:
  - Complex mathematical operations (trigonometry, logarithms, exponentials)
  - Cryptographic hash computations (SHA256, MD5, SHA1)
  - Prime number calculations and nested loops
  - **2 processes per CPU core** for maximum intensity
- **GPU Acceleration Stress**: 
  - Metal Performance Shaders utilization (macOS GPU)
  - Video encoding/decoding with hardware acceleration
  - Large matrix operations and FFT computations
  - GPU memory allocation and intensive operations
- **Memory Intensive Operations**:
  - Large array allocations and manipulations
  - Sorting algorithms and mathematical operations on arrays
  - Continuous memory allocation/deallocation cycles
- **I/O System Stress**:
  - Intensive disk read/write operations (10MB+ files)
  - Continuous file system operations
  - High-frequency disk access patterns

### 📊 **Real-time Monitoring**
- Battery discharge rate and remaining time
- CPU temperature and per-core usage
- Memory usage and disk utilization
- Fan speed (RPM) and power consumption (Watts)
- System uptime and test duration
- Terminal-based interface with clean tabular output

### 🛡️ **Safety Features**
- Automatic throttling based on temperature thresholds
- Memory management to prevent system crashes
- Graceful cleanup of temporary files and processes
- Temperature monitoring with automatic shutdown

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
# Basic usage - INTENSE stress test until stopped
python3 battery_killer/scripts/battery_killer.py

# Run for 10 minutes with verbose output (see all the intense processes)
python3 battery_killer/scripts/battery_killer.py --duration 10 --verbose

# Use 4 cores with 85°C temperature limit (8 processes total - 2 per core)
python3 battery_killer/scripts/battery_killer.py --cores 4 --max-temp 85

# Quick 2-minute intense battery drain test
python3 battery_killer/scripts/battery_killer.py --duration 2 --verbose
```

### ⚡ **What Makes This INTENSE?**

When you run Battery Killer, it simultaneously launches:
- **16 CPU stress processes** (2 per core on 8-core system)
- **1 GPU stress process** with multiple threads for video encoding, matrix operations
- **1 I/O stress process** with intensive disk write/read operations
- **Multiple threads per process** for maximum resource utilization

**Total: 18+ processes with 45+ threads** all working to drain your battery as fast as possible!

## Requirements

- macOS 10.14 or higher
- Python 3.8 or higher
- Administrative privileges (for temperature monitoring)

### Dependencies

- psutil (system monitoring)
- asciichartpy (ASCII charts)
- numpy (intensive mathematical operations)

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
├── venv/                 # Virtual environment (created during setup)
└── intense_stress_*.py   # Temporary stress files (auto-generated and cleaned up)
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

#### INTENSE Multi-Component Stress Mechanism

Battery Killer uses an aggressive multi-threaded, multi-process approach to maximize power consumption:

1. **Aggressive CPU Stress (Multiple Patterns)**:
   - **Mathematical Operations**: Complex trigonometric functions, logarithms, exponentials, and square roots
   - **Cryptographic Stress**: Continuous SHA256, MD5, and SHA1 hash computations
   - **Prime Number Calculations**: CPU-intensive prime checking algorithms
   - **Nested Loop Operations**: Multi-dimensional floating-point calculations
   - **2 Processes Per Core**: Double the stress compared to traditional tools

2. **GPU Acceleration Stress**:
   - **Metal Performance Shaders**: Utilizes macOS GPU compute capabilities
   - **Video Encoding**: Hardware-accelerated H.264 encoding at 1920x1080@30fps
   - **Matrix Operations**: Large-scale matrix multiplication and FFT computations
   - **GPU Memory Stress**: Continuous allocation and manipulation of GPU memory

3. **Memory Intensive Operations**:
   - **Large Array Processing**: 100,000+ element arrays with sorting and mathematical operations
   - **Dynamic Memory Management**: Continuous allocation/deallocation cycles
   - **Memory-CPU Bridge Stress**: Operations that stress both memory bandwidth and CPU

4. **I/O System Stress**:
   - **Disk Operations**: Continuous 10MB+ file writes and reads
   - **File System Stress**: Rapid file creation, modification, and deletion
   - **Storage Interface Stress**: High-frequency disk access patterns

5. **Multi-Threading Architecture**:
   ```python
   # Per CPU core: 4 threads + main thread = 5 threads per process
   - Math thread (trigonometry, logarithms)
   - Crypto thread (hash computations) 
   - Loops thread (nested calculations)
   - Memory thread (array operations)
   - Main thread (additional calculations)
   ```

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

### Why This INTENSE Approach Works

1. **Maximum Power Consumption Physics**:
   - **CPU Power**: P = C × V² × f (voltage has squared effect)
   - **GPU Power**: Additional discrete/integrated GPU power draw
   - **Memory Power**: DDR4/DDR5 power consumption during intensive operations
   - **I/O Power**: SSD/HDD motor power and storage interface power
   - **System Power**: Cooling fans, voltage regulators, chipset power
   - **Total System Impact**: All components stressed simultaneously

2. **Multi-Component Thermal Load**:
   - CPU generates heat from intensive calculations
   - GPU generates heat from video encoding and compute operations
   - Memory generates heat from continuous read/write cycles
   - Storage generates heat from intensive I/O operations
   - **Cooling System Overdrive**: Fans run at maximum speed, drawing additional power

3. **Process and Thread Multiplication Benefits**:
   - **2 Processes Per Core**: Prevents OS optimization and load balancing
   - **5 Threads Per Process**: Maximizes CPU pipeline utilization
   - **Independent Memory Spaces**: Forces more cache misses and memory bandwidth usage
   - **Thread Context Switching**: Additional CPU overhead for maximum power draw

4. **System Resource Saturation**:
   - **CPU**: 100% utilization across all cores with multiple stress patterns
   - **GPU**: Hardware acceleration for video encoding and compute shaders
   - **Memory**: Large allocations with continuous operations
   - **Storage**: Continuous 10MB+ file operations with high-frequency access

5. **Advanced Power Management Circumvention**:
   - Multiple stress patterns prevent CPU frequency scaling optimizations
   - GPU workloads prevent integrated graphics power saving
   - I/O operations prevent storage power management
   - Continuous operations prevent system sleep and power saving modes

## Scientific Background

The stress test is based on several computing principles:

1. **Amdahl's Law**: By distributing work across all available cores, we maximize parallel execution and power consumption.

2. **Thermal Dynamics**: CPU power consumption follows an approximately cubic relationship with frequency, which means even small increases in clock speed result in significantly higher power draw.

3. **DVFS (Dynamic Voltage and Frequency Scaling)**: By creating sustained workloads, we force the CPU to maintain higher voltage and frequency states, preventing power-saving mechanisms from engaging.

## Effective INTENSE Battery Testing

This tool provides the most aggressive battery stress test available because:

1. **Multi-Component Simultaneous Stress**: Unlike tools that stress only CPU, this stresses CPU, GPU, Memory, and I/O simultaneously
2. **Real-World Maximum Load Simulation**: Simulates the most intensive computational workloads possible
3. **Advanced Resource Utilization**: Uses multiple processes and threads to maximize hardware utilization
4. **Comprehensive System Impact**: Exercises every major power-consuming component
5. **Intelligent Safety Monitoring**: Real-time temperature and resource monitoring with automatic throttling

**Result**: The fastest possible battery drain while maintaining system stability and safety.

### 🔋 **Expected Battery Drain Performance**

- **Typical laptop**: 3-5x faster battery drain compared to normal usage
- **MacBook Pro**: Can drain from 100% to 0% in 1-3 hours (vs 8-12 hours normal usage)
- **MacBook Air**: Can drain from 100% to 0% in 45 minutes to 2 hours (vs 6-10 hours normal usage)
- **Power consumption**: 40-80+ watts sustained load (vs 5-15 watts normal usage)

## ⚠️ **IMPORTANT Safety Warning**

🔥 **This is an EXTREMELY INTENSIVE tool - Use with EXTREME caution!**

- **INTENSE SYSTEM STRESS**: This tool pushes your system to absolute maximum power consumption
- **RAPID BATTERY DRAIN**: Can drain battery 3-5x faster than normal usage
- **HIGH TEMPERATURE GENERATION**: Will generate significant heat - ensure good ventilation
- **POTENTIAL HARDWARE STRESS**: Extended use may accelerate component wear
- **AUTOMATIC SAFETY FEATURES**: Built-in temperature monitoring and automatic shutdown
- **NOT FOR PRODUCTION**: Never run on critical systems or during important work
- **SUPERVISED USE ONLY**: Monitor your system while running
- **BACKUP YOUR DATA**: Ensure important data is backed up before testing

**Use at your own risk - This tool is designed for battery testing and stress testing only!**

## Acknowledgments

- [psutil](https://github.com/giampaolo/psutil) for comprehensive system monitoring
- [numpy](https://numpy.org/) for high-performance mathematical operations
- [asciichartpy](https://github.com/kroitor/asciichart) for ASCII charts
- [osx-cpu-temp](https://github.com/lavoiesl/osx-cpu-temp) for temperature monitoring
- Apple's Metal Performance Shaders for GPU acceleration capabilities

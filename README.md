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

import subprocess
import time
import psutil
import logging
import os
from collections import deque
from .utils import get_cpu_temperature, create_ascii_graph

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('battery_killer.log')
    ]
)
logger = logging.getLogger(__name__)

class SystemStresser:
    def __init__(self, config=None):
        self.config = config or {
            'min_battery': 5,
            'check_interval': 10,
            'num_cores': psutil.cpu_count(),
            'enable_gpu': False,
            'gpu_test_path': '',
            'monitor_temp': True,
            'max_temp_celsius': 90,
            'history_points': 60  # Keep 60 data points for graphs
        }
        self.cpu_processes = []
        self.gpu_proc = None
        
        # Initialize history tracking
        self.temp_history = deque(maxlen=self.config['history_points'])
        self.cpu_history = deque(maxlen=self.config['history_points'])
        self.battery_history = deque(maxlen=self.config['history_points'])
        self.memory_history = deque(maxlen=self.config['history_points'])
        
    def get_system_stats(self):
        """Get current system statistics."""
        # Calculate disk usage percentage
        disk_usage = psutil.disk_usage('/')
        disk_usage_percent = (disk_usage.used / disk_usage.total) * 100
        
        stats = {
            'cpu_percent': psutil.cpu_percent(interval=1, percpu=True),
            'memory_percent': psutil.virtual_memory().percent,
            'battery': psutil.sensors_battery(),
            'disk_usage': disk_usage_percent,
        }
        
        # Get CPU temperature
        temp = get_cpu_temperature()
        if temp is not None:
            stats['cpu_temp'] = temp
            
        # Update history
        self.temp_history.append(stats.get('cpu_temp', 0))
        self.cpu_history.append(sum(stats['cpu_percent']) / len(stats['cpu_percent']))
        self.battery_history.append(stats['battery'].percent)
        self.memory_history.append(stats['memory_percent'])
        
        return stats

    def create_graph(self, data, title, height=10):
        """Create ASCII graph from data."""
        if not data:
            return ""
        
        # Convert deque to list and ensure we have float values
        data_list = [float(x) if x is not None else 0.0 for x in list(data)]
        
        if not data_list or all(x == 0 for x in data_list):
            return f"\n{title}\nNo data yet..."
        
        try:
            graph = f"\n{title}\n"
            graph += create_ascii_graph(data_list, height)
            return graph
        except Exception as e:
            logger.error(f"Failed to create graph for {title}: {e}")
            return f"\n{title}\nGraph generation failed"

    def log_system_stats(self):
        """Log current system statistics."""
        stats = self.get_system_stats()
        battery = stats['battery']
        
        # Clear screen and move cursor to top
        print("\033[2J\033[H")
        
        # Print status in a more readable format
        print("=" * 80)
        print("Battery Killer - System Status")
        print("=" * 80)
        
        # Current values
        print(f"Battery: {battery.percent}% {'[Charging]' if battery.power_plugged else '[Discharging]'}")
        print(f"Time remaining: {int(battery.secsleft/60)} minutes" if battery.secsleft > 0 else "Time remaining: Unknown")
        
        if 'cpu_temp' in stats:
            print(f"\nCPU Temperature: {stats['cpu_temp']:.1f}°C")
        
        print("\nCPU Usage:")
        total_cpu = 0
        for i, usage in enumerate(stats['cpu_percent']):
            print(f"Core {i}: {usage:>5.1f}%")
            total_cpu += usage
        print(f"Average CPU: {total_cpu/len(stats['cpu_percent']):>5.1f}%")
        
        print(f"\nMemory Usage: {stats['memory_percent']:.1f}%")
        
        # Graphs section
        print("\nHistorical Data (Last {} readings)".format(self.config['history_points']))
        print("-" * 80)
        
        # Temperature graph
        if any(self.temp_history):
            temp_min = min(x for x in self.temp_history if x is not None and x > 0)
            temp_max = max(x for x in self.temp_history if x is not None)
            print(f"Temperature Range: {temp_min:.1f}°C - {temp_max:.1f}°C")
        print(self.create_graph(self.temp_history, "CPU Temperature (°C)"))
        
        # CPU Usage graph
        if any(self.cpu_history):
            cpu_min = min(self.cpu_history)
            cpu_max = max(self.cpu_history)
            print(f"CPU Usage Range: {cpu_min:.1f}% - {cpu_max:.1f}%")
        print(self.create_graph(self.cpu_history, "Average CPU Usage (%)"))
        
        # Battery graph
        if any(self.battery_history):
            bat_min = min(self.battery_history)
            bat_max = max(self.battery_history)
            print(f"Battery Range: {bat_min:.1f}% - {bat_max:.1f}%")
        print(self.create_graph(self.battery_history, "Battery Level (%)"))
        
        # Memory graph
        if any(self.memory_history):
            mem_min = min(self.memory_history)
            mem_max = max(self.memory_history)
            print(f"Memory Range: {mem_min:.1f}% - {mem_max:.1f}%")
        print(self.create_graph(self.memory_history, "Memory Usage (%)"))
        
        # System Info
        print("\nSystem Information:")
        print("-" * 80)
        print(f"CPU Cores: {psutil.cpu_count()} (Physical: {psutil.cpu_count(logical=False)})")
        print(f"Total Memory: {psutil.virtual_memory().total / (1024**3):.1f} GB")
        print(f"Swap Usage: {psutil.swap_memory().percent}%")
        
        # Active processes
        print("\nActive Stress Processes:")
        print("-" * 80)
        print(f"CPU Processes: {len(self.cpu_processes)}")
        print(f"GPU Process: {'Active' if self.gpu_proc else 'Inactive'}")
        
        print("\nPress Ctrl+C to stop")
        print("=" * 80)

    def check_temperature(self):
        """Check if system temperature is within safe limits."""
        temp = get_cpu_temperature()
        if temp is not None and temp > self.config['max_temp_celsius']:
            logger.warning(f"Temperature too high: {temp}°C")
            return False
        return True

    def start_stress_tasks(self):
        """Start CPU and GPU stress tasks."""
        logger.info(f"Starting stress test with {self.config['num_cores']} CPU cores")
        
        # CPU stress: Run python to max out CPU instead of 'yes'
        cpu_stress_code = """
import multiprocessing

def stress_cpu():
    while True:
        x = 1234.5678
        for _ in range(1000000):
            x = x ** 2
            x = x ** 0.5

if __name__ == '__main__':
    stress_cpu()
"""
        # Write the stress code to a temporary file
        with open('stress_cpu.py', 'w') as f:
            f.write(cpu_stress_code)
        
        # Start CPU stress processes
        for _ in range(self.config['num_cores']):
            proc = subprocess.Popen(['python3', 'stress_cpu.py'],
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL)
            self.cpu_processes.append(proc)
            logger.debug(f"Started CPU stress process {proc.pid}")
        
        # GPU stress if enabled
        if self.config['enable_gpu'] and self.config['gpu_test_path']:
            try:
                self.gpu_proc = subprocess.Popen(
                    [self.config['gpu_test_path'], '/test=fur'],
                    cwd=os.path.dirname(self.config['gpu_test_path'])
                )
                logger.info("Started GPU stress test")
            except Exception as e:
                logger.error(f"Failed to start GPU stress test: {e}")

    def stop_stress_tasks(self):
        """Stop all stress tasks."""
        logger.info("Stopping all stress tasks")
        
        # Kill CPU stress processes
        for proc in self.cpu_processes:
            try:
                proc.kill()
                logger.debug(f"Killed CPU process {proc.pid}")
            except Exception as e:
                logger.error(f"Failed to kill process {proc.pid}: {e}")
        self.cpu_processes.clear()
        
        # Kill GPU stress process if it exists
        if self.gpu_proc:
            try:
                self.gpu_proc.kill()
                logger.info("Killed GPU process")
            except Exception as e:
                logger.error(f"Failed to kill GPU process: {e}")
            self.gpu_proc = None

    def run(self):
        """Main stress test loop."""
        logger.info("Starting battery drain script. Unplug charger to begin stress tasks.")
        logger.info(f"Configuration: {self.config}")
        
        try:
            while True:
                battery = psutil.sensors_battery()
                if battery is None:
                    logger.error("Battery status unavailable. Exiting.")
                    break
                
                self.log_system_stats()
                
                # Run stress tasks when unplugged and battery > min_battery
                if not battery.power_plugged and battery.percent > self.config['min_battery']:
                    logger.info(f"Battery at {battery.percent}%. Starting stress tasks...")
                    self.start_stress_tasks()
                    
                    # Keep running until plugged in or battery drops below minimum
                    while True:
                        battery = psutil.sensors_battery()
                        self.log_system_stats()
                        
                        if (battery.power_plugged or 
                            battery.percent <= self.config['min_battery'] or 
                            (self.config['monitor_temp'] and not self.check_temperature())):
                            
                            logger.info(f"Stopping condition met. Battery: {battery.percent}%")
                            self.stop_stress_tasks()
                            break
                            
                        time.sleep(self.config['check_interval'])
                else:
                    if battery.power_plugged:
                        logger.info(f"Charger plugged in. Battery at {battery.percent}%")
                    else:
                        logger.info(f"Battery at {battery.percent}%. Too low to stress.")
                
                time.sleep(self.config['check_interval'])
                
        except KeyboardInterrupt:
            logger.info("Script terminated by user.")
        finally:
            self.stop_stress_tasks()


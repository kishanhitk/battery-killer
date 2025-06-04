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
        """Start intensive CPU, GPU, Memory, and I/O stress tasks."""
        logger.info(f"Starting INTENSE stress test with {self.config['num_cores']} CPU cores")
        
        # INTENSE CPU stress: Multiple stress patterns per core
        intense_cpu_stress_code = """
import multiprocessing
import threading
import math
import random
import hashlib
import time

def cpu_intensive_math():
    \"\"\"Intensive mathematical operations\"\"\"
    while True:
        # Complex mathematical operations
        for i in range(50000):
            x = random.random() * 1000
            # Trigonometric functions (CPU intensive)
            result = math.sin(x) * math.cos(x) * math.tan(x)
            result = math.sqrt(abs(result)) ** 2.5
            result = math.log(abs(result) + 1) * math.exp(result % 1)
            # Prime number checking (CPU intensive)
            n = int(abs(result * 1000)) + 2
            for j in range(2, int(math.sqrt(n)) + 1):
                if n % j == 0:
                    break

def cpu_intensive_crypto():
    \"\"\"Intensive cryptographic operations\"\"\"
    while True:
        # Hash computations (CPU intensive)
        data = str(random.random() * 1000000).encode()
        for _ in range(10000):
            data = hashlib.sha256(data).digest()
            data = hashlib.md5(data).digest()
            data = hashlib.sha1(data).digest()

def cpu_intensive_loops():
    \"\"\"Intensive nested loops\"\"\"
    while True:
        # Nested loops with floating point operations
        total = 0.0
        for i in range(1000):
            for j in range(1000):
                total += (i * j) ** 0.5
                total = total % 1000000

def memory_intensive():
    \"\"\"Memory allocation and operations\"\"\"
    arrays = []
    while True:
        try:
            # Allocate large arrays and perform operations
            arr = [random.random() for _ in range(100000)]
            # Sort operations (CPU + Memory intensive)
            arr.sort()
            arr.reverse()
            # Mathematical operations on arrays
            result = sum(x ** 2 for x in arr[:10000])
            arrays.append(arr[:1000])  # Keep some data in memory
            
            # Limit memory usage to prevent system crash
            if len(arrays) > 50:
                arrays = arrays[-25:]  # Keep only recent arrays
        except MemoryError:
            arrays = arrays[-10:]  # Reduce memory if needed

def stress_cpu_core():
    \"\"\"Main stress function combining all intensive operations\"\"\"
    # Start multiple threads per core for maximum intensity
    threads = []
    
    # Math thread
    t1 = threading.Thread(target=cpu_intensive_math, daemon=True)
    threads.append(t1)
    
    # Crypto thread  
    t2 = threading.Thread(target=cpu_intensive_crypto, daemon=True)
    threads.append(t2)
    
    # Loops thread
    t3 = threading.Thread(target=cpu_intensive_loops, daemon=True)
    threads.append(t3)
    
    # Memory thread
    t4 = threading.Thread(target=memory_intensive, daemon=True)
    threads.append(t4)
    
    # Start all threads
    for t in threads:
        t.start()
    
    # Keep main thread busy too
    while True:
        x = random.random() * 1000
        for _ in range(100000):
            x = x ** 2.5
            x = math.sqrt(abs(x))
            x = x % 1000

if __name__ == '__main__':
    stress_cpu_core()
"""
        
        # Write the intense stress code to a temporary file
        with open('intense_stress_cpu.py', 'w') as f:
            f.write(intense_cpu_stress_code)
        
        # Start multiple CPU stress processes per core for maximum intensity
        processes_per_core = 2  # Run 2 processes per core for extra intensity
        total_processes = self.config['num_cores'] * processes_per_core
        
        logger.info(f"Starting {total_processes} intense CPU stress processes ({processes_per_core} per core)")
        
        for i in range(total_processes):
            proc = subprocess.Popen(['python3', 'intense_stress_cpu.py'],
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL)
            self.cpu_processes.append(proc)
            logger.debug(f"Started intense CPU stress process {proc.pid}")
        
        # GPU stress using Metal Performance Shaders (macOS GPU acceleration)
        self._start_gpu_stress()
        
        # I/O stress for additional battery drain
        self._start_io_stress()

    def _start_gpu_stress(self):
        """Start GPU stress using Metal compute shaders and other GPU-intensive tasks."""
        gpu_stress_code = """
import subprocess
import threading
import time
import random
import os

def metal_compute_stress():
    \"\"\"Use Metal Performance Shaders for GPU computation\"\"\"
    try:
        # Create a simple Metal compute shader stress test
        metal_code = '''
#include <metal_stdlib>
using namespace metal;

kernel void intensive_compute(device float* data [[buffer(0)]],
                             uint index [[thread_position_in_grid]]) {
    float value = data[index];
    for (int i = 0; i < 10000; i++) {
        value = sin(value) * cos(value) + sqrt(abs(value));
        value = pow(value, 1.5) + log(abs(value) + 1.0);
    }
    data[index] = value;
}
'''
        # This would require Metal compilation, so we'll use alternative GPU stress
        pass
    except:
        pass

def opengl_stress():
    \"\"\"OpenGL rendering stress (if available)\"\"\"
    try:
        # Try to stress GPU with OpenGL operations
        import subprocess
        # Use system GPU stress tools if available
        subprocess.run(['yes'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        pass

def video_encoding_stress():
    \"\"\"Video encoding/decoding for GPU stress\"\"\"
    try:
        # Use ffmpeg for GPU-accelerated video processing if available
        cmd = [
            'ffmpeg', '-f', 'lavfi', '-i', 'testsrc2=duration=3600:size=1920x1080:rate=30',
            '-c:v', 'h264_videotoolbox', '-b:v', '50M', '-f', 'null', '-'
        ]
        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        # Fallback: CPU-based video processing
        while True:
            # Simulate video processing with intensive calculations
            data = [random.random() for _ in range(1920*1080)]
            # Simulate frame processing
            for i in range(len(data)):
                data[i] = (data[i] * 255) ** 0.5
            time.sleep(0.001)  # Small delay to prevent complete system freeze

def gpu_memory_stress():
    \"\"\"Stress GPU memory allocation\"\"\"
    try:
        # Try to allocate and use GPU memory
        import numpy as np
        arrays = []
        while True:
            try:
                # Create large arrays for GPU-like operations
                arr = np.random.random((1000, 1000)).astype(np.float32)
                # Matrix operations (can use GPU acceleration)
                result = np.dot(arr, arr.T)
                result = np.fft.fft2(result)
                arrays.append(result[:100, :100])  # Keep some data
                
                if len(arrays) > 20:
                    arrays = arrays[-10:]
            except:
                arrays = arrays[-5:] if arrays else []
                time.sleep(0.1)
    except ImportError:
        # Fallback without numpy
        while True:
            data = [[random.random() for _ in range(1000)] for _ in range(1000)]
            # Matrix multiplication simulation
            for i in range(100):
                for j in range(100):
                    sum_val = sum(data[i][k] * data[k][j] for k in range(100))

if __name__ == '__main__':
    # Start multiple GPU stress threads
    threads = []
    
    # Video encoding thread
    t1 = threading.Thread(target=video_encoding_stress, daemon=True)
    threads.append(t1)
    
    # GPU memory thread
    t2 = threading.Thread(target=gpu_memory_stress, daemon=True)
    threads.append(t2)
    
    # OpenGL thread
    t3 = threading.Thread(target=opengl_stress, daemon=True)
    threads.append(t3)
    
    for t in threads:
        t.start()
    
    # Keep main thread busy
    metal_compute_stress()
"""
        
        try:
            with open('intense_stress_gpu.py', 'w') as f:
                f.write(gpu_stress_code)
            
            # Start GPU stress process
            self.gpu_proc = subprocess.Popen(['python3', 'intense_stress_gpu.py'],
                                           stdout=subprocess.DEVNULL,
                                           stderr=subprocess.DEVNULL)
            logger.info("Started intense GPU stress test")
        except Exception as e:
            logger.warning(f"Could not start GPU stress test: {e}")

    def _start_io_stress(self):
        """Start I/O stress for additional battery drain."""
        io_stress_code = """
import threading
import time
import random
import os
import tempfile

def disk_write_stress():
    \"\"\"Intensive disk write operations\"\"\"
    temp_dir = tempfile.mkdtemp()
    file_count = 0
    
    while True:
        try:
            # Write large files continuously
            filename = os.path.join(temp_dir, f'stress_file_{file_count}.tmp')
            with open(filename, 'wb') as f:
                # Write 10MB of random data
                data = os.urandom(10 * 1024 * 1024)
                f.write(data)
                f.flush()
                os.fsync(f.fileno())  # Force write to disk
            
            file_count += 1
            
            # Clean up old files to prevent disk full
            if file_count > 10:
                old_file = os.path.join(temp_dir, f'stress_file_{file_count-10}.tmp')
                try:
                    os.remove(old_file)
                except:
                    pass
                    
        except Exception as e:
            time.sleep(0.1)

def disk_read_stress():
    \"\"\"Intensive disk read operations\"\"\"
    while True:
        try:
            # Read system files continuously
            files_to_read = ['/usr/bin/python3', '/bin/bash', '/usr/lib/dyld']
            for filepath in files_to_read:
                try:
                    with open(filepath, 'rb') as f:
                        # Read in chunks
                        while True:
                            chunk = f.read(1024 * 1024)  # 1MB chunks
                            if not chunk:
                                break
                except:
                    pass
        except:
            time.sleep(0.1)

def network_stress():
    \"\"\"Network I/O stress\"\"\"
    import socket
    import urllib.request
    
    while True:
        try:
            # DNS lookups
            socket.gethostbyname('google.com')
            socket.gethostbyname('apple.com')
            socket.gethostbyname('github.com')
            
            # HTTP requests (if network available)
            try:
                urllib.request.urlopen('http://httpbin.org/get', timeout=1)
            except:
                pass
                
        except:
            pass
        time.sleep(0.1)

if __name__ == '__main__':
    # Start I/O stress threads
    threads = []
    
    # Disk write thread
    t1 = threading.Thread(target=disk_write_stress, daemon=True)
    threads.append(t1)
    
    # Disk read thread
    t2 = threading.Thread(target=disk_read_stress, daemon=True)
    threads.append(t2)
    
    # Network thread
    t3 = threading.Thread(target=network_stress, daemon=True)
    threads.append(t3)
    
    for t in threads:
        t.start()
    
    # Keep main thread alive
    while True:
        time.sleep(1)
"""
        
        try:
            with open('intense_stress_io.py', 'w') as f:
                f.write(io_stress_code)
            
            # Start I/O stress process
            io_proc = subprocess.Popen(['python3', 'intense_stress_io.py'],
                                     stdout=subprocess.DEVNULL,
                                     stderr=subprocess.DEVNULL)
            self.cpu_processes.append(io_proc)  # Add to processes list for cleanup
            logger.info("Started intense I/O stress test")
        except Exception as e:
            logger.warning(f"Could not start I/O stress test: {e}")

    def stop_stress_tasks(self):
        """Stop all stress tasks and clean up temporary files."""
        logger.info("Stopping all intense stress tasks")
        
        # Kill all CPU and I/O stress processes
        for proc in self.cpu_processes:
            try:
                proc.kill()
                logger.debug(f"Killed stress process {proc.pid}")
            except Exception as e:
                logger.error(f"Failed to kill process {proc.pid}: {e}")
        self.cpu_processes.clear()
        
        # Kill GPU stress process if it exists
        if self.gpu_proc:
            try:
                self.gpu_proc.kill()
                logger.info("Killed GPU stress process")
            except Exception as e:
                logger.error(f"Failed to kill GPU process: {e}")
            self.gpu_proc = None
        
        # Clean up temporary stress files
        temp_files = [
            'intense_stress_cpu.py',
            'intense_stress_gpu.py', 
            'intense_stress_io.py',
            'stress_cpu.py'  # Legacy file
        ]
        
        for temp_file in temp_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                    logger.debug(f"Cleaned up temporary file: {temp_file}")
            except Exception as e:
                logger.warning(f"Could not remove temporary file {temp_file}: {e}")

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


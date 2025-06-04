import psutil
import time
import subprocess
import logging
import asciichartpy

logger = logging.getLogger(__name__)

def get_cpu_temperature():
    """Get CPU temperature using powermetrics or osx-cpu-temp."""
    try:
        # Try powermetrics first
        cmd = ['sudo', 'powermetrics', '--samplers', 'thermal', '-i1', '-n1']
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            for line in result.stdout.split('\n'):
                if 'CPU die temperature' in line:
                    return float(line.split(':')[1].strip().split()[0])
    except Exception as e:
        logger.warning(f"Could not get CPU temperature using powermetrics: {e}")

    try:
        # Fallback to osx-cpu-temp
        result = subprocess.run(['osx-cpu-temp'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            temp = float(result.stdout.strip().replace('°C', ''))
            return temp
    except Exception as e:
        logger.warning(f"Could not get CPU temperature using osx-cpu-temp: {e}")

    return None

def get_battery_discharge_rate():
    """Calculate the battery discharge rate in % per hour."""
    try:
        # Take two battery readings 5 seconds apart
        battery1 = psutil.sensors_battery()
        if not battery1 or battery1.power_plugged:
            return None
        
        time.sleep(5)  # Wait 5 seconds
        battery2 = psutil.sensors_battery()
        if not battery2 or battery2.power_plugged:
            return None
        
        # Calculate the discharge rate per hour
        percent_diff = battery1.percent - battery2.percent
        hours_fraction = 5 / 3600  # 5 seconds as fraction of hour
        discharge_rate = percent_diff / hours_fraction if hours_fraction > 0 else 0
        
        return discharge_rate
    except Exception as e:
        logger.warning(f"Could not calculate battery discharge rate: {e}")
        return None

def get_fan_speed():
    """Get fan speed in RPM using powermetrics."""
    try:
        cmd = ['sudo', 'powermetrics', '--samplers', 'smc', '-i1', '-n1']
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            for line in result.stdout.split('\n'):
                if 'Fan' in line and 'rpm' in line:
                    return int(line.split(':')[1].strip().split()[0])
    except Exception as e:
        logger.debug(f"Could not get fan speed: {e}")
    return None

def get_power_stats():
    """Get CPU power stats in watts using powermetrics."""
    try:
        cmd = ['sudo', 'powermetrics', '--samplers', 'cpu_power', '-i1', '-n1']
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            power_stats = {}
            for line in result.stdout.split('\n'):
                if 'CPU Power' in line and 'mW' in line:
                    # Convert mW to W
                    power_stats['cpu_power'] = float(line.split(':')[1].strip().split()[0]) / 1000
                if 'GPU Power' in line and 'mW' in line:
                    power_stats['gpu_power'] = float(line.split(':')[1].strip().split()[0]) / 1000
                    
            return power_stats
    except Exception as e:
        logger.debug(f"Could not get power stats: {e}")
    return {}

def get_detailed_system_stats():
    """Get detailed system statistics."""
    # Calculate disk usage percentage
    disk_usage = psutil.disk_usage('/')
    disk_usage_percent = (disk_usage.used / disk_usage.total) * 100
    
    stats = {
        'cpu_percent': psutil.cpu_percent(interval=0.1, percpu=True),
        'memory_percent': psutil.virtual_memory().percent,
        'battery': psutil.sensors_battery(),
        'disk_io': psutil.disk_io_counters(),
        'network': psutil.net_io_counters(),
        'disk_usage': disk_usage_percent,
        'swap_percent': psutil.swap_memory().percent,
        'boot_time': psutil.boot_time(),
        'uptime': time.time() - psutil.boot_time()
    }
    
    # Add CPU temperature
    temp = get_cpu_temperature()
    if temp is not None:
        stats['cpu_temp'] = temp
    
    # Try to get fan speed
    fan_speed = get_fan_speed()
    if fan_speed is not None:
        stats['fan_speed'] = fan_speed
        
    # Try to get power stats
    power_stats = get_power_stats()
    if power_stats:
        for key, value in power_stats.items():
            stats[key] = value
            
    return stats

def create_ascii_graph(data, title, width=60, height=15):
    """Create an ASCII graph from data points."""
    if not data:
        return ""
    
    config = {
        'height': height,
        'colors': [
            asciichartpy.blue,
            asciichartpy.green,
            asciichartpy.yellow,
            asciichartpy.red,
        ]
    }
    
    # Ensure we only show the last 'width' points
    if len(data) > width:
        data = data[-width:]
    
    graph = asciichartpy.plot(data, config)
    lines = graph.split('\n')
    
    # Add title
    max_line_length = max(len(line) for line in lines)
    title_line = title.center(max_line_length)
    
    return f"{title_line}\n{graph}"

def format_time_delta(seconds):
    """Format seconds into human readable time delta."""
    hours, remainder = divmod(int(seconds), 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def format_bytes(bytes, suffix="B"):
    """Format bytes to human readable format."""
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < 1024.0:
            return f"{bytes:.2f} {unit}{suffix}"
        bytes /= 1024.0
    return f"{bytes:.2f} E{suffix}"

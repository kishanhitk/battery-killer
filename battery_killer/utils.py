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

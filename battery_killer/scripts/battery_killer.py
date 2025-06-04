#!/usr/bin/env python3
import sys
import os
import time
import argparse
import signal
import logging

# Add the parent directory to the Python path so we can import battery_killer modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from battery_killer.core import SystemStresser
from battery_killer.utils import format_time_delta, format_bytes

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print("\nExiting gracefully...")
    stresser.stop_stress_tasks()
    sys.exit(0)

def print_stats_line(stats, start_time, show_header=False):
    """Print a clean, formatted line of stats"""
    elapsed_time = time.time() - start_time
    
    # Format CPU info
    cpu_avg = sum(stats['cpu_percent']) / len(stats['cpu_percent'])
    
    # Format battery info
    battery = stats.get('battery')
    if battery:
        status = 'Charging' if battery.power_plugged else 'Discharging'
        batt_txt = f"{battery.percent:.1f}% ({status})"
        
        # Add remaining time if discharging
        if not battery.power_plugged and battery.secsleft > 0 and battery.secsleft < 24*3600:
            hours, remainder = divmod(battery.secsleft, 3600)
            minutes, _ = divmod(remainder, 60)
            batt_txt += f" {hours:02d}h{minutes:02d}m left"
    else:
        batt_txt = "N/A"
    
    # Format temperature
    temp = stats.get('cpu_temp', 'N/A')
    if temp != 'N/A':
        temp_txt = f"{temp:.1f}°C"
    else:
        temp_txt = "N/A"
    
    # Additional stats
    memory_txt = f"{stats['memory_percent']:.1f}%"
    
    # Fan speed
    fan_txt = f"{stats.get('fan_speed', 'N/A')} RPM" if 'fan_speed' in stats else "N/A"
    
    # Power usage
    power_txt = "N/A"
    if 'cpu_power' in stats:
        power_txt = f"{stats['cpu_power']:.1f}W"
    
    # Format disk and network I/O
    disk_txt = f"{stats['disk_usage']:.1f}%"
    
    # Clear the line and print new stats
    if show_header:
        print("\nTIME     | CPU     | TEMP    | MEM     | BATTERY      | FAN      | POWER   | DISK")
        print("---------|---------|---------|---------|--------------|----------|---------|--------")
    
    print(f"\r{format_time_delta(elapsed_time)} | {cpu_avg:6.1f}% | {temp_txt:7s} | {memory_txt:7s} | {batt_txt:12s} | {fan_txt:8s} | {power_txt:7s} | {disk_txt:6s}", end='')

def main():
    parser = argparse.ArgumentParser(description='Battery Killer - INTENSE multi-component stress testing tool')
    parser.add_argument('--cores', type=int, default=None, 
                        help='Number of CPU cores to use (default: all physical cores)')
    parser.add_argument('--max-temp', type=int, default=90, 
                        help='Maximum CPU temperature in Celsius (default: 90°C)')
    parser.add_argument('--duration', type=int, default=0, 
                        help='Duration of stress test in minutes (default: 0 = run until stopped)')
    parser.add_argument('--interval', type=float, default=2.0,
                        help='Update interval in seconds (default: 2.0)')
    parser.add_argument('--verbose', '-v', action='store_true', 
                        help='Show verbose output')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Setup signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    global stresser
    stresser = SystemStresser()
    
    # Configure stresser
    if args.cores:
        stresser.config['num_cores'] = args.cores
    stresser.config['max_temp_celsius'] = args.max_temp
    
    print(f"Battery Killer - CLI Mode")
    print(f"Configuration:")
    print(f"  - CPU Cores: {stresser.config['num_cores']}")
    print(f"  - Max Temperature: {stresser.config['max_temp_celsius']}°C")
    print(f"  - Duration: {'Until stopped' if args.duration == 0 else f'{args.duration} minutes'}")
    print(f"  - Update Interval: {args.interval} seconds")
    
    print("\nStarting stress test...")
    stresser.start_stress_tasks()
    
    try:
        start_time = time.time()
        counter = 0
        
        while True:
            stats = stresser.get_system_stats()
            
            # Print header every 20 lines
            show_header = (counter % 20 == 0)
            print_stats_line(stats, start_time, show_header)
            
            counter += 1
            
            # Check for temperature limit
            temp = stats.get('cpu_temp', -1)
            if temp != -1 and temp > stresser.config['max_temp_celsius']:
                print(f"\n\nTemperature too high: {temp:.1f}°C > {stresser.config['max_temp_celsius']}°C")
                print("Pausing stress test to cool down...")
                stresser.stop_stress_tasks()
                
                # Wait for cooling
                while temp > stresser.config['max_temp_celsius'] - 5:
                    time.sleep(5)
                    stats = stresser.get_system_stats()
                    temp = stats.get('cpu_temp', -1)
                    if temp == -1:
                        break
                    print(f"\rCooling down... Current temperature: {temp:.1f}°C", end='')
                
                print(f"\nTemperature now {temp:.1f}°C, resuming stress test")
                stresser.start_stress_tasks()
                print_stats_line(stats, start_time, True)  # Reprint header after temperature warning
            
            # Check for duration limit
            if args.duration > 0 and (time.time() - start_time) > args.duration * 60:
                print(f"\n\nReached specified duration of {args.duration} minutes.")
                break
            
            time.sleep(args.interval)
            
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
    except Exception as e:
        logger.error(f"Error occurred: {e}")
    finally:
        stresser.stop_stress_tasks()
        print("\nStress test stopped.")
        
        # Print summary
        end_time = time.time()
        duration = end_time - start_time
        print("\nTest Summary:")
        print(f"  - Total duration: {format_time_delta(duration)}")
        print(f"  - Test completed: {'Yes' if args.duration > 0 and duration >= args.duration * 60 else 'No (interrupted)'}")

if __name__ == "__main__":
    main()

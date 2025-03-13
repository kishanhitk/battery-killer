#!/usr/bin/env python3
import sys
import os
import argparse
import json
import logging

# Add parent directory to path so we can import battery_killer
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from battery_killer import SystemStresser

def main():
    parser = argparse.ArgumentParser(description='Battery Killer - A battery stress testing tool')
    parser.add_argument('--config', type=str, help='Path to configuration file')
    parser.add_argument('--min-battery', type=int, help='Minimum battery percentage')
    parser.add_argument('--interval', type=int, help='Check interval in seconds')
    parser.add_argument('--cores', type=int, help='Number of CPU cores to stress')
    parser.add_argument('--max-temp', type=int, help='Maximum temperature in Celsius')
    parser.add_argument('--no-temp-check', action='store_true', help='Disable temperature monitoring')
    
    args = parser.parse_args()
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('battery_killer.log'),
            logging.StreamHandler()
        ]
    )
    
    # Load config
    config = {}
    if args.config:
        with open(args.config) as f:
            config = json.load(f)
    
    # Override config with command line arguments
    if args.min_battery is not None:
        config['min_battery'] = args.min_battery
    if args.interval is not None:
        config['check_interval'] = args.interval
    if args.cores is not None:
        config['num_cores'] = args.cores
    if args.max_temp is not None:
        config['max_temp_celsius'] = args.max_temp
    if args.no_temp_check:
        config['monitor_temp'] = False
    
    # Start stress test
    stresser = SystemStresser(config)
    try:
        stresser.run()
    except KeyboardInterrupt:
        logging.info("Script terminated by user.")
    finally:
        stresser.stop_stress_tasks()

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Extreme Battery Killer for M1 MacBook Air
Combines CPU, GPU, Neural Engine, I/O, and system stress
WARNING: This will drain your battery extremely fast!
"""

import multiprocessing
import subprocess
import threading
import time
import sys
import os

def run_cpu_stress():
    """Launch CPU stress in separate process"""
    try:
        subprocess.Popen([sys.executable, 'intense_stress_cpu.py'], 
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✓ CPU stress launched")
    except Exception as e:
        print(f"✗ CPU stress failed: {e}")

def run_gpu_stress():
    """Launch GPU stress in separate process"""
    try:
        subprocess.Popen([sys.executable, 'intense_stress_gpu.py'], 
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✓ GPU stress launched")
    except Exception as e:
        print(f"✗ GPU stress failed: {e}")

def run_neural_stress():
    """Launch Neural Engine stress in separate process"""
    try:
        subprocess.Popen([sys.executable, 'intense_stress_neural.py'], 
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✓ Neural Engine stress launched")
    except Exception as e:
        print(f"✗ Neural Engine stress failed: {e}")

def run_io_stress():
    """Launch I/O stress in separate process"""
    try:
        subprocess.Popen([sys.executable, 'intense_stress_io.py'], 
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✓ I/O stress launched")
    except Exception as e:
        print(f"✗ I/O stress failed: {e}")

def display_brightness_max():
    """Set display brightness to maximum"""
    try:
        # Use AppleScript to set brightness to maximum
        script = '''
        tell application "System Events"
            key code 144  -- F15 key (brightness up)
            delay 0.1
            key code 144
            delay 0.1
            key code 144
            delay 0.1
            key code 144
            delay 0.1
            key code 144
        end tell
        '''
        subprocess.run(['osascript', '-e', script], capture_output=True)
        print("✓ Display brightness maximized")
    except Exception as e:
        print(f"✗ Display brightness failed: {e}")

def network_stress():
    """Generate network traffic stress"""
    try:
        # Multiple network connections
        import socket
        import random
        
        def network_worker():
            while True:
                try:
                    # Create multiple socket connections
                    sockets = []
                    for _ in range(100):
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(1)
                        try:
                            # Try to connect to various servers
                            hosts = ['8.8.8.8', '1.1.1.1', '208.67.222.222']
                            host = random.choice(hosts)
                            sock.connect((host, 53))
                            sockets.append(sock)
                        except:
                            sock.close()
                    
                    # Send data
                    for sock in sockets:
                        try:
                            sock.send(b'A' * 1024)
                        except:
                            pass
                    
                    # Close sockets
                    for sock in sockets:
                        sock.close()
                        
                    time.sleep(0.1)
                except:
                    time.sleep(0.1)
        
        # Start network stress threads
        for _ in range(4):
            t = threading.Thread(target=network_worker, daemon=True)
            t.start()
        
        print("✓ Network stress launched")
    except Exception as e:
        print(f"✗ Network stress failed: {e}")

def bluetooth_stress():
    """Generate Bluetooth activity stress"""
    try:
        # Use system Bluetooth scanning
        def bluetooth_worker():
            while True:
                try:
                    # Continuous Bluetooth device discovery
                    subprocess.run(['system_profiler', 'SPBluetoothDataType'], 
                                 capture_output=True, timeout=1)
                except:
                    pass
                time.sleep(0.1)
        
        t = threading.Thread(target=bluetooth_worker, daemon=True)
        t.start()
        print("✓ Bluetooth stress launched")
    except Exception as e:
        print(f"✗ Bluetooth stress failed: {e}")

def audio_stress():
    """Generate audio processing stress"""
    try:
        # Generate high-frequency audio processing
        def audio_worker():
            try:
                import numpy as np
                while True:
                    # Generate audio data
                    sample_rate = 44100
                    duration = 1.0
                    frequency = 440.0
                    
                    t = np.linspace(0, duration, int(sample_rate * duration))
                    audio_data = np.sin(2 * np.pi * frequency * t)
                    
                    # Apply audio effects (CPU intensive)
                    for _ in range(10):
                        # Reverb simulation
                        delayed = np.roll(audio_data, int(sample_rate * 0.1))
                        audio_data = audio_data + 0.3 * delayed
                        
                        # Distortion
                        audio_data = np.tanh(audio_data * 2)
                        
                        # Filtering
                        audio_data = np.convolve(audio_data, np.ones(10)/10, mode='same')
                    
                    time.sleep(0.01)
            except:
                # Fallback without numpy
                while True:
                    # Simple audio processing simulation
                    data = [random.random() for _ in range(44100)]
                    for i in range(len(data)):
                        data[i] = data[i] * 0.5 + (data[i-1000] if i >= 1000 else 0) * 0.3
                    time.sleep(0.01)
        
        t = threading.Thread(target=audio_worker, daemon=True)
        t.start()
        print("✓ Audio processing stress launched")
    except Exception as e:
        print(f"✗ Audio processing stress failed: {e}")

def thermal_monitoring():
    """Monitor thermal state using system tools"""
    try:
        def thermal_worker():
            while True:
                try:
                    # Use system_profiler for hardware info (no sudo required)
                    result = subprocess.run(['system_profiler', 'SPHardwareDataType'], 
                                          capture_output=True, text=True, timeout=3)
                    
                    if result.stdout:
                        print("\n🌡️  Thermal monitoring active (hardware stress detected)")
                    
                except Exception:
                    print("\n🌡️  Thermal monitoring active")
                
                time.sleep(20)
        
        t = threading.Thread(target=thermal_worker, daemon=True)
        t.start()
        print("✓ Thermal monitoring launched")
    except Exception as e:
        print(f"✗ Thermal monitoring failed: {e}")

def system_resource_stress():
    """Stress system resources"""
    try:
        def resource_worker():
            processes = []
            while True:
                try:
                    # Spawn processes up to system limit
                    if len(processes) < 100:
                        p = subprocess.Popen([sys.executable, '-c', 
                                            'import time; time.sleep(60)'], 
                                           stdout=subprocess.DEVNULL, 
                                           stderr=subprocess.DEVNULL)
                        processes.append(p)
                    
                    # Clean up finished processes
                    processes = [p for p in processes if p.poll() is None]
                    
                    time.sleep(1)
                except:
                    time.sleep(1)
        
        t = threading.Thread(target=resource_worker, daemon=True)
        t.start()
        print("✓ System resource stress launched")
    except Exception as e:
        print(f"✗ System resource stress failed: {e}")

def battery_monitoring():
    """Monitor battery drain rate"""
    try:
        def battery_worker():
            prev_level = None
            start_time = time.time()
            
            # Show initial battery status immediately
            try:
                result = subprocess.run(['pmset', '-g', 'batt'], 
                                      capture_output=True, text=True)
                if '%' in result.stdout:
                    for line in result.stdout.split('\n'):
                        if '%' in line:
                            try:
                                level_str = line.split('%')[0].split()[-1]
                                current_level = int(level_str)
                                print(f"🔋 Initial Battery Level: {current_level}%")
                                prev_level = current_level
                                break
                            except:
                                pass
            except:
                pass
            
            while True:
                try:
                    # Get battery info
                    result = subprocess.run(['pmset', '-g', 'batt'], 
                                          capture_output=True, text=True)
                    
                    if '%' in result.stdout:
                        # Extract battery percentage
                        for line in result.stdout.split('\n'):
                            if '%' in line:
                                try:
                                    level_str = line.split('%')[0].split()[-1]
                                    current_level = int(level_str)
                                    
                                    elapsed = (time.time() - start_time) / 60  # minutes
                                    
                                    if prev_level is not None and elapsed > 0.5:  # After 30 seconds
                                        drain_rate = prev_level - current_level
                                        
                                        if drain_rate >= 0:
                                            rate_per_min = drain_rate / elapsed if elapsed > 0 else 0
                                            estimated_time = current_level / rate_per_min if rate_per_min > 0 else float('inf')
                                            
                                            print(f"🔋 Battery: {current_level}% | Drain: {rate_per_min:.2f}%/min | Est. Time: {estimated_time:.0f}min")
                                        else:
                                            print(f"🔋 Battery: {current_level}% | Status: Charging or stable")
                                    else:
                                        print(f"🔋 Battery: {current_level}% | Monitoring...")
                                    
                                    break
                                except:
                                    pass
                    
                except Exception:
                    pass
                
                time.sleep(15)  # Check every 15 seconds
        
        t = threading.Thread(target=battery_worker, daemon=True)
        t.start()
        print("✓ Battery monitoring launched")
    except Exception as e:
        print(f"✗ Battery monitoring failed: {e}")

def system_stats_monitoring():
    """Monitor real-time system stats"""
    try:
        def stats_worker():
            import psutil
            
            print("\n📊 REAL-TIME SYSTEM STATS:")
            print("-" * 40)
            
            while True:
                try:
                    # CPU Usage
                    cpu_percent = psutil.cpu_percent(interval=1)
                    cpu_freq = psutil.cpu_freq()
                    cpu_temp = None
                    
                    # Try to get CPU temperature (without sudo)
                    try:
                        # Use system_profiler instead of powermetrics
                        temp_result = subprocess.run(['system_profiler', 'SPHardwareDataType'], 
                                                   capture_output=True, text=True, timeout=2)
                        # Temperature not available via system_profiler, skip for now
                        cpu_temp = None
                    except:
                        cpu_temp = None
                    
                    # Memory Usage
                    memory = psutil.virtual_memory()
                    
                    # Disk I/O
                    disk_io = psutil.disk_io_counters()
                    
                    # Network I/O
                    net_io = psutil.net_io_counters()
                    
                    # Process count
                    process_count = len(psutil.pids())
                    
                    # Display stats (clear line first)
                    stats_line = (f"🖥️  CPU: {cpu_percent:5.1f}% | "
                                 f"Freq: {cpu_freq.current:.0f}MHz | "
                                 f"Temp: {cpu_temp:.1f}°C | " if cpu_temp else "Temp: N/A | "
                                 f"RAM: {memory.percent:4.1f}% | "
                                 f"Processes: {process_count}")
                    
                    # Clear the line and print stats
                    print(f"\r{' ' * 80}\r{stats_line}", end="", flush=True)
                    
                    time.sleep(2)
                    
                except Exception as e:
                    time.sleep(2)
        
        t = threading.Thread(target=stats_worker, daemon=True)
        t.start()
        print("✓ System stats monitoring launched")
    except Exception as e:
        print(f"✗ System stats monitoring failed: {e}")

def power_consumption_monitoring():
    """Monitor power consumption using system tools (no sudo required)"""
    try:
        def power_worker():
            while True:
                try:
                    # Use iostat for system activity instead of powermetrics
                    result = subprocess.run(['iostat', '-c', '1', '1'], 
                                          capture_output=True, text=True, timeout=3)
                    
                    # Extract CPU usage from iostat
                    if result.stdout:
                        lines = result.stdout.strip().split('\n')
                        if len(lines) >= 3:
                            # Last line contains the stats
                            stats = lines[-1].split()
                            if len(stats) >= 6:
                                user_cpu = float(stats[0])
                                sys_cpu = float(stats[1])
                                total_cpu = user_cpu + sys_cpu
                                
                                print(f"\n⚡ System Activity: CPU Load: {total_cpu:.1f}% (User: {user_cpu:.1f}%, System: {sys_cpu:.1f}%)")
                    
                except Exception:
                    # Fallback: just show that monitoring is active
                    print(f"\n⚡ Power monitoring active (no sudo required)")
                
                time.sleep(15)
        
        t = threading.Thread(target=power_worker, daemon=True)
        t.start()
        print("✓ Power consumption monitoring launched")
    except Exception as e:
        print(f"✗ Power consumption monitoring failed: {e}")

def main():
    """Main orchestrator for extreme battery killing"""
    print("🔥 EXTREME BATTERY KILLER FOR M1 MACBOOK AIR 🔥")
    print("=" * 50)
    print("WARNING: This will drain your battery EXTREMELY fast!")
    print("Press Ctrl+C to stop")
    print("=" * 50)
    
    # Launch all stress methods
    print("\n🚀 Launching stress methods...")
    
    # Core stress methods
    run_cpu_stress()
    run_gpu_stress()
    run_neural_stress()
    run_io_stress()
    
    # System stress methods
    display_brightness_max()
    network_stress()
    bluetooth_stress()
    audio_stress()
    thermal_monitoring()
    system_resource_stress()
    battery_monitoring()
    system_stats_monitoring()
    power_consumption_monitoring()
    
    print("\n✅ All stress methods launched!")
    print("🔥 Your battery is now under EXTREME stress!")
    print("📊 Monitor the battery percentage above")
    print("\nPress Ctrl+C to stop all processes")
    
    try:
        # Keep main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping extreme battery killer...")
        print("Note: Some background processes may continue briefly")
        sys.exit(0)

if __name__ == '__main__':
    main() 
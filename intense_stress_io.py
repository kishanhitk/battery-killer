
import threading
import time
import random
import os
import tempfile

def disk_write_stress():
    """Intensive disk write operations"""
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
    """Intensive disk read operations"""
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



if __name__ == '__main__':
    # Start I/O stress threads
    threads = []
    
    # Disk write thread
    t1 = threading.Thread(target=disk_write_stress, daemon=True)
    threads.append(t1)
    
    # Disk read thread
    t2 = threading.Thread(target=disk_read_stress, daemon=True)
    threads.append(t2)
    
    for t in threads:
        t.start()
    
    # Keep main thread alive
    while True:
        time.sleep(1)

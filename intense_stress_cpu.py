
import multiprocessing
import threading
import math
import random
import hashlib
import time

def cpu_intensive_math():
    """Intensive mathematical operations"""
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
    """Intensive cryptographic operations"""
    while True:
        # Hash computations (CPU intensive)
        data = str(random.random() * 1000000).encode()
        for _ in range(10000):
            data = hashlib.sha256(data).digest()
            data = hashlib.md5(data).digest()
            data = hashlib.sha1(data).digest()

def cpu_intensive_loops():
    """Intensive nested loops"""
    while True:
        # Nested loops with floating point operations
        total = 0.0
        for i in range(1000):
            for j in range(1000):
                total += (i * j) ** 0.5
                total = total % 1000000

def memory_intensive():
    """Memory allocation and operations"""
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
    """Main stress function combining all intensive operations"""
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

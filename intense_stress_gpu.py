import subprocess
import threading
import time
import random
import os
import tempfile
import multiprocessing
import numpy as np

def metal_compute_extreme_stress():
    """Extreme Metal compute shader stress for M1 GPU"""
    try:
        # Create Metal compute shader source
        metal_shader_source = '''
#include <metal_stdlib>
using namespace metal;

// Extremely intensive compute kernel
kernel void extreme_compute(device float* input_data [[buffer(0)]],
                           device float* output_data [[buffer(1)]],
                           uint index [[thread_position_in_grid]]) {
    float value = input_data[index];
    
    // Intensive mathematical operations
    for (int i = 0; i < 50000; i++) {
        value = sin(value) * cos(value) + sqrt(abs(value));
        value = pow(value, 2.5) + log(abs(value) + 1.0);
        value = exp(value * 0.001) + tan(value * 0.1);
        value = fmod(value, 1000.0);
        
        // Matrix-like operations
        for (int j = 0; j < 100; j++) {
            value += sin(float(i * j)) * cos(float(i + j));
        }
    }
    
    output_data[index] = value;
}

// Memory bandwidth stress kernel
kernel void memory_bandwidth_stress(device float4* data [[buffer(0)]],
                                   uint index [[thread_position_in_grid]]) {
    uint base_index = index * 1000;
    float4 accumulator = float4(0.0);
    
    // Intensive memory access pattern
    for (uint i = 0; i < 1000; i++) {
        uint read_index = (base_index + i) % 1000000;
        accumulator += data[read_index];
        data[read_index] = accumulator * 1.001;
    }
}
'''
        
        # Write shader to temporary file
        shader_path = os.path.join(tempfile.gettempdir(), 'extreme_compute.metal')
        with open(shader_path, 'w') as f:
            f.write(metal_shader_source)
        
        # Compile Metal shader (requires Xcode command line tools)
        compiled_path = os.path.join(tempfile.gettempdir(), 'extreme_compute.metallib')
        compile_cmd = ['xcrun', '-sdk', 'macosx', 'metal', '-c', shader_path, '-o', compiled_path]
        
        try:
            subprocess.run(compile_cmd, check=True, capture_output=True)
            print("Metal shader compiled successfully")
        except subprocess.CalledProcessError:
            print("Metal compilation failed, using fallback GPU stress")
            gpu_fallback_extreme_stress()
            return
            
    except Exception as e:
        print(f"Metal setup failed: {e}")
        gpu_fallback_extreme_stress()

def gpu_fallback_extreme_stress():
    """Extreme GPU stress fallback using intensive computations"""
    while True:
        try:
            # Massive parallel matrix operations
            size = 2048
            matrix_a = np.random.randn(size, size).astype(np.float32)
            matrix_b = np.random.randn(size, size).astype(np.float32)
            
            # Multiple intensive operations
            for _ in range(10):
                # Matrix multiplication (can use GPU acceleration)
                result = np.dot(matrix_a, matrix_b)
                
                # FFT operations (GPU accelerated)
                fft_result = np.fft.fft2(result)
                
                # Trigonometric operations
                trig_result = np.sin(result) * np.cos(result) + np.sqrt(np.abs(result))
                
                # Element-wise power operations
                power_result = np.power(np.abs(trig_result), 1.5)
                
                # Update matrices for next iteration
                matrix_a = power_result[:size, :size]
                matrix_b = np.transpose(power_result)[:size, :size]
                
        except Exception as e:
            time.sleep(0.01)

def video_encoding_extreme_stress():
    """Extreme video encoding stress using hardware acceleration"""
    try:
        # Multiple simultaneous 4K video encoding streams
        encoding_processes = []
        
        for stream_id in range(8):  # 8 simultaneous streams
            cmd = [
                'ffmpeg', '-y',
                '-f', 'lavfi', 
                '-i', f'testsrc2=duration=3600:size=3840x2160:rate=60',  # 4K 60fps
                '-c:v', 'h264_videotoolbox',  # Hardware acceleration
                '-b:v', '100M',  # High bitrate
                '-preset', 'fast',
                '-f', 'null', '-'
            ]
            
            try:
                process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                encoding_processes.append(process)
            except:
                pass
        
        # Keep processes running
        while True:
            time.sleep(1)
            # Check if any process died and restart
            for i, process in enumerate(encoding_processes):
                if process.poll() is not None:
                    # Restart the process
                    cmd = [
                        'ffmpeg', '-y',
                        '-f', 'lavfi', 
                        '-i', f'testsrc2=duration=3600:size=3840x2160:rate=60',
                        '-c:v', 'h264_videotoolbox',
                        '-b:v', '100M',
                        '-preset', 'fast',
                        '-f', 'null', '-'
                    ]
                    try:
                        encoding_processes[i] = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    except:
                        pass
                        
    except Exception as e:
        print(f"Video encoding stress fallback: {e}")
        # Fallback: CPU-intensive video simulation
        video_processing_simulation()

def video_processing_simulation():
    """Simulate intensive video processing"""
    while True:
        # Simulate 4K video frame processing
        height, width, channels = 2160, 3840, 3
        frame = np.random.randint(0, 256, (height, width, channels), dtype=np.uint8)
        
        # Simulate video filters and effects
        for _ in range(5):  # Multiple effects per frame
            # Color space conversion
            yuv_frame = np.zeros_like(frame, dtype=np.float32)
            yuv_frame[:,:,0] = 0.299 * frame[:,:,0] + 0.587 * frame[:,:,1] + 0.114 * frame[:,:,2]
            yuv_frame[:,:,1] = -0.169 * frame[:,:,0] - 0.331 * frame[:,:,1] + 0.5 * frame[:,:,2]
            yuv_frame[:,:,2] = 0.5 * frame[:,:,0] - 0.419 * frame[:,:,1] - 0.081 * frame[:,:,2]
            
            # Motion blur simulation
            kernel_size = 15
            kernel = np.ones((kernel_size, kernel_size)) / (kernel_size * kernel_size)
            
            # Apply convolution (simplified)
            for c in range(channels):
                for i in range(0, height - kernel_size, 10):
                    for j in range(0, width - kernel_size, 10):
                        patch = frame[i:i+kernel_size, j:j+kernel_size, c]
                        frame[i+kernel_size//2, j+kernel_size//2, c] = np.sum(patch * kernel)

def gpu_memory_extreme_stress():
    """Extreme GPU memory allocation and operations"""
    try:
        import numpy as np
        
        # Allocate massive arrays to stress GPU memory
        gpu_arrays = []
        
        while True:
            try:
                # Allocate large arrays (simulating GPU memory usage)
                for _ in range(20):
                    # Large 3D arrays for GPU-like operations
                    arr = np.random.randn(512, 512, 512).astype(np.float32)
                    
                    # Intensive 3D operations
                    # 3D FFT (very GPU intensive)
                    fft_result = np.fft.fftn(arr)
                    
                    # 3D convolution simulation
                    kernel = np.random.randn(5, 5, 5).astype(np.float32)
                    
                    # Tensor operations
                    reshaped = arr.reshape(512, -1)
                    matrix_result = np.dot(reshaped, reshaped.T)
                    
                    gpu_arrays.append(matrix_result[:100, :100])
                
                # Limit memory usage
                if len(gpu_arrays) > 50:
                    gpu_arrays = gpu_arrays[-25:]
                    
            except MemoryError:
                gpu_arrays = gpu_arrays[-10:] if gpu_arrays else []
                time.sleep(0.1)
                
    except ImportError:
        # Pure Python fallback
        while True:
            # Large nested list operations
            size = 1000
            matrix = [[random.random() for _ in range(size)] for _ in range(size)]
            
            # Matrix operations
            for i in range(100):
                for j in range(100):
                    sum_val = sum(matrix[i][k] * matrix[k][j] for k in range(100))

def opengl_rendering_stress():
    """OpenGL rendering stress (if available)"""
    try:
        # Try to use OpenGL for rendering stress
        import subprocess
        
        # Use system tools for OpenGL stress
        gl_stress_cmd = [
            'python3', '-c', '''
import time
import random
import math

# Simulate OpenGL rendering operations
while True:
    # Simulate vertex processing
    vertices = []
    for _ in range(10000):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        z = random.uniform(-1, 1)
        
        # Transform vertices
        transformed_x = x * math.cos(time.time()) - y * math.sin(time.time())
        transformed_y = x * math.sin(time.time()) + y * math.cos(time.time())
        transformed_z = z
        
        vertices.append((transformed_x, transformed_y, transformed_z))
    
    # Simulate fragment processing
    for vertex in vertices[:1000]:
        r = math.sin(vertex[0] * 10) * 0.5 + 0.5
        g = math.cos(vertex[1] * 10) * 0.5 + 0.5
        b = math.sin(vertex[2] * 10) * 0.5 + 0.5
        color = (r, g, b)
'''
        ]
        
        subprocess.Popen(gl_stress_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
    except Exception as e:
        print(f"OpenGL stress failed: {e}")

def extreme_gpu_stress_orchestrator():
    """Orchestrate all GPU stress methods simultaneously"""
    threads = []
    
    # Metal compute stress
    t1 = threading.Thread(target=metal_compute_extreme_stress, daemon=True)
    threads.append(t1)
    
    # Video encoding stress
    t2 = threading.Thread(target=video_encoding_extreme_stress, daemon=True)
    threads.append(t2)
    
    # GPU memory stress
    t3 = threading.Thread(target=gpu_memory_extreme_stress, daemon=True)
    threads.append(t3)
    
    # OpenGL rendering stress
    t4 = threading.Thread(target=opengl_rendering_stress, daemon=True)
    threads.append(t4)
    
    # Start all threads
    for t in threads:
        t.start()
    
    # Keep main thread busy with fallback GPU stress
    gpu_fallback_extreme_stress()

if __name__ == '__main__':
    print("Starting Extreme GPU Stress for M1 MacBook Air...")
    print("This will stress GPU cores, video encoders, and GPU memory simultaneously")
    
    # Start multiple processes for maximum GPU utilization
    processes = []
    num_processes = min(4, multiprocessing.cpu_count())  # Limit GPU processes
    
    for i in range(num_processes):
        p = multiprocessing.Process(target=extreme_gpu_stress_orchestrator)
        p.start()
        processes.append(p)
    
    # Keep main process busy
    extreme_gpu_stress_orchestrator() 
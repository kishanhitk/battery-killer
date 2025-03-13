import sys
import time
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLabel, QProgressBar, 
                            QSpinBox, QCheckBox, QGroupBox)
from PyQt6.QtCore import QTimer, Qt, pyqtSignal, QThread
import pyqtgraph as pg
from .core import SystemStresser
import psutil
import logging

logger = logging.getLogger(__name__)

class StressWorker(QThread):
    temperature_update = pyqtSignal(float)
    stats_update = pyqtSignal(dict)
    
    def __init__(self, stresser):
        super().__init__()
        self.stresser = stresser
        self.running = False
        self.stress_active = False
        
    def run(self):
        self.running = True
        while self.running:
            try:
                stats = self.stresser.get_system_stats()
                if 'cpu_temp' in stats:
                    self.temperature_update.emit(stats['cpu_temp'])
                self.stats_update.emit(stats)
                
                # If stress test is active, check temperature
                if self.stress_active and 'cpu_temp' in stats:
                    if stats['cpu_temp'] > self.stresser.config['max_temp_celsius']:
                        logger.warning(f"Temperature too high: {stats['cpu_temp']}°C")
                        self.stop_stress()
                
                time.sleep(1)
            except Exception as e:
                logger.error(f"Error in worker thread: {e}")
                time.sleep(1)
    
    def start_stress(self):
        self.stress_active = True
        self.stresser.start_stress_tasks()
    
    def stop_stress(self):
        self.stress_active = False
        self.stresser.stop_stress_tasks()
            
    def stop(self):
        self.running = False
        self.stop_stress()
        self.wait()

class BatteryKillerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.stresser = SystemStresser()
        self.worker = StressWorker(self.stresser)
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle('Battery Killer')
        self.setMinimumSize(800, 600)
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Create controls group
        controls_group = QGroupBox("Controls")
        controls_layout = QHBoxLayout()
        
        # Start/Stop button
        self.start_button = QPushButton('Start Stress Test')
        self.start_button.clicked.connect(self.toggle_stress_test)
        controls_layout.addWidget(self.start_button)
        
        # Core count spinner
        core_layout = QHBoxLayout()
        core_layout.addWidget(QLabel('CPU Cores:'))
        self.core_spinner = QSpinBox()
        self.core_spinner.setRange(1, psutil.cpu_count())
        self.core_spinner.setValue(psutil.cpu_count())
        core_layout.addWidget(self.core_spinner)
        controls_layout.addLayout(core_layout)
        
        # Temperature limit
        temp_layout = QHBoxLayout()
        temp_layout.addWidget(QLabel('Max Temp (°C):'))
        self.temp_spinner = QSpinBox()
        self.temp_spinner.setRange(50, 100)
        self.temp_spinner.setValue(90)
        temp_layout.addWidget(self.temp_spinner)
        controls_layout.addLayout(temp_layout)
        
        controls_group.setLayout(controls_layout)
        layout.addWidget(controls_group)
        
        # Create stats group
        stats_group = QGroupBox("System Stats")
        stats_layout = QHBoxLayout()
        
        # Battery stats
        battery_layout = QVBoxLayout()
        self.battery_label = QLabel('Battery: ---%')
        self.battery_progress = QProgressBar()
        self.battery_progress.setRange(0, 100)
        battery_layout.addWidget(self.battery_label)
        battery_layout.addWidget(self.battery_progress)
        stats_layout.addLayout(battery_layout)
        
        # Temperature
        temp_layout = QVBoxLayout()
        self.temp_label = QLabel('CPU Temperature: ---°C')
        self.temp_progress = QProgressBar()
        self.temp_progress.setRange(0, 100)
        temp_layout.addWidget(self.temp_label)
        temp_layout.addWidget(self.temp_progress)
        stats_layout.addLayout(temp_layout)
        
        # Memory
        memory_layout = QVBoxLayout()
        self.memory_label = QLabel('Memory: ---%')
        self.memory_progress = QProgressBar()
        self.memory_progress.setRange(0, 100)
        memory_layout.addWidget(self.memory_label)
        memory_layout.addWidget(self.memory_progress)
        stats_layout.addLayout(memory_layout)
        
        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)
        
        # Create graphs group
        graphs_group = QGroupBox("Performance Graphs")
        graphs_layout = QVBoxLayout()
        
        # Temperature graph
        self.temp_plot = pg.PlotWidget()
        self.temp_plot.setBackground('w')
        self.temp_plot.setTitle("CPU Temperature")
        self.temp_plot.setLabel('left', 'Temperature', units='°C')
        self.temp_plot.setLabel('bottom', 'Time', units='s')
        self.temp_data = []
        self.temp_curve = self.temp_plot.plot(pen='r')
        graphs_layout.addWidget(self.temp_plot)
        
        # CPU Usage graph
        self.cpu_plot = pg.PlotWidget()
        self.cpu_plot.setBackground('w')
        self.cpu_plot.setTitle("CPU Usage")
        self.cpu_plot.setLabel('left', 'Usage', units='%')
        self.cpu_plot.setLabel('bottom', 'Time', units='s')
        self.cpu_data = []
        self.cpu_curve = self.cpu_plot.plot(pen='b')
        graphs_layout.addWidget(self.cpu_plot)
        
        graphs_group.setLayout(graphs_layout)
        layout.addWidget(graphs_group)
        
        # Setup worker connections
        self.worker.temperature_update.connect(self.update_temperature)
        self.worker.stats_update.connect(self.update_stats)
        
        # Start the monitoring thread
        self.worker.start()
        
    def toggle_stress_test(self):
        if self.start_button.text() == 'Start Stress Test':
            # Update configuration
            self.stresser.config['num_cores'] = self.core_spinner.value()
            self.stresser.config['max_temp_celsius'] = self.temp_spinner.value()
            
            # Start stress test
            self.worker.start_stress()
            self.start_button.setText('Stop Stress Test')
            self.start_button.setStyleSheet('background-color: #ff6b6b;')
        else:
            # Stop stress test
            self.worker.stop_stress()
            self.start_button.setText('Start Stress Test')
            self.start_button.setStyleSheet('')
            
    def update_temperature(self, temp):
        self.temp_label.setText(f'CPU Temperature: {temp:.1f}°C')
        self.temp_progress.setValue(min(int(temp), 100))
        
        # Update temperature graph
        self.temp_data.append(temp)
        if len(self.temp_data) > 60:  # Keep last 60 seconds
            self.temp_data.pop(0)
        self.temp_curve.setData(range(len(self.temp_data)), self.temp_data)
        
    def update_stats(self, stats):
        try:
            # Update battery
            battery = stats['battery']
            self.battery_label.setText(f"Battery: {battery.percent}% {'[Charging]' if battery.power_plugged else '[Discharging]'}")
            self.battery_progress.setValue(int(battery.percent))
            
            # Update CPU
            cpu_avg = sum(stats['cpu_percent']) / len(stats['cpu_percent'])
            self.cpu_data.append(cpu_avg)
            if len(self.cpu_data) > 60:  # Keep last 60 seconds
                self.cpu_data.pop(0)
            self.cpu_curve.setData(range(len(self.cpu_data)), self.cpu_data)
            
            # Update memory
            self.memory_label.setText(f'Memory: {stats["memory_percent"]:.1f}%')
            self.memory_progress.setValue(int(stats['memory_percent']))
            
            # Auto-scale the Y-axis of the graphs
            if self.temp_data:
                self.temp_plot.setYRange(min(self.temp_data), max(self.temp_data) + 5)
            if self.cpu_data:
                self.cpu_plot.setYRange(0, 100)
                
        except Exception as e:
            logger.error(f"Error updating stats: {e}")
        
    def closeEvent(self, event):
        self.worker.stop()
        self.stresser.stop_stress_tasks()
        event.accept()

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern style
    window = BatteryKillerGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
import sys
import os
import logging

# Add parent directory to path so we can import battery_killer
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from battery_killer.gui import BatteryKillerGUI
from PyQt6.QtWidgets import QApplication

def main():
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('battery_killer.log'),
            logging.StreamHandler()
        ]
    )
    
    app = QApplication(sys.argv)
    window = BatteryKillerGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()

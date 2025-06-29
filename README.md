# NVIDIA-SMI GUI Monitor

A real-time graphical interface for monitoring NVIDIA GPU status using `nvidia-smi`, with color-coded metrics, process table, and power limit adjustment.

![image](https://github.com/user-attachments/assets/baf6e177-a31d-49b8-9844-453eb241819a)


## Overview

This application provides a user-friendly GUI that displays key NVIDIA GPU information in real-time, updating every 2 seconds. It is built with Python's Tkinter library and uses the `nvidia-smi` command to fetch GPU status and running processes.

## Features

- Real-time GPU monitoring with automatic updates every 2 seconds
- Color-coded display for utilization, memory, temperature, and power draw
- Table of running GPU processes (PID, name, memory usage)
- Button to open a window for adjusting the GPU power limit (with min/max/current shown)
- Collapsible section showing the full `nvidia-smi` output
- Error handling for missing drivers or command failures
- Cross-platform compatibility (Windows, Linux, macOS)
- Lightweight and minimal dependencies

## Prerequisites

### Hardware Requirements
- NVIDIA GPU with compatible drivers installed
- NVIDIA driver version that supports `nvidia-smi` command

### Software Requirements
- Python 3.6 or higher
- Tkinter (usually included with Python installation)
- NVIDIA drivers with `nvidia-smi` utility

## Installation

1. **Clone or download the project:**
   ```bash
   git clone <repository-url>
   cd nvidia-smi-gui-pt
   ```

2. **Verify Python installation:**
   ```bash
   python --version
   # or
   python3 --version
   ```

3. **Verify NVIDIA drivers:**
   ```bash
   nvidia-smi
   ```
   This command should display your GPU information. If it fails, install appropriate NVIDIA drivers.

## Usage

### Quick Start

#### Windows (PowerShell)
```powershell
.\run.ps1
```

#### Linux/macOS (Bash)
```bash
./run.sh
```

#### Manual Execution
```bash
python App.py
# or
python3 App.py
```

### Application Interface

- The application opens a window titled "NVIDIA-SMI GPU Monitor"
- The top of the window displays the GPU name and a button to adjust the power limit
- Key metrics (utilization, memory, temperature, power) are shown in a color-coded table
- A table lists all running GPU processes (PID, name, memory usage)
- A button toggles display of the full `nvidia-smi` output in a collapsible section
- Information updates automatically every 2 seconds
- Close the window to exit the application

### Adjusting Power Limit

- Click the "Adjust Power Limit" button to open a new window
- The window displays current, minimum, and maximum power limits
- Enter a new value within the allowed range and click "Apply"
- **Note:** Changing the power limit may require administrator/root privileges

## Configuration

### Update Interval
To change the refresh rate, modify the `root.after(2000, update_gui)` line in `App.py` (2000 ms = 2 seconds).

### Color Thresholds
You can adjust the warning/danger thresholds for utilization, memory, temperature, and power in the respective color functions in `App.py`.

## Troubleshooting

### Common Issues

1. **"nvidia-smi not found" error:**
   - Install NVIDIA drivers
   - Ensure `nvidia-smi` is in your system PATH
   - Verify GPU is NVIDIA brand

2. **Python not found:**
   - Install Python from [python.org](https://python.org)
   - Ensure Python is added to system PATH

3. **Tkinter import error:**
   - On Ubuntu/Debian: `sudo apt-get install python3-tk`
   - On CentOS/RHEL: `sudo yum install tkinter`
   - On macOS: Usually included with Python

4. **Permission denied (Linux/macOS):**
   ```bash
   chmod +x run.sh
   ```

5. **Setting Power Limit Fails:**
   - You may need to run the app as administrator/root to change the power limit.

## Building a Standalone Executable

You can compile this app into a single-file executable for Windows or Linux using PyInstaller.

### Linux

1. Ensure you have Python 3.6+, pip, and tkinter installed.
2. Run the build script:
   ```bash
   ./build.sh
   ```
   The executable `./nvidia-smi-gui-pt` will be created in the project directory.

### Windows

1. Ensure you have Python 3.6+, pip, and tkinter installed.
2. Run the build script in PowerShell:
   ```powershell
   .\build.ps1
   ```
   The executable `nvidia-smi-gui-pt.exe` will be created in the project directory.

### Manual Build (Advanced)

You can also run PyInstaller directly:
```bash
python -m pip install pyinstaller
python -m pyinstaller --onefile --name nvidia-smi-gui-pt App.py
```

### Notes
- The resulting executable is portable and does not require Python to be installed on the target system.
- On Linux, you may need to run `chmod +x nvidia-smi-gui-pt` before executing.
- On Windows, double-click or run from the command line.
- If you encounter issues with missing libraries (e.g., tkinter), ensure all dependencies are installed on your build system.

## System Requirements

### Minimum Requirements
- Python 3.6+
- NVIDIA GPU with driver support
- 50MB RAM
- Minimal CPU usage

### Tested Platforms
- Windows 10/11
- Ubuntu 20.04+
- macOS 10.14+
- Various NVIDIA GPU models (GTX, RTX, Tesla, Quadro series)

## License

This project is open source. Please check the repository for specific license terms.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test on your platform
5. Submit a pull request

## Support

For issues and questions:
1. Check the troubleshooting section
2. Verify system requirements
3. Create an issue in the repository

## Changelog

### Version 1.0
- Initial release
- Real-time nvidia-smi monitoring
- Color-coded metrics and process table
- Power limit adjustment window
- Cross-platform support
-

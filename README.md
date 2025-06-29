# NVIDIA-SMI GUI Monitor

A real-time graphical interface for monitoring NVIDIA GPU status using `nvidia-smi`, with color-coded metrics, process table, and power limit adjustment.

![NVIDIA-SMI GUI Screenshot](https://github.com/user-attachments/assets/baf6e177-a31d-49b8-9844-453eb241819a)

## Overview

This application provides a user-friendly GUI that displays key NVIDIA GPU information in real-time, updating every 2 seconds. It is built with Python's Tkinter library and uses the `nvidia-smi` command to fetch GPU status and running processes.

## Features

- 🔄 **Real-time monitoring** - Updates every 2 seconds automatically
- 🎨 **Color-coded display** - Visual indicators for utilization, memory, temperature, and power draw
- 📊 **Process monitoring** - Table of running GPU processes (PID, name, memory usage)
- ⚡ **Power limit control** - Adjust GPU power limits with validation (requires admin privileges)
- 📋 **Full nvidia-smi output** - Collapsible section showing complete nvidia-smi information
- 🛡️ **Error handling** - Graceful handling of missing drivers or command failures
- 🌐 **Cross-platform** - Compatible with Windows, Linux, and macOS
- 🪶 **Lightweight** - No external dependencies, uses only Python standard library

## Project Structure

```
pytk-nvidia-smi-gui/
├── App.py              # Main application file
├── requirements.txt    # Project dependencies (Python stdlib only)
├── LICENSE            # MIT License
└── README.md          # This file
```

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
   git clone https://github.com/yourusername/pytk-nvidia-smi-gui.git
   cd pytk-nvidia-smi-gui
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

### Running the Application

```bash
python App.py
# or
python3 App.py
```

### Application Interface

- The application opens a window titled "NVIDIA-SMI GPU Monitor"
- The top displays the GPU name and a button to adjust the power limit
- Key metrics (utilization, memory, temperature, power) are shown in a color-coded table:
  - 🟢 **Green**: Normal/Good values
  - 🟠 **Orange**: Warning levels
  - 🔴 **Red**: Critical/High values
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

You can adjust the warning/danger thresholds for utilization, memory, temperature, and power in the respective color functions in `App.py`:

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

   - On Ubuntu/Debian:

     ```bash
     sudo apt-get install python3-tk
     ```

   - On CentOS/RHEL:

     ```bash
     sudo yum install tkinter
     ```

   - On macOS: Usually included with Python

4. **Permission denied (Linux/macOS):**

   ```bash
   chmod +x App.py
   ```

5. **Setting Power Limit Fails:**
   - You may need to run the app as administrator/root to change the power limit
   - On Linux: `sudo python App.py`
   - On Windows: Run Command Prompt/PowerShell as Administrator

## Building a Standalone Executable (Optional)

You can compile this app into a single-file executable using PyInstaller:

1. **Install PyInstaller:**

   ```bash
   pip install pyinstaller
   ```

2. **Build the executable:**

   ```bash
   pyinstaller --onefile --name nvidia-smi-gui-monitor App.py
   ```

3. **Find the executable:**
   - The executable will be created in the `dist/` directory
   - On Linux: `dist/nvidia-smi-gui-monitor`
   - On Windows: `dist/nvidia-smi-gui-monitor.exe`

### Notes

- The resulting executable is portable and does not require Python to be installed on the target system
- On Linux, you may need to run `chmod +x nvidia-smi-gui-monitor` before executing
- If you encounter issues with missing libraries (e.g., tkinter), ensure all dependencies are installed on your build system

## Technical Details

### Performance

- **Memory Usage**: ~10-20MB RAM
- **CPU Usage**: Minimal (periodic nvidia-smi calls)
- **Update Frequency**: 2 seconds (configurable)
- **Dependencies**: Python standard library only

### Tested Platforms

- **Windows**: 10, 11
- **Linux**: Ubuntu 20.04+, CentOS 7+, Fedora 35+
- **macOS**: 10.14+
- **NVIDIA GPUs**: GTX, RTX, Tesla, Quadro series

### Color Coding System

- **Utilization/Memory**:
  - Green: < 70%
  - Orange: 70-90%
  - Red: > 90%

- **Temperature**:
  - Green: < 65°C
  - Orange: 65-80°C
  - Red: > 80°C

- **Power Draw**:
  - Green: < 80% of limit
  - Orange: 80-95% of limit
  - Red: > 95% of limit

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Support

For issues and questions:

1. Check the troubleshooting section above
2. Verify system requirements
3. Create an issue in the repository with:
   - Your operating system
   - Python version
   - NVIDIA driver version
   - Error message (if any)

## Author

Palaash Atri

## Acknowledgments

- NVIDIA for the `nvidia-smi` utility
- Python Software Foundation for Tkinter
- The open-source community for inspiration and feedback

---

Made with ❤️ for GPU monitoring enthusiasts

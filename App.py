import tkinter as tk
from tkinter import ttk
import subprocess
import re

power_win = None

def get_gpu_info():
    try:
        info = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=name", "--format=csv,noheader,nounits"],
            encoding="utf-8", stderr=subprocess.STDOUT
        ).strip()
        name = info.split("\n")[0].strip()
        return name
    except Exception:
        return "Unknown"

def get_power_limits():
    try:
        smi = subprocess.check_output(
            ["nvidia-smi", "-q", "-d", "POWER"],
            encoding="utf-8", stderr=subprocess.STDOUT
        )
        cur = min_ = max_ = None
        for line in smi.splitlines():
            line = line.strip()
            m_cur = re.match(r"^Power Limit\s*:\s*([\d\.]+) W", line)
            m_min = re.match(r"^Min Power Limit\s*:\s*([\d\.]+) W", line)
            m_max = re.match(r"^Max Power Limit\s*:\s*([\d\.]+) W", line)
            if m_cur:
                cur = float(m_cur.group(1))
            elif m_min:
                min_ = float(m_min.group(1))
            elif m_max:
                max_ = float(m_max.group(1))
        return cur, min_, max_
    except Exception:
        return None, None, None

def set_power_limit(new_limit):
    try:
        result = subprocess.check_output(
            ["sudo", "nvidia-smi", "-pl", str(int(new_limit))],
            encoding="utf-8", stderr=subprocess.STDOUT
        )
        return True, result
    except subprocess.CalledProcessError as e:
        return False, e.output
    except Exception as e:
        return False, str(e)

def get_nvidia_smi_output():
    try:
        result = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=utilization.gpu,memory.used,memory.total,temperature.gpu,power.draw,power.limit", "--format=csv,noheader,nounits"],
            encoding="utf-8", stderr=subprocess.STDOUT
        )
        proc_result = subprocess.check_output(
            ["nvidia-smi", "--query-compute-apps=pid,process_name,used_memory", "--format=csv,noheader,nounits"],
            encoding="utf-8", stderr=subprocess.STDOUT
        )
        return result.strip(), proc_result.strip()
    except FileNotFoundError:
        return "Error: nvidia-smi not found. Ensure drivers are installed.", ""
    except Exception as e:
        return f"Error: {e}", ""

def parse_gpu_metrics(output):
    metrics = {}
    try:
        parts = [x.strip() for x in output.split(",")]
        metrics["utilization"] = float(parts[0])
        metrics["mem_used"] = float(parts[1])
        metrics["mem_total"] = float(parts[2])
        metrics["temperature"] = int(parts[3])
        metrics["power_draw"] = float(parts[4])
        metrics["power_limit"] = float(parts[5])
    except Exception:
        pass
    return metrics

def parse_processes(proc_output):
    processes = []
    for line in proc_output.splitlines():
        if not line.strip():
            continue
        parts = [x.strip() for x in line.split(",")]
        if len(parts) == 3:
            pid, name, mem = parts
            processes.append({
                "pid": pid,
                "name": name,
                "mem": mem
            })
    return processes

def format_memory(mem_used, mem_total):
    percent = (mem_used / mem_total) * 100 if mem_total else 0
    if mem_total >= 1024:
        used_str = f"{mem_used/1024:.1f} GB"
        total_str = f"{mem_total/1024:.1f} GB"
    else:
        used_str = f"{mem_used:.0f} MB"
        total_str = f"{mem_total:.0f} MB"
    return f"{used_str} / {total_str} ({percent:.1f}%)", percent

def color_for_percent(val, warn=70, danger=90):
    if val < warn:
        return "green"
    elif val < danger:
        return "orange"
    else:
        return "red"

def color_for_temp(temp):
    if temp < 65:
        return "green"
    elif temp < 80:
        return "orange"
    else:
        return "red"

def color_for_power(draw, limit):
    if draw < limit * 0.8:
        return "green"
    elif draw < limit * 0.95:
        return "orange"
    else:
        return "red"

def open_power_limit_window():
    global power_win
    if power_win is not None and tk.Toplevel.winfo_exists(power_win):
        power_win.lift()
        return
    cur, min_, max_ = get_power_limits()
    power_win = tk.Toplevel()
    power_win.title("Adjust GPU Power Limit")
    power_win.resizable(False, False)
    power_win.grab_set()
    ttk.Label(power_win, text=f"Current Power Limit: {cur if cur is not None else 'Unknown'} W", font=("Arial", 11)).pack(pady=5)
    ttk.Label(power_win, text=f"Min Power Limit: {min_ if min_ is not None else 'Unknown'} W", font=("Arial", 11)).pack()
    ttk.Label(power_win, text=f"Max Power Limit: {max_ if max_ is not None else 'Unknown'} W", font=("Arial", 11)).pack()
    ttk.Label(power_win, text="Enter new power limit (W):", font=("Arial", 11)).pack(pady=(10,0))
    entry = ttk.Entry(power_win, width=10)
    entry.pack()
    msg = tk.StringVar()
    msg_label = ttk.Label(power_win, textvariable=msg, font=("Arial", 10))
    msg_label.pack(pady=5)
    def apply_limit():
        try:
            val = float(entry.get())
            if min_ is not None and max_ is not None and (val < min_ or val > max_):
                msg.set(f"Value must be between {min_} and {max_} W.")
                msg_label.config(foreground="red")
                return
            ok, out = set_power_limit(val)
            if ok:
                msg.set("Power limit set successfully.")
                msg_label.config(foreground="green")
            else:
                msg.set(f"Failed: {out}")
                msg_label.config(foreground="red")
        except Exception as e:
            msg.set(f"Invalid input: {e}")
            msg_label.config(foreground="red")
    ttk.Button(power_win, text="Apply", command=apply_limit).pack(pady=5)
    ttk.Label(power_win, text="Note: Changing power limit may require admin/root privileges.", font=("Arial", 9, "italic")).pack(pady=(5,10))
    def on_close():
        global power_win
        power_win.destroy()
        power_win = None
    power_win.protocol("WM_DELETE_WINDOW", on_close)

# --- GUI Setup ---
root = tk.Tk()
root.title("NVIDIA-SMI GPU Monitor")
root.resizable(False, False)

# Store label references for updating
labels = {}

def init_gui():
    # Header
    name = get_gpu_info()
    header = ttk.Frame(root)
    header.pack(padx=10, pady=(10,0), fill="x")
    labels['gpu'] = ttk.Label(header, text=f"GPU: {name}", font=("Arial", 14, "bold"))
    labels['gpu'].pack(side="left", padx=(0,20))
    ttk.Button(header, text="Adjust Power Limit", command=open_power_limit_window).pack(side="right", padx=10)

    # Metrics Table
    table = ttk.Frame(root)
    table.pack(padx=10, pady=10)
    headers = ["Metric", "Value"]
    for col, text in enumerate(headers):
        ttk.Label(table, text=text, font=("Arial", 12, "bold")).grid(row=0, column=col, padx=8, pady=4)

    # Utilization
    labels['util'] = ttk.Label(table, font=("Arial", 11))
    labels['util'].grid(row=1, column=1, sticky="w")
    ttk.Label(table, text="Utilization", font=("Arial", 11)).grid(row=1, column=0, sticky="w")

    # Memory
    labels['mem'] = ttk.Label(table, font=("Arial", 11))
    labels['mem'].grid(row=2, column=1, sticky="w")
    ttk.Label(table, text="Memory Usage", font=("Arial", 11)).grid(row=2, column=0, sticky="w")

    # Temperature
    labels['temp'] = ttk.Label(table, font=("Arial", 11))
    labels['temp'].grid(row=3, column=1, sticky="w")
    ttk.Label(table, text="Temperature", font=("Arial", 11)).grid(row=3, column=0, sticky="w")

    # Power
    labels['power'] = ttk.Label(table, font=("Arial", 11))
    labels['power'].grid(row=4, column=1, sticky="w")
    ttk.Label(table, text="Power Draw", font=("Arial", 11)).grid(row=4, column=0, sticky="w")

    # Processes Table
    labels['proc_label'] = ttk.Label(root, text="Running GPU Processes", font=("Arial", 12, "bold"))
    labels['proc_label'].pack(pady=(10, 0))
    labels['proc_table'] = ttk.Treeview(root, columns=("PID", "Name", "Memory"), show="headings", height=6)
    labels['proc_table'].heading("PID", text="PID")
    labels['proc_table'].heading("Name", text="Process Name")
    labels['proc_table'].heading("Memory", text="GPU Memory")
    labels['proc_table'].column("PID", width=60, anchor="center")
    labels['proc_table'].column("Name", width=200, anchor="w")
    labels['proc_table'].column("Memory", width=100, anchor="center")
    labels['proc_table'].pack(padx=10, pady=5)

    # Collapsible nvidia-smi output
    def toggle_full_output():
        if labels['full_output_frame'].winfo_ismapped():
            labels['full_output_frame'].pack_forget()
            labels['show_btn'].config(text="Show Full nvidia-smi Output")
        else:
            labels['full_output_frame'].pack(padx=10, pady=5)
            labels['show_btn'].config(text="Hide Full nvidia-smi Output")

    labels['show_btn'] = ttk.Button(root, text="Show Full nvidia-smi Output", command=toggle_full_output)
    labels['show_btn'].pack(pady=5)
    labels['full_output_frame'] = ttk.Frame(root)
    labels['full_output_text'] = tk.Text(labels['full_output_frame'], height=12, width=90, font=("Courier New", 9), wrap="none")
    labels['full_output_text'].pack()
    labels['full_output_text'].config(state="disabled")

def update_gui():
    gpu_output, proc_output = get_nvidia_smi_output()
    if gpu_output.startswith("Error"):
        labels['gpu'].config(text=gpu_output)
        root.after(3000, update_gui)
        return

    metrics = parse_gpu_metrics(gpu_output)
    processes = parse_processes(proc_output)

    # Update metrics
    util_val = metrics.get("utilization", 0)
    util_color = color_for_percent(util_val)
    labels['util'].config(text=f"{util_val:.1f}%", foreground=util_color)

    mem_used = metrics.get("mem_used", 0)
    mem_total_val = metrics.get("mem_total", 1)
    mem_str, mem_percent = format_memory(mem_used, mem_total_val)
    mem_color = color_for_percent(mem_percent)
    labels['mem'].config(text=mem_str, foreground=mem_color)

    temp = metrics.get("temperature", 0)
    temp_color = color_for_temp(temp)
    labels['temp'].config(text=f"{temp}°C", foreground=temp_color)

    power_draw = metrics.get("power_draw", 0)
    power_limit = metrics.get("power_limit", 1)
    power_color = color_for_power(power_draw, power_limit)
    power_str = f"{power_draw:.1f} W / {power_limit:.1f} W"
    labels['power'].config(text=power_str, foreground=power_color)

    # Update processes table
    labels['proc_table'].delete(*labels['proc_table'].get_children())
    for proc in processes:
        labels['proc_table'].insert("", "end", values=(proc["pid"], proc["name"], proc["mem"]))

    # Update full nvidia-smi output
    labels['full_output_text'].config(state="normal")
    labels['full_output_text'].delete("1.0", tk.END)
    labels['full_output_text'].insert("1.0", subprocess.getoutput("nvidia-smi"))
    labels['full_output_text'].config(state="disabled")

    root.after(2000, update_gui)

init_gui()
update_gui()
root.mainloop()
import tkinter as tk
from tkinter import messagebox, simpledialog
import psutil
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import GPUtil
import platform
import shutil
from monitor import SystemMonitor  # Import SystemMonitor class from monitor.py


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("System Monitor")

        self.monitor = SystemMonitor()
        self.cpu_data = []
        self.gpu_data = []  # Store GPU usage data
        self.memory_data = []
        self.disk_data = []
        self.cpu_temp_data = []  # Store CPU temperatures
        self.gpu_temp_data = []  # Store GPU temperatures

        self.cpu_threshold = 80
        self.gpu_threshold = 80
        self.memory_threshold = 80
        self.disk_threshold = 80
        self.cpu_temp_threshold = 70
        self.gpu_temp_threshold = 70

        self.after_id = None #Store after_id so we can cancel later

        self.create_widgets()
        self.update_metrics()

    def create_widgets(self):
        # Configure dark theme colors
        bg_color = "#2E2E2E"
        fg_color = "white"

        self.root.configure(bg=bg_color)

        self.frame = tk.Frame(self.root, bg=bg_color)
        self.frame.pack(expand=True, fill=tk.BOTH)

        # CPU Usage Label
        self.cpu_label = tk.Label(self.frame, text="CPU Usage: ", bg=bg_color, fg=fg_color)
        self.cpu_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

        # GPU Usage Label
        self.gpu_label = tk.Label(self.frame, text="GPU Usage: ", bg=bg_color, fg=fg_color)
        self.gpu_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)

        # CPU Temperature Label
        self.cpu_temp_label = tk.Label(self.frame, text="CPU Temp: ", bg=bg_color, fg=fg_color)
        self.cpu_temp_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)

        # GPU Temperature Label
        self.gpu_temp_label = tk.Label(self.frame, text="GPU Temp: ", bg=bg_color, fg=fg_color)
        self.gpu_temp_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)

        # Memory Usage Label
        self.memory_label = tk.Label(self.frame, text="Memory Usage: ", bg=bg_color, fg=fg_color)
        self.memory_label.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)

        # Disk Usage Label
        self.disk_label = tk.Label(self.frame, text="Disk Usage: ", bg=bg_color, fg=fg_color)
        self.disk_label.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)

        # Disk Health Label
        self.disk_health_label = tk.Label(self.frame, text="Disk Health: ", bg=bg_color, fg=fg_color)
        self.disk_health_label.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)

        # Fan Speed Label
        self.fan_speed_label = tk.Label(self.frame, text="Fan Speed: ", bg=bg_color, fg=fg_color)
        self.fan_speed_label.grid(row=3, column=1, padx=10, pady=5, sticky=tk.W)

        # Log Metrics Button
        self.log_button = tk.Button(self.frame, text="Log Metrics", command=self.log_metrics, bg="#4CAF50",
                                     fg="white")
        self.log_button.grid(row=4, column=0, padx=10, pady=5, sticky=tk.W + tk.E)

        # Set Thresholds Button
        self.set_threshold_button = tk.Button(self.frame, text="Set Thresholds", command=self.set_thresholds,
                                                bg="#007BFF", fg="white")
        self.set_threshold_button.grid(row=4, column=1, padx=10, pady=5, sticky=tk.W + tk.E)

        # Metrics Plot
        self.figure, self.ax = plt.subplots(figsize=(8, 6), facecolor=bg_color)
        self.ax.set_facecolor(bg_color)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Set plot labels and title
        self.ax.set_title('System Metrics Over Time', color=fg_color)
        self.ax.set_xlabel('Time (s)', color=fg_color)
        self.ax.set_ylabel('Usage (%) / Temperature (°C)', color=fg_color)
        self.ax.tick_params(colors=fg_color, which='both')  # Set the color of tick labels

        # Add protocol handler for window close event
        self.root.protocol("WM_DELETE_WINDOW", self.close_window)

    def update_metrics(self):
        # Get system metrics
        cpu_usage = self.monitor.get_cpu_usage()
        memory_usage = self.monitor.get_memory_usage()
        disk_usage = self.monitor.get_disk_usage()
        disk_health = self.monitor.get_disk_health()
        fan_speed = self.monitor.get_fan_speed()
        cpu_temp = self.monitor.get_cpu_temperature()
        gpu_usage = self.monitor.get_gpu_usage()
        gpu_temp = self.monitor.get_gpu_temperature()

        # Update labels
        self.cpu_label.config(text=f"CPU Usage: {cpu_usage}%")
        self.gpu_label.config(text=f"GPU Usage: {gpu_usage}%")

        # Check if cpu_temp can be converted to float, for correct display
        if isinstance(cpu_temp, (int, float)):
            self.cpu_temp_label.config(text=f"CPU Temp: {cpu_temp}°C")
        else:
            self.cpu_temp_label.config(text=f"CPU Temp: Not Available")

        # Check if gpu_temp can be converted to float, for correct display
        if isinstance(gpu_temp, (int, float)):
            self.gpu_temp_label.config(text=f"GPU Temp: {gpu_temp}°C")
        else:
            self.gpu_temp_label.config(text=f"GPU Temp: Not Available")

        self.memory_label.config(text=f"Memory Usage: {memory_usage}%")
        self.disk_label.config(text=f"Disk Usage: {disk_usage}%")
        self.disk_health_label.config(text=f"Disk Health: {disk_health}")
        self.fan_speed_label.config(text=f"Fan Speed: {fan_speed} RPM")

        # Append data for plotting

        self.cpu_data.append(cpu_usage)
        self.gpu_data.append(gpu_usage)
        self.memory_data.append(memory_usage)
        self.disk_data.append(disk_usage)
        self.cpu_temp_data.append(cpu_temp)
        self.gpu_temp_data.append(gpu_temp)

        # Plot data
        self.ax.clear()
        self.ax.plot(self.cpu_data, label='CPU Usage', color='blue')
        self.ax.plot(self.gpu_data, label='GPU Usage', color='green')
        self.ax.plot(self.memory_data, label='Memory Usage', color='red')
        self.ax.plot(self.disk_data, label='Disk Usage', color='cyan')

        # Check if it's safe to plot temperatures
        if all(isinstance(temp, (int, float)) for temp in self.cpu_temp_data):
            self.ax.plot(self.cpu_temp_data, label='CPU Temp', color='magenta')
        if all(isinstance(temp, (int, float)) for temp in self.gpu_temp_data):
            self.ax.plot(self.gpu_temp_data, label='GPU Temp', color='yellow')

        self.ax.legend(loc='upper left', facecolor="#2E2E2E", edgecolor="white", labelcolor="white")
        self.ax.set_title('System Metrics Over Time', color='white')
        self.ax.set_xlabel('Time (s)', color='white')
        self.ax.set_ylabel('Usage (%) / Temperature (°C)', color='white')
        self.ax.tick_params(colors="white", which='both')

        self.canvas.draw()

        # Check thresholds and display warnings (Placeholder values)
        if cpu_usage > self.cpu_threshold:
            messagebox.showwarning("Warning", "CPU usage is high!")
        if gpu_usage > self.gpu_threshold:
            messagebox.showwarning("Warning", "GPU usage is high!")
        if memory_usage > self.memory_threshold:
            messagebox.showwarning("Warning", "Memory usage is high!")
        if disk_usage > self.disk_threshold:
            messagebox.showwarning("Warning", "Disk usage is high!")

        # Checking temperatures:
        if isinstance(cpu_temp, (int, float)) and cpu_temp > self.cpu_temp_threshold:
            messagebox.showwarning("Warning", "CPU temperature is high!")
        if isinstance(gpu_temp, (int, float)) and gpu_temp > self.gpu_temp_threshold:
            messagebox.showwarning("Warning", "GPU temperature is high!")
        try:
            self.after_id = self.root.after(1000, self.update_metrics)  # Update every 1 second
        except tk.TclError:
            pass #Do nothing, its already destroyed


    def log_metrics(self):
        cpu_usage = self.monitor.get_cpu_usage()
        memory_usage = self.monitor.get_memory_usage()
        disk_usage = self.monitor.get_disk_usage()
        cpu_temp = self.monitor.get_cpu_temperature()
        gpu_usage = self.monitor.get_gpu_usage()
        gpu_temp = self.monitor.get_gpu_temperature()
        self.monitor.log_metrics(cpu_usage, memory_usage, disk_usage, cpu_temp, gpu_usage, gpu_temp)
        messagebox.showinfo("Info", "Metrics logged successfully!")

    def set_thresholds(self):
        cpu_threshold = simpledialog.askinteger("Input", "Set CPU threshold (0-100):", minvalue=0, maxvalue=100,
                                                 initialvalue=self.cpu_threshold)
        if cpu_threshold is not None:
            self.cpu_threshold = cpu_threshold

        gpu_threshold = simpledialog.askinteger("Input", "Set GPU threshold (0-100):", minvalue=0, maxvalue=100,
                                                 initialvalue=self.gpu_threshold)
        if gpu_threshold is not None:
            self.gpu_threshold = gpu_threshold

        memory_threshold = simpledialog.askinteger("Input", "Set Memory threshold (0-100):", minvalue=0,
                                                    maxvalue=100, initialvalue=self.memory_threshold)
        if memory_threshold is not None:
            self.memory_threshold = memory_threshold

        disk_threshold = simpledialog.askinteger("Input", "Set Disk threshold (0-100):", minvalue=0, maxvalue=100,
                                                  initialvalue=self.disk_threshold)
        if disk_threshold is not None:
            self.disk_threshold = disk_threshold

        cpu_temp_threshold = simpledialog.askinteger("Input", "Set CPU Temperature threshold (°C):", minvalue=0,
                                                       maxvalue=100, initialvalue=self.cpu_temp_threshold)
        if cpu_temp_threshold is not None:
            self.cpu_temp_threshold = cpu_temp_threshold

        gpu_temp_threshold = simpledialog.askinteger("Input", "Set GPU Temperature threshold (°C):", minvalue=0,
                                                       maxvalue=100, initialvalue=self.gpu_temp_threshold)
        if gpu_temp_threshold is not None:
            self.gpu_temp_threshold = gpu_temp_threshold

    def close_window(self):
        if self.after_id:
            self.root.after_cancel(self.after_id) #Cancel update_metrics if running
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
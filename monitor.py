# monitor.py
import psutil
import datetime
import GPUtil
import platform
import shutil

class SystemMonitor:
    def __init__(self):
        self.log_file = "system_metrics.log"

    def get_cpu_usage(self):
        return psutil.cpu_percent()

    def get_memory_usage(self):
        memory_info = psutil.virtual_memory()
        return memory_info.percent

    def get_disk_usage(self):
        disk_info = psutil.disk_usage('/')
        return disk_info.percent

    def get_disk_health(self):
         try:
             # Only works on Windows
             import wmi
             c = wmi.WMI()
             for disk in c.Win32_DiskDrive():
                 return disk.Status
         except ImportError:
             return "Not available (Windows only)"

    def get_fan_speed(self):
        try:
            sensors = psutil.sensors_fans()
            fan_speed = 0
            for name, entries in sensors.items():
                for entry in entries:
                    fan_speed += entry.current
            return fan_speed  # Total speed of all fans
        except AttributeError:
            return "Not available"  # psutil version is too old
        except Exception as e:
            return f"Error: {e}"

    def get_cpu_temperature(self):
        try:
            temps = psutil.sensors_temperatures()
            if temps:
                for name, entries in temps.items():
                    for entry in entries:
                        if name == "coretemp": #Most common sensor name
                            try:
                                return float(entry.current)  # Try to convert to float
                            except ValueError:
                                return -1  # Return a default value if conversion fails
            return -1 # Or None if prefered
        except AttributeError:
            return -1 # Or None if prefered
        except Exception as e:
            print(f"Error getting CPU temperature: {e}") # Log the error
            return -1 # Or None if prefered

    def get_gpu_usage(self):
        try:
            gpus = GPUtil.getGPUs()
            if gpus:
                return gpus[0].load * 100  # Returns percentage usage of the first GPU
            return 0
        except Exception as e:
            return f"Not available {e}"

    def get_gpu_temperature(self):
        try:
            gpus = GPUtil.getGPUs()
            if gpus:
                return gpus[0].temperature
            return -1  # or None
        except Exception as e:
            return f"Not available {e}"


    def log_metrics(self, cpu, memory, disk, cpu_temp, gpu_usage, gpu_temp):
        with open(self.log_file, "a") as f:
            timestamp = datetime.datetime.now().isoformat()
            f.write(f"{timestamp}, CPU: {cpu}%, GPU: {gpu_usage}%, Memory: {memory}%, Disk: {disk}%, CPU Temp: {cpu_temp}°C, GPU Temp: {gpu_temp}°C\n")
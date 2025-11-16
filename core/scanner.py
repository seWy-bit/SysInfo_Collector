import psutil
import platform
import socket
from datetime import datetime

class SystemScanner:
    def __init__(self):
        self.scan_data = {}
        self.current_progress = 0
        self.current_operation = ""
    
    def scan_hardware(self):
        self.current_operation = "Сканирование аппаратного обеспечения"
        
        # Процессор
        cpu_info = {
            'processor': platform.processor(),
            'physical_cores': psutil.cpu_count(logical=False),
            'total_cores': psutil.cpu_count(logical=True),
            'frequency': psutil.cpu_freq().current if psutil.cpu_freq() else None
        }
        
        # Память
        memory = psutil.virtual_memory()
        memory_info = {
            'total': round(memory.total / (1024**3), 2),
            'available': round(memory.available / (1024**3), 2),
            'used_percent': memory.percent
        }
        
        # Диски
        disks = []
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disk_info = {
                    'device': partition.device,
                    'total': round(usage.total / (1024**3), 2),
                    'used': round(usage.used / (1024**3), 2),
                    'free': round(usage.free / (1024**3), 2),
                    'percent': usage.percent
                }
                disks.append(disk_info)
            except PermissionError:
                continue
        
        return {
            'cpu': cpu_info,
            'memory': memory_info,
            'disks': disks
        }
    
    def scan_software(self):
        self.current_operation = "Сканирование программного обеспечения"
        
        os_info = {
            'system': platform.system(),
            'release': platform.release(),
            'version': platform.version(),
            'hostname': socket.gethostname()
        }
        
        return {
            'os': os_info,
            'installed_software': []
        }
    
    def scan_network(self):
        self.current_operation = "Сканирование сетевых настроек"
        
        interfaces = []
        for name, addresses in psutil.net_if_addrs().items():
            interface_info = {
                'name': name,
                'addresses': [
                    {
                        'family': str(addr.family),
                        'address': addr.address,
                        'netmask': addr.netmask
                    }
                    for addr in addresses
                ]
            }
            interfaces.append(interface_info)
        
        return {
            'interfaces': interfaces
        }
    
    def selective_scan(self, categories):
        print("Запуск выборочного сканирования...")
        
        result = {
            'timestamp': datetime.now().isoformat(),
            'scan_categories': {}
        }
        
        if categories.get('hardware', False):
            result['scan_categories']['hardware'] = self.scan_hardware()
        
        if categories.get('software', False):
            result['scan_categories']['software'] = self.scan_software()
        
        if categories.get('network', False):
            result['scan_categories']['network'] = self.scan_network()
        
        print("Выборочное сканирование завершено!")
        return result
    
    def get_scan_progress(self):
        return {
            'current_operation': self.current_operation,
            'progress': self.current_progress
        }
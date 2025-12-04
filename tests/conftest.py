import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def sample_scan_data():
    """Фикстура с тестовыми данными сканирования."""
    return {
        'timestamp': '2024-01-01T12:00:00',
        'scan_categories': {
            'hardware': {
                'cpu': {'processor': 'Intel', 'cores': 8},
                'memory': {'total': 16, 'used': 8}
            },
            'software': {
                'os': {'system': 'Windows', 'version': '10'}
            },
            'network': {
                'interfaces': [{'name': 'eth0', 'ip': '192.168.1.1'}]
            }
        }
    }

@pytest.fixture
def scanner_instance():
    """Фикстура для экземпляра SystemScanner."""
    from core.scanner import SystemScanner
    return SystemScanner()

@pytest.fixture
def exporter_instance():
    """Фикстура для экземпляра DataExporter."""
    from core.exporter import DataExporter
    return DataExporter()
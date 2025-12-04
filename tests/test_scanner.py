import pytest
import sys
import platform
from unittest.mock import patch, MagicMock

class TestSystemScanner:
    """Тесты для класса SystemScanner."""
    
    def test_scanner_initialization(self, scanner_instance):
        """Тест инициализации сканера."""
        assert scanner_instance.scan_data == {}
        assert scanner_instance.current_progress == 0
        assert scanner_instance.current_operation == ""
    
    def test_scan_hardware_cpu_info(self, scanner_instance):
        """Тест сбора информации о процессоре."""
        with patch('psutil.cpu_count') as mock_cpu_count, \
             patch('psutil.cpu_freq') as mock_cpu_freq, \
             patch('platform.processor') as mock_processor:
            
            mock_cpu_count.side_effect = [4, 8]  # physical, logical
            mock_cpu_freq.return_value = MagicMock(current=3600.0)
            mock_processor.return_value = 'Intel(R) Core(TM) i7'
            
            result = scanner_instance.scan_hardware()
            
            assert 'cpu' in result
            assert result['cpu']['physical_cores'] == 4
            assert result['cpu']['total_cores'] == 8
            assert result['cpu']['frequency'] == 3600.0
    
    def test_scan_hardware_memory_info(self, scanner_instance):
        """Тест сбора информации о памяти."""
        with patch('psutil.virtual_memory') as mock_memory:
            mock_memory.return_value = MagicMock(
                total=16 * 1024**3,  # 16 GB
                available=8 * 1024**3,  # 8 GB
                percent=50.0
            )
            
            result = scanner_instance.scan_hardware()
            
            assert 'memory' in result
            assert result['memory']['total'] == 16.0
            assert result['memory']['available'] == 8.0
            assert result['memory']['used_percent'] == 50.0
    
    def test_scan_software_os_info(self, scanner_instance):
        """Тест сбора информации об ОС."""
        with patch('platform.system') as mock_system, \
             patch('platform.release') as mock_release, \
             patch('platform.version') as mock_version, \
             patch('socket.gethostname') as mock_hostname:
            
            mock_system.return_value = 'Windows'
            mock_release.return_value = '10'
            mock_version.return_value = '10.0.19045'
            mock_hostname.return_value = 'DESKTOP-ABC123'
            
            result = scanner_instance.scan_software()
            
            assert 'os' in result
            assert result['os']['system'] == 'Windows'
            assert result['os']['release'] == '10'
            assert result['os']['hostname'] == 'DESKTOP-ABC123'
    
    def test_selective_scan_hardware_only(self, scanner_instance):
        """Тест выборочного сканирования только аппаратного обеспечения."""
        categories = {'hardware': True, 'software': False, 'network': False}
        
        with patch.object(scanner_instance, 'scan_hardware') as mock_scan:
            mock_scan.return_value = {'cpu': 'test', 'memory': 'test'}
            
            result = scanner_instance.selective_scan(categories)
            
            assert 'hardware' in result['scan_categories']
            assert 'software' not in result['scan_categories']
            assert 'network' not in result['scan_categories']
            assert 'timestamp' in result
    
    def test_selective_scan_no_categories(self, scanner_instance):
        """Негативный тест: сканирование без выбранных категорий."""
        categories = {'hardware': False, 'software': False, 'network': False}
        
        result = scanner_instance.selective_scan(categories)
        
        assert result['scan_categories'] == {}
        assert 'timestamp' in result
    
    @pytest.mark.parametrize("category_count,expected_progress", [
        (1, 100),  # Одна категория = 100% прогресса
        (2, 50),   # Две категории = 50% за каждую
        (3, 33.33) # Три категории = ~33.33% за каждую
    ])
    def test_scan_progress_calculation(self, scanner_instance, category_count, expected_progress):
        """Параметризованный тест расчета прогресса сканирования."""
        categories = {
            'hardware': category_count >= 1,
            'software': category_count >= 2,
            'network': category_count >= 3
        }
        
        # Мокаем методы сканирования
        with patch.object(scanner_instance, 'scan_hardware'), \
             patch.object(scanner_instance, 'scan_software'), \
             patch.object(scanner_instance, 'scan_network'):
            
            scanner_instance.selective_scan(categories)
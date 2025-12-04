import pytest
import json
import xml.etree.ElementTree as ET
import os
import tempfile
from unittest.mock import patch, MagicMock

class TestDataExporter:
    """Тесты для класса DataExporter."""
    
    def test_export_json_success(self, exporter_instance, sample_scan_data):
        """Тест успешного экспорта в JSON."""
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            result = exporter_instance.export_json(sample_scan_data, tmp_path)
            
            assert result['success'] is True
            assert result['filename'] == tmp_path
            
            # Проверяем, что файл создан и содержит валидный JSON
            with open(tmp_path, 'r', encoding='utf-8') as f:
                loaded_data = json.load(f)
            
            assert loaded_data['timestamp'] == sample_scan_data['timestamp']
            assert 'hardware' in loaded_data['scan_categories']
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    
    def test_export_json_automatic_filename(self, exporter_instance, sample_scan_data):
        """Тест экспорта в JSON с автоматическим именем файла."""
        result = exporter_instance.export_json(sample_scan_data)
        
        assert result['success'] is True
        assert result['filename'].endswith('.json')
        assert 'system_info_' in result['filename']
        
        # Удаляем созданный файл
        if os.path.exists(result['filename']):
            os.unlink(result['filename'])
    
    def test_export_xml_success(self, exporter_instance, sample_scan_data):
        """Тест успешного экспорта в XML."""
        with tempfile.NamedTemporaryFile(suffix='.xml', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            result = exporter_instance.export_xml(sample_scan_data, tmp_path)
            
            assert result['success'] is True
            assert result['filename'] == tmp_path
            
            # Проверяем, что файл создан и содержит валидный XML
            tree = ET.parse(tmp_path)
            root = tree.getroot()
            
            assert root.tag == 'SystemInfo'
            assert len(root.find('categories')) > 0
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    
    import tempfile

    def test_export_json_invalid_path(self, exporter_instance, sample_scan_data):
        """Негативный тест: симуляция ошибки при создании директории."""
        invalid_path = '/nonexistent/path/system_info.json'
        
        # Мокаем os.makedirs, чтобы он вызывал исключение
        with patch('os.makedirs') as mock_makedirs:
            # Симулируем PermissionError (нет прав на запись)
            mock_makedirs.side_effect = PermissionError("Отказано в доступе")
            
            result = exporter_instance.export_json(sample_scan_data, invalid_path)
            
            assert result['success'] is False
            assert 'error' in result
            # Проверяем, что в ошибке содержится информация об отказе в доступе
            assert "Отказано в доступе" in result['error']
    
    def test_export_xml_with_special_characters(self, exporter_instance):
        """Тест экспорта XML с особыми символами в данных."""
        test_data = {
            'timestamp': '2024-01-01T12:00:00',
            'scan_categories': {
                'test': {
                    'name': 'Тест & <спец> "символов" \'в\' данных',
                    'value': 100
                }
            }
        }
        
        with tempfile.NamedTemporaryFile(suffix='.xml', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            result = exporter_instance.export_xml(test_data, tmp_path)
            
            assert result['success'] is True
            
            # Проверяем, что XML парсится без ошибок
            tree = ET.parse(tmp_path)
            root = tree.getroot()
            
            # Проверяем экранирование символов
            with open(tmp_path, 'r', encoding='utf-8') as f:
                content = f.read()
                assert '&amp;' in content  # Амперсанд должен быть экранирован
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    
    def test_dict_to_xml_conversion(self, exporter_instance):
        """Тест внутреннего метода преобразования dict в XML."""
        test_dict = {
            'cpu': {
                'name': 'Intel',
                'cores': [4, 8],
                'frequency': 3600
            }
        }
        
        import xml.etree.ElementTree as ET
        parent = ET.Element('test')
        
        # Вызываем приватный метод через экземпляр класса
        exporter_instance._dict_to_xml(parent, test_dict)
        
        # Проверяем структуру XML
        assert parent.find('cpu') is not None
        assert parent.find('cpu/name').text == 'Intel'
        assert len(parent.findall('cpu/cores/item')) == 2
        assert parent.find('cpu/frequency').text == '3600'
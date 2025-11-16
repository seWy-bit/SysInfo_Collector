import json
import xml.etree.ElementTree as ET
from datetime import datetime
import os

class DataExporter:
    @staticmethod
    def export_json(data, filename=None):
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"system_info_{timestamp}.json"
        
        try:
            directory = os.path.dirname(filename)
            if directory:
                os.makedirs(directory, exist_ok=True)
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return {'success': True, 'filename': filename}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def export_xml(data, filename=None):
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"system_info_{timestamp}.xml"
        
        try:
            directory = os.path.dirname(filename)
            if directory:
                os.makedirs(directory, exist_ok=True)
            
            root = ET.Element("SystemInfo")

            timestamp_elem = ET.SubElement(root, "timestamp")
            timestamp_elem.text = data.get('timestamp', '')

            categories = ET.SubElement(root, "categories")
            for category_name, category_data in data.get('scan_categories', {}).items():
                category_elem = ET.SubElement(categories, category_name)

                DataExporter._dict_to_xml(category_elem, category_data)

            tree = ET.ElementTree(root)
            tree.write(filename, encoding='utf-8', xml_declaration=True)
            return {'success': True, 'filename': filename}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def _dict_to_xml(parent, data):
        if isinstance(data, dict):
            for key, value in data.items():
                child = ET.SubElement(parent, key.replace(' ', '_'))
                DataExporter._dict_to_xml(child, value)
        elif isinstance(data, list):
            for item in data:
                child = ET.SubElement(parent, 'item')
                DataExporter._dict_to_xml(child, item)
        else:
            parent.text = str(data)
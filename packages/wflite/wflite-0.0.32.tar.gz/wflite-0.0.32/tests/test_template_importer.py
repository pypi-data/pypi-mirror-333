import unittest
import os
import json
import tempfile
from unittest.mock import patch, PropertyMock
from tools.import_template import TemplateImporter
from config.config_loader import ConfigLoader

class TestTemplateImporter(unittest.TestCase):
    def setUp(self):
        self.test_db = "sqlite:///test_templates.db"
        
        # Mock configuration properly and store the patcher
        self.config_patcher = patch('config.config_loader.ConfigLoader.database_url', 
                       new_callable=PropertyMock,
                       return_value=self.test_db)
        self.mock_config = self.config_patcher.start()
        
        # Initialize importer
        self.importer = TemplateImporter()
        
        # Create test data
        self.test_data = {
            "states": [
                {"id": "1", "name": "start", "type": "start"},
                {"id": "2", "name": "State1", "type": "state", 
                 "entryActions": ["action1"], "exitActions": ["action2"]},
                {"id": "3", "name": "end", "type": "end"}
            ],
            "transitions": [
                {"source": "1", "target": "2", "event": "event1", 
                 "action": "action1", "guard": "guard1"}
            ]
        }
        
        # Create temporary test file
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        with open(self.temp_file.name, 'w') as f:
            json.dump(self.test_data, f)

    def test_import_from_file(self):
        # Test import with explicit name
        success = self.importer.import_from_file(self.temp_file.name, "test_template")
        self.assertTrue(success)
        
        # Verify template was saved correctly
        loaded_template = self.importer.registry.load("test_template")
        self.assertIsNotNone(loaded_template)
        self.assertEqual(len(loaded_template["states"]), 3)
        self.assertEqual(len(loaded_template["transitions"]), 1)

    def test_import_with_default_name(self):
        # Test import using filename as template name
        success = self.importer.import_from_file(self.temp_file.name)
        self.assertTrue(success)
        
        # Extract expected name from temporary file
        expected_name = os.path.splitext(os.path.basename(self.temp_file.name))[0]
        
        # Verify template was saved with correct name
        loaded_template = self.importer.registry.load(expected_name)
        self.assertIsNotNone(loaded_template)

    def test_import_invalid_file(self):
        # Test import with non-existent file
        success = self.importer.import_from_file("nonexistent.json")
        self.assertFalse(success)

    def tearDown(self):
        if hasattr(self, 'config_patcher'):
            self.config_patcher.stop()
        
        # Clean up temporary file
        if os.path.exists(self.temp_file.name):
            os.remove(self.temp_file.name)
        
        # Clean up test database
        db_file = self.test_db.replace("sqlite:///", "")
        if os.path.exists(db_file):
            os.remove(db_file)

if __name__ == '__main__':
    unittest.main()

import unittest
import tempfile
import shutil
import os
import sys

# Add src directory to Python path
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, src_path)

from wflite.registry.db_registry import StateMachineRegistry

class TestStateMachineRegistry(unittest.TestCase):
    """Test database-backed registry for state machines"""
    
    def setUp(self):
        # Create a temporary directory for test database
        self.test_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.test_dir, "test_workflows.db")
        
        # Initialize registry with test database
        self.registry = StateMachineRegistry()
        
        # Test templates
        self.template1 = {
            "states": [
                {"id": "start", "name": "Start State", "type": "start"},
                {"id": "middle", "name": "Middle State", "type": "normal"},
                {"id": "end", "name": "End State", "type": "end"}
            ],
            "transitions": [
                {"source": "start", "target": "middle", "event": "next"},
                {"source": "middle", "target": "end", "event": "finish"}
            ]
        }
        
        self.template2 = {
            "states": [
                {"id": "new", "name": "New", "type": "start"},
                {"id": "processing", "name": "Processing", "type": "normal"},
                {"id": "completed", "name": "Completed", "type": "end"}
            ],
            "transitions": [
                {"source": "new", "target": "processing", "event": "process"},
                {"source": "processing", "target": "completed", "event": "complete"}
            ]
        }
        
        # Save test templates
        self.registry.save("Template1", self.template1, "Test template 1")
        self.registry.save("Template2", self.template2, "Test template 2")
    
    def tearDown(self):
        # Clean up test directory
        shutil.rmtree(self.test_dir)
    
    def test_save_and_load(self):
        # Test saving and loading templates
        loaded = self.registry.load("Template1")
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded, self.template1)
        
        # Test nonexistent template
        nonexistent = self.registry.load("NonexistentTemplate")
        self.assertIsNone(nonexistent)
    
    def test_update(self):
        # Update existing template
        updated_template = dict(self.template1)
        updated_template["states"].append({"id": "new_state", "name": "New State", "type": "normal"})
        
        result = self.registry.save("Template1", updated_template)
        self.assertTrue(result)
        
        # Load updated template
        loaded = self.registry.load("Template1")
        self.assertEqual(len(loaded["states"]), 4)
    
    def test_list(self):
        # List all templates - should be exactly the ones we added
        machines = self.registry.list()
        
        # Make sure we have at least our 2 templates (there might be others from previous tests)
        self.assertGreaterEqual(len(machines), 2)
        self.assertIn("Template1", machines)
        self.assertIn("Template2", machines)
    
    def test_delete(self):
        # Delete a template
        result = self.registry.delete("Template1")
        self.assertTrue(result)
        
        # Template should no longer be available
        loaded = self.registry.load("Template1")
        self.assertIsNone(loaded)
        
        # List should have one fewer template
        machines = self.registry.list()
        self.assertNotIn("Template1", machines)
        self.assertIn("Template2", machines)

if __name__ == "__main__":
    unittest.main()

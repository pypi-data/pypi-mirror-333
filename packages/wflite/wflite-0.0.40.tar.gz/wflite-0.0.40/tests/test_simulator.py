import unittest
import tempfile
import os
import os
import sys

# Add src directory to Python path
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, src_path)

from wflite.runtime.statemachine_runtime import StateMachineRuntime

class TestStateMachineSimulator(unittest.TestCase):
    def setUp(self):
        self.simulator = StateMachineRuntime()
        self.template_data = {
            "states": [
                {"id": "1", "name": "start", "type": "start"},
                {"id": "2", "name": "state1", "type": "state"},
                {"id": "3", "name": "end", "type": "end"}
            ],
            "transitions": [
                {"source": "1", "target": "2", "event": "event1"},
                {"source": "2", "target": "3", "event": "event2"}
            ]
        }
        
    def test_context_merge(self):
        """Test that context is properly merged during multiple events"""
        instance_id = "test-merge-001"
        
        # Create instance
        self.simulator.create_instance(instance_id, "test_template", self.template_data)
        
        # First event with initial data
        event_details1 = {
            "data": {
                "key1": "value1",
                "key2": "value2"
            }
        }
        self.simulator.trigger_event(instance_id, "event1", self.template_data, event_details1)
        
        # Verify first context update
        context1 = self.simulator.get_raw_context(instance_id)
        self.assertEqual(context1["key1"], "value1")
        self.assertEqual(context1["key2"], "value2")
        
        # Second event with additional data
        event_details2 = {
            "data": {
                "key3": "value3",
                "key2": "updated_value2"  # This should override the previous value
            }
        }
        self.simulator.trigger_event(instance_id, "event2", self.template_data, event_details2)
        
        # Verify merged context
        context2 = self.simulator.get_raw_context(instance_id)
        self.assertEqual(context2["key1"], "value1")  # Original value preserved
        self.assertEqual(context2["key2"], "updated_value2")  # Value updated
        self.assertEqual(context2["key3"], "value3")  # New value added
        
    def test_direct_context_merge(self):
        """Test that direct context updates (without 'data' key) are merged properly"""
        instance_id = "test-direct-merge-001"
        
        # Create instance
        self.simulator.create_instance(instance_id, "test_template", self.template_data)
        
        # First event with direct context
        event_details1 = {
            "direct_key1": "direct_value1",
            "shared_key": "original_value"
        }
        self.simulator.trigger_event(instance_id, "event1", self.template_data, event_details1)
        
        # Verify first context update
        context1 = self.simulator.get_raw_context(instance_id)
        self.assertEqual(context1["direct_key1"], "direct_value1")
        self.assertEqual(context1["shared_key"], "original_value")
        
        # Second event with more direct context
        event_details2 = {
            "direct_key2": "direct_value2",
            "shared_key": "updated_value"
        }
        self.simulator.trigger_event(instance_id, "event2", self.template_data, event_details2)
        
        # Verify merged context
        context2 = self.simulator.get_raw_context(instance_id)
        self.assertEqual(context2["direct_key1"], "direct_value1")  # Original value preserved
        self.assertEqual(context2["direct_key2"], "direct_value2")  # New value added
        self.assertEqual(context2["shared_key"], "updated_value")  # Value updated

if __name__ == '__main__':
    unittest.main()

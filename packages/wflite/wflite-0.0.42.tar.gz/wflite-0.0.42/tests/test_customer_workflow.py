import unittest
import sys
import os

# Add project root to Python path
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, src_path)

from wflite.runtime.statemachine_runtime import StateMachineRuntime
from wflite.registry.db_registry import StateMachineRegistry

class TestCustomerWorkflow(unittest.TestCase):
    def setUp(self):
        self.simulator = StateMachineRuntime()
        self.registry = StateMachineRegistry()
        
        # Sample template data
        self.template_data = {
            "name": "test_workflow",
            "states": [
                {"id": "1", "name": "Start", "type": "start"},
                {"id": "2", "name": "Processing", "type": "normal"},
                {"id": "3", "name": "End", "type": "end"}
            ],
            "transitions": [
                {"source": "1", "target": "2", "event": "begin"},
                {"source": "2", "target": "3", "event": "finish"}
            ]
        }
        
        # Save test template
        self.registry.save("test_template", self.template_data)

    def test_assign_workflow_to_customer(self):
        """Test assigning a workflow template to a customer"""
        customer_id = "TEST-CUST-001"
        template_name = "test_template"
        
        # Assign workflow
        success = self.simulator.assign_customer_workflow(
            customer_id, template_name, self.template_data
        )
        self.assertTrue(success)
        
        # Verify assignment
        template, instance_id = self.simulator.get_customer_instance(customer_id)
        self.assertEqual(template, template_name)
        self.assertIsNotNone(instance_id)

    def test_customer_workflow_state(self):
        """Test that customer workflow maintains correct state"""
        customer_id = "TEST-CUST-002"
        template_name = "test_template"
        
        # Assign and verify initial state
        self.simulator.assign_customer_workflow(customer_id, template_name, self.template_data)
        template, instance_id = self.simulator.get_customer_instance(customer_id)
        
        current_state = self.simulator.get_current_state(instance_id, self.template_data)
        self.assertEqual(current_state["id"], "1")  # Should be in start state

    def test_reassign_workflow(self):
        """Test reassigning a workflow to a customer with existing assignment"""
        customer_id = "TEST-CUST-003"
        
        # First assignment
        self.simulator.assign_customer_workflow(
            customer_id, "test_template", self.template_data
        )
        _, first_instance = self.simulator.get_customer_instance(customer_id)
        
        # Second assignment
        self.simulator.assign_customer_workflow(
            customer_id, "test_template", self.template_data
        )
        _, second_instance = self.simulator.get_customer_instance(customer_id)
        
        # Verify new assignment
        self.assertNotEqual(first_instance, second_instance)

    def test_customer_workflow_context(self):
        """Test that customer workflow maintains context correctly"""
        customer_id = "TEST-CUST-004"
        template_name = "test_template"
        
        # Assign workflow
        self.simulator.assign_customer_workflow(customer_id, template_name, self.template_data)
        _, instance_id = self.simulator.get_customer_instance(customer_id)
        
        # Trigger event with context
        event_details = {
            "customer_data": "test_value",
            "data": {"nested_data": "test_nested"}
        }
        
        success, _ = self.simulator.trigger_event(
            instance_id, "begin", self.template_data, event_details
        )
        self.assertTrue(success)
        
        # Verify context
        context = self.simulator.get_raw_context(instance_id)
        self.assertEqual(context.get("customer_data"), "test_value")
        self.assertEqual(context.get("nested_data"), "test_nested")

    def tearDown(self):
        """Clean up after tests"""
        # Remove test template
        self.registry.delete("test_template")

if __name__ == '__main__':
    unittest.main()

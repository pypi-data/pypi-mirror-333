import unittest
import sys
import os
import tempfile

# Add src directory to Python path
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, src_path)

from wflite.core.statemachine_core import State, Event, StateMachine, Transition
from wflite.runtime.statemachine_runtime import StateMachineRuntime
from wflite.registry.repository_mock import StateMachineRepository


class RuntimeIntegrationTest(unittest.TestCase):
    """Test integration between state machine core and runtime"""
    
    def setUp(self):
        # Create registry with test templates
        self.registry = StateMachineRepository()
        
        # Create OrderProcess template
        order_process = {
            "states": [
                {"id": "New", "name": "New", "type": "start"},
                {"id": "Processing", "name": "Processing", "type": "normal"},
                {"id": "Completed", "name": "Completed", "type": "end"}
            ],
            "transitions": [
                {"source": "New", "target": "Processing", "event": "process"},
                {"source": "Processing", "target": "Completed", "event": "complete"}
            ]
        }
        self.registry.register_template("OrderProcess", order_process)
        
        # Create DefaultProcess template
        default_process = {
            "states": [
                {"id": "New", "name": "New", "type": "start"},
                {"id": "Processing", "name": "Processing", "type": "normal"},
                {"id": "Completed", "name": "Completed", "type": "end"}
            ],
            "transitions": [
                {"source": "New", "target": "Processing", "event": "process"},
                {"source": "Processing", "target": "Completed", "event": "complete"}
            ]
        }
        self.registry.register_template("DefaultProcess", default_process)
        
        # Initialize runtime with mock registry
        self.runtime = StateMachineRuntime(registry_provider=self.registry)
    
    def test_get_new_state_machine(self):
        # Get a state machine for a customer
        sm = self.runtime.get_state_machine("customer-001")
        self.assertIsNotNone(sm)
        self.assertEqual(sm.name, "OrderProcess")
        self.assertEqual(sm.current_state.name, "New")
    
    def test_send_event(self):
        # Set up a state machine directly for testing
        sm = StateMachine("OrderProcess")
        new_state = State("New")
        processing_state = State("Processing")
        
        # Add states
        sm.add_state(new_state)
        sm.add_state(processing_state)
        
        # Add transition
        event = Event("process")
        transition = Transition(
            source_state=new_state,
            target_state=processing_state,
            event=event
        )
        new_state.add_transition(transition)
        sm.initialize()
        
        # Set the test machine in runtime's cache
        test_customer = "test-customer"
        instance_id = self.runtime._generate_instance_id("OrderProcess", test_customer)
        self.runtime.active_machines[instance_id] = sm
        
        # Associate with customer
        self.runtime.customer_manager.assign_workflow(test_customer, "OrderProcess", instance_id)
        
        # Send event and update context
        success = self.runtime.send_event(test_customer, "process", {"order_id": "ORD-123"})
        self.assertTrue(success)
        
        # Check new state
        self.assertEqual(sm.current_state.name, "Processing")
        
        # Check context
        self.assertEqual(sm.context.get("order_id"), "ORD-123")
    
    def test_default_state_machine(self):
        # Get state machine for unknown customer
        sm = self.runtime.get_state_machine("unknown-customer")
        self.assertIsNotNone(sm)
        self.assertEqual(sm.name, "DefaultProcess")
    
    def test_context_update(self):
        # Create a test machine directly
        sm = StateMachine("TestMachine")
        state = State("TestState")
        sm.add_state(state)
        sm.initialize()
        
        # Add context values
        sm.context = {}
        sm.set_context("order_id", "ORD-123")
        
        # Register in runtime
        instance_id = "test-instance"
        self.runtime.active_machines[instance_id] = sm
        
        # Verify context
        self.assertEqual(sm.context.get("order_id"), "ORD-123")


if __name__ == "__main__":
    unittest.main()

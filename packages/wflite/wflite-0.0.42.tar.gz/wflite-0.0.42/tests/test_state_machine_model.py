import unittest
import sys
import os

# Add src directory to Python path
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, src_path)

from wflite.core.statemachine_core import State, Event, Transition, StateMachine, StateMachineModel


class StateMachineModelTest(unittest.TestCase):
    """Test state machine model serialization/deserialization"""
    
    def setUp(self):
        self.sm = StateMachine("ModelTestMachine")
        
        # Create states
        self.state1 = State("State1")
        self.state2 = State("State2")
        
        # Add states
        self.sm.add_state(self.state1)
        self.sm.add_state(self.state2)
        
        # Create event and transition
        self.event = Event("go")
        self.transition = Transition(
            source_state=self.state1,
            target_state=self.state2,
            event=self.event
        )
        
        # Add transition
        self.state1.add_transition(self.transition)
        
        # Initialize
        self.sm.initialize()
        
        # Set context data
        self.sm.set_context("key1", "value1")
        self.sm.set_context("key2", 42)
    
    def test_model_creation(self):
        # Create model from state machine
        model = StateMachineModel.from_state_machine(self.sm, customer_id="CUST-001")
        
        # Check model properties
        self.assertEqual(model.id, self.sm.id)
        self.assertEqual(model.name, "ModelTestMachine")
        self.assertEqual(model.current_state, "State1")
        self.assertEqual(model.customer_id, "CUST-001")
        self.assertEqual(model.context["key1"], "value1")
        self.assertEqual(model.context["key2"], 42)
    
    def test_model_without_customer_id(self):
        # Create model without customer ID
        model = StateMachineModel.from_state_machine(self.sm)
        
        # Check model properties
        self.assertIsNone(model.customer_id)
        
    def test_model_after_transition(self):
        # Trigger transition
        self.sm.send_event(self.event)
        
        # Create model from updated state machine
        model = StateMachineModel.from_state_machine(self.sm)
        
        # Check current state is updated
        self.assertEqual(model.current_state, "State2")


if __name__ == "__main__":
    unittest.main()

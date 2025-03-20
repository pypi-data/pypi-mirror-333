import unittest
import sys
import os

# Add src directory to Python path
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, src_path)

from wflite.core.statemachine_core import State, Event, Action, Transition, StateMachine


class BasicStateMachineTest(unittest.TestCase):
    """Test basic state machine functionality"""

    def setUp(self):
        self.sm = StateMachine("TestMachine")

        # Create states
        self.state1 = State("State1")
        self.state2 = State("State2")
        self.state3 = State("State3")

        # Add states to machine
        self.sm.add_state(self.state1)
        self.sm.add_state(self.state2)
        self.sm.add_state(self.state3)

        # Create events
        self.event1 = Event("event1")
        self.event2 = Event("event2")

        # Create transitions
        self.transition1 = Transition(
            source_state=self.state1,
            target_state=self.state2,
            event=self.event1
        )

        self.transition2 = Transition(
            source_state=self.state2,
            target_state=self.state3,
            event=self.event2
        )

        # Add transitions to states
        self.state1.add_transition(self.transition1)
        self.state2.add_transition(self.transition2)

        # Initialize state machine
        self.sm.initialize()

    def test_initial_state(self):
        self.assertEqual(self.sm.current_state, self.state1)

    def test_transition(self):
        # First transition
        result = self.sm.send_event(self.event1)
        self.assertTrue(result)
        self.assertEqual(self.sm.current_state, self.state2)

        # Second transition
        result = self.sm.send_event(self.event2)
        self.assertTrue(result)
        self.assertEqual(self.sm.current_state, self.state3)

    def test_invalid_event(self):
        # Try invalid event
        invalid_event = Event("invalid")
        result = self.sm.send_event(invalid_event)
        self.assertFalse(result)
        self.assertEqual(self.sm.current_state, self.state1)

    def test_context_manipulation(self):
        # Set context values
        self.sm.set_context("key1", "value1")
        self.sm.set_context("key2", 42)

        # Get context
        context = self.sm.get_context()
        
        self.assertEqual(context["key1"], "value1")
        self.assertEqual(context["key2"], 42)


if __name__ == "__main__":
    unittest.main()

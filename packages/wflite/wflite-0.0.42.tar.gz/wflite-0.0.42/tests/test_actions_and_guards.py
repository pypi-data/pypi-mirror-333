import unittest
import sys
import os

# Add project root to Python path
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, src_path)

from wflite.core.statemachine_core import State, Event, Action, Transition, StateMachine, ActionHandler


class MockActionHandler(ActionHandler):
    def __init__(self):
        self.executed_actions = []
        
    def can_handle(self, action_type: str) -> bool:
        return True
    
    def handle_action(self, action, context):
        self.executed_actions.append(action)


class ActionsTest(unittest.TestCase):
    """Test actions in state machines"""

    def setUp(self):
        self.sm = StateMachine("ActionTestMachine")
        
        # Create action context tracking
        self.action_context = {}
        
        # Create actions
        self.entry_action = Action("entry_action", lambda ctx: ctx.update({"entry_executed": True}))
        self.exit_action = Action("exit_action", lambda ctx: ctx.update({"exit_executed": True}))
        self.transition_action = Action("transition_action", lambda ctx: ctx.update({"transition_executed": True}))
        
        # Create states with entry/exit actions
        self.state1 = State("State1", entry_actions=[self.entry_action], exit_actions=[self.exit_action])
        self.state2 = State("State2")
        
        # Add states
        self.sm.add_state(self.state1)
        self.sm.add_state(self.state2)
        
        # Create events and transitions
        self.event = Event("go")
        self.transition = Transition(
            source_state=self.state1,
            target_state=self.state2,
            event=self.event,
            actions=[self.transition_action]
        )
        
        # Add transitions
        self.state1.add_transition(self.transition)
        
        # Set the context
        self.sm.context = self.action_context
        
        # Mock action handler
        self.handler = MockActionHandler()

    def test_entry_actions(self):
        # Initialize should execute entry actions
        self.sm.initialize()
        self.assertTrue(self.action_context.get("entry_executed", False))
    
    def test_exit_and_transition_actions(self):
        # Initialize and then send event
        self.sm.initialize()
        self.action_context.clear()  # Clear after initialize
        
        # Send event to trigger transition
        self.sm.send_event(self.event, action_handler=self.handler)
        
        # Check if all actions were executed
        self.assertTrue(self.action_context.get("exit_executed", False))
        self.assertTrue(self.action_context.get("transition_executed", False))
        
        # Check action handler
        self.assertIn("exit_action", self.handler.executed_actions)
        self.assertIn("transition_action", self.handler.executed_actions)


class GuardsTest(unittest.TestCase):
    """Test guard conditions in state machines"""
    
    def setUp(self):
        self.sm = StateMachine("GuardTestMachine")
        
        # Create states
        self.state1 = State("State1")
        self.state2 = State("State2")
        self.state3 = State("State3")
        
        # Add states
        self.sm.add_state(self.state1)
        self.sm.add_state(self.state2)
        self.sm.add_state(self.state3)
        
        # Create events
        self.event = Event("check")
        
        # Guard functions
        def allow_guard(ctx):
            return ctx.get("allowed", False)
            
        def deny_guard(ctx):
            return False
        
        # Create transitions with guards
        self.transition1 = Transition(
            source_state=self.state1,
            target_state=self.state2,
            event=self.event,
            guard=allow_guard
        )
        
        self.transition2 = Transition(
            source_state=self.state1,
            target_state=self.state3,
            event=self.event,
            guard=deny_guard
        )
        
        # Add transitions - order matters for testing
        self.state1.add_transition(self.transition2)  # Denied transition first
        self.state1.add_transition(self.transition1)  # Allowed transition second
        
        # Initialize
        self.sm.initialize()
    
    def test_denied_guard(self):
        # Guard should prevent transition
        result = self.sm.send_event(self.event)
        self.assertFalse(result)
        self.assertEqual(self.sm.current_state, self.state1)
    
    def test_allowed_guard(self):
        # Set context to allow transition
        self.sm.set_context("allowed", True)
        
        # Now transition should succeed
        result = self.sm.send_event(self.event)
        self.assertTrue(result)
        self.assertEqual(self.sm.current_state, self.state2)


if __name__ == "__main__":
    unittest.main()

import unittest
import sys
import os

# Add src directory to Python path
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, src_path)

from wflite.core.statemachine_core import State, Event, Action, Transition, StateMachine


class ParallelStateTest(unittest.TestCase):
    """Test parallel state functionality"""
    
    def setUp(self):
        self.sm = StateMachine("ParallelTestMachine")
        
        # Create states
        self.start = State("Start")
        self.parallel = State("Parallel", is_parallel=True)
        self.branch1 = State("Branch1")
        self.branch2 = State("Branch2")
        self.end = State("End")
        
        # Add states
        self.sm.add_state(self.start)
        self.sm.add_state(self.parallel)
        self.sm.add_state(self.branch1)
        self.sm.add_state(self.branch2)
        self.sm.add_state(self.end)
        
        # Create events
        self.fork_event = Event("fork")
        self.join_event = Event("join")
        
        # Create transitions
        self.fork_transition = Transition(
            source_state=self.start,
            target_state=self.parallel,
            event=self.fork_event
        )
        
        self.parallel_to_branch1 = Transition(
            source_state=self.parallel,
            target_state=self.branch1,
            event=Event("activate_branch1")
        )
        
        self.parallel_to_branch2 = Transition(
            source_state=self.parallel,
            target_state=self.branch2,
            event=Event("activate_branch2")
        )
        
        self.join_transition1 = Transition(
            source_state=self.branch1,
            target_state=self.end,
            event=self.join_event
        )
        
        self.join_transition2 = Transition(
            source_state=self.branch2,
            target_state=self.end,
            event=self.join_event
        )
        
        # Add transitions
        self.start.add_transition(self.fork_transition)
        self.parallel.add_transition(self.parallel_to_branch1)
        self.parallel.add_transition(self.parallel_to_branch2)
        self.branch1.add_transition(self.join_transition1)
        self.branch2.add_transition(self.join_transition2)
        
        # Initialize
        self.sm.initialize()
    
    def test_parallel_states(self):
        # Fork into parallel state
        result = self.sm.send_event(self.fork_event)
        self.assertTrue(result)
        
        # Check that we're in a parallel state
        states = self.sm.get_current_states()
        self.assertEqual(len(states), 1)
        self.assertTrue(states[0].is_parallel)
        self.assertEqual(states[0].name, "Parallel")
        
        # Move to Branch1 from parallel
        result = self.sm.send_event(Event("activate_branch1"))
        self.assertTrue(result)
        self.assertEqual(self.sm.current_state.name, "Branch1")
    
    def test_join_from_parallel(self):
        # Fork into parallel state
        self.sm.send_event(self.fork_event)
        
        # Move to branch1 from parallel
        self.sm.send_event(Event("activate_branch1"))
        self.assertEqual(self.sm.current_state.name, "Branch1")
        
        # Join back to a single state
        result = self.sm.send_event(self.join_event)
        self.assertTrue(result)
        
        # Check that we're in the end state
        self.assertEqual(self.sm.current_state.name, "End")


if __name__ == "__main__":
    unittest.main()

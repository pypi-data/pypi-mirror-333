import uuid
from typing import Dict, List, Optional, Callable, Any, Union
from enum import Enum
from dataclasses import dataclass, field

class ActionHandler():
    def can_handle(self, action_type: str) -> bool:
        return False
    
    async def handle_action(self, action_type: str, context: dict) -> bool:
        """Execute action and return success status"""
        pass

class Event:
    """Represents an event that can trigger state transitions"""
    
    def __init__(self, name: str):
        self.name = name
        
    def __str__(self):
        return f"Event({self.name})"
    
    def __eq__(self, other):
        if not isinstance(other, Event):
            return False
        return self.name == other.name
    
    def __hash__(self):
        return hash(self.name)


class Action:
    """Represents an action that can be executed during transitions"""
    
    def __init__(self, name: str, handler: Callable = None):
        self.name = name
        self.handler = handler or (lambda context: None)
        print(f"Action {name} created")
        
    def execute(self, context: Dict[str, Any]) -> None:
        """Execute the action using the provided context"""
        return self.handler(context)
    
    def __str__(self):
        return f"Action({self.name})"


@dataclass
class Transition:
    """Represents a transition between two states"""
    
    source_state: 'State'
    target_state: 'State'
    event: Event
    actions: List[Action] = field(default_factory=list)
    guard: Optional[Callable[[Dict[str, Any]], bool]] = None
    
    def can_transit(self, context: Dict[str, Any]) -> bool:
        """Check if the transition can be executed based on guard conditions"""
        if self.guard is None:
            return True
        return self.guard(context)
    
    def execute(self, context: Dict[str, Any], action_handler: ActionHandler = None) -> None:
        """Execute all actions associated with this transition"""
        for action in self.actions:
            action.execute(context)
        if action_handler:
            for action in self.actions:
                if action.name:
                    action_handler.handle_action(action.name, context)

class State:
    """Represents a state in the state machine"""
    
    def __init__(self, name: str, entry_actions: List[Action] = None, exit_actions: List[Action] = None, is_parallel: bool = False):
        self.name = name
        self.entry_actions = entry_actions or []
        self.exit_actions = exit_actions or []
        self.transitions: Dict[Event, List[Transition]] = {}
        self.is_parallel = is_parallel
        
    def add_transition(self, transition: Transition) -> None:
        """Add a transition to this state"""
        if transition.event not in self.transitions:
            self.transitions[transition.event] = []
        self.transitions[transition.event].append(transition)
    
    def get_transitions(self, event: Event) -> List[Transition]:
        """Get all transitions for a specific event"""
        return self.transitions.get(event, [])
    
    def enter(self, context: Dict[str, Any], action_handler: ActionHandler = None) -> None:
        """Execute entry actions when entering this state"""
        for action in self.entry_actions:
            action.execute(context)
        if action_handler:
            for action in self.entry_actions:
                action_handler.handle_action(action.name, context)
            
    def exit(self, context: Dict[str, Any], action_handler: ActionHandler = None) -> None:
        """Execute exit actions when leaving this state"""
        for action in self.exit_actions:
            action.execute(context)
        if action_handler:
            for action in self.exit_actions:
                action_handler.handle_action(action.name, context)
    
    def __str__(self):
        return f"State({self.name})"
    
    def __eq__(self, other):
        if not isinstance(other, State):
            return False
        return self.name == other.name
    
    def __hash__(self):
        return hash(self.name)


class StateMachine:
    """The main state machine class that manages states and handles transitions"""
    
    def __init__(self, name: str, initial_state: State = None):
        self.name = name
        self.states: Dict[str, State] = {}
        self.current_state: Union[State, List[State]] = None  # Can be a single state or list of states
        self.initial_state = initial_state
        self.context: Dict[str, Any] = {}
        self.id = str(uuid.uuid4())
    
    def add_state(self, state: State) -> None:
        """Add a state to the state machine"""
        self.states[state.name] = state
        
        # Set as initial state if this is the first state or if it's explicitly set
        if len(self.states) == 1 or state == self.initial_state:
            self.initial_state = state
            
    def get_state(self, name: str) -> Optional[State]:
        """Get a state by name"""
        return self.states.get(name)
    
    def initialize(self) -> None:
        """Initialize the state machine by entering the initial state"""
        if not self.initial_state:
            raise ValueError("No initial state defined")
        
        self.current_state = self.initial_state
        
        # Handle the case where the initial state is a parallel state
        if isinstance(self.current_state, State) and self.current_state.is_parallel:
            self.current_state = [self.current_state]
        
        # Execute entry actions for the initial state
        if isinstance(self.current_state, list):
            for state in self.current_state:
                state.enter(self.context)
        else:
            self.current_state.enter(self.context)
    
    def send_event(self, event: Event, action_handler: ActionHandler = None) -> bool:
        """
        Process an event
        
        Returns:
            bool: True if a transition occurred, False otherwise
        """
        if not self.current_state:
            raise ValueError("State machine not initialized")
        
        # Handle parallel states
        if isinstance(self.current_state, list):
            # For parallel states, we need to find transitions from any active state
            any_transition = False
            new_states = []
            
            for state in self.current_state:
                transitions = state.get_transitions(event)
                
                # Find the first valid transition for this state
                for transition in transitions:
                    if transition.can_transit(self.context):
                        # Execute state exit actions
                        state.exit(self.context)
                        
                        # Execute transition actions
                        transition.execute(self.context, action_handler=action_handler)
                        
                        # Add target state to new states
                        target = transition.target_state
                        if target.is_parallel:
                            new_states.append(target)
                        else:
                            new_states = [target]  # Reset to single target if not parallel
                        
                        # Execute state entry actions
                        target.enter(self.context, action_handler=action_handler)
                        
                        any_transition = True
                        break
                        
                if not any_transition:
                    # No transition occurred for this state, keep it
                    new_states.append(state)
            
            self.current_state = new_states if len(new_states) > 1 else new_states[0]
            return any_transition
        else:
            # Regular single state handling
            transitions = self.current_state.get_transitions(event)
            
            # Find the first valid transition
            for transition in transitions:
                if transition.can_transit(self.context):
                    # Execute state exit actions
                    self.current_state.exit(self.context, action_handler=action_handler)
                    
                    # Execute transition actions
                    transition.execute(self.context, action_handler=action_handler)
                    
                    # Update current state
                    target = transition.target_state
                    
                    # Handle target state
                    if isinstance(target, list):
                        self.current_state = target  # Already a list of states
                    elif target.is_parallel:
                        self.current_state = [target]  # Wrap in list for parallel state
                    else:
                        self.current_state = target  # Regular single state
                    
                    # Execute state entry actions
                    if isinstance(self.current_state, list):
                        for state in self.current_state:
                            state.enter(self.context, action_handler=action_handler)
                    else:
                        self.current_state.enter(self.context, action_handler=action_handler)
                    
                    return True
            
            # No valid transition found
            return False
    
    def get_current_state(self) -> Optional[State]:
        """Get the current state (returns first state if parallel)"""
        if isinstance(self.current_state, list):
            return self.current_state[0] if self.current_state else None
        return self.current_state
    
    def get_current_states(self) -> List[State]:
        """Get all current states (for parallel states)"""
        if isinstance(self.current_state, list):
            return self.current_state
        return [self.current_state] if self.current_state else []
    
    def set_context(self, key: str, value: Any) -> None:
        """Set a value in the state machine context"""
        # Ensure context is initialized
        if not hasattr(self, 'context') or self.context is None:
            self.context = {}
            
        # Handle direct key-value assignment
        if isinstance(key, str):
            self.context[key] = value
        else:
            print(f"Warning: Invalid context key type: {type(key)}")
    
    def update_context(self, new_context: Dict[str, Any]) -> None:
        """Update multiple context values at once"""
        print(f"DEBUG: Current context before update: {self.context}")
        print(f"DEBUG: Updating with: {new_context}")
        
        # Initialize context if needed
        if not hasattr(self, 'context'):
            self.context = {}
        if self.context is None:
            self.context = {}
        
        # Safely handle the update
        try:
            if isinstance(new_context, dict):
                # Create a new dictionary for updates
                updates = {}
                
                # Handle the data field if present
                if 'data' in new_context:
                    data = new_context['data']
                    if isinstance(data, dict):
                        updates.update(data)
                        print(f"DEBUG: Added data fields: {data}")
                
                # Add all non-data fields
                for key, value in new_context.items():
                    if key != 'data':
                        updates[key] = value
                        print(f"DEBUG: Added field: {key}={value}")
                
                # Update the context
                print(f"DEBUG: Applying updates: {updates}")
                self.context.update(updates)
                print(f"DEBUG: Final context: {self.context}")
        except Exception as e:
            print(f"ERROR in update_context: {str(e)}")
            print(f"ERROR type: {type(e)}")
            print(f"ERROR args: {e.args}")
            raise
    
    def get_context(self) -> Dict[str, Any]:
        """Get the current context"""
        if not hasattr(self, 'context') or self.context is None:
            self.context = {}
        return self.context


class StateMachineModel:
    """Data model for serializing/deserializing a state machine"""
    
    def __init__(self, 
                 id: str,
                 name: str, 
                 current_state: str, 
                 customer_id: str = None,
                 context: Dict[str, Any] = None):
        self.id = id
        self.name = name
        self.current_state = current_state
        self.customer_id = customer_id
        self.context = context or {}
    
    @staticmethod
    def from_state_machine(state_machine: StateMachine, customer_id: str = None) -> 'StateMachineModel':
        """Create a model from a state machine instance"""
        if not state_machine.current_state:
            raise ValueError("State machine not initialized")
        
        # Get current state name, handling both single state and list of states
        if isinstance(state_machine.current_state, list):
            current_state = state_machine.current_state[0].name if state_machine.current_state else "start"
        else:
            current_state = state_machine.current_state.name
            
        return StateMachineModel(
            id=state_machine.id,
            name=state_machine.name,
            current_state=current_state,
            customer_id=customer_id,
            context=state_machine.context
        )
from typing import Dict, List, Optional, Callable, Any, Set
from .statemachine_core import State, Event, Action, Transition, StateMachine


class StateBuilder:
    """Builder for State objects with a fluent API"""
    
    def __init__(self, name: str, machine_builder: 'StateMachineBuilder'):
        self.name = name
        self.machine_builder = machine_builder
        self.entry_actions: List[Action] = []
        self.exit_actions: List[Action] = []
        
    def on_entry(self, action: Action) -> 'StateBuilder':
        """Add an entry action to the state"""
        self.entry_actions.append(action)
        return self
        
    def on_exit(self, action: Action) -> 'StateBuilder':
        """Add an exit action to the state"""
        self.exit_actions.append(action)
        return self
        
    def transition_to(self, target_state_name: str, event_name: str) -> 'TransitionBuilder':
        """Start building a transition to another state"""
        return TransitionBuilder(self.name, target_state_name, event_name, self.machine_builder)
        
    def build(self) -> State:
        """Build and return the State object"""
        return State(self.name, self.entry_actions, self.exit_actions)


class TransitionBuilder:
    """Builder for Transition objects with a fluent API"""
    
    def __init__(self, source_state_name: str, target_state_name: str, 
                 event_name: str, machine_builder: 'StateMachineBuilder'):
        self.source_state_name = source_state_name
        self.target_state_name = target_state_name
        self.event_name = event_name
        self.machine_builder = machine_builder
        self.actions: List[Action] = []
        self.guard_function: Optional[Callable[[Dict[str, Any]], bool]] = None
        
    def with_action(self, action: Action) -> 'TransitionBuilder':
        """Add an action to the transition"""
        self.actions.append(action)
        return self
        
    def with_guard(self, guard: Callable[[Dict[str, Any]], bool]) -> 'TransitionBuilder':
        """Add a guard condition to the transition"""
        self.guard_function = guard
        return self
        
    def and_from(self, state_name: str) -> StateBuilder:
        """Return to building the source state"""
        # Register this transition first
        self.machine_builder.add_transition(
            self.source_state_name,
            self.target_state_name,
            self.event_name,
            self.actions,
            self.guard_function
        )
        return StateBuilder(state_name, self.machine_builder)
        
    def and_state(self, state_name: str) -> StateBuilder:
        """Continue building another state"""
        # Register this transition first
        self.machine_builder.add_transition(
            self.source_state_name,
            self.target_state_name,
            self.event_name,
            self.actions,
            self.guard_function
        )
        return self.machine_builder.state(state_name)
        
    def build_state_machine(self) -> StateMachine:
        """Finalize and build the state machine"""
        # Register this transition first
        self.machine_builder.add_transition(
            self.source_state_name,
            self.target_state_name,
            self.event_name,
            self.actions,
            self.guard_function
        )
        return self.machine_builder.build()


class StateMachineBuilder:
    """Builder for StateMachine objects with a fluent API"""
    
    def __init__(self, name: str):
        self.name = name
        self.states: Dict[str, State] = {}
        self.events: Dict[str, Event] = {}
        self.initial_state_name: Optional[str] = None
        self.pending_transitions: List[Dict[str, Any]] = []
        
    def state(self, name: str) -> StateBuilder:
        """Start building a state"""
        return StateBuilder(name, self)
        
    def initial_state(self, name: str) -> StateBuilder:
        """Define the initial state"""
        self.initial_state_name = name
        return StateBuilder(name, self)
        
    def add_transition(self, source_state_name: str, target_state_name: str, 
                      event_name: str, actions: List[Action], guard: Optional[Callable]):
        """Register a transition to be built later"""
        self.pending_transitions.append({
            'source': source_state_name,
            'target': target_state_name,
            'event': event_name,
            'actions': actions,
            'guard': guard
        })
        
    def _get_or_create_state(self, name: str) -> State:
        """Get a state by name or create it if it doesn't exist"""
        if name not in self.states:
            self.states[name] = State(name)
        return self.states[name]
    
    def _get_or_create_event(self, name: str) -> Event:
        """Get an event by name or create it if it doesn't exist"""
        if name not in self.events:
            self.events[name] = Event(name)
        return self.events[name]
    
    def build(self) -> StateMachine:
        """Build and return the StateMachine object"""
        sm = StateMachine(self.name)
        
        # Create all states first
        states = {}
        for transition in self.pending_transitions:
            source_name = transition['source']
            target_name = transition['target']
            
            if source_name not in states:
                states[source_name] = State(source_name)
            if target_name not in states:
                states[target_name] = State(target_name)
        
        # Add all states to the state machine
        for state in states.values():
            sm.add_state(state)
        
        # Set initial state if specified
        if self.initial_state_name:
            sm.initial_state = states[self.initial_state_name]
        
        # Build all transitions
        for t in self.pending_transitions:
            source_state = states[t['source']]
            target_state = states[t['target']]
            event = Event(t['event'])
            
            transition = Transition(
                source_state=source_state,
                target_state=target_state,
                event=event,
                actions=t['actions'],
                guard=t['guard']
            )
            
            source_state.add_transition(transition)
            
        return sm

    @staticmethod
    def build_from_template(template_data: dict) -> StateMachine:
        if 'name' in template_data:
            machine = StateMachine(template_data['name'])
        else:
            machine = StateMachine('Unnamed')
        
        # Create states
        states = {}
        for state_data in template_data['states']:
            entry_actions = [Action(action) for action in state_data.get('entryActions', [])]
            exit_actions = [Action(action) for action in state_data.get('exitActions', [])]
            state = State(state_data['id'], entry_actions, exit_actions)
            states[state_data['id']] = state
            machine.add_state(state)
            
            if state_data.get('type') == 'start':
                machine.initial_state = state
        
        # Create transitions
        for trans_data in template_data['transitions']:
            source = states[trans_data['source']]
            target = states[trans_data['target']]
            event = Event(trans_data['event']) if 'event' in trans_data else None
            
            actions = []
            if 'action' in trans_data:
                actions.append(Action(trans_data['action']))
            
            transition = Transition(source, target, event, actions)
            source.add_transition(transition)
        
        return machine
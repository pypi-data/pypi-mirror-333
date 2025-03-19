from typing import Optional
import graphviz
from .statemachine_core import StateMachine, State, Transition

class StateMachineVisualizer:
    """Visualizes state machines using Graphviz"""
    
    @staticmethod
    def to_dot(state_machine: StateMachine, title: Optional[str] = None) -> graphviz.Digraph:
        """Convert a state machine to a Graphviz dot graph"""
        dot = graphviz.Digraph(comment=title or state_machine.name)
        dot.attr(rankdir='LR')  # Left to right layout
        
        # Add states
        for state in state_machine.states.values():
            # Mark initial state with different style
            if state == state_machine.initial_state:
                dot.node(state.name, state.name, shape='doubleoctagon')
            else:
                dot.node(state.name, state.name, shape='rectangle')
            
            # Add transitions
            for event, transitions in state.transitions.items():
                for transition in transitions:
                    # Create label with event name and guard if present
                    label = event.name
                    if transition.guard:
                        label += f"\n[{transition.guard.__name__}]"
                    if transition.actions:
                        label += f"\n{{{', '.join(a.name for a in transition.actions)}}}"
                    
                    dot.edge(
                        transition.source_state.name,
                        transition.target_state.name,
                        label
                    )
        
        return dot
    
    @staticmethod
    def save_diagram(state_machine: StateMachine, 
                    filename: str,
                    format: str = 'png',
                    title: Optional[str] = None) -> None:
        """
        Save state machine diagram to a file
        
        Args:
            state_machine: The state machine to visualize
            filename: Output filename (without extension)
            format: Output format ('png', 'svg', 'pdf', etc.)
            title: Optional title for the diagram
        """
        dot = StateMachineVisualizer.to_dot(state_machine, title)
        dot.render(filename, format=format, cleanup=True)
    
    @staticmethod
    def visualize_runtime(runtime, customer_id: str,
                         filename: str,
                         format: str = 'png') -> None:
        """
        Visualize a customer's current state machine instance
        
        Args:
            runtime: StateMachineRuntime instance
            customer_id: Customer ID to visualize
            filename: Output filename (without extension)
            format: Output format ('png', 'svg', 'pdf', etc.)
        """
        sm = runtime.get_state_machine(customer_id)
        if not sm:
            raise ValueError(f"No state machine found for customer {customer_id}")
        
        dot = StateMachineVisualizer.to_dot(sm)
        
        # Highlight current state
        if sm.current_state:
            dot.node(
                sm.current_state.name,
                sm.current_state.name,
                style='filled',
                fillcolor='lightblue'
            )
        
        dot.render(filename, format=format, cleanup=True)

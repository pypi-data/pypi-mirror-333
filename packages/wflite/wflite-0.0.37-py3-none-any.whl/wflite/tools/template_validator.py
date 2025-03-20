import json
from typing import Dict, Any, List, Optional

class TemplateValidator:
    """
    Utility class to validate and fix state machine templates.
    """
    
    @staticmethod
    def validate_and_repair(template_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate template structure and repair common issues.
        Returns the fixed template.
        """
        if not template_data:
            print("Error: Template data is empty")
            return template_data
            
        # Make a copy to avoid modifying the original
        fixed_template = template_data.copy()
        
        # Check and fix transitions
        fixed_template = TemplateValidator._fix_transitions(fixed_template)
        
        # Log the changes
        print(f"Debug - Template validated and repaired")
        return fixed_template
    
    @staticmethod
    def _fix_transitions(template_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fix missing or incorrect transitions in template"""
        states = template_data.get('states', [])
        if not states:
            return template_data
            
        # Check if any transitions exist at all
        has_transitions = any(state.get('transitions') for state in states)
        
        # Look for transitions section in the template
        template_transitions = template_data.get('transitions', [])
        
        # If no transitions defined in states but there's a transitions section
        if not has_transitions and template_transitions:
            print("Debug - Template has a separate transitions section, moving transitions to states")
            # Create a mapping of state IDs to states for easier lookup
            state_map = {state.get('id'): state for state in states}
            
            # Process each transition and add it to the appropriate state
            for transition in template_transitions:
                source_id = transition.get('source')
                if source_id in state_map:
                    source_state = state_map[source_id]
                    if 'transitions' not in source_state:
                        source_state['transitions'] = []
                    source_state['transitions'].append({
                        'target': transition.get('target'),
                        'event': transition.get('event'),
                        'condition': transition.get('condition', None)
                    })
                    print(f"Debug - Added transition from '{source_state.get('name')}' to '{transition.get('target')}' on event '{transition.get('event')}'")
        
        # Check for start states with no transitions
        start_states = [s for s in states if s.get('type') == 'start']
        for start_state in start_states:
            # If start state has no transitions, try to find a logical next state
            if not start_state.get('transitions'):
                print(f"Debug - Start state '{start_state.get('name')}' has no transitions")
                
                # Find potential next states (non-start, non-end)
                next_states = [s for s in states 
                              if s.get('type') not in ['start', 'end'] 
                              and s.get('id') != start_state.get('id')]
                              
                if next_states:
                    # Choose the first non-start, non-end state as target
                    target_state = next_states[0]
                    
                    # Create a transition from start to this state
                    if 'transitions' not in start_state:
                        start_state['transitions'] = []
                        
                    start_state['transitions'].append({
                        'target': target_state.get('id'),
                        'event': 'case_created'  # Default event for starting the workflow
                    })
                    
                    print(f"Debug - Added missing transition from start state '{start_state.get('name')}' to '{target_state.get('name')}' on event 'case_created'")
        
        # Check transitions between states to ensure a valid path to end state
        TemplateValidator._ensure_path_to_end(states)
        
        return template_data
    
    @staticmethod
    def _ensure_path_to_end(states: List[Dict[str, Any]]) -> None:
        """Ensure there's a path from every state to an end state"""
        # Find end states
        end_states = [s for s in states if s.get('type') == 'end']
        if not end_states:
            print("Warning: No end states defined in template")
            return
            
        # Check each non-end state
        for state in states:
            if state.get('type') == 'end':
                continue
                
            # If state has no transitions, add a transition to the first end state
            if not state.get('transitions'):
                if 'transitions' not in state:
                    state['transitions'] = []
                    
                state['transitions'].append({
                    'target': end_states[0].get('id'),
                    'event': 'complete'
                })
                
                print(f"Debug - Added missing transition from '{state.get('name')}' to end state on event 'complete'")
    
    @staticmethod
    def print_template_structure(template_data: Dict[str, Any]) -> None:
        """Print the structure of a template for debugging"""
        print("\nTemplate Structure:")
        print(f"States: {len(template_data.get('states', []))}")
        
        for state in template_data.get('states', []):
            state_id = state.get('id', 'unknown')
            state_name = state.get('name', 'unknown')
            state_type = state.get('type', 'unknown')
            transitions = state.get('transitions', [])
            
            print(f"  State: {state_name} (ID: {state_id}, Type: {state_type})")
            print(f"    Transitions: {len(transitions)}")
            
            for trans in transitions:
                target = trans.get('target', 'unknown')
                event = trans.get('event', 'unknown')
                condition = trans.get('condition', 'None')
                
                # Find target state name for better readability
                target_name = "unknown"
                for s in template_data.get('states', []):
                    if s.get('id') == target:
                        target_name = s.get('name', 'unknown')
                        break
                        
                print(f"      On '{event}' → '{target_name}' (ID: {target}) [condition: {condition}]")
```

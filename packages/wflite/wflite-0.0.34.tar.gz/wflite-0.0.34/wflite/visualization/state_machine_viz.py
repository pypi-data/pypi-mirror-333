import os
import sys
import graphviz
import logging
from typing import Dict, Any, List, Optional

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from wflite.config.config_loader import ConfigLoader

logger = logging.getLogger(__name__)

class StateMachineVisualizer:
    """Visualizes state machine templates as GraphViz diagrams"""
    
    def __init__(self):
        """Initialize the visualizer with configuration"""
        config_loader = ConfigLoader()
        visualization_config = config_loader._config.get('visualization', {})
        
        # Set defaults if not in config
        self.config = {
            'rankdir': visualization_config.get('rankdir', 'LR'),
            'colors': {
                'state_fill': visualization_config.get('colors', {}).get('state_fill', '#FFFACD'),  # Light yellow
                'current_state_fill': visualization_config.get('colors', {}).get('current_state_fill', '#FFA500'),  # Orange
                'state_border': visualization_config.get('colors', {}).get('state_border', 'black'),
            },
            'sizes': {
                'start_end_node': visualization_config.get('sizes', {}).get('start_end_node', '0.3'),
                'border_width': visualization_config.get('sizes', {}).get('border_width', '1.0'),
                'current_border_width': visualization_config.get('sizes', {}).get('current_border_width', '3.0'),
            }
        }
        
        logger.info(f"Visualizer initialized with rankdir={self.config['rankdir']}")
        
    def generate_graph(self, template_data: Dict, current_state: str = None) -> graphviz.Digraph:
        """
        Generate a GraphViz diagram from a state machine template.
        
        Args:
            template_data: The template data containing states and transitions
            current_state: The current state ID to highlight (optional)
            
        Returns:
            A GraphViz diagram object
        """
        # Create a new directed graph
        graph = graphviz.Digraph(format='svg')
        
        # Set graph attributes
        graph.attr(rankdir=self.config['rankdir'])
        graph.attr(splines='ortho')  # Orthogonal lines
        
        # Process states
        states = template_data.get('states', [])
        transitions = template_data.get('transitions', [])
        
        # Map for quick access to state details
        state_map = {state['id']: state for state in states}
        
        # Add states to graph
        for state in states:
            state_id = state['id']
            state_name = state.get('name', state_id)
            state_type = state.get('type', 'normal')
            
            # Determine if this is the current state
            is_current = current_state and state_id == current_state
            
            # Set node attributes based on state type and whether it's the current state
            attrs = {}
            
            if state_type == 'start':
                attrs['shape'] = 'circle'
                attrs['width'] = self.config['sizes']['start_end_node']
                attrs['height'] = self.config['sizes']['start_end_node']
                attrs['label'] = ''
                attrs['style'] = 'filled'
                attrs['fillcolor'] = 'black'
            elif state_type == 'end':
                attrs['shape'] = 'doublecircle'
                attrs['width'] = self.config['sizes']['start_end_node']
                attrs['height'] = self.config['sizes']['start_end_node']
                attrs['label'] = ''
                attrs['style'] = 'filled'
                attrs['fillcolor'] = 'black'
            else:
                attrs['shape'] = 'box'
                attrs['style'] = 'filled,rounded'
                attrs['label'] = state_name
                
                if is_current:
                    attrs['fillcolor'] = self.config['colors']['current_state_fill']
                    attrs['penwidth'] = self.config['sizes']['current_border_width']
                else:
                    attrs['fillcolor'] = self.config['colors']['state_fill']
                    attrs['penwidth'] = self.config['sizes']['border_width']
            
            # Add the state node to the graph
            graph.node(state_id, **attrs)
        
        # Add transitions to graph
        for transition in transitions:
            source = transition['source']
            target = transition['target']
            event = transition.get('event', '')
            actions = transition.get('actions', [])
            
            # Build label for the transition
            label = f"{event}"
            if actions:
                action_text = ', '.join(actions)
                label = f"{label}\n[{action_text}]"
            
            # Add the transition edge to the graph
            graph.edge(source, target, label=label)
        
        return graph
    
    def save_graph(self, template_data: Dict, output_path: str, current_state: str = None) -> str:
        """
        Generate and save a GraphViz diagram to a file.
        
        Args:
            template_data: The template data containing states and transitions
            output_path: The file path to save the diagram to (without extension)
            current_state: The current state ID to highlight (optional)
            
        Returns:
            The path to the generated file
        """
        graph = self.generate_graph(template_data, current_state)
        return graph.render(output_path, cleanup=True)

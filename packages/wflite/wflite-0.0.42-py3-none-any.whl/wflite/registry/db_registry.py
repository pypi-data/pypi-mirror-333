import os
import sys
import json
import logging
from typing import Dict, Any, List, Optional

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from wflite.config.config_loader import ConfigLoader
from wflite.persistence.provider_factory import PersistenceProviderFactory
from wflite.core.statemachine_core import StateMachine

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class StateMachineRegistry:
    """Registry for state machine templates using the configured persistence provider"""
    
    def __init__(self):
        # Load configuration
        self.config = ConfigLoader()
        self.config_dict = getattr(self.config, '_config', {})
        
        # Create persistence provider
        self.persistence = PersistenceProviderFactory.create_provider(self.config_dict)
        provider_type = self.config_dict.get('persistence', {}).get('provider', 'sqlite')
        logger.info(f"Registry using persistence provider: {provider_type}")
    
    def save(self, name: str, template_data: Dict[str, Any], description: str = None) -> bool:
        """Save a template using the persistence provider"""
        try:
            return self.persistence.save_template(name, template_data, description)
        except Exception as e:
            logger.error(f"Error saving template '{name}': {e}")
            return False
    
    def load(self, name: str) -> Optional[Dict[str, Any]]:
        """Load a template using the persistence provider"""
        try:
            return self.persistence.load_template(name)
        except Exception as e:
            logger.error(f"Error loading template '{name}': {e}")
            return None
    
    def delete(self, name: str) -> bool:
        """Delete a template using the persistence provider"""
        try:
            return self.persistence.delete_template(name)
        except Exception as e:
            logger.error(f"Error deleting template '{name}': {e}")
            return False
    
    def list(self) -> List[str]:
        """List all template names using the persistence provider"""
        try:
            return self.persistence.list_templates()
        except Exception as e:
            logger.error(f"Error listing templates: {e}")
            return []
            
    def register(self, state_machine: StateMachine, description: str = None) -> bool:
        """
        Register a state machine template by converting it to a dictionary representation
        and saving it with the state machine's name
        """
        try:
            # Convert state machine to template format
            template_data = {
                "name": state_machine.name,
                "states": [],
                "transitions": []
            }
            
            # Add states
            for state_name, state in state_machine.states.items():
                state_data = {
                    "id": state.name,
                    "name": state.name,
                    "type": "end" if not state.transitions else "normal",
                    "is_parallel": state.is_parallel
                }
                # Mark the initial state as "start"
                if state == state_machine.initial_state:
                    state_data["type"] = "start"
                    
                template_data["states"].append(state_data)
            
            # Add transitions
            for state_name, state in state_machine.states.items():
                for event, transitions in state.transitions.items():
                    for transition in transitions:
                        transition_data = {
                            "source": transition.source_state.name,
                            "target": transition.target_state.name,
                            "event": transition.event.name,
                            "actions": [action.name for action in transition.actions]
                        }
                        template_data["transitions"].append(transition_data)
            
            # Save the template
            return self.save(state_machine.name, template_data, description)
            
        except Exception as e:
            logger.error(f"Error registering state machine: {e}")
            return False

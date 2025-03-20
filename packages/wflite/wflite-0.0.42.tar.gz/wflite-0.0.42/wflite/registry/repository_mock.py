from typing import Dict, Any, Optional

class StateMachineRepository:
    """A mock repository class for testing"""
    
    def __init__(self):
        self.templates = {}
        self._setup_defaults()
        
    def _setup_defaults(self):
        """Set up some default templates for testing"""
        default_template = {
            "states": [
                {"id": "New", "name": "New", "type": "start"},
                {"id": "Processing", "name": "Processing", "type": "normal"},
                {"id": "Complete", "name": "Complete", "type": "end"}
            ],
            "transitions": [
                {"source": "New", "target": "Processing", "event": "process"},
                {"source": "Processing", "target": "Complete", "event": "complete"}
            ]
        }
        self.templates["Default"] = default_template
    
    def get(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a template by name"""
        return self.templates.get(name)
    
    def register_template(self, name: str, template: Dict[str, Any]) -> bool:
        """Register a new template"""
        self.templates[name] = template
        return True
    
    def get_all_templates(self) -> Dict[str, Dict[str, Any]]:
        """Get all templates"""
        return self.templates

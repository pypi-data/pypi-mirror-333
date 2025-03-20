import os
import sys
import sqlite3
import logging
from typing import Dict, Tuple, List, Optional

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from wflite.config.config_loader import ConfigLoader

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class CustomerManager:
    """Manages customer's workflow assignments"""
    
    def __init__(self, persistence_provider=None):
        """
        Initialize the customer manager.
        
        Args:
            persistence_provider: Provider for persisting customer assignments
        """
        # Store persistence provider
        self.persistence = persistence_provider
        
        # If no persistence provider given, create a default SQLite one
        if self.persistence is None:
            from wflite.persistence.sqlite_provider import SQLitePersistenceProvider
            self.persistence = SQLitePersistenceProvider()
    
    def assign_workflow(self, customer_id: str, template_name: str, instance_id: str) -> bool:
        """Assign a workflow template instance to a customer"""
        return self.persistence.assign_customer_workflow(customer_id, template_name, instance_id)
    
    def get_customer_workflow(self, customer_id: str) -> Tuple[Optional[str], Optional[str]]:
        """Get the current workflow assignment for a customer"""
        return self.persistence.get_customer_workflow(customer_id)

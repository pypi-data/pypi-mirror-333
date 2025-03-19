import sqlite3
import json
from typing import Optional, List, Dict, Any
from .statemachine_core import StateMachine, State, StateMachineModel

class StateMachineRepository:
    """Repository for storing and retrieving state machines from SQLite"""
    
    def __init__(self, db_path: str = "statemachine.db"):
        self.db_path = db_path
        self._initialize_db()
    
    def _initialize_db(self) -> None:
        """Initialize the database and create tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create table for state machines
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS state_machines (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            current_state TEXT NOT NULL,
            customer_id TEXT,
            context TEXT NOT NULL
        )
        ''')
        
        # Create index for customer_id for efficient lookups
        cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_state_machines_customer_id 
        ON state_machines(customer_id)
        ''')
        
        conn.commit()
        conn.close()
    
    def save(self, model: StateMachineModel) -> None:
        """Save a state machine model to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Serialize context as JSON
        context_json = json.dumps(model.context)
        
        cursor.execute('''
        INSERT OR REPLACE INTO state_machines 
        (id, name, current_state, customer_id, context)
        VALUES (?, ?, ?, ?, ?)
        ''', (model.id, model.name, model.current_state, 
              model.customer_id, context_json))
        
        conn.commit()
        conn.close()
    
    def find_by_id(self, id: str) -> Optional[StateMachineModel]:
        """Find a state machine by its ID"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT id, name, current_state, customer_id, context
        FROM state_machines
        WHERE id = ?
        ''', (id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return StateMachineModel(
                id=row['id'],
                name=row['name'],
                current_state=row['current_state'],
                customer_id=row['customer_id'],
                context=json.loads(row['context'])
            )
        
        return None
    
    def find_by_customer_id(self, customer_id: str) -> List[StateMachineModel]:
        """Find all state machines for a specific customer ID"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT id, name, current_state, customer_id, context
        FROM state_machines
        WHERE customer_id = ?
        ''', (customer_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            StateMachineModel(
                id=row['id'],
                name=row['name'],
                current_state=row['current_state'],
                customer_id=row['customer_id'],
                context=json.loads(row['context'])
            )
            for row in rows
        ]
    
    def delete(self, id: str) -> bool:
        """Delete a state machine by its ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM state_machines WHERE id = ?', (id,))
        deleted = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        
        return deleted


class StateMachineHydrator:
    """Helper class to hydrate a StateMachine instance from a StateMachineModel"""
    
    def __init__(self, state_machine_templates: Dict[str, StateMachine]):
        """
        Initialize with templates of state machines
        
        Args:
            state_machine_templates: Dictionary mapping state machine names to template instances
        """
        self.templates = state_machine_templates
    
    def hydrate(self, model: StateMachineModel) -> Optional[StateMachine]:
        """
        Hydrate a state machine from a model
        
        Args:
            model: The state machine model to hydrate from
            
        Returns:
            StateMachine: The hydrated state machine or None if template not found
        """
        if model.name not in self.templates:
            return None
        
        # Clone the template
        template = self.templates[model.name]
        state_machine = StateMachine(template.name)
        
        # Copy states and transitions from template
        for name, state in template.states.items():
            state_machine.add_state(state)
        
        # Set the ID from the model
        state_machine.id = model.id
        
        # Set the current state
        current_state = state_machine.get_state(model.current_state)
        if not current_state:
            raise ValueError(f"State '{model.current_state}' not found in state machine template")
        
        state_machine.current_state = current_state
        
        # Set the context
        state_machine.context = model.context
        
        return state_machine
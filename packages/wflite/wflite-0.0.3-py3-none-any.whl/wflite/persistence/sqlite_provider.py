import os
import sqlite3
import json
import time
from typing import Dict, Any, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class SQLitePersistenceProvider:
    """SQLite implementation of persistence for state machines"""
    
    def __init__(self, db_path="workflows.db",
                 templates_table='workflow_templates',
                 instances_table='workflow_instances',
                 customers_table='workflow_assignments'):
        """
        Initialize the SQLite persistence provider.
        
        Args:
            db_path: Path to SQLite database file
            templates_table: Name of templates table
            instances_table: Name of instances table
            customers_table: Name of customers table
        """
        self.db_path = db_path
        self.templates_table = templates_table
        self.instances_table = instances_table
        self.customers_table = customers_table
        
        # Create directory if it doesn't exist
        db_dir = os.path.dirname(os.path.abspath(db_path))
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
            
        # Initialize database tables
        self._initialize_db()
    
    def _initialize_db(self):
        """Initialize the database with required tables."""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create templates table if it doesn't exist
            cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {self.templates_table} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                data TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')
            
            # Create instances table if it doesn't exist
            cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {self.instances_table} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                instance_id TEXT UNIQUE NOT NULL,
                template_name TEXT NOT NULL,
                current_state TEXT NOT NULL,
                context TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')
            
            # Create customer workflows table if it doesn't exist
            cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {self.customers_table} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id TEXT UNIQUE NOT NULL,
                template_name TEXT NOT NULL,
                instance_id TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')
            
            conn.commit()
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            if conn:
                conn.rollback()
        finally:
            if conn:
                conn.close()
    
    # Template Methods
    
    def save_template(self, name: str, template_data: Dict[str, Any], description: str = None) -> bool:
        """Save a template to the database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Convert data to JSON string
            data_json = json.dumps(template_data)
            
            # Insert or replace template
            cursor.execute(
                f"INSERT OR REPLACE INTO {self.templates_table} (name, description, data) VALUES (?, ?, ?)",
                (name, description or "", data_json)
            )
            
            conn.commit()
            conn.close()
            logger.info(f"Saved template '{name}' successfully")
            return True
        except Exception as e:
            logger.error(f"Error saving template '{name}': {e}")
            return False
    
    def load_template(self, name: str) -> Optional[Dict[str, Any]]:
        """Load a template from the database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(f"SELECT data FROM {self.templates_table} WHERE name = ?", (name,))
            result = cursor.fetchone()
            
            conn.close()
            
            if result:
                return json.loads(result[0])
            return None
        except Exception as e:
            logger.error(f"Error loading template '{name}': {e}")
            return None
    
    def delete_template(self, name: str) -> bool:
        """Delete a template from the database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(f"DELETE FROM {self.templates_table} WHERE name = ?", (name,))
            
            conn.commit()
            conn.close()
            logger.info(f"Deleted template '{name}' successfully")
            return True
        except Exception as e:
            logger.error(f"Error deleting template '{name}': {e}")
            return False
    
    def list_templates(self) -> List[str]:
        """List all template names"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(f"SELECT name FROM {self.templates_table}")
            results = cursor.fetchall()
            
            conn.close()
            
            return [row[0] for row in results]
        except Exception as e:
            logger.error(f"Error listing templates: {e}")
            return []
    
    # Instance Methods
    
    def create_instance(self, instance_id: str, template_name: str, current_state: str, context: Dict[str, Any] = None) -> bool:
        """Create a new state machine instance"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if instance already exists
            cursor.execute(f"SELECT instance_id FROM {self.instances_table} WHERE instance_id = ?", (instance_id,))
            existing = cursor.fetchone()
            
            if existing:
                # Delete existing instance
                cursor.execute(f"DELETE FROM {self.instances_table} WHERE instance_id = ?", (instance_id,))
            
            # Insert new instance
            cursor.execute(
                f"INSERT INTO {self.instances_table} (instance_id, template_name, current_state, context) VALUES (?, ?, ?, ?)",
                (
                    instance_id, 
                    template_name, 
                    current_state, 
                    json.dumps(context or {})
                )
            )
            
            conn.commit()
            conn.close()
            logger.info(f"Created instance '{instance_id}' successfully")
            return True
        except Exception as e:
            logger.error(f"Error creating instance '{instance_id}': {e}")
            return False
    
    def update_instance(self, instance_id: str, current_state: str, context: Dict[str, Any]) -> bool:
        """Update an existing state machine instance"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                f"UPDATE {self.instances_table} SET current_state = ?, context = ?, updated_at = CURRENT_TIMESTAMP WHERE instance_id = ?",
                (current_state, json.dumps(context), instance_id)
            )
            
            conn.commit()
            conn.close()
            logger.info(f"Updated instance '{instance_id}' successfully")
            return True
        except Exception as e:
            logger.error(f"Error updating instance '{instance_id}': {e}")
            return False
    
    def get_instance(self, instance_id: str) -> Optional[Dict[str, Any]]:
        """Get a state machine instance"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                f"SELECT template_name, current_state, context FROM {self.instances_table} WHERE instance_id = ?",
                (instance_id,)
            )
            result = cursor.fetchone()
            
            conn.close()
            
            if result:
                context = json.loads(result[2]) if result[2] else {}
                return {
                    'instance_id': instance_id,
                    'template_name': result[0],
                    'current_state': result[1],
                    'context': context
                }
            return None
        except Exception as e:
            logger.error(f"Error getting instance '{instance_id}': {e}")
            return None
    
    def delete_instance(self, instance_id: str) -> bool:
        """Delete a state machine instance"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(f"DELETE FROM {self.instances_table} WHERE instance_id = ?", (instance_id,))
            
            conn.commit()
            conn.close()
            logger.info(f"Deleted instance '{instance_id}' successfully")
            return True
        except Exception as e:
            logger.error(f"Error deleting instance '{instance_id}': {e}")
            return False
    
    # Customer Methods
    
    def assign_customer_workflow(self, customer_id: str, template_name: str, instance_id: str) -> bool:
        """Assign a workflow template instance to a customer"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if customer already has a workflow assigned
            cursor.execute(
                f"SELECT template_name, instance_id FROM {self.customers_table} WHERE customer_id = ?", 
                (customer_id,)
            )
            existing = cursor.fetchone()
            
            if existing:
                # Update existing assignment
                cursor.execute(
                    f"UPDATE {self.customers_table} SET template_name = ?, instance_id = ? WHERE customer_id = ?",
                    (template_name, instance_id, customer_id)
                )
            else:
                # Create new assignment
                cursor.execute(
                    f"INSERT INTO {self.customers_table} (customer_id, template_name, instance_id) VALUES (?, ?, ?)",
                    (customer_id, template_name, instance_id)
                )
            
            conn.commit()
            conn.close()
            logger.info(f"Assigned workflow '{template_name}' to customer '{customer_id}'")
            return True
        except Exception as e:
            logger.error(f"Error assigning workflow to customer '{customer_id}': {e}")
            return False
    
    def get_customer_workflow(self, customer_id: str) -> Tuple[Optional[str], Optional[str]]:
        """Get the current workflow assignment for a customer"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                f"SELECT template_name, instance_id FROM {self.customers_table} WHERE customer_id = ?", 
                (customer_id,)
            )
            result = cursor.fetchone()
            
            conn.close()
            
            if result:
                return (result[0], result[1])
            return (None, None)
        except Exception as e:
            logger.error(f"Error getting workflow for customer '{customer_id}': {e}")
            return (None, None)

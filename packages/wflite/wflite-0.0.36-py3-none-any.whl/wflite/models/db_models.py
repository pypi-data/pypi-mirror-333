from sqlalchemy import Column, Integer, String, ForeignKey, JSON, create_engine, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import json
import os
import sys

# Import our own config loader using absolute imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from wflite.config.config_loader import ConfigLoader

Base = declarative_base()
config = ConfigLoader()

# Get table names from config
workflow_db = getattr(config, '_config', {}).get('workflow_db', {})
table_names = workflow_db.get('tables', {})
templates_table = table_names.get('templates', 'workflow_templates')
instances_table = table_names.get('instances', 'workflow_instances')
customers_table = table_names.get('customers', 'workflow_assignments')
states_table = table_names.get('states', 'workflow_states')
transitions_table = table_names.get('transitions', 'workflow_transitions')

# Only define one class per table - let's use StateMachine as the main templates class
class StateMachine(Base):
    __tablename__ = templates_table
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(String(255))
    data = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    states = relationship("State", back_populates="state_machine", cascade="all, delete-orphan")
    transitions = relationship("Transition", back_populates="state_machine", cascade="all, delete-orphan")

class StateMachineInstance(Base):
    __tablename__ = instances_table
    
    id = Column(Integer, primary_key=True)
    instance_id = Column(String(255), unique=True, nullable=False)
    template_name = Column(String(255), nullable=False, index=True)
    current_state = Column(String(255), nullable=False)
    context = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    def __init__(self, instance_id, template_name, current_state, context=None):
        """Initialize an instance with proper context handling"""
        self.instance_id = instance_id
        self.template_name = template_name
        self.current_state = current_state
        self.set_context(context)

    def _ensure_dict(self, value):
        """Convert value to dictionary if possible"""
        if isinstance(value, dict):
            return dict(value)
        if isinstance(value, str):
            try:
                parsed = json.loads(value)
                if isinstance(parsed, dict):
                    return parsed
            except json.JSONDecodeError:
                pass
        return {}

    def set_context(self, context):
        """Set context with proper merging"""
        try:
            # Get current context as dictionary
            current = self._ensure_dict(self.context)
            
            # Convert new context to dictionary
            new_context = self._ensure_dict(context)
            
            # Handle data field specially
            if 'data' in new_context:
                data = self._ensure_dict(new_context['data'])
                # Remove data field and add its contents directly
                del new_context['data']
                current.update(data)
            
            # Update with remaining fields
            current.update(new_context)
            
            # Store as JSON string
            self.context = json.dumps(current)
            
        except Exception as e:
            print(f"Error in set_context: {str(e)}")
            self.context = "{}"

    @property
    def context_dict(self):
        """Get context as dictionary"""
        return self._ensure_dict(self.context)

    @context_dict.setter
    def context_dict(self, value):
        """Set context from dictionary"""
        if isinstance(value, dict):
            self.context = json.dumps(value)
        else:
            self.context = "{}"

class CustomerWorkflow(Base):
    __tablename__ = customers_table
    
    id = Column(Integer, primary_key=True)
    customer_id = Column(String(255), unique=True, nullable=False, index=True)
    template_name = Column(String(255), nullable=False)
    instance_id = Column(String(255), ForeignKey(f"{instances_table}.instance_id"), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class State(Base):
    __tablename__ = states_table
    
    id = Column(Integer, primary_key=True)
    state_id = Column(String(50))
    name = Column(String(255))
    type = Column(String(50))
    entry_actions = Column(JSON, nullable=True)
    exit_actions = Column(JSON, nullable=True)
    state_machine_id = Column(Integer, ForeignKey(f"{templates_table}.id"))
    state_machine = relationship("StateMachine", back_populates="states")

class Transition(Base):
    __tablename__ = transitions_table
    
    id = Column(Integer, primary_key=True)
    source = Column(String(50))
    target = Column(String(50))
    event = Column(String(255), nullable=True)
    action = Column(String(255), nullable=True)
    guard = Column(String(255), nullable=True)
    state_machine_id = Column(Integer, ForeignKey(f"{templates_table}.id"))
    state_machine = relationship("StateMachine", back_populates="transitions")

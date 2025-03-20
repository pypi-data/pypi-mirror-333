import os
import json
import time
import logging
from typing import Dict, Any, List, Optional, Tuple
from pymongo import MongoClient, ASCENDING
from pymongo.errors import PyMongoError, OperationFailure
from datetime import datetime

logger = logging.getLogger(__name__)

class MongoDBPersistenceProvider:
    """MongoDB implementation of persistence for state machines"""
    
    def __init__(self, 
                 connection_string=None,
                 host="localhost", 
                 port=27017,
                 username=None,
                 password=None,
                 database_name="workflow_db",
                 templates_collection="templates",
                 instances_collection="instances",
                 customers_collection="customers",
                 cosmos_db_mode=False):
        """
        Initialize the MongoDB persistence provider.
        
        Args:
            connection_string: MongoDB connection string (overrides other connection params)
            host: MongoDB host
            port: MongoDB port
            username: MongoDB username
            password: MongoDB password
            database_name: Name of the database to use
            templates_collection: Name of collection for templates
            instances_collection: Name of collection for instances
            customers_collection: Name of collection for customer mappings
            cosmos_db_mode: Set to True for Azure Cosmos DB with MongoDB API
        """
        # Use connection string if provided, otherwise build from parameters
        if connection_string:
            self.client = MongoClient(connection_string)
            # Check if this is likely a Cosmos DB connection
            if "cosmos" in connection_string.lower():
                cosmos_db_mode = True
        else:
            # Try to read from environment variables if not provided
            connection_string = os.environ.get('MONGODB_URI')
            if connection_string:
                self.client = MongoClient(connection_string)
                if "cosmos" in connection_string.lower():
                    cosmos_db_mode = True
            else:
                # Build connection from parameters
                if username and password:
                    self.client = MongoClient(
                        host=host,
                        port=port,
                        username=username,
                        password=password
                    )
                else:
                    self.client = MongoClient(host=host, port=port)
                
                # Check if this is likely a Cosmos DB host
                if isinstance(host, str) and "cosmos" in host.lower():
                    cosmos_db_mode = True
        
        # Set database and collection names
        self.database_name = database_name
        self.templates_collection_name = templates_collection
        self.instances_collection_name = instances_collection
        self.customers_collection_name = customers_collection
        self.cosmos_db_mode = cosmos_db_mode
        
        if self.cosmos_db_mode:
            logger.info("Cosmos DB mode enabled - adapting operations for Cosmos DB")
        
        # Get database and collections
        self._initialize_db()
    
    def _initialize_db(self):
        """Initialize database and collections"""
        try:
            # Get database
            self.db = self.client[self.database_name]
            
            # Get collections
            self.templates_collection = self.db[self.templates_collection_name]
            self.instances_collection = self.db[self.instances_collection_name]
            self.customers_collection = self.db[self.customers_collection_name]
            
            # Try to create indexes, but don't fail if we can't (for CosmosDB)
            if not self.cosmos_db_mode:
                try:
                    self.templates_collection.create_index([("name", ASCENDING)], unique=True)
                    logger.info("Created name index on templates collection")
                    
                    self.instances_collection.create_index([("instance_id", ASCENDING)], unique=True)
                    self.instances_collection.create_index([("template_name", ASCENDING)])
                    logger.info("Created indexes on instances collection")
                    
                    self.customers_collection.create_index([("customer_id", ASCENDING)], unique=True)
                    logger.info("Created customer_id index on customers collection")
                except Exception as e:
                    logger.warning(f"Could not create indexes: {e}")
            else:
                logger.info("Skipping index creation in Cosmos DB mode")
            
            logger.info("Connected to MongoDB collections")
            
        except Exception as e:
            logger.error(f"Error initializing MongoDB: {e}")
            raise
    
    # Template Methods
    
    def save_template(self, name: str, template_data: Dict[str, Any], description: str = None) -> bool:
        """Save a template to MongoDB"""
        try:
            # Define the document to save
            timestamp = datetime.utcnow()
            
            if self.cosmos_db_mode:
                # For Cosmos DB, we need to include the partition key
                # The shard key appears to be the collection name
                document = {
                    'id': name,  # Required for Cosmos DB
                    'templates': self.templates_collection_name,  # Shard key
                    'name': name,
                    'description': description or '',
                    'data': template_data,  # MongoDB can store JSON natively
                    'updated_at': timestamp
                }
            else:
                # Standard MongoDB document
                document = {
                    'name': name,
                    'description': description or '',
                    'data': template_data,
                    'updated_at': timestamp
                }
            
            # Check if template already exists
            existing = None
            try:
                if self.cosmos_db_mode:
                    existing = self.templates_collection.find_one({'id': name})
                else:
                    existing = self.templates_collection.find_one({'name': name})
            except Exception as e:
                logger.warning(f"Error checking for existing template: {e}")
            
            if existing:
                # Preserve created_at
                document['created_at'] = existing.get('created_at', timestamp)
                # Update the document
                if self.cosmos_db_mode:
                    self.templates_collection.replace_one({'id': name}, document)
                else:
                    self.templates_collection.replace_one({'name': name}, document)
            else:
                # Set created_at for new documents
                document['created_at'] = timestamp
                # Insert new document
                self.templates_collection.insert_one(document)
            
            logger.info(f"Saved template '{name}' successfully")
            return True
        except PyMongoError as e:
            logger.error(f"Error saving template '{name}': {e}")
            return False
    
    def load_template(self, name: str) -> Optional[Dict[str, Any]]:
        """Load a template from MongoDB"""
        try:
            # For Cosmos DB, search by id, otherwise by name
            if self.cosmos_db_mode:
                document = self.templates_collection.find_one({'id': name})
            else:
                document = self.templates_collection.find_one({'name': name})
                
            if not document:
                return None
                
            # Return the template data
            return document['data']
        except PyMongoError as e:
            logger.error(f"Error loading template '{name}': {e}")
            return None
    
    def delete_template(self, name: str) -> bool:
        """Delete a template from MongoDB"""
        try:
            # For Cosmos DB, delete by id, otherwise by name
            if self.cosmos_db_mode:
                result = self.templates_collection.delete_one({'id': name})
            else:
                result = self.templates_collection.delete_one({'name': name})
                
            logger.info(f"Deleted template '{name}' successfully" if result.deleted_count > 0 
                        else f"Template '{name}' not found for deletion")
            return True
        except PyMongoError as e:
            logger.error(f"Error deleting template '{name}': {e}")
            return False
    
    def list_templates(self) -> List[str]:
        """List all template names from MongoDB"""
        try:
            # Use projection to only return the name field
            if self.cosmos_db_mode:
                documents = self.templates_collection.find({}, {'name': 1, '_id': 0})
            else:
                documents = self.templates_collection.find({}, {'name': 1, '_id': 0})
                
            return [doc['name'] for doc in documents]
        except PyMongoError as e:
            logger.error(f"Error listing templates: {e}")
            return []
    
    # Instance Methods
    
    def create_instance(self, instance_id: str, template_name: str, current_state: str, context: Dict[str, Any] = None) -> bool:
        """Create a new state machine instance in MongoDB"""
        try:
            # Define the document to save
            timestamp = datetime.utcnow()
            
            if self.cosmos_db_mode:
                # For Cosmos DB, include the shard key
                document = {
                    'id': instance_id,  # Required for Cosmos DB
                    'instances': self.instances_collection_name,  # Shard key
                    'instance_id': instance_id,
                    'template_name': template_name,
                    'current_state': current_state,
                    'context': context or {},
                    'updated_at': timestamp
                }
            else:
                document = {
                    'instance_id': instance_id,
                    'template_name': template_name,
                    'current_state': current_state,
                    'context': context or {},
                    'updated_at': timestamp
                }
            
            # Check if instance already exists
            existing = None
            try:
                if self.cosmos_db_mode:
                    existing = self.instances_collection.find_one({'id': instance_id})
                else:
                    existing = self.instances_collection.find_one({'instance_id': instance_id})
            except Exception as e:
                logger.warning(f"Error checking for existing instance: {e}")
            
            if existing:
                # Preserve created_at
                document['created_at'] = existing.get('created_at', timestamp)
                # Update the document
                if self.cosmos_db_mode:
                    self.instances_collection.replace_one({'id': instance_id}, document)
                else:
                    self.instances_collection.replace_one({'instance_id': instance_id}, document)
            else:
                # Set created_at for new documents
                document['created_at'] = timestamp
                # Insert new document
                self.instances_collection.insert_one(document)
            
            logger.info(f"Created instance '{instance_id}' successfully")
            return True
        except PyMongoError as e:
            logger.error(f"Error creating instance '{instance_id}': {e}")
            return False
    
    def update_instance(self, instance_id: str, current_state: str, context: Dict[str, Any]) -> bool:
        """Update an existing state machine instance in MongoDB"""
        try:
            # Define the update
            timestamp = datetime.utcnow()
            
            if self.cosmos_db_mode:
                # For Cosmos DB, need to get the document and replace it
                # because $set operations may not work as expected
                try:
                    existing = self.instances_collection.find_one({'id': instance_id})
                    if existing:
                        document = existing.copy()
                        document['current_state'] = current_state
                        document['context'] = context
                        document['updated_at'] = timestamp
                        self.instances_collection.replace_one({'id': instance_id}, document)
                    else:
                        # Create new document with required fields
                        document = {
                            'id': instance_id,
                            'instances': self.instances_collection_name,  # Shard key
                            'instance_id': instance_id,
                            'template_name': "unknown",  # We don't know it at this point
                            'current_state': current_state,
                            'context': context,
                            'created_at': timestamp,
                            'updated_at': timestamp
                        }
                        self.instances_collection.insert_one(document)
                except Exception as e:
                    logger.error(f"Error updating instance with replacement: {e}")
                    return False
            else:
                # Standard MongoDB update
                update = {
                    '$set': {
                        'current_state': current_state,
                        'context': context,
                        'updated_at': timestamp
                    }
                }
                
                # Update with upsert=True to create if not exists
                self.instances_collection.update_one(
                    {'instance_id': instance_id}, 
                    update,
                    upsert=True
                )
            
            logger.info(f"Updated instance '{instance_id}' successfully")
            return True
        except PyMongoError as e:
            logger.error(f"Error updating instance '{instance_id}': {e}")
            return False
    
    def get_instance(self, instance_id: str) -> Optional[Dict[str, Any]]:
        """Get a state machine instance from MongoDB"""
        try:
            # For Cosmos DB, search by id, otherwise by instance_id
            if self.cosmos_db_mode:
                document = self.instances_collection.find_one({'id': instance_id})
            else:
                document = self.instances_collection.find_one({'instance_id': instance_id})
                
            if not document:
                return None
                
            # Return only the necessary data, omitting internal fields
            return {
                'instance_id': instance_id,
                'template_name': document['template_name'],
                'current_state': document['current_state'],
                'context': document['context'],
                'created_at': document.get('created_at'),
                'updated_at': document.get('updated_at')
            }
        except PyMongoError as e:
            logger.error(f"Error getting instance '{instance_id}': {e}")
            return None
    
    def delete_instance(self, instance_id: str) -> bool:
        """Delete a state machine instance from MongoDB"""
        try:
            # For Cosmos DB, delete by id, otherwise by instance_id
            if self.cosmos_db_mode:
                result = self.instances_collection.delete_one({'id': instance_id})
            else:
                result = self.instances_collection.delete_one({'instance_id': instance_id})
                
            logger.info(f"Deleted instance '{instance_id}' successfully" if result.deleted_count > 0 
                        else f"Instance '{instance_id}' not found for deletion")
            return True
        except PyMongoError as e:
            logger.error(f"Error deleting instance '{instance_id}': {e}")
            return False
    
    # Customer Methods
    
    def assign_customer_workflow(self, customer_id: str, template_name: str, instance_id: str) -> bool:
        """Assign a workflow template instance to a customer in MongoDB"""
        try:
            # Define the document
            timestamp = datetime.utcnow()
            
            if self.cosmos_db_mode:
                # For Cosmos DB, include the shard key
                document = {
                    'id': customer_id,  # Required for Cosmos DB
                    'customers': self.customers_collection_name,  # Shard key
                    'customer_id': customer_id,
                    'template_name': template_name,
                    'instance_id': instance_id,
                    'updated_at': timestamp
                }
            else:
                document = {
                    'customer_id': customer_id,
                    'template_name': template_name,
                    'instance_id': instance_id,
                    'updated_at': timestamp
                }
            
            # Check if customer already exists
            existing = None
            try:
                if self.cosmos_db_mode:
                    existing = self.customers_collection.find_one({'id': customer_id})
                else:
                    existing = self.customers_collection.find_one({'customer_id': customer_id})
            except Exception as e:
                logger.warning(f"Error checking for existing customer: {e}")
            
            if existing:
                # Preserve created_at
                document['created_at'] = existing.get('created_at', timestamp)
                # Update the document
                if self.cosmos_db_mode:
                    self.customers_collection.replace_one({'id': customer_id}, document)
                else:
                    self.customers_collection.replace_one({'customer_id': customer_id}, document)
            else:
                # Set created_at for new documents
                document['created_at'] = timestamp
                # Insert new document
                self.customers_collection.insert_one(document)
            
            logger.info(f"Assigned workflow '{template_name}' to customer '{customer_id}'")
            return True
        except PyMongoError as e:
            logger.error(f"Error assigning workflow to customer '{customer_id}': {e}")
            return False
    
    def get_customer_workflow(self, customer_id: str) -> Tuple[Optional[str], Optional[str]]:
        """Get the current workflow assignment for a customer from MongoDB"""
        try:
            # For Cosmos DB, search by id, otherwise by customer_id
            if self.cosmos_db_mode:
                document = self.customers_collection.find_one({'id': customer_id})
            else:
                document = self.customers_collection.find_one({'customer_id': customer_id})
                
            if not document:
                return (None, None)
                
            return (document['template_name'], document['instance_id'])
        except PyMongoError as e:
            logger.error(f"Error getting workflow for customer '{customer_id}': {e}")
            return (None, None)

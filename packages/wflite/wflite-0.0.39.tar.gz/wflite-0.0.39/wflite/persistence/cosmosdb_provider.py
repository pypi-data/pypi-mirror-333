import os
import json
import time
import logging
from typing import Dict, Any, List, Optional, Tuple
from azure.cosmos import CosmosClient, PartitionKey, exceptions
from datetime import datetime

logger = logging.getLogger(__name__)

class CosmosDBPersistenceProvider:
    """Azure Cosmos DB implementation of persistence for state machines"""
    
    def __init__(self, 
                 connection_string=None,
                 endpoint=None, 
                 key=None,
                 database_name="workflow_db",
                 templates_container="templates",
                 instances_container="instances",
                 customers_container="customers"):
        """
        Initialize the Cosmos DB persistence provider.
        
        Args:
            connection_string: Azure Cosmos DB connection string (overrides endpoint/key)
            endpoint: Azure Cosmos DB endpoint URL
            key: Azure Cosmos DB access key
            database_name: Name of the database to use
            templates_container: Name of container for templates
            instances_container: Name of container for instances
            customers_container: Name of container for customer mappings
        """
        # Use connection string if provided, otherwise use endpoint and key
        if connection_string:
            self.client = CosmosClient.from_connection_string(connection_string)
        elif endpoint and key:
            self.client = CosmosClient(url=endpoint, credential=key)
        else:
            # Try to read from environment variables
            connection_string = os.environ.get('COSMOS_CONNECTION_STRING')
            if connection_string:
                self.client = CosmosClient.from_connection_string(connection_string)
            else:
                endpoint = os.environ.get('COSMOS_ENDPOINT')
                key = os.environ.get('COSMOS_KEY')
                if not (endpoint and key):
                    raise ValueError("Either connection_string or both endpoint and key must be provided")
                self.client = CosmosClient(url=endpoint, credential=key)
        
        # Set container names
        self.database_name = database_name
        self.templates_container_name = templates_container
        self.instances_container_name = instances_container
        self.customers_container_name = customers_container
        
        # Initialize containers
        self._initialize_db()
    
    @staticmethod
    def create_database(connection_string=None, endpoint=None, key=None,
                       database_name="workflow_db",
                       templates_container="templates",
                       instances_container="instances", 
                       customers_container="customers"):
        """
        Create Cosmos DB database and containers required by the persistence provider.
        
        Returns:
            True if database created successfully, False otherwise
        """
        try:
            # Create client
            if connection_string:
                client = CosmosClient.from_connection_string(connection_string)
            elif endpoint and key:
                client = CosmosClient(url=endpoint, credential=key)
            else:
                # Try to read from environment variables
                connection_string = os.environ.get('COSMOS_CONNECTION_STRING')
                if connection_string:
                    client = CosmosClient.from_connection_string(connection_string)
                else:
                    endpoint = os.environ.get('COSMOS_ENDPOINT')
                    key = os.environ.get('COSMOS_KEY')
                    if not (endpoint and key):
                        raise ValueError("Either connection_string or both endpoint and key must be provided")
                    client = CosmosClient(url=endpoint, credential=key)
            
            # Create database
            try:
                database = client.create_database(id=database_name)
                logger.info(f"Created database: {database_name}")
            except exceptions.CosmosResourceExistsError:
                database = client.get_database_client(database_name)
                logger.info(f"Database already exists: {database_name}")
            
            # Create containers
            containers = [
                (templates_container, "/id"),
                (instances_container, "/instance_id"),
                (customers_container, "/customer_id")
            ]
            
            for container_name, partition_key_path in containers:
                try:
                    database.create_container(
                        id=container_name, 
                        partition_key=PartitionKey(path=partition_key_path),
                        offer_throughput=400  # Minimum throughput
                    )
                    logger.info(f"Created container: {container_name}")
                except exceptions.CosmosResourceExistsError:
                    logger.info(f"Container already exists: {container_name}")
            
            logger.info("All containers created successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error creating Cosmos DB database: {e}")
            return False
    
    def _initialize_db(self):
        """Initialize database and containers"""
        try:
            # Get database (create if not exists)
            try:
                self.database = self.client.create_database(id=self.database_name)
            except exceptions.CosmosResourceExistsError:
                self.database = self.client.get_database_client(self.database_name)
            
            # Get containers (create if not exist)
            containers_to_create = [
                (self.templates_container_name, "/id"),
                (self.instances_container_name, "/instance_id"),
                (self.customers_container_name, "/customer_id")
            ]
            
            for container_name, partition_key_path in containers_to_create:
                try:
                    self.database.create_container(
                        id=container_name, 
                        partition_key=PartitionKey(path=partition_key_path)
                    )
                except exceptions.CosmosResourceExistsError:
                    pass
            
            # Set container clients
            self.templates_container = self.database.get_container_client(self.templates_container_name)
            self.instances_container = self.database.get_container_client(self.instances_container_name)
            self.customers_container = self.database.get_container_client(self.customers_container_name)
            
            logger.info("Connected to Cosmos DB containers")
            
        except Exception as e:
            logger.error(f"Error initializing Cosmos DB: {e}")
            raise
    
    # Template Methods
    
    def save_template(self, name: str, template_data: Dict[str, Any], description: str = None) -> bool:
        """Save a template to Cosmos DB"""
        try:
            # Define the item to save
            timestamp = datetime.utcnow().isoformat()
            item = {
                'id': name,
                'name': name,
                'description': description or '',
                'data': json.dumps(template_data),
                'created_at': timestamp,
                'updated_at': timestamp
            }
            
            # Check if template already exists
            try:
                existing_item = self.templates_container.read_item(item=name, partition_key=name)
                # If exists, update the timestamp
                item['created_at'] = existing_item.get('created_at', timestamp)
            except exceptions.CosmosResourceNotFoundError:
                pass
            
            # Create or replace the item
            self.templates_container.upsert_item(body=item)
            logger.info(f"Saved template '{name}' successfully")
            return True
        except Exception as e:
            logger.error(f"Error saving template '{name}': {e}")
            return False
    
    def load_template(self, name: str) -> Optional[Dict[str, Any]]:
        """Load a template from Cosmos DB"""
        try:
            item = self.templates_container.read_item(item=name, partition_key=name)
            template_data = json.loads(item['data'])
            return template_data
        except exceptions.CosmosResourceNotFoundError:
            return None
        except Exception as e:
            logger.error(f"Error loading template '{name}': {e}")
            return None
    
    def delete_template(self, name: str) -> bool:
        """Delete a template from Cosmos DB"""
        try:
            self.templates_container.delete_item(item=name, partition_key=name)
            logger.info(f"Deleted template '{name}' successfully")
            return True
        except exceptions.CosmosResourceNotFoundError:
            logger.warning(f"Template '{name}' not found for deletion")
            return True  # Consider it a success if it doesn't exist
        except Exception as e:
            logger.error(f"Error deleting template '{name}': {e}")
            return False
    
    def list_templates(self) -> List[str]:
        """List all template names from Cosmos DB"""
        try:
            query = "SELECT c.name FROM c"
            items = list(self.templates_container.query_items(
                query=query,
                enable_cross_partition_query=True
            ))
            return [item['name'] for item in items]
        except Exception as e:
            logger.error(f"Error listing templates: {e}")
            return []
    
    # Instance Methods
    
    def create_instance(self, instance_id: str, template_name: str, current_state: str, context: Dict[str, Any] = None) -> bool:
        """Create a new state machine instance in Cosmos DB"""
        try:
            # Define the item to save
            timestamp = datetime.utcnow().isoformat()
            item = {
                'id': instance_id,
                'instance_id': instance_id,
                'template_name': template_name,
                'current_state': current_state,
                'context': json.dumps(context or {}),
                'created_at': timestamp,
                'updated_at': timestamp
            }
            
            # Create or replace the item
            self.instances_container.upsert_item(body=item)
            logger.info(f"Created instance '{instance_id}' successfully")
            return True
        except Exception as e:
            logger.error(f"Error creating instance '{instance_id}': {e}")
            return False
    
    def update_instance(self, instance_id: str, current_state: str, context: Dict[str, Any]) -> bool:
        """Update an existing state machine instance in Cosmos DB"""
        try:
            # Get the existing item to preserve created_at
            try:
                existing_item = self.instances_container.read_item(item=instance_id, partition_key=instance_id)
                created_at = existing_item.get('created_at')
            except exceptions.CosmosResourceNotFoundError:
                # If not found, this will be treated as a new item
                timestamp = datetime.utcnow().isoformat()
                created_at = timestamp
            
            # Update the item
            timestamp = datetime.utcnow().isoformat()
            item = {
                'id': instance_id,
                'instance_id': instance_id,
                'template_name': existing_item.get('template_name', ''),
                'current_state': current_state,
                'context': json.dumps(context),
                'created_at': created_at,
                'updated_at': timestamp
            }
            
            self.instances_container.upsert_item(body=item)
            logger.info(f"Updated instance '{instance_id}' successfully")
            return True
        except Exception as e:
            logger.error(f"Error updating instance '{instance_id}': {e}")
            return False
    
    def get_instance(self, instance_id: str) -> Optional[Dict[str, Any]]:
        """Get a state machine instance from Cosmos DB"""
        try:
            item = self.instances_container.read_item(item=instance_id, partition_key=instance_id)
            
            # Parse context from JSON
            context = json.loads(item['context']) if 'context' in item else {}
            
            return {
                'instance_id': instance_id,
                'template_name': item['template_name'],
                'current_state': item['current_state'],
                'context': context,
                'created_at': item.get('created_at'),
                'updated_at': item.get('updated_at')
            }
        except exceptions.CosmosResourceNotFoundError:
            return None
        except Exception as e:
            logger.error(f"Error getting instance '{instance_id}': {e}")
            return None
    
    def delete_instance(self, instance_id: str) -> bool:
        """Delete a state machine instance from Cosmos DB"""
        try:
            self.instances_container.delete_item(item=instance_id, partition_key=instance_id)
            logger.info(f"Deleted instance '{instance_id}' successfully")
            return True
        except exceptions.CosmosResourceNotFoundError:
            logger.warning(f"Instance '{instance_id}' not found for deletion")
            return True  # Consider it a success if it doesn't exist
        except Exception as e:
            logger.error(f"Error deleting instance '{instance_id}': {e}")
            return False
    
    # Customer Methods
    
    def assign_customer_workflow(self, customer_id: str, template_name: str, instance_id: str) -> bool:
        """Assign a workflow template instance to a customer in Cosmos DB"""
        try:
            # Define the item to save
            timestamp = datetime.utcnow().isoformat()
            item = {
                'id': customer_id,
                'customer_id': customer_id,
                'template_name': template_name,
                'instance_id': instance_id,
                'created_at': timestamp,
                'updated_at': timestamp
            }
            
            # Check if customer already exists to preserve created_at
            try:
                existing_item = self.customers_container.read_item(item=customer_id, partition_key=customer_id)
                item['created_at'] = existing_item.get('created_at', timestamp)
            except exceptions.CosmosResourceNotFoundError:
                pass
            
            # Create or replace the item
            self.customers_container.upsert_item(body=item)
            logger.info(f"Assigned workflow '{template_name}' to customer '{customer_id}'")
            return True
        except Exception as e:
            logger.error(f"Error assigning workflow to customer '{customer_id}': {e}")
            return False
    
    def get_customer_workflow(self, customer_id: str) -> Tuple[Optional[str], Optional[str]]:
        """Get the current workflow assignment for a customer from Cosmos DB"""
        try:
            item = self.customers_container.read_item(item=customer_id, partition_key=customer_id)
            return (item['template_name'], item['instance_id'])
        except exceptions.CosmosResourceNotFoundError:
            return (None, None)
        except Exception as e:
            logger.error(f"Error getting workflow for customer '{customer_id}': {e}")
            return (None, None)

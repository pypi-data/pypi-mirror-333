import os
import sys
from typing import Dict, Any
import logging
import importlib

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from wflite.config.config_loader import ConfigLoader

logger = logging.getLogger(__name__)

class PersistenceProviderFactory:
    """Factory for creating persistence providers based on configuration"""
    
    @staticmethod
    def create_provider(config: Dict[str, Any] = None):
        """
        Create a persistence provider instance based on configuration.
        
        Args:
            config: Configuration dictionary, if None will load from ConfigLoader
            
        Returns:
            A persistence provider instance
        """
        if config is None:
            config_loader = ConfigLoader()
            config = getattr(config_loader, '_config', {})
        
        # Get persistence settings
        persistence = config.get('persistence', {})
        provider_type = persistence.get('provider', 'sqlite')
        
        logger.info(f"Creating persistence provider: {provider_type}")
        
        if provider_type == 'mongodb':
            try:
                # Import the MongoDB provider with absolute import
                from wflite.persistence.mongodb_provider import MongoDBPersistenceProvider
                
                # Get MongoDB config
                mongo_config = persistence.get('mongodb', {})
                connection_string = mongo_config.get('connection_string')
                host = mongo_config.get('host', 'localhost')
                port = mongo_config.get('port', 27017)
                username = mongo_config.get('username')
                password = mongo_config.get('password')
                database = mongo_config.get('database', 'workflow_db')
                templates_collection = mongo_config.get('templates_collection', 'templates')
                instances_collection = mongo_config.get('instances_collection', 'instances')
                customers_collection = mongo_config.get('customers_collection', 'customers')
                cosmos_db_mode = mongo_config.get('cosmos_db_mode', False)
                
                return MongoDBPersistenceProvider(
                    connection_string=connection_string,
                    host=host,
                    port=port,
                    username=username,
                    password=password,
                    database_name=database,
                    templates_collection=templates_collection,
                    instances_collection=instances_collection,
                    customers_collection=customers_collection,
                    cosmos_db_mode=cosmos_db_mode
                )
            except ImportError:
                logger.error("Failed to import MongoDB provider. Make sure pymongo is installed.")
                logger.info("Falling back to SQLite provider.")
                # Fall back to SQLite
        elif provider_type == 'cosmosdb':
            try:
                # Import the CosmosDB provider with absolute import
                from wflite.persistence.cosmosdb_provider import CosmosDBPersistenceProvider
                
                # Get CosmosDB config
                cosmos_config = persistence.get('cosmosdb', {})
                connection_string = cosmos_config.get('connection_string')
                endpoint = cosmos_config.get('endpoint')
                key = cosmos_config.get('key')
                database = cosmos_config.get('database', 'workflow_db')
                templates_container = cosmos_config.get('templates_container', 'templates')
                instances_container = cosmos_config.get('instances_container', 'instances')
                customers_container = cosmos_config.get('customers_container', 'customers')
                
                return CosmosDBPersistenceProvider(
                    connection_string=connection_string,
                    endpoint=endpoint,
                    key=key,
                    database_name=database,
                    templates_container=templates_container,
                    instances_container=instances_container,
                    customers_container=customers_container
                )
            except ImportError:
                logger.error("Failed to import CosmosDB provider. Make sure azure-cosmos is installed.")
                logger.info("Falling back to SQLite provider.")
                # Fall back to SQLite
        elif provider_type == 'dynamodb':
            try:
                # Import the DynamoDB provider with absolute import
                from wflite.persistence.dynamodb_provider import DynamoDBPersistenceProvider
                
                # Get DynamoDB config
                dynamodb_config = persistence.get('dynamodb', {})
                region = dynamodb_config.get('region', 'us-east-1')
                endpoint = dynamodb_config.get('endpoint_url')
                templates_table = dynamodb_config.get('templates_table', 'workflow_templates')
                instances_table = dynamodb_config.get('instances_table', 'workflow_instances')
                customers_table = dynamodb_config.get('customers_table', 'workflow_assignments')
                
                return DynamoDBPersistenceProvider(
                    region_name=region,
                    endpoint_url=endpoint,
                    templates_table=templates_table,
                    instances_table=instances_table,
                    customers_table=customers_table
                )
            except ImportError:
                logger.error("Failed to import DynamoDB provider. Make sure boto3 is installed.")
                logger.info("Falling back to SQLite provider.")
                # Fall back to SQLite
        
        # Default to SQLite with absolute import
        from wflite.persistence.sqlite_provider import SQLitePersistenceProvider
        
        db_path = persistence.get('sqlite', {}).get('db_path', 'workflows.db')
        
        return SQLitePersistenceProvider(db_path=db_path)

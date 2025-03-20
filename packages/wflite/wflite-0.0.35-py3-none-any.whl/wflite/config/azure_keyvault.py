"""
Azure Key Vault integration for securely storing and retrieving configuration secrets
"""
import os
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

def get_keyvault_secrets() -> Dict[str, str]:
    """
    Get secrets from Azure Key Vault using Azure managed identity
    
    Returns:
        Dictionary of secret name to secret value
    """
    # Check if we're running in Azure Functions environment
    is_azure_functions = os.environ.get('FUNCTIONS_WORKER_RUNTIME') is not None
    
    # Early return if not in Azure environment and no credentials provided
    if not is_azure_functions and not os.environ.get('AZURE_TENANT_ID'):
        logger.info("Not running in Azure environment with managed identity")
        return {}
    
    try:
        # Import the Azure libraries (these will be installed in Azure Functions)
        from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
        from azure.keyvault.secrets import SecretClient
        
        # Get Key Vault URL from environment variable
        vault_url = os.environ.get('KEYVAULT_URL', 'https://wflite-kv.vault.azure.net/')
        
        # Try to get a credential in order of preference
        credential = None
        
        # First try Managed Identity if we're in Azure Functions
        if is_azure_functions:
            try:
                credential = ManagedIdentityCredential()
                logger.info("Using Managed Identity credential")
            except Exception as e:
                logger.warning(f"Failed to get ManagedIdentityCredential: {str(e)}")
                
        # Fall back to DefaultAzureCredential which tries multiple methods
        if credential is None:
            try:
                credential = DefaultAzureCredential()
                logger.info("Using Default Azure credential")
            except Exception as e:
                logger.error(f"Failed to get DefaultAzureCredential: {str(e)}")
                return {}
        
        # Create client and get secrets
        client = SecretClient(vault_url=vault_url, credential=credential)
        
        # These are the secrets we want to retrieve - add or modify as needed
        secret_names = [
            'MONGODB-CONNECTION-STRING',
            'MONGODB_DATABASE',
            'MONGODB_TEMPLATES_COLLECTION',
            'MONGODB_INSTANCES_COLLECTION',
            'MONGODB_CUSTOMERS_COLLECTION',
            # Add more secret names as needed
        ]
        
        # Get all secrets
        secrets = {}
        for name in secret_names:
            try:
                secret = client.get_secret(name)
                secrets[name] = secret.value
                
                # Also set as environment variable for config loader to use
                env_name = name.replace('-', '_')
                os.environ[env_name] = secret.value
                logger.info(f"Retrieved and set environment variable: {env_name}")
            except Exception as e:
                logger.warning(f"Could not retrieve secret {name}: {str(e)}")
        
        return secrets
        
    except ImportError:
        logger.warning("Azure libraries not installed. Install with: pip install azure-identity azure-keyvault-secrets")
        return {}
    except Exception as e:
        logger.error(f"Error retrieving Key Vault secrets: {str(e)}")
        return {}

def map_secrets_to_config(secrets: Dict[str, str]) -> Dict[str, Any]:
    """
    Maps Key Vault secrets to configuration structure
    
    Args:
        secrets: Dictionary of secrets from Key Vault
        
    Returns:
        Configuration dictionary compatible with wflite
    """
    # Setting environment variables is now done in get_keyvault_secrets
    # This is kept for backwards compatibility
    
    config = {}
    
    # MongoDB configuration
    mongo_conn_str = secrets.get('MONGODB-CONNECTION-STRING') or secrets.get('MONGODB_CONNECTION_STRING')
    if mongo_conn_str:
        if 'persistence' not in config:
            config['persistence'] = {}
            
        config['persistence']['provider'] = 'mongodb'
        config['persistence']['mongodb'] = {
            'connection_string': mongo_conn_str,
            'database': os.environ.get('MONGODB_DATABASE', 'workflow_db'),
            'templates_collection': os.environ.get('MONGODB_TEMPLATES_COLLECTION', 'templates'),
            'instances_collection': os.environ.get('MONGODB_INSTANCES_COLLECTION', 'instances'),
            'customers_collection': os.environ.get('MONGODB_CUSTOMERS_COLLECTION', 'customers'),
            'cosmos_db_mode': os.environ.get('MONGODB_COSMOS_MODE', 'true').lower() == 'true'
        }
    
    # Add mappings for other secrets as needed
    
    return config

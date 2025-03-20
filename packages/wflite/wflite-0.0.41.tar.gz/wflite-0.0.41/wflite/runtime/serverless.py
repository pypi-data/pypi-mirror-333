from http.client import HTTPException
import os
import sys
import logging
import json

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from pydantic import BaseModel
from typing import Dict, Any, Optional, List

from wflite.registry.db_registry import StateMachineRegistry
from wflite.runtime.statemachine_runtime import StateMachineRuntime
from wflite.config.config_loader import ConfigLoader
from wflite.persistence.provider_factory import PersistenceProviderFactory

# Import KeyVault helper (to be created)
try:
    from wflite.config.azure_keyvault import get_keyvault_secrets
except ImportError:
    # Define a placeholder function if the module is not available
    def get_keyvault_secrets():
        return {}

# Define request models
class EventRequest(BaseModel):
    customer_id: str
    event_name: str
    event_details: Optional[Dict[str, Any]] = None

class EventsRequest(BaseModel):
    events: List[EventRequest]
    
class CustomerWorkflowRequest(BaseModel):
    customer_id: str
    template_name: str
    
class BatchCustomerWorkflowRequest(BaseModel):
    customer_ids: List[str]
    template_name: str

def initialize_runtime(config_json: Optional[Dict[str, Any]] = None):
    """
    Initialize runtime components with the provided configuration or from environment.
    
    Args:
        config_json: Optional configuration dictionary to override the default config
        
    Returns:
        Tuple of (StateMachineRegistry, StateMachineRuntime, config)
    """
    # Load environment variables if dotenv is available
    try:
        from dotenv import load_dotenv
        # Look for .env file in project root
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        env_file = os.path.join(project_root, '.env')
        if os.path.exists(env_file):
            logger.info(f"Loading environment from {env_file}")
            load_dotenv(env_file, override=True)
            logger.info(f"PERSISTENCE_PROVIDER: {os.environ.get('PERSISTENCE_PROVIDER', 'not set')}")
    except ImportError:
        pass
    
    # Create config loader - will load from environment variables
    config_loader = ConfigLoader()
    
    # Debug what's in the configuration
    logger.info(f"Loaded config persistence provider: {config_loader._config.get('persistence', {}).get('provider', 'not set')}")
    
    # Try to load secrets from Azure Key Vault
    try:
        keyvault_secrets = get_keyvault_secrets()
        if keyvault_secrets:
            logger.info("Successfully loaded secrets from Azure Key Vault")
            # No need to manually apply them as they're set as environment variables
            # and will be processed by the config_loader
    except Exception as e:
        logger.warning(f"Failed to load secrets from Azure Key Vault: {str(e)}")
    
    # Override config if provided (request config overrides KeyVault and env vars)
    if config_json:
        logger.info(f"Overriding configuration with provided JSON")
        config_loader._config.update(config_json)
    
    config = config_loader._config
    
    # Create persistence provider
    persistence_provider = PersistenceProviderFactory.create_provider(config)
    
    # Log the selected provider
    provider_type = config.get('persistence', {}).get('provider', 'sqlite')
    logger.info(f"Using persistence provider: {provider_type}")
    
    # Create registry
    registry = StateMachineRegistry()
    
    # Create runtime with the configured persistence provider
    runtime = StateMachineRuntime(
        persistence_provider=persistence_provider,
        registry_provider=registry
    )
    
    logger.info(f"Serverless runtime initialized with {provider_type} persistence provider")
    
    return registry, runtime, config

def _process_single_event(request: EventRequest, registry, runtime, action_handler=None):
    """
    Helper function to process a single event with provided runtime components.
    
    Args:
        request: EventRequest object
        registry: State machine registry
        runtime: State machine runtime
        action_handler: Optional callback function to handle workflow actions
        
    Returns:
        Dict with event processing result
    """
    try:
        logger.info(f"Processing event '{request.event_name}' for customer {request.customer_id}")
        
        # Get customer's workflow instance
        template_name, instance_id = runtime.get_customer_instance(request.customer_id)
        
        if not template_name or not instance_id:
            logger.error(f"No workflow assigned to customer {request.customer_id}")
            return {
                "success": False,
                "error": f"No workflow assigned to customer {request.customer_id}",
                "customer_id": request.customer_id
            }
        
        # Get template data
        template_data = registry.load(template_name)
        if not template_data:
            logger.error(f"Template {template_name} not found")
            return {
                "success": False,
                "error": f"Template {template_name} not found",
                "customer_id": request.customer_id
            }
            
        # Process the event - now passing the action_handler
        success, actions = runtime.trigger_event(
            instance_id=instance_id,
            event_name=request.event_name,
            template_data=template_data,
            event_details=request.event_details,
            action_handler=action_handler
        )
        
        if not success:
            logger.error(f"Event '{request.event_name}' could not be processed")
            return {
                "success": False,
                "error": f"Event '{request.event_name}' could not be processed",
                "customer_id": request.customer_id
            }
        
        # Get updated state info
        current_state = runtime.get_current_state(instance_id, template_data)
        context = runtime.get_context(instance_id)
        
        return {
            "success": True,
            "customer_id": request.customer_id,
            "instance_id": instance_id,
            "template_name": template_name,
            "current_state": current_state["id"],
            "state_name": current_state["name"],
            "context": context,
            "actions": actions
        }
    except Exception as e:
        logger.error(f"Error processing event: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "customer_id": request.customer_id
        }

def _normalize_event_request(request_data):
    """
    Convert various input formats to EventRequest object.
    
    Args:
        request_data: Input data in various formats (dict, EventRequest, etc.)
        
    Returns:
        EventRequest object or None if conversion fails
    """
    try:
        if isinstance(request_data, EventRequest):
            return request_data
            
        if hasattr(request_data, 'get_json'):
            # Handle Flask/Function request objects
            request_data = request_data.get_json()
        elif isinstance(request_data, str):
            # Try parsing a JSON string
            request_data = json.loads(request_data)
        
        if isinstance(request_data, dict):
            return EventRequest(
                customer_id=request_data.get('customer_id'),
                event_name=request_data.get('event_name'),
                event_details=request_data.get('event_details')
            )
        
        logger.error(f"Unsupported request type: {type(request_data)}")
        return None
    except Exception as e:
        logger.error(f"Error normalizing event request: {str(e)}")
        return None

def trigger_event(request, config_json: Optional[Dict[str, Any]] = None, action_handler=None):
    """
    Trigger an event for a customer's workflow instance, suitable for serverless environments.
    
    Args:
        request: Either EventRequest object or dict/JSON with customer_id, event_name, and optional event_details
        config_json: Optional configuration to initialize the runtime
        action_handler: Optional callback function to handle workflow actions
        
    Returns:
        Dict with event processing result
    """
    try:
        # Convert request to EventRequest if needed
        normalized_request = _normalize_event_request(request)
        if not normalized_request:
            return {
                "success": False,
                "error": "Invalid request format"
            }
        
        # Initialize runtime components
        registry, runtime, _ = initialize_runtime(config_json)
        
        # Process the event using the shared helper function, passing action_handler
        return _process_single_event(normalized_request, registry, runtime, action_handler)
        
    except Exception as e:
        logger.error(f"Error processing event: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

def trigger_events(requests, config_json: Optional[Dict[str, Any]] = None, action_handler=None):
    """
    Trigger multiple events for customers' workflow instances in batch, optimizing resource usage.
    
    Args:
        requests: List of EventRequest objects or list of dicts with customer_id, event_name, and optional event_details
        config_json: Optional configuration to initialize the runtime
        action_handler: Optional callback function to handle workflow actions
        
    Returns:
        List of dicts with event processing results
    """
    try:
        if not isinstance(requests, list):
            # Try to handle EventsRequest object
            if hasattr(requests, 'events'):
                requests = requests.events
            elif isinstance(requests, dict) and 'events' in requests:
                requests = requests['events']
            else:
                return [{
                    "success": False,
                    "error": "Invalid batch request format"
                }]
        
        logger.info(f"Processing batch of {len(requests)} events")
        
        # Initialize runtime components once for all events
        registry, runtime, _ = initialize_runtime(config_json)
        
        results = []
        
        # Process each event using shared runtime
        for req_item in requests:
            # Normalize the request
            normalized_request = _normalize_event_request(req_item)
            if not normalized_request:
                results.append({
                    "success": False,
                    "error": f"Invalid request format: {type(req_item)}"
                })
                continue
                
            # Process using the shared helper function, passing action_handler
            result = _process_single_event(normalized_request, registry, runtime, action_handler)
            results.append(result)
        
        return results
        
    except Exception as e:
        logger.error(f"Error in batch processing: {str(e)}")
        return [{
            "success": False,
            "error": f"Batch processing error: {str(e)}"
        }]
    
def assign_customers(request, config_json: Optional[Dict[str, Any]] = None):
    """
    Assign a workflow template to multiple customers at once, suitable for serverless environments.
    
    Args:
        request: Either BatchCustomerWorkflowRequest object or dict/JSON with customer_ids and template_name
        config_json: Optional configuration to initialize the runtime
        
    Returns:
        Dict with assignment results for each customer
    """
    try:
        # Normalize the request
        if isinstance(request, BatchCustomerWorkflowRequest):
            customer_ids = request.customer_ids
            template_name = request.template_name
        elif hasattr(request, 'get_json'):
            # Handle Flask/Function request objects
            request_data = request.get_json()
            customer_ids = request_data.get('customer_ids', [])
            template_name = request_data.get('template_name')
        elif isinstance(request, str):
            # Try parsing a JSON string
            request_data = json.loads(request)
            customer_ids = request_data.get('customer_ids', [])
            template_name = request_data.get('template_name')
        elif isinstance(request, dict):
            customer_ids = request.get('customer_ids', [])
            template_name = request.get('template_name')
        else:
            return {
                "success": False,
                "error": "Invalid request format"
            }
            
        if not customer_ids:
            return {
                "success": False,
                "error": "No customer IDs provided"
            }
            
        if not template_name:
            return {
                "success": False,
                "error": "No template name provided"
            }
        
        # Initialize runtime components
        registry, runtime, _ = initialize_runtime(config_json)
        
        # Validate template exists
        template_data = registry.load(template_name)
        if not template_data:
            return {
                "success": False,
                "error": f"Template {template_name} not found"
            }

        results = []
        
        # Assign workflow to each customer
        for customer_id in customer_ids:
            try:
                # Assign workflow to customer
                success = runtime.assign_customer_workflow(
                    customer_id=customer_id,
                    template_name=template_name,
                    template_data=template_data
                )
                
                if not success:
                    results.append({
                        "customer_id": customer_id,
                        "success": False,
                        "error": "Failed to assign workflow"
                    })
                    continue
                
                # Get instance details
                assigned_template_name, instance_id = runtime.get_customer_instance(customer_id)
                if not instance_id:
                    results.append({
                        "customer_id": customer_id,
                        "success": False,
                        "error": "Failed to create workflow instance"
                    })
                    continue
                    
                # Get current state
                current_state = runtime.get_current_state(instance_id, template_data)
                
                results.append({
                    "customer_id": customer_id,
                    "success": True,
                    "template_name": assigned_template_name,
                    "instance_id": instance_id,
                    "current_state": current_state["id"],
                    "state_name": current_state["name"]
                })
                
            except Exception as e:
                logger.error(f"Error assigning workflow to customer {customer_id}: {str(e)}")
                results.append({
                    "customer_id": customer_id,
                    "success": False,
                    "error": str(e)
                })
        
        # Calculate overall stats
        total = len(customer_ids)
        succeeded = sum(1 for r in results if r.get("success", False))
        failed = total - succeeded
        
        return {
            "success": True,
            "template_name": template_name,
            "total_customers": total,
            "succeeded": succeeded,
            "failed": failed,
            "results": results
        }
        
    except Exception as e:
        logger.error(f"Error in batch assignment: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }
            
def get_customers_context(payload, config_json: Optional[Dict[str, Any]] = None):
    """
    Get context data for multiple customers at once
    
    Expected event format:
    {
        "customer_ids": ["CUST-001", "CUST-002", "CUST-003"]
    }
    
    Returns:
    {
        "CUST-001": { ... context data ... },
        "CUST-002": { ... context data ... },
        "CUST-003": { ... context data ... }
    }
    """
    try:
        # Parse input
        customer_ids = payload.get('customer_ids', [])
        
        if not customer_ids or not isinstance(customer_ids, list):
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing or invalid customer_ids list'})
            }
        
        # Initialize runtime
        registry, runtime, _ = initialize_runtime(config_json)
        
        # Get context data for all customers
        context_data = runtime.get_customers_context(customer_ids)
        
        return {
            'statusCode': 200,
            'body': context_data
        }
    
    except Exception as e:
        logger.exception("Error getting customers context")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
    
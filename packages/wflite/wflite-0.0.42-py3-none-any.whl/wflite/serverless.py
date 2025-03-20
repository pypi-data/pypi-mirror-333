import json
import logging
from typing import Dict, Any, List

from wflite.runtime.statemachine_runtime import StateMachineRuntime
from wflite.registry.db_registry import StateMachineRegistry

logger = logging.getLogger(__name__)

def initialize_runtime():
    """Initialize the state machine runtime and registry"""
    registry = StateMachineRegistry()
    runtime = StateMachineRuntime(registry_provider=registry)
    return runtime, registry

def assign_workflow(payload, context=None):
    """
    Assign a workflow to a customer
    
    Expected event format:
    {
        "customer_id": "CUST-001",
        "template_name": "OrderProcess"
    }
    """
    try:
        # Parse input
        customer_id = payload.get('customer_id')
        template_name = payload.get('template_name')
        
        if not customer_id or not template_name:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing customer_id or template_name'})
            }
        
        # Initialize runtime
        runtime, registry = initialize_runtime()
        
        # Get the template
        template_data = registry.load(template_name)
        if not template_data:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': f'Template {template_name} not found'})
            }
        
        # Assign workflow
        success = runtime.assign_customer_workflow(customer_id, template_name, template_data)
        
        if success:
            return {
                'statusCode': 200,
                'body': json.dumps({'message': f'Workflow {template_name} assigned to {customer_id}'})
            }
        else:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': 'Failed to assign workflow'})
            }
    
    except Exception as e:
        logger.exception("Error assigning workflow")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def trigger_event(payload, context=None):
    """
    Trigger an event for a customer's workflow
    
    Expected event format:
    {
        "customer_id": "CUST-001",
        "event_name": "order_placed",
        "event_details": {
            "order_id": "ORD-123",
            "product": "Widget"
        }
    }
    """
    try:
        # Parse input
        customer_id = payload.get('customer_id')
        event_name = payload.get('event_name')
        event_details = payload.get('event_details', {})
        
        if not customer_id or not event_name:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing customer_id or event_name'})
            }
        
        # Initialize runtime
        runtime, registry = initialize_runtime()
        
        # Send event
        success = runtime.send_event(customer_id, event_name, event_details)
        
        if success:
            return {
                'statusCode': 200,
                'body': json.dumps({'message': f'Event {event_name} triggered for {customer_id}'})
            }
        else:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': 'Failed to trigger event'})
            }
    
    except Exception as e:
        logger.exception("Error triggering event")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def get_customer_state(payload, context=None):
    """
    Get current state for a customer's workflow
    
    Expected event format:
    {
        "customer_id": "CUST-001"
    }
    """
    try:
        # Parse input
        customer_id = payload.get('customer_id')
        
        if not customer_id:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing customer_id'})
            }
        
        # Initialize runtime
        runtime, registry = initialize_runtime()
        
        # Get customer workflow
        template_name, instance_id = runtime.get_customer_instance(customer_id)
        
        if not template_name or not instance_id:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': f'No workflow found for customer {customer_id}'})
            }
        
        # Get template data
        template_data = registry.load(template_name)
        
        # Get current state and context
        current_state = runtime.get_current_state(instance_id, template_data)
        context = runtime.get_context(instance_id)
        available_events = runtime.get_available_events(instance_id, template_data)
        is_end_state = runtime.is_end_state(instance_id, template_data)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'customer_id': customer_id,
                'template_name': template_name,
                'instance_id': instance_id,
                'current_state': current_state,
                'context': context,
                'available_events': available_events,
                'is_end_state': is_end_state
            })
        }
    
    except Exception as e:
        logger.exception("Error getting customer state")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def get_customers_context(payload, context=None):
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
        runtime, registry = initialize_runtime()
        
        # Get context data for all customers
        context_data = runtime.get_customers_context(customer_ids)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'contexts': context_data
            })
        }
    
    except Exception as e:
        logger.exception("Error getting customers context")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

# Add more serverless functions as needed

import os
import sys
import logging

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional, List

from wflite.registry.db_registry import StateMachineRegistry
from wflite.runtime.statemachine_runtime import StateMachineRuntime
from wflite.config.config_loader import ConfigLoader
from wflite.persistence.provider_factory import PersistenceProviderFactory
from wflite.runtime.serverless import trigger_events

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Define a factory function to create the app
def create_app():
    # Load configuration
    config_loader = ConfigLoader()
    config = getattr(config_loader, '_config', {})
    
    # Create persistence provider based on configuration
    persistence_provider = PersistenceProviderFactory.create_provider(config)
    
    # Log the selected provider
    provider_type = config.get('persistence', {}).get('provider', 'sqlite')
    logger.info(f"Using persistence provider: {provider_type}")
    
    # Create FastAPI app
    app = FastAPI(title="Workflow API")
    
    # Create registry and runtime instances
    registry = StateMachineRegistry()
    
    # Create runtime with the configured persistence provider
    runtime = StateMachineRuntime(
        persistence_provider=persistence_provider,
        registry_provider=registry
    )
    
    # Log successful initialization
    logger.info(f"Workflow API initialized with {provider_type} persistence provider")

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

    class CustomerEventRequest(BaseModel):
        customer_id: str
        event_name: str
        event_details: Optional[Dict[str, Any]] = None

    class TemplateCreateRequest(BaseModel):
        name: str
        template_data: Dict[str, Any]

    class TemplateUpdateRequest(BaseModel):
        template_data: Dict[str, Any]

    class BatchCustomerWorkflowRequest(BaseModel):
        customer_ids: List[str]
        template_name: str
    
    # Define API endpoints
    @app.get("/workflow/customer/{customer_id}")
    async def get_customer_workflow(customer_id: str):
        """Get the current workflow assignment for a customer."""
        try:
            template_name, instance_id = runtime.get_customer_instance(customer_id)
            if not template_name:
                raise HTTPException(status_code=404, detail=f"No workflow assigned to customer {customer_id}")
            
            template_data = registry.load(template_name)
            current_state = runtime.get_current_state(instance_id, template_data)
            context = runtime.get_context(instance_id)
            
            return {
                "customer_id": customer_id,
                "template_name": template_name,
                "instance_id": instance_id,
                "current_state": current_state["id"],
                "state_name": current_state["name"],
                "context": context
            }
            
        except Exception as e:
            logger.error(f"Error getting customer workflow: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.post("/workflow/customer/assign")
    async def assign_customer_workflow(request: CustomerWorkflowRequest):
        """
        Assign a workflow template to a customer.

        Example:
        curl -X POST http://localhost:8000/workflow/customer/assign \
        -H "Content-Type: application/json" \
        -d '{
            "customer_id": "CUST-001",
            "template_name": "Simple"
        }'

        """
        logger.info(f"Attempting to assign workflow {request.template_name} to customer {request.customer_id}")
        
        try:
            # Validate template exists
            template_data = registry.load(request.template_name)
            if not template_data:
                raise HTTPException(status_code=404, detail=f"Template {request.template_name} not found")

            # Assign workflow to customer
            result = runtime.assign_customer_workflow(
                customer_id=request.customer_id,
                template_name=request.template_name,
                template_data=template_data
            )
            
            if not result:
                raise HTTPException(status_code=500, detail="Failed to assign workflow")
            
            # Get instance details
            template_name, instance_id = runtime.get_customer_instance(request.customer_id)
            if not instance_id:
                raise HTTPException(status_code=500, detail="Failed to create workflow instance")
                
            # Get current state
            current_state = runtime.get_current_state(instance_id, template_data)
            
            return {
                "customer_id": request.customer_id,
                "template_name": template_name,
                "instance_id": instance_id,
                "current_state": current_state["id"],
                "state_name": current_state["name"]
            }
            
        except HTTPException:
            raise
            
        except Exception as e:
            logger.error(f"Error assigning workflow: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
        
    @app.post("/workflow/event")
    async def trigger_event(request: EventRequest):
        """Trigger an event for a customer's workflow instance."""
        try:
            logger.info(f"Processing event '{request.event_name}' for customer {request.customer_id}")
            
            # Get customer's workflow instance
            template_name, instance_id = runtime.get_customer_instance(request.customer_id)
            
            if not template_name or not instance_id:
                raise HTTPException(status_code=404, detail=f"No workflow assigned to customer {request.customer_id}")
            
            # Get template data
            template_data = registry.load(template_name)
            if not template_data:
                raise HTTPException(status_code=500, detail=f"Template {template_name} not found")
                
            # Process the event
            success, actions = runtime.trigger_event(
                instance_id=instance_id,
                event_name=request.event_name,
                template_data=template_data,
                event_details=request.event_details
            )
            
            if not success:
                raise HTTPException(status_code=400, detail=f"Event '{request.event_name}' could not be processed")
            
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
            
        except HTTPException:
            raise
            
        except Exception as e:
            logger.error(f"Error processing event: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/workflow/events")
    async def batch_trigger_events(request: EventsRequest):
        """
        Trigger multiple events in batch for customers' workflow instances.
        
        Example:
        curl -X POST http://localhost:8000/workflow/events \
        -H "Content-Type: application/json" \
        -d '{
            "events": [
                {
                    "customer_id": "CUST-001",
                    "event_name": "submit",
                    "event_details": {"data": "value1"}
                },
                {
                    "customer_id": "CUST-002",
                    "event_name": "approve",
                    "event_details": {"data": "value2"}
                }
            ]
        }'
        """
        try:
            logger.info(f"Processing batch of {len(request.events)} events")
            
            # Use the trigger_events function to process the batch
            results = trigger_events(request.events)
            
            return {
                "success": True,
                "results": results
            }
            
        except Exception as e:
            logger.error(f"Error processing batch events: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/workflow/state/{customer_id}")
    async def get_state(customer_id: str):
        """
        Get the current state of a customer's workflow instance.

        Example:
        curl http://localhost:8000/workflow/state/CUST-001
        """
        try:
            # Get customer's workflow instance
            template_name, instance_id = runtime.get_customer_instance(customer_id)
            
            if not template_name or not instance_id:
                raise HTTPException(status_code=404, detail=f"No workflow assigned to customer {customer_id}")
            
            # Get template data
            template_data = registry.load(template_name)
            if not template_data:
                raise HTTPException(status_code=500, detail=f"Template {template_name} not found")
                
            # Get current state and context
            current_state = runtime.get_current_state(instance_id, template_data)
            context = runtime.get_context(instance_id)
            is_end_state = runtime.is_end_state(instance_id, template_data)
            
            # Get available events for current state
            available_events = runtime.get_available_events(instance_id, template_data)
            
            return {
                "customer_id": customer_id,
                "instance_id": instance_id,
                "template_name": template_name,
                "current_state": current_state["id"],
                "state_name": current_state["name"],
                "context": context,
                "available_events": available_events,
                "is_end_state": is_end_state
            }
            
        except Exception as e:
            logger.error(f"Error getting state: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/templates", response_model=List[str])
    async def list_templates():
        """
        Get a list of all available workflow templates.
        
        Example:
        curl http://localhost:8000/templates
        """
        try:
            templates = registry.list()
            return templates
        except Exception as e:
            logger.error(f"Error listing templates: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/templates/{name}")
    async def get_template(name: str):
        """
        Get a specific workflow template by name.
        
        Example:
        curl http://localhost:8000/templates/Simple
        """
        try:
            template = registry.load(name)
            if not template:
                raise HTTPException(status_code=404, detail=f"Template {name} not found")
            
            return {"name": name, "template_data": template}
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error getting template: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/templates", status_code=201)
    async def create_template(template: TemplateCreateRequest):
        """
        Create a new workflow template.
        
        Example:
        curl -X POST http://localhost:8000/templates \
        -H "Content-Type: application/json" \
        -d '{
            "name": "NewTemplate",
            "template_data": {
                "states": [...],
                "transitions": [...]
            }
        }'
        """
        try:
            # Check if template already exists
            existing = registry.load(template.name)
            if existing:
                raise HTTPException(status_code=409, detail=f"Template {template.name} already exists")
            
            # Save the new template
            success = registry.save(template.name, template.template_data)
            if not success:
                raise HTTPException(status_code=500, detail="Failed to save template")
            
            return {"message": f"Template '{template.name}' created successfully"}
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error creating template: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    @app.put("/templates/{name}")
    async def update_template(name: str, template: TemplateUpdateRequest):
        """
        Update an existing workflow template.
        
        Example:
        curl -X PUT http://localhost:8000/templates/Simple \
        -H "Content-Type: application/json" \
        -d '{
            "template_data": {
                "states": [...],
                "transitions": [...]
            }
        }'
        """
        try:
            # Check if template exists
            existing = registry.load(name)
            if not existing:
                raise HTTPException(status_code=404, detail=f"Template {name} not found")
            
            # Update the template
            success = registry.save(name, template.template_data)
            if not success:
                raise HTTPException(status_code=500, detail="Failed to update template")
            
            return {"message": f"Template '{name}' updated successfully"}
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error updating template: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    @app.delete("/templates/{name}")
    async def delete_template(name: str):
        """
        Delete a workflow template.
        
        Example:
        curl -X DELETE http://localhost:8000/templates/Simple
        """
        try:
            # Check if template exists
            existing = registry.load(name)
            if not existing:
                raise HTTPException(status_code=404, detail=f"Template {name} not found")
            
            # Delete the template
            success = registry.delete(name)
            if not success:
                raise HTTPException(status_code=500, detail="Failed to delete template")
            
            return {"message": f"Template '{name}' deleted successfully"}
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error deleting template: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    @app.get("/system/info")
    async def system_info():
        """Get information about the system configuration."""
        try:
            # Create a filtered version of the configuration to avoid exposing credentials
            filtered_config = {}
            
            # Copy persistence type but exclude credentials
            if 'persistence' in config:
                filtered_config['persistence'] = {
                    'provider': config.get('persistence', {}).get('provider', 'sqlite')
                }
                
            # Only include non-sensitive workflow_db settings if needed
            if 'workflow_db' in config:
                filtered_config['workflow_db'] = {
                    'type': config.get('workflow_db', {}).get('type', 'sqlite')
                }
                # Include path for SQLite but not credentials for other DB types
                if filtered_config['workflow_db']['type'] == 'sqlite':
                    filtered_config['workflow_db']['path'] = config.get('workflow_db', {}).get('path', 'workflows.db')
            
            return {
                "name": "Workflow Lite",
                "version": "0.0.1",
                "persistence_provider": provider_type,
                "environment": os.environ.get('WFLITE_ENV', 'development'),
                "config": filtered_config
            }
        except Exception as e:
            logger.error(f"Error getting system info: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
    
    @app.post("/workflow/customers/assign")
    async def batch_assign_customer_workflow(request: BatchCustomerWorkflowRequest):
        """
        Assign a workflow template to multiple customers at once.

        Example:
        curl -X POST http://localhost:8000/workflow/customers/assign \
        -H "Content-Type: application/json" \
        -d '{
            "customer_ids": ["CUST-001", "CUST-002", "CUST-003"],
            "template_name": "Simple"
        }'
        """
        logger.info(f"Attempting to assign workflow {request.template_name} to {len(request.customer_ids)} customers")
        
        try:
            # Validate template exists
            template_data = registry.load(request.template_name)
            if not template_data:
                raise HTTPException(status_code=404, detail=f"Template {request.template_name} not found")

            results = []
            
            # Assign workflow to each customer
            for customer_id in request.customer_ids:
                try:
                    # Assign workflow to customer
                    success = runtime.assign_customer_workflow(
                        customer_id=customer_id,
                        template_name=request.template_name,
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
                    template_name, instance_id = runtime.get_customer_instance(customer_id)
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
                        "template_name": template_name,
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
            total = len(request.customer_ids)
            succeeded = sum(1 for r in results if r.get("success", False))
            failed = total - succeeded
            
            return {
                "template_name": request.template_name,
                "total_customers": total,
                "succeeded": succeeded,
                "failed": failed,
                "results": results
            }
            
        except HTTPException:
            raise
            
        except Exception as e:
            logger.error(f"Error in batch workflow assignment: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
    
    return app

# If this module is run directly, create and start the app
if __name__ == "__main__":
    import uvicorn
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8000)

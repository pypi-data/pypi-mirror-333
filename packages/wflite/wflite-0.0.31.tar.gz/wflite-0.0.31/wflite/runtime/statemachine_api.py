import os
import sys
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional, List


# Add src directory to Python path
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'wflite'))
sys.path.insert(0, src_path)

from registry.db_registry import StateMachineRegistry
from runtime.statemachine_runtime import StateMachineRuntime

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI(title="Workflow API")
runtime = StateMachineRuntime()
registry = StateMachineRegistry()

class EventRequest(BaseModel):
    customer_id: str  # Changed from instance_id
    event_name: str
    event_details: Optional[Dict[str, Any]] = None

class CustomerWorkflowRequest(BaseModel):
    customer_id: str
    template_name: str

class CustomerEventRequest(BaseModel):
    customer_id: str
    event_name: str
    event_details: Optional[Dict[str, Any]] = None

# New models for template management
class TemplateCreateRequest(BaseModel):
    name: str
    template_data: Dict[str, Any]

class TemplateUpdateRequest(BaseModel):
    template_data: Dict[str, Any]


@app.get("/workflow/customer/{customer_id}")
async def get_customer_workflow(customer_id: str):
    """
    Get the current workflow assignment for a customer.

    Example:
    curl http://localhost:8000/workflow/customer/CUST-001

    """
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
            logger.error(f"Template {request.template_name} not found")
            raise HTTPException(
                status_code=404, 
                detail=f"Template {request.template_name} not found"
            )
            
        logger.debug(f"Loaded template data: {template_data}")
        
        # Create new instance
        instance_id = runtime.create_instance(request.customer_id, request.template_name, template_data)
        logger.info(f"Created new instance {instance_id}")
                    
        # Assign to customer
        success = runtime.assign_customer_workflow(
            customer_id=request.customer_id,
            template_name=request.template_name,
            template_data=template_data
        )
        
        if not success:
            logger.error(f"Failed to assign workflow to customer {request.customer_id}")
            raise HTTPException(
                status_code=400, 
                detail="Failed to assign workflow"
            )
        
        # Get assigned instance details
        template_name, instance_id = runtime.get_customer_instance(request.customer_id)
        current_state = runtime.get_current_state(instance_id, template_data)
        
        return {
            "customer_id": request.customer_id,
            "template_name": template_name,
            "instance_id": instance_id,
            "current_state": current_state["id"] if current_state else None,
            "state_name": current_state["name"] if current_state else None
        }
        
    except Exception as e:
        logger.exception(f"Error assigning workflow: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal error: {str(e)}"
        )
    
@app.post("/workflow/event")
async def trigger_event(request: EventRequest):
    """
    Trigger an event for a customer's workflow instance.

    Example:
    curl -X POST http://localhost:8000/workflow/event \
    -H "Content-Type: application/json" \
    -d '{
        "customer_id": "CUST-001",
        "event_name": "start",
        "event_details": {"data": "example"}
    }'
    """
    try:
        logger.debug(f"Processing event for customer {request.customer_id}: {request.event_name}")
        
        # Get customer's workflow instance
        template_name, instance_id = runtime.get_customer_instance(request.customer_id)
        if not template_name or not instance_id:
            raise HTTPException(
                status_code=404, 
                detail=f"No workflow assigned to customer {request.customer_id}"
            )
        
        # Load template data
        template_data = registry.load(template_name)
        if not template_data:
            raise HTTPException(
                status_code=500, 
                detail=f"Template {template_name} not found"
            )
        
        # Trigger event
        success, actions = runtime.trigger_event(
            instance_id,
            request.event_name,
            template_data,
            request.event_details
        )
        
        if not success:
            raise HTTPException(status_code=400, detail="Event trigger failed")
        
        # Get updated state
        current_state = runtime.get_current_state(instance_id, template_data)
        context = runtime.get_context(instance_id)
        
        return {
            "success": True,
            "customer_id": request.customer_id,
            "instance_id": instance_id,
            "template_name": template_name,
            "current_state": current_state["id"] if current_state else None,
            "state_name": current_state["name"] if current_state else None,
            "context": context,
            "actions": actions
        }
        
    except Exception as e:
        logger.exception(f"Error processing event for customer {request.customer_id}: {str(e)}")
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
            raise HTTPException(
                status_code=404, 
                detail=f"No workflow assigned to customer {customer_id}"
            )
        
        # Load template data
        template_data = registry.load(template_name)
        if not template_data:
            raise HTTPException(
                status_code=500, 
                detail=f"Template {template_name} not found"
            )
        
        # Get current state and context
        current_state = runtime.get_current_state(instance_id, template_data)
        if not current_state:
            raise HTTPException(
                status_code=404, 
                detail=f"State not found for instance {instance_id}"
            )
        
        context = runtime.get_context(instance_id)
        available_events = runtime.get_available_events(instance_id, template_data)
        
        return {
            "customer_id": customer_id,
            "instance_id": instance_id,
            "template_name": template_name,
            "current_state": current_state["id"],
            "state_name": current_state["name"],
            "context": context,
            "available_events": available_events,
            "is_end_state": runtime.is_end_state(instance_id, template_data)
        }
        
    except Exception as e:
        logger.exception(f"Error getting state for customer {customer_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# New endpoints for template management

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
        logger.exception(f"Error listing templates: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/templates/{name}")
async def get_template(name: str):
    """
    Get a specific workflow template by name.
    
    Example:
    curl http://localhost:8000/templates/Simple
    """
    try:
        template_data = registry.load(name)
        if not template_data:
            raise HTTPException(status_code=404, detail=f"Template '{name}' not found")
        
        return {
            "name": name,
            "template_data": template_data
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error getting template {name}: {str(e)}")
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
            raise HTTPException(status_code=409, detail=f"Template '{template.name}' already exists")
        
        # Save new template
        success = registry.save(template.name, template.template_data)
        if not success:
            raise HTTPException(status_code=400, detail="Failed to save template")
        
        return {"message": f"Template '{template.name}' created successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error creating template {template.name}: {str(e)}")
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
            raise HTTPException(status_code=404, detail=f"Template '{name}' not found")
        
        # Update template
        success = registry.save(name, template.template_data)
        if not success:
            raise HTTPException(status_code=400, detail="Failed to update template")
        
        return {"message": f"Template '{name}' updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error updating template {name}: {str(e)}")
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
            raise HTTPException(status_code=404, detail=f"Template '{name}' not found")
        
        # Delete template
        success = registry.delete(name)
        if not success:
            raise HTTPException(status_code=400, detail="Failed to delete template")
        
        return {"message": f"Template '{name}' deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error deleting template {name}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

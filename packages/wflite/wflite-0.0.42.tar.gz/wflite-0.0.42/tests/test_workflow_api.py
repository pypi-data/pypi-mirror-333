import pytest
from fastapi.testclient import TestClient

def test_assign_workflow(client: TestClient, test_cleanup):
    """Test workflow assignment"""
    response = client.post("/workflow/customer/assign", 
        json={"customer_id": "CUST-001", "template_name": "Simple"})
    
    assert response.status_code == 200
    data = response.json()
    assert data["customer_id"] == "CUST-001"
    assert data["template_name"] == "Simple"
    assert "instance_id" in data
    
    # Register for cleanup
    test_cleanup.register_instance(data["instance_id"])

@pytest.fixture(autouse=True)
def setup_cleanup(test_cleanup, simulator):
    """Auto-setup cleanup for all tests"""
    test_cleanup.set_repository(simulator.state_repository)
    return test_cleanup

# Update other test functions to register instances
def test_trigger_event(client: TestClient, test_cleanup):
    # First create an instance
    assign_response = client.post("/workflow/customer/assign", 
        json={"customer_id": "CUST-002", "template_name": "Simple"})
    instance_id = assign_response.json()["instance_id"]
    test_cleanup.register_instance(instance_id)
    
    # Now test the event
    response = client.post(f"/workflow/customer/{instance_id}/event",
        json={"event_name": "start"})
    assert response.status_code == 200
    # ...rest of test...

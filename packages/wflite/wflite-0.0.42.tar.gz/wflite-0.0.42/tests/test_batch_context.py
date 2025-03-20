clearimport unittest
import sys
import os
import json

# Add project root to Python path
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, src_path)

from wflite.runtime.statemachine_runtime import StateMachineRuntime
from wflite.registry.db_registry import StateMachineRegistry
from wflite.serverless import get_customers_context


class TestBatchContextFunctionality(unittest.TestCase):
    """Test the batch context retrieval functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.runtime = StateMachineRuntime()
        self.registry = StateMachineRegistry()
        
        # Sample template data
        self.template_data = {
            "name": "batch_test_workflow",
            "states": [
                {"id": "1", "name": "Start", "type": "start"},
                {"id": "2", "name": "Processing", "type": "normal"},
                {"id": "3", "name": "End", "type": "end"}
            ],
            "transitions": [
                {"source": "1", "target": "2", "event": "begin"},
                {"source": "2", "target": "3", "event": "finish"}
            ]
        }
        
        # Save test template
        self.registry.save("batch_test_template", self.template_data)
        
        # Create test customers with different contexts
        self.test_customers = [
            "BATCH-CUST-001",
            "BATCH-CUST-002",
            "BATCH-CUST-003",
            "BATCH-CUST-004",
        ]
        
        # Assign workflows to customers
        for i, customer_id in enumerate(self.test_customers):
            # Assign workflow
            self.runtime.assign_customer_workflow(
                customer_id, "batch_test_template", self.template_data
            )
            
            # Get instance ID
            _, instance_id = self.runtime.get_customer_instance(customer_id)
            
            # Add unique context data for each customer
            context = {
                "customer_number": i,
                "customer_id": customer_id,
                "test_value": f"value-{i}",
                "is_active": i % 2 == 0,  # Even customers are active
                "details": {
                    "priority": i,
                    "tags": [f"tag{j}" for j in range(i)]
                }
            }
            
            # Update instance context
            self.runtime.update_context(instance_id, context)

    def test_runtime_get_customers_context(self):
        """Test StateMachineRuntime.get_customers_context method"""
        # Get contexts for all test customers
        contexts = self.runtime.get_customers_context(self.test_customers)
        
        # Verify all customers are included
        self.assertEqual(len(contexts), len(self.test_customers))
        
        # Check each customer context
        for i, customer_id in enumerate(self.test_customers):
            self.assertIn(customer_id, contexts)
            context = contexts[customer_id]
            
            # Check specific fields
            self.assertEqual(context["customer_number"], i)
            self.assertEqual(context["customer_id"], customer_id)
            self.assertEqual(context["test_value"], f"value-{i}")
            self.assertEqual(context["is_active"], i % 2 == 0)
            self.assertEqual(context["details"]["priority"], i)
            
    def test_runtime_get_customers_context_subset(self):
        """Test retrieving contexts for a subset of customers"""
        # Get contexts for the first two customers
        subset = self.test_customers[:2]
        contexts = self.runtime.get_customers_context(subset)
        
        # Verify only requested customers are included
        self.assertEqual(len(contexts), 2)
        for customer_id in subset:
            self.assertIn(customer_id, contexts)
            
        # Customers not in subset should not be included
        for customer_id in self.test_customers[2:]:
            self.assertNotIn(customer_id, contexts)
            
    def test_runtime_get_customers_context_nonexistent(self):
        """Test retrieving contexts with some non-existent customers"""
        # Include a non-existent customer ID
        test_ids = self.test_customers + ["NONEXISTENT-CUSTOMER"]
        contexts = self.runtime.get_customers_context(test_ids)
        
        # Should have entry for non-existent customer, but value should be None
        self.assertIn("NONEXISTENT-CUSTOMER", contexts)
        self.assertIsNone(contexts["NONEXISTENT-CUSTOMER"])
        
    def test_serverless_get_customers_context(self):
        """Test the serverless get_customers_context function"""
        # Create event payload
        event = {
            "customer_ids": self.test_customers
        }
        
        # Call serverless function
        response = get_customers_context(event)
        
        # Check response
        self.assertEqual(response["statusCode"], 200)
        
        # Parse response body
        body = json.loads(response["body"])
        self.assertIn("contexts", body)
        
        contexts = body["contexts"]
        self.assertEqual(len(contexts), len(self.test_customers))
        
        # Verify contexts for each customer
        for i, customer_id in enumerate(self.test_customers):
            self.assertIn(customer_id, contexts)
            context = contexts[customer_id]
            
            # Check specific fields
            self.assertEqual(context["customer_number"], i)
            self.assertEqual(context["customer_id"], customer_id)
            
    def test_serverless_get_customers_context_invalid_input(self):
        """Test the serverless function with invalid input"""
        # Test with missing customer_ids
        response = get_customers_context({})
        self.assertEqual(response["statusCode"], 400)
        
        # Test with non-list customer_ids
        response = get_customers_context({"customer_ids": "BATCH-CUST-001"})
        self.assertEqual(response["statusCode"], 400)
        
        # Test with empty list
        response = get_customers_context({"customer_ids": []})
        self.assertEqual(response["statusCode"], 400)

    def tearDown(self):
        """Clean up after tests"""
        # Remove test template
        self.registry.delete("batch_test_template")
        
        # Close database connections to avoid ResourceWarnings
        if hasattr(self.runtime, 'persistence') and hasattr(self.runtime.persistence, 'close'):
            self.runtime.persistence.close()
            
        if hasattr(self.registry, 'persistence') and hasattr(self.registry.persistence, 'close'):
            self.registry.persistence.close()


if __name__ == "__main__":
    unittest.main()

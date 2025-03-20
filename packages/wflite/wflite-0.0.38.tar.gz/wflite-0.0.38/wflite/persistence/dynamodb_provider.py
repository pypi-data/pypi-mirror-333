import boto3
import json
import time
import uuid
from typing import Dict, Any, List, Optional, Tuple
import logging
from decimal import Decimal
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

class DecimalEncoder(json.JSONEncoder):
    """Helper class to convert Decimal values from DynamoDB to JSON-serializable format"""
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

class DynamoDBPersistenceProvider:
    """DynamoDB implementation of persistence for state machines"""
    
    def __init__(self, region_name='us-east-1', endpoint_url=None, 
                 templates_table='workflow_templates',
                 instances_table='workflow_instances',
                 customers_table='workflow_assignments'):
        """
        Initialize the DynamoDB persistence provider.
        
        Args:
            region_name: AWS region name
            endpoint_url: Optional endpoint URL for localstack or custom endpoints
            tables_prefix: Optional prefix for all table names
        """
        self.dynamodb = boto3.resource('dynamodb', region_name=region_name, endpoint_url=endpoint_url)
        self.templates_table_name = templates_table
        self.instances_table_name = instances_table 
        self.customers_table_name = customers_table
        
        # Initialize tables
        self.templates_table = self.dynamodb.Table(self.templates_table_name)
        self.instances_table = self.dynamodb.Table(self.instances_table_name)
        self.customers_table = self.dynamodb.Table(self.customers_table_name)
    
    @staticmethod
    def create_tables(region_name='us-east-1', endpoint_url=None,
                     templates_table='workflow_templates',
                     instances_table='workflow_instances',
                     customers_table='workflow_assignments'):
        """
        Create DynamoDB tables required by the persistence provider.
        
        Returns:
            True if tables created successfully, False otherwise
        """
        dynamodb = boto3.resource('dynamodb', region_name=region_name, endpoint_url=endpoint_url)
        
        try:
            # Templates table
            dynamodb.create_table(
                TableName=templates_table,
                KeySchema=[
                    {'AttributeName': 'name', 'KeyType': 'HASH'}  # Partition key
                ],
                AttributeDefinitions=[
                    {'AttributeName': 'name', 'AttributeType': 'S'}
                ],
                ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
            )
            
            # Instances table
            dynamodb.create_table(
                TableName=instances_table,
                KeySchema=[
                    {'AttributeName': 'instance_id', 'KeyType': 'HASH'}  # Partition key
                ],
                AttributeDefinitions=[
                    {'AttributeName': 'instance_id', 'AttributeType': 'S'},
                    {'AttributeName': 'template_name', 'AttributeType': 'S'}
                ],
                GlobalSecondaryIndexes=[
                    {
                        'IndexName': 'template_name-index',
                        'KeySchema': [
                            {'AttributeName': 'template_name', 'KeyType': 'HASH'}
                        ],
                        'Projection': {'ProjectionType': 'ALL'},
                        'ProvisionedThroughput': {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
                    }
                ],
                ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
            )
            
            # Customer workflows table
            dynamodb.create_table(
                TableName=customers_table,
                KeySchema=[
                    {'AttributeName': 'customer_id', 'KeyType': 'HASH'}  # Partition key
                ],
                AttributeDefinitions=[
                    {'AttributeName': 'customer_id', 'AttributeType': 'S'}
                ],
                ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
            )
            
            logger.info("Waiting for tables to be created...")
            
            # Wait for tables to be created
            templates_table = dynamodb.Table(templates_table)
            templates_table.meta.client.get_waiter('table_exists').wait(TableName=templates_table)
            
            instances_table = dynamodb.Table(instances_table)
            instances_table.meta.client.get_waiter('table_exists').wait(TableName=instances_table)
            
            customers_table = dynamodb.Table(customers_table)
            customers_table.meta.client.get_waiter('table_exists').wait(TableName=customers_table)
            
            logger.info("All tables created successfully")
            return True
            
        except ClientError as e:
            logger.error(f"Error creating DynamoDB tables: {e}")
            return False
    
    # Template Methods
    
    def save_template(self, name: str, template_data: Dict[str, Any], description: str = None) -> bool:
        """Save a template to DynamoDB"""
        try:
            item = {
                'name': name,
                'description': description or '',
                'data': json.dumps(template_data),
                'created_at': int(time.time()),
                'updated_at': int(time.time())
            }
            
            self.templates_table.put_item(Item=item)
            logger.info(f"Saved template '{name}' successfully")
            return True
        except Exception as e:
            logger.error(f"Error saving template '{name}': {e}")
            return False
    
    def load_template(self, name: str) -> Optional[Dict[str, Any]]:
        """Load a template from DynamoDB"""
        try:
            response = self.templates_table.get_item(Key={'name': name})
            
            if 'Item' not in response:
                return None
                
            item = response['Item']
            template_data = json.loads(item['data'])
            return template_data
            
        except Exception as e:
            logger.error(f"Error loading template '{name}': {e}")
            return None
    
    def delete_template(self, name: str) -> bool:
        """Delete a template from DynamoDB"""
        try:
            self.templates_table.delete_item(Key={'name': name})
            logger.info(f"Deleted template '{name}' successfully")
            return True
        except Exception as e:
            logger.error(f"Error deleting template '{name}': {e}")
            return False
    
    def list_templates(self) -> List[str]:
        """List all template names from DynamoDB"""
        try:
            response = self.templates_table.scan(ProjectionExpression='#n', ExpressionAttributeNames={'#n': 'name'})
            items = response.get('Items', [])
            
            # Handle pagination if needed
            while 'LastEvaluatedKey' in response:
                response = self.templates_table.scan(
                    ProjectionExpression='#n', 
                    ExpressionAttributeNames={'#n': 'name'},
                    ExclusiveStartKey=response['LastEvaluatedKey']
                )
                items.extend(response.get('Items', []))
            
            return [item['name'] for item in items]
        except Exception as e:
            logger.error(f"Error listing templates: {e}")
            return []
    
    # Instance Methods
    
    def create_instance(self, instance_id: str, template_name: str, current_state: str, context: Dict[str, Any] = None) -> bool:
        """Create a new state machine instance in DynamoDB"""
        try:
            item = {
                'instance_id': instance_id,
                'template_name': template_name,
                'current_state': current_state,
                'context': json.dumps(context or {}),
                'created_at': int(time.time()),
                'updated_at': int(time.time())
            }
            
            self.instances_table.put_item(Item=item)
            logger.info(f"Created instance '{instance_id}' successfully")
            return True
        except Exception as e:
            logger.error(f"Error creating instance '{instance_id}': {e}")
            return False
    
    def update_instance(self, instance_id: str, current_state: str, context: Dict[str, Any]) -> bool:
        """Update an existing state machine instance in DynamoDB"""
        try:
            response = self.instances_table.update_item(
                Key={'instance_id': instance_id},
                UpdateExpression="SET current_state = :state, #ctx = :context, updated_at = :updated",
                ExpressionAttributeNames={'#ctx': 'context'},
                ExpressionAttributeValues={
                    ':state': current_state,
                    ':context': json.dumps(context),
                    ':updated': int(time.time())
                },
                ReturnValues="UPDATED_NEW"
            )
            logger.info(f"Updated instance '{instance_id}' successfully")
            return True
        except Exception as e:
            logger.error(f"Error updating instance '{instance_id}': {e}")
            return False
    
    def get_instance(self, instance_id: str) -> Optional[Dict[str, Any]]:
        """Get a state machine instance from DynamoDB"""
        try:
            response = self.instances_table.get_item(Key={'instance_id': instance_id})
            
            if 'Item' not in response:
                return None
                
            item = response['Item']
            
            # Parse context from JSON
            context = json.loads(item['context']) if item.get('context') else {}
            
            return {
                'instance_id': item['instance_id'],
                'template_name': item['template_name'],
                'current_state': item['current_state'],
                'context': context,
                'created_at': item.get('created_at'),
                'updated_at': item.get('updated_at')
            }
            
        except Exception as e:
            logger.error(f"Error getting instance '{instance_id}': {e}")
            return None
    
    def delete_instance(self, instance_id: str) -> bool:
        """Delete a state machine instance from DynamoDB"""
        try:
            self.instances_table.delete_item(Key={'instance_id': instance_id})
            logger.info(f"Deleted instance '{instance_id}' successfully")
            return True
        except Exception as e:
            logger.error(f"Error deleting instance '{instance_id}': {e}")
            return False
    
    # Customer Methods
    
    def assign_customer_workflow(self, customer_id: str, template_name: str, instance_id: str) -> bool:
        """Assign a workflow template instance to a customer in DynamoDB"""
        try:
            item = {
                'customer_id': customer_id,
                'template_name': template_name,
                'instance_id': instance_id,
                'created_at': int(time.time()),
                'updated_at': int(time.time())
            }
            
            self.customers_table.put_item(Item=item)
            logger.info(f"Assigned workflow '{template_name}' to customer '{customer_id}'")
            return True
        except Exception as e:
            logger.error(f"Error assigning workflow to customer '{customer_id}': {e}")
            return False
    
    def get_customer_workflow(self, customer_id: str) -> Tuple[Optional[str], Optional[str]]:
        """Get the current workflow assignment for a customer from DynamoDB"""
        try:
            response = self.customers_table.get_item(Key={'customer_id': customer_id})
            
            if 'Item' not in response:
                return (None, None)
                
            item = response['Item']
            return (item['template_name'], item['instance_id'])
            
        except Exception as e:
            logger.error(f"Error getting workflow for customer '{customer_id}': {e}")
            return (None, None)

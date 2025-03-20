#!/usr/bin/env python
"""
Command-line interface for Workflow Lite
"""
import sys
import os
import argparse
import json
import logging
from typing import Dict, Any, Optional, List

from wflite.runtime.serverless import trigger_event

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Try to import dotenv for environment variables - LOAD BEFORE OTHER IMPORTS
try:
    from dotenv import load_dotenv
    # Look for .env file in project root
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    env_file = os.path.join(project_root, '.env')
    if os.path.exists(env_file):
        print(f"Loading environment from {env_file}")
        load_dotenv(env_file, override=True)
        print(f"PERSISTENCE_PROVIDER: {os.environ.get('PERSISTENCE_PROVIDER', 'not set')}")
    else:
        print("No .env file found")
except ImportError:
    pass  # dotenv not installed, will use existing environment variables

from wflite.app.workflow_api_client import WorkflowAPI
from wflite.config.config_loader import ConfigLoader

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Workflow Lite CLI")
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Event command
    event_parser = subparsers.add_parser("event", help="Trigger a workflow event")
    event_parser.add_argument("--customer-id", "-c", default="CUST-001", 
                             help="Customer ID (default: CUST-001)")
    event_parser.add_argument("--event-name", "-e", default="submit", 
                             help="Event name (default: submit)")
    event_parser.add_argument("--data", "-d", type=str, default=None,
                             help="Event data as JSON string or path to JSON file")
    event_parser.add_argument("--api-url", default=os.environ.get("WFLITE_API_URL", "http://localhost:8000"),
                             help="API URL (default: from WFLITE_API_URL or http://localhost:8000)")
    
    # State command
    state_parser = subparsers.add_parser("state", help="Get workflow state for a customer")
    state_parser.add_argument("--customer-id", "-c", default="CUST-001", 
                             help="Customer ID (default: CUST-001)")
    state_parser.add_argument("--api-url", default=os.environ.get("WFLITE_API_URL", "http://localhost:8000"),
                             help="API URL (default: from WFLITE_API_URL or http://localhost:8000)")
    
    # Assign command
    assign_parser = subparsers.add_parser("assign", help="Assign a workflow template to a customer")
    assign_parser.add_argument("--customer-id", "-c", default="CUST-001", 
                             help="Customer ID (default: CUST-001)")
    assign_parser.add_argument("--template", "-t", default="Simple",
                              help="Template name (default: Simple)")
    assign_parser.add_argument("--api-url", default=os.environ.get("WFLITE_API_URL", "http://localhost:8000"),
                             help="API URL (default: from WFLITE_API_URL or http://localhost:8000)")
    
    # List templates command
    templates_parser = subparsers.add_parser("templates", help="List available workflow templates")
    templates_parser.add_argument("--api-url", default=os.environ.get("WFLITE_API_URL", "http://localhost:8000"),
                                 help="API URL (default: from WFLITE_API_URL or http://localhost:8000)")

    return parser.parse_args()


def parse_json_data(data_arg: Optional[str]) -> Optional[Dict[str, Any]]:
    """
    Parse the JSON data from string or file path
    
    Args:
        data_arg: JSON string or file path
        
    Returns:
        Parsed JSON data as dictionary
    """
    if not data_arg:
        return {}
    
    try:
        # First try to parse as a JSON string
        return json.loads(data_arg)
    except json.JSONDecodeError:
        # If that fails, try to read from file
        if os.path.isfile(data_arg):
            try:
                with open(data_arg, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load JSON from file {data_arg}: {e}")
                return {}
        else:
            logger.error(f"Invalid JSON and not a file path: {data_arg}")
            return {}


def main():
    """Main CLI entry point"""
    args = parse_arguments()
    
    if not args.command:
        # If no command is specified, show help
        parse_arguments()
        return 1
    
    try:
        # Initialize the workflow API client
        workflow = None
        
        if args.command == "event":
            # Parse the event data
            event_data = parse_json_data(args.data)
            
            logger.info(f"Triggering event '{args.event_name}' for customer '{args.customer_id}'")
            logger.debug(f"Event data: {json.dumps(event_data)}")
            result = trigger_event({
                "customer_id": args.customer_id,
                "event_name": args.event_name,
                "event_details": event_data
            })
            
            if result:
                print(json.dumps(result, indent=2))
                return 0
            else:
                logger.error("Failed to trigger event")
                return 1
        
        elif args.command == "state":
            logger.info(f"Getting state for customer '{args.customer_id}'")
            state_info = workflow.get_state(args.customer_id)
            if state_info:
                print(json.dumps(state_info, indent=2))
                return 0
            else:
                logger.error("Failed to get state")
                return 1
        
        elif args.command == "assign":
            logger.info(f"Assigning template '{args.template}' to customer '{args.customer_id}'")
            result = workflow.assign_workflow(
                customer_id=args.customer_id,
                template_name=args.template
            )
            if result:
                # Get the state after assignment
                state_info = workflow.get_state(args.customer_id)
                print(json.dumps(state_info, indent=2))
                return 0
            else:
                logger.error("Failed to assign workflow")
                return 1
        
        elif args.command == "templates":
            logger.info("Listing available templates")
            templates = workflow.list_templates()
            if templates:
                print("Available templates:")
                for template in templates:
                    print(f"  - {template}")
                return 0
            else:
                logger.error("Failed to list templates or no templates available")
                return 1
        
        else:
            logger.error(f"Unknown command: {args.command}")
            return 1
    
    except Exception as e:
        logger.exception(f"Error executing command: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

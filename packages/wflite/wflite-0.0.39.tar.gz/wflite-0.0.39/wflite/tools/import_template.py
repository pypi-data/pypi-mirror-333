import json
import argparse

from wflite.registry.db_registry import StateMachineRegistry

class TemplateImporter:
    def __init__(self):
        self.registry = StateMachineRegistry()

    def import_from_file(self, json_file_path, template_name=None):
        """Import a state machine template from a JSON file."""
        try:
            with open(json_file_path, 'r') as f:
                template_data = json.load(f)

            # Use filename without extension as template name if not provided
            if not template_name:
                template_name = json_file_path.split('/')[-1].split('.')[0]

            # Save or update template in database
            self.registry.save(template_name, template_data)
            return True
        except Exception as e:
            print(f"Error importing template: {str(e)}")
            return False

def main():
    parser = argparse.ArgumentParser(description='Import state machine template from JSON file')
    parser.add_argument('json_file', help='Path to JSON file containing state machine template')
    parser.add_argument('--name', help='Name for the template (optional)', default=None)
    
    args = parser.parse_args()
    
    importer = TemplateImporter()
    success = importer.import_from_file(args.json_file, args.name)
    
    if success:
        print(f"Template successfully imported")
    else:
        print(f"Failed to import template")
        exit(1)

if __name__ == '__main__':
    main()

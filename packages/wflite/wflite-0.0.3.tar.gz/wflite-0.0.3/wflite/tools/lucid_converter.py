import csv
import json
import re

class LucidConverter:
    def parse_transition(self, text):
        """Parse transition text into event, action, and guard components."""
        if not text:
            return {}
        
        # Pattern: event/action [guard]
        pattern = r'([^/\[]*)?(?:/([^\[]+))?(?:\[([^\]]+)\])?'
        match = re.match(pattern, text)
        
        if not match:
            return {}
            
        return {
            'event': match.group(1).strip() if match.group(1) else None,
            'action': match.group(2).strip() if match.group(2) else None,
            'guard': match.group(3).strip() if match.group(3) else None
        }

    def parse_actions(self, text):
        """Parse state actions into entry and exit actions."""
        if not text:
            return [], []
            
        entry_actions = []
        exit_actions = []
        
        for line in text.split('\n'):
            line = line.strip()
            if line.startswith('entry/'):
                entry_actions.append(line[6:].strip())
            elif line.startswith('exit/'):
                exit_actions.append(line[5:].strip())
                
        return entry_actions, exit_actions

    def parse_csv(self, file_path):
        """Parse the Lucid CSV file and return a state machine representation."""
        states = []
        transitions = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                if row['Shape Library'] == 'UML':
                    if row['Name'] == 'Start':
                        states.append({
                            'id': row['Id'],
                            'name': 'start',
                            'type': 'start'
                        })
                    elif row['Name'] == 'End':
                        states.append({
                            'id': row['Id'],
                            'name': 'end',
                            'type': 'end'
                        })
                    elif row['Name'] == 'State Name':
                        entry_actions, exit_actions = self.parse_actions(row['Text Area 2'])
                        state = {
                            'id': row['Id'],
                            'name': row['Text Area 1'],
                            'type': 'state'
                        }
                        if entry_actions:
                            state['entryActions'] = entry_actions
                        if exit_actions:
                            state['exitActions'] = exit_actions
                        states.append(state)
                
                elif row['Name'] == 'Line':
                    transition = {
                        'source': row['Line Source'],
                        'target': row['Line Destination']
                    }
                    transition_info = self.parse_transition(row['Text Area 1'])
                    transition.update(transition_info)
                    transitions.append(transition)
        
        return {
            'states': states,
            'transitions': transitions
        }

    def convert_to_json(self, file_path, output_path=None):
        """Convert CSV to JSON and optionally save to file."""
        state_machine = self.parse_csv(file_path)
        json_output = json.dumps(state_machine, indent=2)
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(json_output)
        
        return json_output

if __name__ == '__main__':
    converter = LucidConverter()
    # Example usage
    json_output = converter.convert_to_json('examples/Simple.csv', 'examples/Simple.json')
    print(json_output)

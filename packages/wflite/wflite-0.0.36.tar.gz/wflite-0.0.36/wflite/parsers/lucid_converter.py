import csv
from io import StringIO

class LucidConverter:
    def parse_transition(self, text):
        """Parse transition text into event, action, and guard components."""
        if not text:
            return {}
        
        # Pattern: event/action [guard]
        parts = text.split('/')
        event = parts[0].strip() if parts else None
        
        action = parts[1] if len(parts) > 1 else None
        action_guard = None
        guard = None
        
        if action and '[' in action:
            action_part = action.split('[')[0].strip()
            guard = action.split('[')[1].rstrip(']').strip()
            action = action_part if action_part else None
            
        return {
            'event': event,
            'action': action,
            'guard': guard
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
            else:
                entry_actions.append(line.strip())
                
        return entry_actions, exit_actions

    def parse(self, csv_content):
        """Parse CSV content into state machine structure."""
        reader = csv.DictReader(StringIO(csv_content))
        states = []
        transitions = []
        
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
                transition_info = self.parse_transition(row['Text Area 1'])
                transition = {
                    'source': row['Line Source'],
                    'target': row['Line Destination'],
                    **transition_info
                }
                transitions.append(transition)
        
        return {
            'states': states,
            'transitions': transitions
        }

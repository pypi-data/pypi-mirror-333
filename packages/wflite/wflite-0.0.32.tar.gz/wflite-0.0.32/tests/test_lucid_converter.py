import unittest
import json
import os
from unittest.mock import patch
from parsers.lucid_converter import LucidConverter
from config.config_loader import ConfigLoader

class TestLucidConverter(unittest.TestCase):
    def setUp(self):
        # Mock configuration
        self.config_patcher = patch.object(ConfigLoader, '_instance', None)
        self.config_patcher.start()
        
        self.converter = LucidConverter()
        self.test_dir = os.path.dirname(os.path.abspath(__file__))
        self.example_csv = os.path.join(os.path.dirname(self.test_dir), 'examples', 'Simple.csv')

    def tearDown(self):
        self.config_patcher.stop()
        
    def test_parse_transition(self):
        test_cases = [
            ("event1/action1 [guard1]", 
             {"event": "event1", "action": "action1", "guard": "guard1"}),
            ("event2/action2", 
             {"event": "event2", "action": "action2", "guard": None}),
            ("event3", 
             {"event": "event3", "action": None, "guard": None}),
            ("", 
             {}),
        ]
        
        for input_text, expected in test_cases:
            result = self.converter.parse_transition(input_text)
            self.assertEqual(result, expected)

    def test_parse_actions(self):
        test_cases = [
            ("entry/action1\nexit/action2", 
             (["action1"], ["action2"])),
            ("entry/action1\nentry/action2", 
             (["action1", "action2"], [])),
            ("exit/action1\nexit/action2", 
             ([], ["action1", "action2"])),
            ("", 
             ([], [])),
        ]
        
        for input_text, expected in test_cases:
            entry_actions, exit_actions = self.converter.parse_actions(input_text)
            self.assertEqual((entry_actions, exit_actions), expected)

    def test_parse_csv(self):
        with open(self.example_csv, 'r') as f:
            csv_content = f.read()
        result = self.converter.parse(csv_content)
        
        # Test structure
        self.assertIn('states', result)
        self.assertIn('transitions', result)
        
        # Test states
        states = result['states']
        self.assertEqual(len(states), 4)  # Start, State1, State2, End
        
        # Verify start state
        start_state = next(s for s in states if s['type'] == 'start')
        self.assertEqual(start_state['id'], '4')
        
        # Verify end state
        end_state = next(s for s in states if s['type'] == 'end')
        self.assertEqual(end_state['id'], '6')
        
        # Verify regular state
        state1 = next(s for s in states if s['name'] == 'State1')
        self.assertEqual(state1['entryActions'], ['action1_1'])
        self.assertEqual(state1['exitActions'], ['action1_2'])
        
        # Test transitions
        transitions = result['transitions']
        self.assertEqual(len(transitions), 4)  # Updated to match the CSV file
        
        # Verify transition with all attributes
        full_transition = next(t for t in transitions if t['source'] == '4')
        self.assertEqual(full_transition['event'], 'event1')
        self.assertEqual(full_transition['action'], 'action1')
        self.assertEqual(full_transition['guard'], 'guard1')

    def test_convert_to_json(self):
        # Test with output file
        temp_output = os.path.join(self.test_dir, 'temp_output.json')
        with open(self.example_csv, 'r') as f:
            csv_content = f.read()
        result = self.converter.parse(csv_content)
        
        # Write result to JSON file
        with open(temp_output, 'w') as f:
            json.dump(result, f)
        
        # Verify JSON is valid
        try:
            with open(temp_output, 'r') as f:
                parsed_json = json.load(f)
            self.assertIsInstance(parsed_json, dict)
        except json.JSONDecodeError:
            self.fail("Invalid JSON output")
            
        # Clean up
        if os.path.exists(temp_output):
            os.remove(temp_output)

if __name__ == '__main__':
    unittest.main()

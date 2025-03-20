import unittest
import os
import sys
from unittest.mock import patch, MagicMock

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from wflite.parsers.lucid_converter import LucidConverter
from wflite.config.config_loader import ConfigLoader

class TestLucidConverter(unittest.TestCase):
    def setUp(self):
        # Create a mock config with a mock _config attribute
        self.mock_config = MagicMock()
        self.mock_config._config = {
            'converters': {
                'lucid_chart': {
                    'state_name_column': 'Name',
                    'state_id_column': 'ID',
                    'transition_source_column': 'Source',
                    'transition_target_column': 'Target',
                    'transition_event_column': 'Event',
                    'transition_action_column': 'Actions',
                    'transition_guard_column': 'Guard',
                    'state_type_column': 'Type',
                }
            }
        }
        
        # Path ConfigLoader's constructor to return our mock
        self.patcher = patch('wflite.config.config_loader', return_value=self.mock_config)
        self.patcher.start()
        
        # Initialize the converter
        self.converter = LucidConverter()
        
        # Test data
        self.test_csv = """ID,Name,Source,Target,Event,Actions,Type
1,Start,,,,,start
2,Processing,1,2,begin,"log('started')",
3,End,2,3,finish,"log('finished'),notify()",end"""
        
        self.test_row = {
            'Source': '1',
            'Target': '2',
            'Event': 'begin',
            'Actions': "log('started')"
        }
        
    def tearDown(self):
        # Stop the patcher
        self.patcher.stop()

    def test_parse_csv(self):
        """Test parsing CSV data"""
        states, transitions = self.converter.parse_csv(self.test_csv)
        
        # Check states
        self.assertEqual(len(states), 3)
        self.assertEqual(states[0]['id'], '1')
        self.assertEqual(states[0]['name'], 'Start')
        self.assertEqual(states[0]['type'], 'start')
        
        # Check transitions
        self.assertEqual(len(transitions), 2)
        self.assertEqual(transitions[0]['source'], '1')
        self.assertEqual(transitions[0]['target'], '2')
        self.assertEqual(transitions[0]['event'], 'begin')

    def test_parse_transition(self):
        """Test parsing transition row"""
        transition = self.converter.parse_transition_row(self.test_row)
        
        self.assertEqual(transition['source'], '1')
        self.assertEqual(transition['target'], '2')
        self.assertEqual(transition['event'], 'begin')
        self.assertEqual(transition['actions'], ["log('started')"])

    def test_parse_actions(self):
        """Test parsing action strings"""
        actions_str = "log('test'),send_email('user@example.com'),update_status()"
        actions = self.converter.parse_actions(actions_str)
        
        self.assertEqual(len(actions), 3)
        self.assertEqual(actions[0], "log('test')")
        self.assertEqual(actions[1], "send_email('user@example.com')")
        self.assertEqual(actions[2], "update_status()")

    def test_convert_to_json(self):
        """Test converting CSV to JSON workflow"""
        template = self.converter.convert_to_json(self.test_csv, "TestWorkflow")
        
        self.assertEqual(template['name'], "TestWorkflow")
        self.assertEqual(len(template['states']), 3)
        self.assertEqual(len(template['transitions']), 2)
        
        # Check start state
        start_state = next(s for s in template['states'] if s['type'] == 'start')
        self.assertEqual(start_state['name'], 'Start')
        
        # Check end state
        end_state = next(s for s in template['states'] if s['type'] == 'end')
        self.assertEqual(end_state['name'], 'End')
        
        # Check transition actions
        begin_transition = next(t for t in template['transitions'] if t['event'] == 'begin')
        self.assertEqual(begin_transition['actions'], ["log('started')"])

if __name__ == '__main__':
    unittest.main()

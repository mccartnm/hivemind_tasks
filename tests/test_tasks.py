"""
Tests for the optional tasks featureset
"""
import os
import sys
import copy
import time
import platform
import unittest
import requests
import argparse

TEST_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(TEST_BASE_DIR))

from hivemind.core import log
from hivemind.util import global_settings
from hivemind.util.misc import temp_dir
from hivemind.util.hivecontroller import HiveController
from hivemind.util.cliparse import build_hivemind_parser

from hivemind_tasks import TaskNode

class ATaskNode(TaskNode):
    use_config = 'sampledata/tasks_a.yaml'

class BadTaskNode(TaskNode):
    use_config = 'sampledata/badtasks.yaml'

def _within_test_hive(func):
    """
    Wrapper function to build a text hive and
    run a function within it
    """
    def _hive_func(self):

        parser = build_hivemind_parser()
        with temp_dir() as hive_dir:
            string_args = ['new', 'testhive']
            args = parser.parse_args(string_args)
            args.func(args)

            # Now move into said hive
            os.chdir('testhive')

            func(self)

    return _hive_func


class TestTasks(unittest.TestCase):

    @_within_test_hive
    def test_task_initial(self):
        """
        Test we can handle a basic task execute
        """
        parser = build_hivemind_parser()
        additional_args = [
            'create_node',
            'FooBarTask',
            '-c',
            'hivemind_tasks.TaskNode'
        ]
        args = parser.parse_args(additional_args)
        args.func(args)


        hive_controller = HiveController(
            os.getcwd(),
            nodes=[ATaskNode],
            augment_settings={
                'hive_features' : [
                    # Need to turn the feature on
                    'hivemind_tasks'
                ],
                'default_port' : 9999
            }
        )

        with hive_controller.async_exec_():
            time.sleep(2.0)
            # -- TODO: Make this a better test and augment
            # the task funciton to create a file we can read
            # or something like that

            port = hive_controller.settings['default_port']

            def fire():
                requests.post(f'http://127.0.0.1:{port}/tasks/execute',
                               json={
                                   'node': 'ATaskNode',
                                   'name': 'test_task_a',
                                   'parameters' : {}
                               })

            for i in range(1):
                fire()

            res = requests.get(f'http://127.0.0.1:{port}/tasks')
            res.raise_for_status()


    @_within_test_hive
    def test_task_feature_required(self):
        """
        Test that we fail when trying to run task nodes without
        the feature
        """
        hive_controller = HiveController(
            os.getcwd(),
            nodes=[ATaskNode],
            augment_settings={
                # Make sure the feature is off
                'hive_features' : [
                    # 'hivemind_tasks'
                ],
                'default_port' : 10455
            }
        )

        with self.assertRaises(EnvironmentError):
            hive_controller.exec_(1.0)


    def test_task_node_validation(self):
        """
        Given a set of task nodes, validate them.
        """
        settings = {
            'hive_features' : ['hivemind_tasks']
        }

        with global_settings.override(settings):
            bad = BadTaskNode(name='testme')
            errors, warnings = bad.verify_config(chatty=False)
            self.assertFalse(bad.valid)


def build_test_parser() -> argparse.ArgumentParser:
    # TODO: Get a test utilities environment setup for
    # the whole feature toolkit
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', action='append', help='Test select directories at a time')
    return parser


if __name__ == '__main__':
    log.start(False)
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    parser = build_test_parser()

    args, unknown = parser.parse_known_args()

    if args.test:
        for t in args.test:
            suite.addTests(loader.discover(
                TEST_BASE_DIR + '/' + t
            ))
    else:
        # suite.addTests(loader.loadTestsFromTestCase(HiveMindTests))

        # Test the util library
        suite.addTests(loader.discover(
            TEST_BASE_DIR
        ))

    res = unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful()
    sys.exit(1 if not res else 0)
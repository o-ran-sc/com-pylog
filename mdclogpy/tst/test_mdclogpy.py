# Copyright (c) 2019 AT&T Intellectual Property.
# Copyright (c) 2018-2019 Nokia.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# This source code is part of the near-RT RIC (RAN Intelligent Controller)
# platform project (RICP).
#
"""Unit tests for mdclogpy root logger"""
import unittest
from unittest.mock import patch
import sys

import mdclogpy
from .mdclogtestutils import TestMdcLogUtils


class TestMdcLog(unittest.TestCase):
    """Unit tests for mdclog.py"""

    def setUp(self):
        self.prog_id = sys.argv[0]

    def tearDown(self):
        pass


    @patch('mdclogpy.Logger._output_log')
    def test_that_root_logger_logs_the_message_using_the_proc_name(self, output_mock):

        mdclogpy.log(mdclogpy.Level.DEBUG, "This is a test log")
        mdclogpy.error("This is an error log")
        mdclogpy.warning("This is a warning log")
        mdclogpy.info("This is an info log")
        mdclogpy.debug("This is a debug log")

        logs = TestMdcLogUtils.get_logs_as_json(output_mock.call_args_list)
        self.assertEqual(self.prog_id, logs[0]["id"])
        self.assertEqual(self.prog_id, logs[1]["id"])
        self.assertEqual(self.prog_id, logs[2]["id"])
        self.assertEqual(self.prog_id, logs[3]["id"])
        self.assertEqual(self.prog_id, logs[4]["id"])
        self.assertEqual("This is a test log", logs[0]["msg"])
        self.assertEqual("This is an error log", logs[1]["msg"])
        self.assertEqual("This is a warning log", logs[2]["msg"])
        self.assertEqual("This is an info log", logs[3]["msg"])
        self.assertEqual("This is a debug log", logs[4]["msg"])

    def test_that_root_logger_get_level_returns_the_current_log_level(self):

        
        mdclogpy.set_level(mdclogpy.Level.INFO)
        self.assertEqual(mdclogpy.get_level(), mdclogpy.Level.INFO)
        mdclogpy.set_level(mdclogpy.Level.WARNING)
        self.assertEqual(mdclogpy.get_level(), mdclogpy.Level.WARNING)
        mdclogpy.set_level(mdclogpy.Level.ERROR)
        self.assertEqual(mdclogpy.get_level(), mdclogpy.Level.ERROR)
        mdclogpy.set_level(mdclogpy.Level.DEBUG)
        self.assertEqual(mdclogpy.get_level(), mdclogpy.Level.DEBUG)

    @patch('mdclogpy.Logger._output_log')
    def test_that_root_logger_logs_with_correct_criticality(self, output_mock):

        mdclogpy.set_level(mdclogpy.Level.DEBUG)

        mdclogpy.log(mdclogpy.Level.DEBUG, "debug test log")
        mdclogpy.log(mdclogpy.Level.INFO, "info test log")
        mdclogpy.log(mdclogpy.Level.WARNING, "warning test log")
        mdclogpy.log(mdclogpy.Level.ERROR, "error test log")

        mdclogpy.debug("another debug test log")
        mdclogpy.info("another info test log")
        mdclogpy.warning("another warning test log")
        mdclogpy.error("another error test log")

        logs = TestMdcLogUtils.get_logs_as_json(output_mock.call_args_list)
        self.assertEqual(8, output_mock.call_count)
        self.assertEqual(logs[0]["crit"], "DEBUG")
        self.assertEqual(logs[1]["crit"], "INFO")
        self.assertEqual(logs[2]["crit"], "WARNING")
        self.assertEqual(logs[3]["crit"], "ERROR")
        self.assertEqual(logs[4]["crit"], "DEBUG")
        self.assertEqual(logs[5]["crit"], "INFO")
        self.assertEqual(logs[6]["crit"], "WARNING")
        self.assertEqual(logs[7]["crit"], "ERROR")

    @patch('mdclogpy.Logger._output_log')
    def test_that_root_logger_logs_mdc_values_correctly(self, output_mock):

        mdclogpy.add_mdc("key1", "value1")
        mdclogpy.add_mdc("key2", "value2")
        mdclogpy.error("mdc test")

        logs = TestMdcLogUtils.get_logs_as_json(output_mock.call_args_list)
        self.assertEqual(logs[0]["mdc"]["key1"], "value1")
        self.assertEqual(logs[0]["mdc"]["key2"], "value2")

    @patch('mdclogpy.Logger._output_log')
    def test_that_non_printable_characters_are_logged_correctly(self, output_mock):

        mdclogpy.set_level(mdclogpy.Level.DEBUG)
        mdclogpy.info("line feed\ntest")
        mdclogpy.info("tab\ttest")
        mdclogpy.info("carriage return\rtest")
        logs = TestMdcLogUtils.get_logs_as_json(output_mock.call_args_list)
        self.assertEqual(logs[0]["msg"], "line feed\ntest")
        self.assertEqual(logs[1]["msg"], "tab\ttest")
        self.assertEqual(logs[2]["msg"], "carriage return\rtest")

if __name__ == '__main__':
    unittest.main()

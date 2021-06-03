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
"""Unit tests for Logger.py"""
import unittest
from unittest.mock import patch
import sys
import os
import time

from mdclogpy import Logger
from mdclogpy import Level
import mdclogpy
from .mdclogtestutils import TestMdcLogUtils


class TestMdcLog(unittest.TestCase):
    """Unit tests for mdclog.py"""

    def setUp(self):
        self.logger = Logger()

    def tearDown(self):
        pass


    def test_that_get_level_returns_the_current_log_level(self):

        # default level is ERROR
        self.assertEqual(self.logger.get_level(), Level.ERROR)
        self.logger.set_level(Level.INFO)
        self.assertEqual(self.logger.get_level(), Level.INFO)
        self.logger.set_level(Level.WARNING)
        self.assertEqual(self.logger.get_level(), Level.WARNING)
        self.logger.set_level(Level.ERROR)
        self.assertEqual(self.logger.get_level(), Level.ERROR)
        self.logger.set_level(Level.DEBUG)
        self.assertEqual(self.logger.get_level(), Level.DEBUG)

    def test_that_set_level_does_not_accept_incorrect_level(self):

        self.logger.set_level(Level.INFO)
        self.logger.set_level(55)
        self.assertEqual(self.logger.get_level(), Level.INFO)

    @patch('mdclogpy.Logger._output_log')
    def test_that_logs_with_lower_than_current_level_(self, output_mock):

        self.logger.set_level(Level.WARNING)
        self.logger.log(Level.DEBUG, "DEBUG")
        self.logger.log(Level.INFO, "INFO")
        self.logger.log(Level.WARNING, "WARNING")
        self.logger.log(Level.ERROR, "ERROR")

        self.assertEqual(2, output_mock.call_count)
        logs = TestMdcLogUtils.get_logs_as_json(output_mock.call_args_list)
        self.assertEqual(logs[0]["msg"], "WARNING")
        self.assertEqual(logs[1]["msg"], "ERROR")

    @patch('mdclogpy.Logger._output_log')
    def test_that_logs_with_lower_than_current_level_are_not_logged(self, output_mock):

        self.logger.set_level(Level.WARNING)
        self.logger.log(Level.DEBUG, "DEBUG")
        self.logger.log(Level.INFO, "INFO")
        self.logger.log(Level.WARNING, "WARNING")
        self.logger.log(Level.ERROR, "ERROR")

        self.assertEqual(2, output_mock.call_count)
        logs = TestMdcLogUtils.get_logs_as_json(output_mock.call_args_list)
        self.assertEqual(logs[0]["msg"], "WARNING")
        self.assertEqual(logs[1]["msg"], "ERROR")

    @patch('mdclogpy.Logger._output_log')
    def test_that_log_contains_correct_criticality(self, output_mock):

        self.logger.set_level(Level.DEBUG)

        self.logger.log(Level.DEBUG, "debug test log")
        self.logger.log(Level.INFO, "info test log")
        self.logger.log(Level.WARNING, "warning test log")
        self.logger.log(Level.ERROR, "error test log")

        self.logger.debug("another debug test log")
        self.logger.info("another info test log")
        self.logger.warning("another warning test log")
        self.logger.error("another error test log")

        self.assertEqual(8, output_mock.call_count)
        logs = TestMdcLogUtils.get_logs_as_json(output_mock.call_args_list)
        self.assertEqual(logs[0]["crit"], "DEBUG")
        self.assertEqual(logs[1]["crit"], "INFO")
        self.assertEqual(logs[2]["crit"], "WARNING")
        self.assertEqual(logs[3]["crit"], "ERROR")
        self.assertEqual(logs[4]["crit"], "DEBUG")
        self.assertEqual(logs[5]["crit"], "INFO")
        self.assertEqual(logs[6]["crit"], "WARNING")
        self.assertEqual(logs[7]["crit"], "ERROR")

    @patch('time.time')
    @patch('mdclogpy.Logger._output_log')
    def test_that_log_contains_correct_timestamp(self, output_mock, mock_time):

        mock_time.return_value = 1554806251.4388545
        self.logger.error("timestamp test")

        logs = TestMdcLogUtils.get_logs_as_json(output_mock.call_args_list)
        self.assertEqual(logs[0]["ts"], 1554806251439)

    @patch('mdclogpy.Logger._output_log')
    def test_that_log_contains_correct_message(self, output_mock):

        self.logger.error("message test")
        logs = TestMdcLogUtils.get_logs_as_json(output_mock.call_args_list)
        print(logs)
        self.assertEqual(logs[0]["msg"], "message test")

    @patch('mdclogpy.Logger._output_log')
    def test_that_log_message_is_escaped_to_valid_json_string(self, output_mock):

        self.logger.set_level(Level.DEBUG)

        self.logger.info('\ and "')

        logs = TestMdcLogUtils.get_logs(output_mock.call_args_list)
        self.assertTrue(r'\\ and \"' in logs[0])
        logs = TestMdcLogUtils.get_logs_as_json(output_mock.call_args_list)
        self.assertEqual(logs[0]["msg"], '\ and "')

    @patch('mdclogpy.Logger._output_log')
    def test_that_empty_mdc_is_logged_correctly(self, output_mock):
        self.logger.mdclog_format_init(configmap_monitor=True)
        self.logger.error("empty mdc test")
        logs = TestMdcLogUtils.get_logs_as_json(output_mock.call_args_list)
        self.assertEqual(logs[0]["msg"],'empty mdc test')
 
    @patch('mdclogpy.Logger._output_log')
    def test_that_config_map_is_monitored_correctly(self, output_mock):
        src = open("//tmp//log","w")
        src.write("log-level: debug\n")
        src.close()
        self.logger.filename = "/tmp/log"
        self.logger.dirname = "/tmp/"
        self.logger.mdc = {"PID":"","SYSTEM_NAME":"","HOST_NAME":"","SERVICE_NAME":"","CONTAINER_NAME":"","POD_NAME":""}
        self.logger.get_env_params_values()
        self.logger.parse_file()
        self.logger.error("Hello")
        self.assertEqual(self.logger.get_level(),Level.DEBUG)

    @patch('mdclogpy.Logger._output_log')
    def test_that_mdc_values_are_logged_correctly(self, output_mock):

        self.logger.add_mdc("key1", "value1")
        self.logger.add_mdc("key2", "value2")
        self.logger.error("mdc test")

        logs = TestMdcLogUtils.get_logs_as_json(output_mock.call_args_list)
        self.assertEqual(logs[0]["mdc"]["key1"], "value1")
        self.assertEqual(logs[0]["mdc"]["key2"], "value2")

    @patch('mdclogpy.Logger._output_log')
    def test_that_mdc_pid_logged_correctly(self, output_mock):
        self.logger.mdclog_format_init(configmap_monitor=True)
        self.logger.error("mdc test")
        logs = TestMdcLogUtils.get_logs_as_json(output_mock.call_args_list)
        self.assertTrue(logs[0]["mdc"]["PID"])
        

    def test_that_mdc_values_can_be_added_and_removed(self):

        self.logger.add_mdc("key1", "value1")
        self.logger.add_mdc("key2", "value2")
        self.assertEqual(self.logger.get_mdc("key2"), "value2")
        self.assertEqual(self.logger.get_mdc("key1"), "value1")
        self.assertEqual(self.logger.get_mdc("non_existent"), None)
        self.logger.remove_mdc("key1")
        self.assertEqual(self.logger.get_mdc("key1"), None)
        self.logger.remove_mdc("non_existent")
        self.logger.clean_mdc()
        self.assertEqual(self.logger.get_mdc("key2"), None)



    @patch('mdclogpy.Logger._output_log')
    def test_update_mdc_log_level_severity(self, output_mock):
       self.logger.update_mdc_log_level_severity("error")
       self.logger.update_mdc_log_level_severity("warning")
       self.logger.update_mdc_log_level_severity("info")
       self.logger.update_mdc_log_level_severity("debug")
       self.logger.update_mdc_log_level_severity("")

    @patch('mdclogpy.Logger._output_log')
    def test_output_log(self, output_mock):
        self.logger._output_log("Logger")

    @patch('mdclogpy.Logger._output_log')
    def test_register_log_change_notify(self, output_mock):
        self.logger.dirname = "/tmp/"
        self.logger.filename = "/tmp/log"
        self.logger.register_log_change_notify()

    @patch('mdclogpy.Logger._output_log')
    def test_multiple_logger_instances(self, output_mock):

        logger1 = Logger("logger1")
        logger2 = Logger("logger2")
        logger1.add_mdc("logger1_key1", "logger1_value1")
        logger1.add_mdc("logger1_key2", "logger1_value2")
        logger2.add_mdc("logger2_key1", "logger2_value1")
        logger2.add_mdc("logger2_key2", "logger2_value2")
        mdclogpy.add_mdc("key", "value")

        logger1.error("error msg")
        logger2.error("warning msg")
        mdclogpy.error("info msg")

        logs = TestMdcLogUtils.get_logs_as_json(output_mock.call_args_list)
        self.assertEqual(3, output_mock.call_count)

        self.assertEqual(logs[0]["id"], "logger1")
        self.assertEqual(logs[0]["crit"], "ERROR")
        self.assertEqual(logs[0]["msg"], "error msg")
        self.assertEqual(logs[0]["mdc"]["logger1_key1"], "logger1_value1")
        self.assertEqual(logs[0]["mdc"]["logger1_key2"], "logger1_value2")
        self.assertEqual(len(logs[0]["mdc"]), 2)

        self.assertEqual(logs[1]["id"], "logger2")
        self.assertEqual(logs[1]["crit"], "ERROR")
        self.assertEqual(logs[1]["msg"], "warning msg")
        self.assertEqual(logs[1]["mdc"]["logger2_key1"], "logger2_value1")
        self.assertEqual(logs[1]["mdc"]["logger2_key2"], "logger2_value2")
        self.assertEqual(len(logs[1]["mdc"]), 2)

        self.assertEqual(logs[2]["id"], sys.argv[0])
        self.assertEqual(logs[2]["crit"], "ERROR")
        self.assertEqual(logs[2]["msg"], "info msg")
        self.assertEqual(logs[2]["mdc"]["key"], "value")
        self.assertEqual(len(logs[2]["mdc"]), 1)

if __name__ == '__main__':
    unittest.main()

# Licensed to the Software Freedom Conservancy (SFC) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The SFC licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""
Exceptions that may happen in the qaviton code.
"""


class RequiredCapabilitiesException(Exception):
    """
    Thrown when a mandatory capability is missing of configured with invalid value: from DesiredCapabilities.
    """

    def __init__(self, msg=None):
        self.msg = msg

    def __str__(self):
        exception_msg = "Message: %s\n" % self.msg
        return exception_msg


class MissingRequiredCapabilitiesException(Exception):
    """
    Thrown when a mandatory capability is missing: from DesiredCapabilities.
    """

    def __init__(self, msg=None):
        self.msg = msg

    def __str__(self):
        exception_msg = "Message: %s\n" % self.msg
        return exception_msg


class DriverConnectionException(Exception):
    """
    Thrown when a remote connection to desired driver is not possible due to error with the driver or network failure.
    """

    def __init__(self, msg=None):
        self.msg = msg

    def __str__(self):
        exception_msg = "Message: %s\n" % self.msg
        return exception_msg


class DiffException(Exception):
    """
    Thrown when unexpected difference is detected.
    """

    def __init__(self, msg=None):
        self.msg = msg

    def __str__(self):
        exception_msg = "Message: %s\n" % self.msg
        return exception_msg



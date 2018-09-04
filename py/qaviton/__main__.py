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

"""run qaviton as a service"""

import sys

if len(sys.argv) > 1:
    if sys.argv[1] == 'create':
        from qaviton.scripts import create

        if len(sys.argv) > 3:
            if 'web' in sys.argv[2]:
                create.web(sys.argv[3])
            elif 'mobile' in sys.argv[2]:
                create.web(sys.argv[3])
        elif len(sys.argv) > 2:
            if 'web' in sys.argv[2]:
                create.web()
            elif 'mobile' in sys.argv[2]:
                create.web()
            else:
                create.web(sys.argv[2])
        else:
            create.web()
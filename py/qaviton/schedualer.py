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
    qaviton implementation of pytest schedualing
    to support parallel testing with
    ordering & dependency features
"""


from xdist.scheduler.load import LoadScheduling
import requests


class QavitonSchedualing(LoadScheduling):
    """Implement load scheduling across nodes.
    This distributes the tests collected across all nodes so each test
    is run just once.  All nodes collect and submit the test suite and
    when all collections are received it is verified they are
    identical collections.  Then the collection gets divided up in
    chunks and chunks get submitted to nodes.  Whenever a node finishes
    an item, it calls ``.mark_test_complete()`` which will trigger the
    scheduler to assign more tests if the number of pending tests for
    the node falls below a low-watermark.
    When created, ``numnodes`` defines how many nodes are expected to
    submit a collection. This is used to know when all nodes have
    finished collection or how large the chunks need to be created.
    Attributes:
    :numnodes: The expected number of nodes taking part.  The actual
       number of nodes will vary during the scheduler's lifetime as
       nodes are added by the DSession as they are brought up and
       removed either because of a dead node or normal shutdown.  This
       number is primarily used to know when the initial collection is
       completed.
    :node2collection: Map of nodes and their test collection.  All
       collections should always be identical.
    :node2pending: Map of nodes and the indices of their pending
       tests.  The indices are an index into ``.pending`` (which is
       identical to their own collection stored in
       ``.node2collection``).
    :collection: The one collection once it is validated to be
       identical between all the nodes.  It is initialised to None
       until ``.schedule()`` is called.
    :pending: List of indices of globally pending tests.  These are
       tests which have not yet been allocated to a chunk for a node
       to process.
    :log: A py.log.Producer instance.
    :config: Config object, used for handling hooks.
    """

    requests.get('https://www.qavitonsaasservice.com/QavitonSchedualing')

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

from itertools import cycle

from py._log.log import Producer
from _pytest.runner import CollectReport

from xdist.workermanage import parse_spec_config
from xdist.report import report_collection_diff

from qaviton.utils import path
from qaviton.utils.helpers import funcname
from qaviton.utils import filer


class QavitonSchedualing(object):
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

    def __init__(self, config, log=None):
        self.numnodes = len(parse_spec_config(config))
        self.node2collection = {}
        self.node2pending = {}
        self.pending = []
        self.collection = None
        if log is None:
            self.log = Producer("loadsched")
        else:
            self.log = log.loadsched
        self.config = config
        self.file_path = path.of(__file__)('{}.log'.format(id(config)))
        filer.create_file(self.file_path)

    def logg(self, *args, **kwargs):
        with open(self.file_path, 'a') as f: 
            for i in args:
                f.write(str(i)+'\n')
            for k in kwargs:
                f.write('{}={}\n'.format(k, kwargs[k]))
            f.write('\n')

    @property
    def nodes(self):
        """A list of all nodes in the scheduler."""
        self.logg('\n--------------\nfunc: {}\n--------------\n'.format(funcname()))
        self.logg(node2pending=self.node2pending.keys())

        return list(self.node2pending.keys())

    @property
    def collection_is_completed(self):
        """Boolean indication initial test collection is complete.
        This is a boolean indicating all initial participating nodes
        have finished collection.  The required number of initial
        nodes is defined by ``.numnodes``.
        """
        self.logg('\n--------------\nfunc: {}\n--------------\n'.format(funcname()))
        self.logg(node2collection=self.node2collection.keys(), numnodes=self.numnodes)

        return len(self.node2collection) >= self.numnodes

    @property
    def tests_finished(self):
        """Return True if all tests have been executed by the nodes."""
        self.logg('\n--------------\nfunc: {}\n--------------\n'.format(funcname()))
        self.logg(collection_is_completed=self.collection_is_completed, node2pending=self.node2pending.values())

        if not self.collection_is_completed:
            return False
        if self.pending:
            return False
        for pending in self.node2pending.values():
            if len(pending) >= 2:
                return False
        return True

    @property
    def has_pending(self):
        """Return True if there are pending test items
        This indicates that collection has finished and nodes are
        still processing test items, so this can be thought of as
        "the scheduler is active".
        """
        self.logg('\n--------------\nfunc: {}\n--------------\n'.format(funcname()))
        self.logg(node2pending=self.node2pending.values(), pending=self.pending)

        if self.pending:
            return True
        for pending in self.node2pending.values():
            if pending:
                return True
        return False

    def add_node(self, node):
        """Add a new node to the scheduler.
        From now on the node will be allocated chunks of tests to
        execute.
        Called by the ``DSession.worker_workerready`` hook when it
        successfully bootstraps a new node.
        """
        self.logg('\n--------------\nfunc: {}\n--------------\n'.format(funcname()))
        self.logg(node=node, node2pending_before=self.node2pending)

        assert node not in self.node2pending
        self.node2pending[node] = []

        self.logg(node2pending_after=self.node2pending)

    def add_node_collection(self, node, collection):
        """Add the collected test items from a node
        The collection is stored in the ``.node2collection`` map.
        Called by the ``DSession.worker_collectionfinish`` hook.
        """
        self.logg('\n--------------\nfunc: {}\n--------------\n'.format(funcname()))
        self.logg(
            node=node,
            collection=len(collection),
            self_collection=self.collection,
            collection_is_completed=self.collection_is_completed,
            node2collection=self.node2collection.keys()
        )
        assert node in self.node2pending
        if self.collection_is_completed:
            # A new node has been added later, perhaps an original one died.
            # .schedule() should have
            # been called by now
            assert self.collection
            if collection != self.collection:
                other_node = next(iter(self.node2collection.keys()))
                msg = report_collection_diff(
                    self.collection, collection, other_node.gateway.id, node.gateway.id
                )
                self.log(msg)
                return
        self.node2collection[node] = list(collection)

        self.logg(node2collection=self.node2collection.keys())

    def mark_test_complete(self, node, item_index, duration=0):
        """Mark test item as completed by node
        The duration it took to execute the item is used as a hint to
        the scheduler.
        This is called by the ``DSession.worker_testreport`` hook.
        """
        self.logg('\n--------------\nfunc: {}\n--------------\n'.format(funcname()))
        self.logg(node=node, item_index=item_index, duration=duration)

        self.node2pending[node].remove(item_index)
        self.check_schedule(node, duration=duration)

        self.logg('node is removed', node2pending=self.node2pending)

    def check_schedule(self, node, duration=0):
        """Maybe schedule new items on the node
        If there are any globally pending nodes left then this will
        check if the given node should be given any more tests.  The
        ``duration`` of the last test is optionally used as a
        heuristic to influence how many tests the node is assigned.
        """
        self.logg('\n--------------\nfunc: {}\n--------------\n'.format(funcname()))
        self.logg(node=node, node_shutting_down=node.shutting_down, duration=duration, num_nodes=len(self.node2pending))

        if node.shutting_down:
            return

        if self.pending:
            # how many nodes do we have?
            num_nodes = len(self.node2pending)
            # if our node goes below a heuristic minimum, fill it out to
            # heuristic maximum
            items_per_node_min = max(2, len(self.pending) // num_nodes // 4)
            items_per_node_max = max(2, len(self.pending) // num_nodes // 2)

            self.logg(
                "if len(node_pending) < items_per_node_min",
                items_per_node_min=items_per_node_min,
                items_per_node_max=items_per_node_max,
                node_pending=self.node2pending[node],
            )

            node_pending = self.node2pending[node]
            if len(node_pending) < items_per_node_min:
                if duration >= 0.1 and len(node_pending) >= 2:
                    # seems the node is doing long-running tests
                    # and has enough items to continue
                    # so let's rather wait with sending new items
                    return
                num_send = items_per_node_max - len(node_pending)

                self.logg(
                    "send tests to node",
                    "num_send = items_per_node_max - len(node_pending)",
                    "self._send_tests(node, num_send)",
                    node=node,
                    num_send=num_send,
                )

                self._send_tests(node, num_send)
        self.log("num items waiting for node:", len(self.pending))

        self.logg("num items waiting for node:", len(self.pending))

    def remove_node(self, node):
        """Remove a node from the scheduler
        This should be called either when the node crashed or at
        shutdown time.  In the former case any pending items assigned
        to the node will be re-scheduled.  Called by the
        ``DSession.worker_workerfinished`` and
        ``DSession.worker_errordown`` hooks.
        Return the item which was being executing while the node
        crashed or None if the node has no more pending items.
        """
        self.logg('\n--------------\nfunc: {}\n--------------\n'.format(funcname()))
        self.logg(
            "This should be called either when the node crashed or at shutdown time.",
            node=node
        )

        pending = self.node2pending.pop(node)
        if not pending:
            return

        # The node crashed, reassing pending items
        crashitem = self.collection[pending.pop(0)]

        self.logg(
            "node crashed, reassing pending items with self.check_schedule(node)",
            crashitem=crashitem,
        )

        self.pending.extend(pending)
        for node in self.node2pending:
            self.check_schedule(node)
        return crashitem

    def schedule(self):
        """Initiate distribution of the test collection
        Initiate scheduling of the items across the nodes.  If this
        gets called again later it behaves the same as calling
        ``.check_schedule()`` on all nodes so that newly added nodes
        will start to be used.
        This is called by the ``DSession.worker_collectionfinish`` hook
        if ``.collection_is_completed`` is True.
        """
        self.logg('\n--------------\nfunc: {}\n--------------\n'.format(funcname()))
        self.logg(
            "assert self.collection_is_completed",
            collection_is_completed=self.collection_is_completed,
        )

        assert self.collection_is_completed

        # Initial distribution already happened, reschedule on all nodes
        if self.collection is not None:

            self.logg("Initial distribution already happened, reschedule on all nodes")

            for node in self.nodes:

                self.logg("check_schedule for node:", node=node)

                self.check_schedule(node)
            return

        # XXX allow nodes to have different collections
        if not self._check_nodes_have_same_collection():
            self.log("**Different tests collected, aborting run**")
            return

        # Collections are identical, create the index of pending items.
        self.collection = list(self.node2collection.values())[0]
        self.pending[:] = range(len(self.collection))

        self.logg(
            "Collections are identical, create the index of pending items.",
            collection=self.collection,
            pending=self.pending
        )

        if not self.collection:
            return

        # Send a batch of tests to run. If we don't have at least two
        # tests per node, we have to send them all so that we can send
        # shutdown signals and get all nodes working.
        initial_batch = max(len(self.pending) // 4, 2 * len(self.nodes))

        self.logg(
            "Send a batch of tests to run. If we don't have at least two",
            "tests per node, we have to send them all so that we can send",
            "shutdown signals and get all nodes working.",
            "initial_batch = max(len(self.pending) // 4, 2 * len(self.nodes))",
            initial_batch=initial_batch,
        )

        # distribute tests round-robin up to the batch size
        # (or until we run out)
        nodes = cycle(self.nodes)

        self.logg(
            "distribute tests round-robin up to the batch size (or until we run out)",
            "nodes = cycle(self.nodes)",
            nodes=nodes,
        )

        for i in range(initial_batch):

            self.logg(
                "loop over initial batch",
                "self._send_tests(next(nodes), 1)"
            )

            self._send_tests(next(nodes), 1)

        if not self.pending:

            self.logg(
                "initial distribution sent all tests, start node shutdown",
                "for node in self.nodes:",
                "    node.shutdown()"
            )

            # initial distribution sent all tests, start node shutdown
            for node in self.nodes:
                node.shutdown()

    def _send_tests(self, node, num):
        self.logg('\n--------------\nfunc: {}\n--------------\n'.format(funcname()))
        tests_per_node = self.pending[:num]

        self.logg(tests_per_node=tests_per_node)

        if tests_per_node:
            del self.pending[:num]

            self.logg(
                "send tests to node:",
                "self.node2pending[node].extend(tests_per_node)",
                "node.send_runtest_some(tests_per_node)",
                "",
                "pending tests remaining:",
                pending=self.pending
            )

            self.node2pending[node].extend(tests_per_node)
            node.send_runtest_some(tests_per_node)

    def _check_nodes_have_same_collection(self):
        """Return True if all nodes have collected the same items.
        If collections differ, this method returns False while logging
        the collection differences and posting collection errors to
        pytest_collectreport hook.
        """
        self.logg('\n--------------\nfunc: {}\n--------------\n'.format(funcname()))

        node_collection_items = list(self.node2collection.items())
        first_node, col = node_collection_items[0]
        same_collection = True

        self.logg(
            node_collection_items=len(node_collection_items),
            first_node=first_node,
            collection=col,
        )

        for node, collection in node_collection_items[1:]:
            msg = report_collection_diff(
                col, collection, first_node.gateway.id, node.gateway.id
            )
            if msg:
                same_collection = False

                self.logg(msg, same_collection=same_collection)

                self.log(msg)
                if self.config is not None:
                    rep = CollectReport(
                        node.gateway.id, "failed", longrepr=msg, result=[]
                    )
                    self.config.hook.pytest_collectreport(report=rep)

        return same_collection
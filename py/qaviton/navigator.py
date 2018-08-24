"""
Uniform Cost Search
"""


import heapq
from qaviton.page import Page


class PriorityQueue:
    """class implementation of priority queue using heapq module"""
    def __init__(self):
        self._queue = []
        self._index = 0

    def insert(self, item, priority):
        heapq.heappush(self._queue, (priority, self._index, item))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._queue)[-1]

    def is_empty(self):
        return len(self._queue) == 0


class Node:
    """class implementation of a node"""
    def __init__(self, node_object):
        """
        :param uuid: unique id - each node in the graph should possess a distinguished id
        self.neighbors represents weight of edges
        """
        self.uuid = str(node_object)
        self.neighbors = {}
        self.object = node_object

    def connect(self, node, action, weight):
        """add node connection and neighbor registration.
        :param action: the action/function to take in order to advance in the graph
        :type node: Node
        :param weight: cost to the neighbor
        """
        self.neighbors[node.uuid] = (node, action, weight)


# TODO: prevent long term loops and re-occurrences
class Graph:
    """class implementation of a graph directed with weight
    The graph not supports multiple edges with the same extremes
    (same output node and same input node)
    """
    def __init__(self):
        """create an empty dict to describe the graph nodes
        with node.key as keys and node objects as values
        """
        self.nodes = {}
        
    def addNodes(self, nodes):
        """add nodes to graph by unique keys"""
        for node in nodes:
            self.addNode(node)
    
    def addNode(self, node):
        """add node to graph by unique key"""
        if str(node) not in self.nodes:
            self.nodes[str(node)] = Node(node)

    def connect(self, source, destination, action, weight):
        """checks if keys exists in the graph and connect the nodes
        
        :param source_id: source node uuid
        :param destination_id: destination node uuid
        :param action: the action/function to take in order to advance in the graph
        :param weight: cost to the neighbor
        """
        self.nodes[str(source)].connect(self.nodes[str(destination)], action, weight)

    def get_neighbor_weight(self, source_id: str, neighbor_id: str):
        return self.nodes[source_id].neighbors[neighbor_id][2]

    def get_neighbors_ids(self, node_id: str):
        """return list of node neighbors uuids"""
        return self.nodes[node_id].neighbors.keys()

    def find_path(self, start, goal):
        if str(start) not in self.nodes or str(goal) not in self.nodes:
            raise Exception('graph is missing node_key_start \'%s\' or node_key_goal \'%s\' does not exist' % (start, goal))
        else:
            # UCS uses priority queue, priority is the cumulative cost (smaller cost)
            queue = PriorityQueue()

            # insert initial neighbor ids to priority queue
            for neighbor in self.nodes[str(start)].neighbors.values():
                # each item of queue is a tuple (neighbor, cumulative_cost, [real functions to take])
                queue.insert((neighbor[2], [(neighbor[1], neighbor[0])]), neighbor[2])

            reached_goal, cumulative_cost_goal = False, -1

            while not queue.is_empty():
                # pop queue item: tuple(neighbor, cumulative_cost, [real functions to take])
                cost, actions = queue.pop()

                # if goal has been reached
                if actions[-1][1].uuid == str(goal):
                    reached_goal, cumulative_cost_goal = True, cost
                    break

                # get all neighbor_ids from current_node_id
                neighbor_ids = self.get_neighbors_ids(actions[-1][1].uuid)

                if neighbor_ids:
                    # insert all neighbors of current_node_id to priority queue
                    for neighbor_id in neighbor_ids:
                        cumulative_cost = self.get_neighbor_weight(actions[-1][1].uuid, neighbor_id) + cost
                        tmp_actions = list(actions)
                        tmp_actions.append((self.nodes[actions[-1][1].uuid].neighbors[neighbor_id][1], self.nodes[neighbor_id]))
                        queue.insert((cumulative_cost, tmp_actions), cumulative_cost)

            if reached_goal:
                return cumulative_cost_goal, actions
            else:
                raise Exception('path is unreachable')


class Navigator(Page):
    """this is a really cool feature meant to do navigation automatically
    please try not to use any arguments with your navigations to keep the process simple
    if you must try to use lambda functions or make sure all your navigations can receive any kind of argument
    """

    def __init__(self, driver, landing_page, timeout=None):
        Page.__init__(self, driver, timeout)
        self.driver = driver
        self.current_page = landing_page
        self.actions = []
        self.cost = None
        self.graph = Graph()

    def node(self, page):
        self.graph.addNode(page)

    def nodes(self, pages):
        for page in pages:
            self.node(page)

    def connect(self, page_bound_navigation, page_to_navigate, weight=100):
        self.nodes((page_bound_navigation.__self__, page_to_navigate))
        self.graph.connect(page_bound_navigation.__self__, page_to_navigate, page_bound_navigation, weight)

    def connect_all(self, *connections):
        for connection in connections:
            self.connect(*connection)

    def froM(self, page):
        self.current_page = page
        return self

    def to(self, page):
        self.cost, self.actions = self.graph.find_path(self.current_page, page)
        return self

    def perform(self, *args, **kwargs):
        try:
            for navigation in self.actions:
                navigation[0](*args, **kwargs)
                self.current_page = str(navigation[1])
        finally:
            self.actions = []
            self.cost = None

    def set_current_page(self, page):
        self.current_page = page

    def get_navigations(self):
        navigations = self.actions
        self.actions = []
        return navigations

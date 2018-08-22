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
    def __init__(self, uuid:str):
        """
        :param uuid: unique id - each node in the graph should possess a distinguished id
        self.neighbors represents weight of edges
        """
        self.uuid = uuid
        self.neighbors = {}

    def connect(self, node, action=None, weight:int=100):
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
        
    def addNodes(self, node_keys:set):
        """add nodes to graph by unique keys"""
        for key in node_keys:
            self.addNode(key)
    
    def addNode(self, node_key:str):
        """add node to graph by unique key"""
        if node_key in self.nodes:
            raise Exception('node with key %s already exists' % node_key)
        else:
            self.nodes[node_key] = Node(node_key)

    def connect(self, source_id:str, destination_id:str, action=None, weight:int=100):
        """checks if keys exists in the graph and connect the nodes
        
        :param source_id: source node uuid
        :param destination_id: destination node uuid
        :param action: the action/function to take in order to advance in the graph
        :param weight: cost to the neighbor
        """
        self.nodes[source_id].connect(self.nodes[destination_id], action, weight)
        return self

    def get_neighbor_weight(self, source_id:str, neighbor_id:str):
        return self.nodes[source_id].neighbors[neighbor_id][2]

    def get_neighbors_ids(self, node_id:str):
        """return list of node neighbors uuids"""
        return self.nodes[node_id].neighbors.keys()

    def find_path(self, start_node_id:str, goal_node_id:str):
        if start_node_id not in self.nodes or goal_node_id not in self.nodes:
            raise Exception('graph is missing node_key_start \'%s\' or node_key_goal \'%s\' does not exist' % (start_node_id, goal_node_id))
        else:
            # UCS uses priority queue, priority is the cumulative cost (smaller cost)
            queue = PriorityQueue()

            # insert initial neighbor ids to priority queue
            for neighbor in self.nodes[start_node_id].neighbors.values():
                weight = neighbor[2]
                # each item of queue is a tuple (neighbor id, cumulative_cost, [real functions to take])
                queue.insert((neighbor[0].uuid, weight, [neighbor[1]]), weight)

            reached_goal, cumulative_cost_goal = False, -1

            while not queue.is_empty():
                # pop queue item: tuple(neighbor id, cumulative_cost, [real functions to take])
                current_node_id, cost, actions = queue.pop()

                # if goal has been reached
                if current_node_id == goal_node_id:
                    reached_goal, cumulative_cost_goal = True, cost
                    break

                # get all neighbor_ids from current_node_id
                neighbor_ids = self.get_neighbors_ids(current_node_id)

                if neighbor_ids:
                    # insert all neighbors of current_node_id to priority queue
                    for neighbor_id in neighbor_ids:
                        cumulative_cost = self.get_neighbor_weight(current_node_id, neighbor_id) + cost
                        tmp_actions = list(actions)
                        tmp_actions.append(self.nodes[current_node_id].neighbors[neighbor_id][1])
                        queue.insert((neighbor_id, cumulative_cost, tmp_actions), cumulative_cost)

            if reached_goal:
                return cumulative_cost_goal, actions
            else:
                raise Exception('path is unreachable')


class Navigator(Page):
    """this is a really cool feature meant to do navigation automatically
    please try not to use any arguments with your navigations to keep the process simple
    if you must try to use lambda functions or make sure all your navigations can receive any kind of argument
    """

    graph = Graph()

    def __init__(self, driver, landing_page, timeout=None):
        Page.__init__(self, driver, timeout)
        self.driver = driver
        self.current_page = str(landing_page)
        self.actions = []
        self.cost = None

    @classmethod
    def add(cls, page_class):
        cls.graph.addNode(str(page_class))

    @classmethod
    def add_all(cls, page_classes):
        for page_class in page_classes:
            cls.add(page_class)

    @classmethod
    def connect(cls, page_class, page_class_to_navigate, action=None, weight=100):
        cls.graph.connect(str(page_class), str(page_class_to_navigate), action, weight)

    def froM(self, page):
        self.current_page = str(page.__class__)
        return self

    def to(self, page):
        self.cost, self.actions = self.graph.find_path(self.current_page, str(page.__class__))
        return self

    def perform(self, *args, **kwargs):
        try:
            for navigation in self.actions:
                navigation(*args, **kwargs)
                self.current_page = str(navigation.__class__)
        finally:
            self.actions = []
            self.cost = None

    def set_current_page(self, page):
        self.current_page = str(page.__class__)

    def get_navigations(self):
        navigations = self.actions
        self.actions = []
        return navigations

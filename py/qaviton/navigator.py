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
Uniform Cost Search
"""

import inspect
import heapq
from qaviton.page import Page
from qaviton.exceptions import PathUnreachableException, PageNavigationException


default_weight = 100
page_attributes = dir(Page)


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
        self.neighbors = {}
        self.object = node_object

    def connect(self, node, action, weight):
        """add node connection and neighbor registration.
        :param action: the action/function to take in order to advance in the graph
        :type node: Node
        :param weight: cost to the neighbor
        """
        self.neighbors[str(node.object)] = (node, action, weight)


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
        
    def add_nodes(self, nodes):
        """add nodes to graph
        :param nodes: a list of node_objects
        """
        for node in nodes:
            self.add_node(node)
    
    def add_node(self, node):
        """add node to graph
        :param node: a node_object
        """
        if str(node) not in self.nodes:
            self.nodes[str(node)] = Node(node)

    def connect(self, source, destination, action, weight):
        """checks if keys exists in the graph and connect the nodes
        
        :param source: source node uuid or node_object
        :param destination: destination node uuid or node_object
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
        if str(start) == str(goal):
            return 0, [], []
        elif str(start) not in self.nodes or str(goal) not in self.nodes:
            raise PathUnreachableException('graph is missing start_node {} or goal_node {} does not exist'.format(start, goal))
        else:
            # UCS uses priority queue, priority is the cumulative cost (smaller cost)
            queue = PriorityQueue()

            # insert initial neighbors (cost, actions, nodes) to priority queue
            for neighbor in self.nodes[str(start)].neighbors.values():
                # each item of queue is a tuple (neighbor cumulative_cost, actions to take, nodes to go through)
                if neighbor[0].object != start:
                    queue.insert((neighbor[2], [neighbor[1]], [neighbor[0]]), neighbor[2])

            reached_goal, cumulative_cost_goal = False, -1

            while not queue.is_empty():
                # pop queue item: tuple(cumulative_cost, [real functions to take], [nodes])
                cost, actions, nodes = queue.pop()

                # if goal has been reached
                if str(nodes[-1].object) == str(goal):
                    reached_goal, cumulative_cost_goal = True, cost
                    break

                # insert all neighbors of current node to priority queue
                for neighbor in nodes[-1].neighbors:
                    # check for loops, don't add neighbors that already exist
                    if nodes[-1].neighbors[neighbor][0] not in nodes and nodes[-1].neighbors[neighbor][0].object != start:
                        cumulative_cost = self.get_neighbor_weight(str(nodes[-1].object), neighbor) + cost
                        new_actions, new_nodes = list(actions), list(nodes)
                        new_actions.append(self.nodes[str(nodes[-1].object)].neighbors[neighbor][1])
                        new_nodes.append(self.nodes[neighbor])
                        # insert a new path item into the priority queue.
                        # a tuple (neighbor cumulative_cost, actions to take, nodes to go through)
                        queue.insert((cumulative_cost, new_actions, new_nodes), cumulative_cost)

            if reached_goal:
                return cumulative_cost_goal, actions, nodes
            else:
                raise PathUnreachableException('path is unreachable')


class Navigator:
    """this is a really cool feature meant to do navigation automatically.
        Warnings:
          - please try not to use any arguments with your navigations to keep the process simple,
            if you must try to use lambda functions or make sure all your navigations can receive any kind of argument,
            for extreme cases just use the pull_path method instead of perform.

          - don't use more than 1 instance per page object,
            it will be painfull for the auto-connect function of the navigator.

            examples:
                ###########
                # imports #
                ###########

                from qaviton.page import Page
                from qaviton.locator import Locator
                from qaviton.drivers.webdriver import WebDriver


                #########
                # pages #
                #########

                class BaddaPage(Page):
                    pass


                class BoogiPage(Page):
                    def goPro_navigate_to_BaddaPage(self, weight=5):
                        self.find(Locator.id('badda')).click(timeout=weight * 3)
                        self.wait_until_page_loads()

                    def navigate_to_BaddaPage(self):
                        self.find(Locator.id('badda')).click(timeout=5)

            example 1

                ###################
                # model based app #
                ###################

                class App(Page):
                    def __init__(self, driver):
                        Page.__init__(self, driver)
                        self.boogi_page = BoogiPage(driver)
                        self.badda_page = BaddaPage(driver)
                        self.navigate = Navigator(self.boogi_page, auto_connect=self)

                # create app with driver (if you wanna try this example make sure to send a real webdriver object to your app instead of 0)
                app = App(0)

                # magic!
                print(app.navigate.graph.nodes)
                print(app.navigate.to(app.badda_page).get_path())

                # make sure to send a real webdriver object to your app (app = App(WebDriver()))
                app.navigate.to(app.badda_page).perform()

            example 2

                ###################
                # model based app #
                ###################

                class App(Page):
                    def __init__(self, driver):
                        Page.__init__(self, driver)
                        self.boogi_page = BoogiPage(driver)
                        self.badda_page = BaddaPage(driver)

                navigate = Navigator(self.boogi_page, auto_connect=self)
                navigate.connect_all(
                    (app.boogi_page.goPro_navigate_to_BaddaPage, badda_page, 5),
                    (app.boogi_page.navigate_to_BaddaPage, badda_page))

                app = App(0)
                print(navigate.graph.nodes)
                print(navigate.to(app.badda_page).get_path())

                # make sure to send a real webdriver object to your app (app = App(WebDriver()))
                navigate.to(app.badda_page).perform()
        """

    def __init__(self, landing_page, auto_connect=None):
        """
        :type landing_page: Page
        :type auto_connect: Page | None
        """
        self.current_page = landing_page
        self.from_page = landing_page
        self.nodes = []
        self.actions = []
        self.cost = None
        self.graph = Graph()
        if auto_connect is not None:
            self.auto_connect(auto_connect)

    def __call__(self, page: Page, *args, **kwargs):
        """:rtype: page"""
        return self.to(page).perform(*args, **kwargs)

    def add_node(self, page):
        """ create a new node from page as a node_object
        and add the new node to the Uniform Cost Search Graph

        :type page: Page
        """
        self.graph.add_node(page)

    def add_nodes(self, *pages):
        """ create new nodes from list with pages as a node_objects
        and add the nodes to the Uniform Cost Search Graph

        :type pages: list[Page] | tuple(Page)
        """
        for page in pages:
            self.add_node(page)

    def connect(self, page_bound_navigation, page_to_navigate, weight=default_weight):
        """ connect 2 nodes with pages as node_objects with a bound page navigation method

        :param page_bound_navigation: Page action to take to advance to the neighbor Page
        :param page_to_navigate: the Page neighbor of the Page with the bound method
        :param weight: navigation cost
        :return:
        """
        self.add_nodes(page_bound_navigation.__self__, page_to_navigate)
        self.graph.connect(page_bound_navigation.__self__, page_to_navigate, page_bound_navigation, weight)

    def connect_all(self, *connections):
        """ create multiple nodes connections with lists of (pages as node_objects with a bound page navigation method)

        :param connections: (page_bound_navigation, page_to_navigate, weight=100),
                            (page_bound_navigation, page_to_navigate, weight=100)
        """
        for connection in connections:
            self.connect(*connection)

    def auto_connect(self, app):
        """parse the app for pages/components with
            def {put any thing here}navigate_to_{exact class name of navigated page}(self, optional_but_not_recommended_args, *args, **kwargs):

            example:
                ###########
                # imports #
                ###########

                from qaviton.page import Page
                from qaviton.locator import Locator
                from qaviton.drivers.webdriver import WebDriver


                #########
                # pages #
                #########

                class BaddaPage(Page):
                    pass


                class BoogiPage(Page):
                    def goPro_navigate_to_BaddaPage(self, weight=5):
                        self.find(Locator.id('badda')).click(timeout=weight * 3)
                        self.wait_until_page_loads()

                    def navigate_to_BaddaPage(self):
                        self.find(Locator.id('badda')).click(timeout=5)


                ###################
                # model based app #
                ###################

                class App(Page):
                    def __init__(self, driver):
                        Page.__init__(self, driver)
                        self.boogi_page = BoogiPage(driver)
                        self.badda_page = BaddaPage(driver)
                        self.navigate = Navigator(self.boogi_page, auto_connect=self)


                # create app with driver (if you wanna try this example make sure to send a real webdriver object to your app instead of 0)
                app = App(0)

                # magic!
                print(app.navigate.graph.nodes)
                print(app.navigate.to(app.badda_page).get_path())

                # make sure to send a real webdriver object to your app (app = App(WebDriver()))
                app.navigate.to(app.badda_page).perform()

            in this example the navigation would carry through
            the goPro_navigate_to_BaddaPage which has a timeout of 15 seconds
            instead of the navigate_to_BaddaPage with only 5 seconds to timeout.
            that's because the default weight for navigation functions is 100.
            your best practice would be passing your navigation methods a weight
            equal to a 1/3 of its timeout or equal to the navigation's median run time.

        :type app: Page
        """
        def find_pages_to_navigate():
            for page_connections in connections:
                for i in range(len(page_connections)):
                    for page in pages.values():
                        if page_connections[i][1] == page.__class__.__name__:
                            page_connections[i] = (page_connections[i][0], page, page_connections[i][2])
                            break

        def find_navigations():
            for page in navigation_attributes:
                connections.append([])
                for i in range(len(navigation_attributes[page])):
                    try:
                        at = getattr(pages[page], navigation_attributes[page][i])
                        class_name = navigation_attributes[page][i].split('navigate_to_')[1]
                        if len(class_name) > 0:
                            sig = inspect.signature(at)
                            if 'weight' in sig.parameters:
                                try:
                                    weight = float(str(sig.parameters['weight']).split('=')[1])
                                except:
                                    weight = default_weight
                            else:
                                weight = default_weight
                            connections[-1].append((at, class_name, weight))
                    except:
                        pass

        def find_all_pages(page):
            if str(page) not in pages:
                pages[str(page)] = page
                navigation_attributes[str(page)] = []
                attributes = [m
                    for m in dir(page)
                    if m not in page_attributes
                    and m not in {'timeout', 'driver', 'url'}]

                for i in range(len(attributes)):
                    if 'navigate_to_' in attributes[i]:
                        navigation_attributes[str(page)].append(attributes[i])
                    else:
                        try:
                            at = getattr(page, attributes[i])
                            if issubclass(at.__class__, Page):
                                find_all_pages(getattr(page, attributes[i]))
                        except:
                            pass

        pages = {}
        navigation_attributes = {}
        connections = []

        find_all_pages(app)
        find_navigations()
        find_pages_to_navigate()

        for c in connections:
            self.connect_all(*c)

    def froM(self, page):
        """navigate from specific page

        :type page: Page
        """
        self.set_from_page(page)
        return self

    def to(self, page):
        """find the best path to navigate to a page

        :type page: Page
        """
        self.cost, self.actions, self.nodes = self.graph.find_path(self.from_page, page)
        return self

    def perform(self, *args, **kwargs):
        """perform navigation actions chain
        navigate from any where to anywhere"""
        try:
            for i in range(len(self.actions)):
                self.actions[i](*args, **kwargs)
                self.current_page = self.nodes[i].object
        except Exception as e:
            raise PageNavigationException("navigation interruption at {}".format(self.current_page)) from e
        finally:
            self.actions = []
            self.cost = None
            self.from_page = self.current_page
        return self.current_page

    def set_from_page(self, page):
        """set the page from which to start the navigation chain"""
        self.from_page = self.graph.nodes[str(page)].object

    def update_current_page(self, page):
        """update the navigator with the application's current page"""
        self.current_page = self.graph.nodes[str(page)].object
        self.set_from_page(page)

    def get_path(self):
        return self.actions

    def reset_path(self):
        self.actions = []

    def pull_path(self):
        """use this method if you want to perform the path
        of navigation actions chain outside of the navigator
        to get a list of the navigation methods
        and reset the navigator's path
        """
        navigations = self.actions
        self.actions = []
        return navigations

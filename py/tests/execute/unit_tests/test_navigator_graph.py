from qaviton.navigator import Graph


def test_graph():
    # build graph
    graph = Graph()

    # add nodes
    graph.addNodes({'S','a','b','c','d','e','f','h','p','q','r','G'})

    # describe node connections
    graph.connect('S', 'd', 'S -> d', 3)
    graph.connect('S', 'e', 'S -> e', 9)
    graph.connect('S', 'p', 'S -> p', 1)
    graph.connect('b', 'a', 'b -> a', 2)
    graph.connect('c', 'a', 'c -> a', 2)
    graph.connect('d', 'b', 'd -> b', 1)
    graph.connect('d', 'c', 'd -> c', 8)
    graph.connect('d', 'e', 'd -> e', 2)
    graph.connect('e', 'h', 'e -> h', 8)
    graph.connect('e', 'r', 'e -> r', 2)
    graph.connect('f', 'c', 'f -> c', 3)
    graph.connect('f', 'G', 'f -> G', 2)
    graph.connect('h', 'p', 'h -> p', 4)
    graph.connect('h', 'q', 'h -> q', 4)
    graph.connect('p', 'q', 'p -> q', 15)
    graph.connect('r', 'f', 'r -> f', 1)

    # find shortest path
    path = graph.find_path(start_node_id='S', goal_node_id='G')
    assert str(path) == "(10, ['S -> d', 'd -> e', 'e -> r', 'r -> f', 'f -> G'])"

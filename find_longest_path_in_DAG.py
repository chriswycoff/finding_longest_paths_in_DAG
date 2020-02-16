### Christopher Wycoff

### Python 3

#please import the following modules

import sys # for FILE I/O

import math

class edge(object):
    def __init__(self, from_vertex, to_vertex, weight):
        self.from_vertex = from_vertex
        self.to_vertex = to_vertex
        self.weight = weight

    # to beutify the printing of the adj list graph
    def __str__(self):
        return str(self.to_vertex)

    def __repr__(self):
        return str(self.to_vertex)

class vertex(object):
    def __init__(self, name):
        self.name = name
        self.color = "white"
        self.discovery = 0
        self.finish = None
        self.distance = math.inf
        self.num_of_paths = 0

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self.name)

class adjacency_list(dict):
    # initialize all the edgelists to len 0
    def __init__(self, num_of_vertices, num_of_edges):
        self.num_of_vertices = num_of_vertices
        self.num_of_edges = num_of_edges
        for i in range(1,num_of_vertices+1):
            self[i] = []

    def add_edge(self, an_edge_object):
        self[an_edge_object.from_vertex].append(an_edge_object)


class paths_list(object):
    def __init__(self, a_graph, vertex_of_interest):
        self.distance = []
        self.vertices = []
        self.vertex_of_interest = vertex_of_interest
        self.topo_sort = []

        for i in range(a_graph.num_of_vertices):
            self.distance.append(math.inf)
            self.vertices.append(vertex(i+1))


############# end class definitions #########################################################

############# begin function definitions ####################################################

def dfs_visit(a_graph, a_path_list, a_vertex, time):
    time += 1
    a_vertex.color = "grey"
    a_vertex.discovery = time
    for a_edge in a_graph[a_vertex.name]:
        new_vertex = a_edge.to_vertex
        new_vertex = a_path_list.vertices[new_vertex - 1]
        if new_vertex.color == "white":
            dfs_visit(a_graph, a_path_list, new_vertex, time)
    a_vertex.color = "black"
    a_vertex.finish = time
    a_path_list.topo_sort.insert(0, a_vertex)


def dfs_toposort(a_graph, a_path_list):
    time = 0

    for i in range(len(a_path_list.vertices)):

        a_vertex = a_path_list.vertices[i]

        if a_vertex.color == "white":
            dfs_visit(a_graph, a_path_list, a_vertex, time)


def longest_or_shortest_path(a_graph, a_path_list, node_n, longest = True):
    # to find shortest indicate longets = False
    longest_path_counter = 0

    start_vertex = a_path_list.vertex_of_interest


    index_counter = 0
    for item in a_path_list.topo_sort:
        if item.name == start_vertex:
            break
        index_counter+=1

    index_of_start = index_counter

    a_path_list.topo_sort[index_of_start].distance = 0
    a_path_list.topo_sort[index_of_start].num_of_paths = 1

    if longest:
        x = -1
    else:
        x = 1

    change_occured = True

    while change_occured:
        change_occured = False

        for i in range(0,len(a_path_list.topo_sort)):
            for edge in a_graph[a_path_list.topo_sort[i].name]:
                if a_path_list.vertices[edge.to_vertex-1].distance > edge.weight * x + a_path_list.topo_sort[i].distance:
                    a_path_list.vertices[edge.to_vertex-1].distance = edge.weight * x + a_path_list.topo_sort[i].distance 
                    change_occured = True


    value_of_longest_path = a_path_list.topo_sort[-1].distance * x

#### now try to determine the amount of longest paths ####


#### here #####
    for i in range(0,len(a_path_list.topo_sort)):

        for a_edge in a_graph[a_path_list.topo_sort[i].name]:
            if a_path_list.vertices[a_edge.from_vertex-1].distance*x == a_path_list.vertices[a_edge.to_vertex-1].distance * x - a_edge.weight:

                a_path_list.vertices[a_edge.to_vertex-1].num_of_paths += a_path_list.vertices[a_edge.from_vertex-1].num_of_paths

    number_of_longest_paths = a_path_list.topo_sort[-1].num_of_paths

    return value_of_longest_path, number_of_longest_paths

def collect_graph(file_pointer):

    first_line = file_pointer.readline()

    first_line = first_line.split()

    num_of_vertices, num_of_edges = int(first_line[0]), int(first_line[1])

    the_graph = adjacency_list(num_of_vertices, num_of_edges)

    for i in range(num_of_edges):

        split_line = file_pointer.readline().split()

        from_vertex, to_vertex, weight = int(split_line[0]), int(split_line[1]), int(split_line[2])

        the_edge = edge(from_vertex, to_vertex, weight)

        the_graph.add_edge(the_edge)
        
    return the_graph


def main():

    file = sys.stdin

    the_graph = collect_graph(file)

    node_n = len(the_graph)

    the_paths_list = paths_list(the_graph, 1)


    dfs_toposort(the_graph, the_paths_list)


    value_of_longest_path, number_of_longest_paths = longest_or_shortest_path(the_graph, the_paths_list, node_n)

    distances = []

    num_of_paths = []

    for i in range(len(the_paths_list.topo_sort)):
        distances.append(the_paths_list.topo_sort[i].distance)

    print("longest path:", value_of_longest_path)
    print("number of longest paths:", number_of_longest_paths)



if __name__ == "__main__":
    main()

    

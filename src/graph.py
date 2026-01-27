import math

class Node:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.neighbors = {}

    def add_neighbor(self, neighbor, cost):
        self.neighbors[neighbor] = cost

class Graph:
    def __init__(self):
        self.nodes = {}

    def add_station(self, name, x, y):
        if name not in self.nodes:
            self.nodes[name] = Node(name, x, y)

    def add_connection(self, u, v, minutes):
        if u not in self.nodes: self.add_station(u, 0, 0)
        if v not in self.nodes: self.add_station(v, 0, 0)
        
        node_u = self.nodes[u]
        node_v = self.nodes[v]
        node_u.add_neighbor(node_v, minutes)
        node_v.add_neighbor(node_u, minutes) # Bi-directional

    def get_node(self, name):
        return self.nodes.get(name)

    def get_heuristic(self, node_name, goal_name):
        n1 = self.nodes[node_name]
        n2 = self.nodes[goal_name]
        # Assume 1 unit distance ~= 2 minutes travel time roughly
        return math.sqrt((n1.x - n2.x)**2 + (n1.y - n2.y)**2) * 1.5

def build_network(mode="TODAY"):
    g = Graph()
    
    # DEFINE STATIONS (Coordinates)
    stations = {
        "Jurong East":(5, 14),
        "Buona Vista":(12, 9),  
        "HarbourFront":(14, 2), 
        "Orchard":(19, 8),  
        "City Hall":(21, 6),  
        "Marina Bay":(22, 4),   
        "Gardens by the Bay":(23, 5),  
        "Bishan":(21, 16),  
        "Paya Lebar":(29, 10),  
        "Tanah Merah":(37, 11),  
        "Expo":(39, 9),   
        "Tampines":(39, 14),  
        "Pasir Ris":(42, 16),  
        "Changi Airport":(48, 11)
    }
    
    if mode == "FUTURE":
        stations["Changi Terminal 5"] = (50, 8) 
        stations["Sungei Bedok"] = (43, 6)
    
    for name, (x, y) in stations.items():
        g.add_station(name, x, y)

    # DEFINE CONNECTIONS
    # East-West Line
    g.add_connection("Jurong East", "Buona Vista", 9)
    g.add_connection("Buona Vista", "City Hall", 16)
    g.add_connection("City Hall", "Paya Lebar", 10)
    g.add_connection("Paya Lebar", "Tanah Merah", 11)
    g.add_connection("Tanah Merah", "Pasir Ris", 7)
    g.add_connection("Tanah Merah", "Tampines", 5)
     
    # North-South Line
    g.add_connection("Jurong East", "Bishan", 20)
    g.add_connection("Bishan", "Orchard", 10)
    g.add_connection("Orchard", "City Hall", 7)
    g.add_connection("City Hall", "Marina Bay", 5)

    # Circle Line
    g.add_connection("HarbourFront", "Buona Vista", 14)
    g.add_connection("Buona Vista", "Bishan", 13)
    g.add_connection("Bishan", "Paya Lebar", 10)
    g.add_connection("Paya Lebar", "Marina Bay", 13)
    
    # Thomson-East Coast Line
    g.add_connection("Orchard", "Gardens by the Bay", 17)
    
    # Connection A: The existing CGA Branch
    g.add_connection("Tanah Merah", "Expo", 3)
    g.add_connection("Expo", "Changi Airport", 4)

    if mode == "FUTURE":
        g.add_connection("Gardens by the Bay", "Sungei Bedok", 15)
        g.add_connection("Sungei Bedok", "Changi Terminal 5", 6)
        g.add_connection("Changi Terminal 5", "Changi Airport", 4) # The Inter-terminal Skytrain/Subway
        g.add_connection("Pasir Ris", "Changi Terminal 5", 10) # Hypothetical CRL link

    return g
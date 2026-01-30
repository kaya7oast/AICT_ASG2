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
        # Ensure nodes exist
        if u not in self.nodes: self.add_station(u, 0, 0)
        if v not in self.nodes: self.add_station(v, 0, 0)
        
        node_u = self.nodes[u]
        node_v = self.nodes[v]
        
        # Bi-directional connection
        node_u.add_neighbor(node_v, minutes)
        node_v.add_neighbor(node_u, minutes)

    def get_node(self, name):
        return self.nodes.get(name)

    def get_heuristic(self, node_name, goal_name):
        n1 = self.nodes[node_name]
        n2 = self.nodes[goal_name]
        # 1.5 multiplier maps distance units to approx minutes
        return math.sqrt((n1.x - n2.x)**2 + (n1.y - n2.y)**2) * 1.5

    def set_edge_weight(self, u, v, new_weight):
        """Allows simulating disruptions (breaking tracks) or delays."""
        if u in self.nodes and v in self.nodes:
            node_u = self.nodes[u]
            node_v = self.nodes[v]
            
            if node_v in node_u.neighbors:
                node_u.neighbors[node_v] = new_weight
            if node_u in node_v.neighbors:
                node_v.neighbors[node_u] = new_weight

def build_network(mode="TODAY"):
    g = Graph()
    
    # (Scaled: 1 unit ~= 1km)
    stations = {
        "Jurong East": (5, 14), "Buona Vista": (12, 9), "HarbourFront": (14, 2),
        "Orchard": (19, 8), "City Hall": (21, 6), "Marina Bay": (22, 4),
        "Gardens by the Bay": (23, 5), "Bishan": (21, 16), "Paya Lebar": (29, 10),
        "Tanah Merah": (37, 11), "Expo": (39, 9), "Tampines": (39, 14),
        "Pasir Ris": (42, 16), "Changi Airport": (48, 11)
    }
    
    if mode == "FUTURE":
        stations["Changi Terminal 5"] = (50, 8)
        stations["Sungei Bedok"] = (43, 6)
    
    for name, (x, y) in stations.items():
        g.add_station(name, x, y)

    # EWL
    g.add_connection("Jurong East", "Buona Vista", 9)
    g.add_connection("Buona Vista", "City Hall", 16)
    g.add_connection("City Hall", "Paya Lebar", 10)
    g.add_connection("Paya Lebar", "Tanah Merah", 11)
    g.add_connection("Tanah Merah", "Pasir Ris", 7)
    g.add_connection("Tanah Merah", "Tampines", 5)
    
    # NSL
    g.add_connection("Jurong East", "Bishan", 20)
    g.add_connection("Bishan", "Orchard", 10)
    g.add_connection("Orchard", "City Hall", 7)
    g.add_connection("City Hall", "Marina Bay", 5)

    # CCL
    g.add_connection("HarbourFront", "Buona Vista", 14)
    g.add_connection("Buona Vista", "Bishan", 13)
    g.add_connection("Bishan", "Paya Lebar", 10)
    g.add_connection("Paya Lebar", "Marina Bay", 13)
    
    # TEL
    g.add_connection("Orchard", "Gardens by the Bay", 17)
    
    # Changi Branch
    g.add_connection("Tanah Merah", "Expo", 3)
    g.add_connection("Expo", "Changi Airport", 4)

    # 3. FUTURE LINKS
    if mode == "FUTURE":
        g.add_connection("Gardens by the Bay", "Sungei Bedok", 15)
        g.add_connection("Sungei Bedok", "Changi Terminal 5", 6)
        g.add_connection("Changi Terminal 5", "Changi Airport", 4) 
        g.add_connection("Pasir Ris", "Changi Terminal 5", 10)

    return g
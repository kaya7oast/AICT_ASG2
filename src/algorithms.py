import time
from collections import deque
import heapq

class Pathfinder:
    def __init__(self, graph):
        self.graph = graph

    # BFS
    def bfs(self, start_name, goal_name):
        start_time = time.perf_counter()
        start_node = self.graph.get_node(start_name)
        goal_node = self.graph.get_node(goal_name)
        
        if not start_node or not goal_node: return None, 0, 0, 0

        queue = deque([(start_node, [start_node.name], 0)]) 
        visited = set([start_name])
        nodes_expanded = 0

        while queue:
            current_node, path, cost = queue.popleft()
            nodes_expanded += 1

            if current_node == goal_node:
                end_time = time.perf_counter()
                exec_time = (end_time - start_time) * 1000
                return path, nodes_expanded, cost, exec_time

            for neighbor, weight in current_node.neighbors.items():
                if neighbor.name not in visited:
                    visited.add(neighbor.name)
                    queue.append((neighbor, path + [neighbor.name], cost + weight))
        return None, nodes_expanded, 0, 0

    # DFS
    def dfs(self, start_name, goal_name):
        start_time = time.perf_counter()
        start_node = self.graph.get_node(start_name)
        goal_node = self.graph.get_node(goal_name)
        
        if not start_node or not goal_node: return None, 0, 0, 0

        stack = [(start_node, [start_node.name], 0)]
        visited = set()
        nodes_expanded = 0

        while stack:
            current_node, path, cost = stack.pop() # LIFO 
            
            if current_node.name in visited: continue
            visited.add(current_node.name)
            nodes_expanded += 1

            if current_node == goal_node:
                end_time = time.perf_counter()
                exec_time = (end_time - start_time) * 1000
                return path, nodes_expanded, cost, exec_time

            for neighbor, weight in current_node.neighbors.items():
                if neighbor.name not in visited:
                    stack.append((neighbor, path + [neighbor.name], cost + weight))
        return None, nodes_expanded, 0, 0

    # GBFS
    def gbfs(self, start_name, goal_name):
        start_time = time.perf_counter()
        start_node = self.graph.get_node(start_name)
        goal_node = self.graph.get_node(goal_name)
        
        if not start_node or not goal_node: return None, 0, 0, 0

        h_start = self.graph.get_heuristic(start_name, goal_name)
        open_set = [(h_start, start_name, [start_name], 0)]
        visited = set([start_name])
        nodes_expanded = 0

        while open_set:
            _, current_name, path, current_g = heapq.heappop(open_set)
            nodes_expanded += 1
            current_node = self.graph.get_node(current_name)

            if current_name == goal_name:
                end_time = time.perf_counter()
                exec_time = (end_time - start_time) * 1000
                return path, nodes_expanded, current_g, exec_time

            for neighbor, weight in current_node.neighbors.items():
                if neighbor.name not in visited:
                    visited.add(neighbor.name)
                    h = self.graph.get_heuristic(neighbor.name, goal_name)
                    new_g = current_g + weight
                    heapq.heappush(open_set, (h, neighbor.name, path + [neighbor.name], new_g))
        return None, nodes_expanded, 0, 0

    # A*
    def a_star(self, start_name, goal_name):
        start_time = time.perf_counter()
        start_node = self.graph.get_node(start_name)
        goal_node = self.graph.get_node(goal_name)
        
        if not start_node or not goal_node: return None, 0, 0, 0

        open_set = [] 
        heapq.heappush(open_set, (0, start_name, [start_name], 0))
        
        visited_costs = {start_name: 0}
        nodes_expanded = 0

        while open_set:
            _, current_name, path, current_g = heapq.heappop(open_set)
            nodes_expanded += 1

            if current_name == goal_name:
                end_time = time.perf_counter()
                exec_time = (end_time - start_time) * 1000
                return path, nodes_expanded, current_g, exec_time

            current_node = self.graph.get_node(current_name)
            
            for neighbor, weight in current_node.neighbors.items():
                new_g = current_g + weight
                
                if neighbor.name not in visited_costs or new_g < visited_costs[neighbor.name]:
                    visited_costs[neighbor.name] = new_g
                    h = self.graph.get_heuristic(neighbor.name, goal_name)
                    f = new_g + h
                    heapq.heappush(open_set, (f, neighbor.name, path + [neighbor.name], new_g))
        return None, nodes_expanded, 0, 0
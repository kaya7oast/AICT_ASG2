import time
import heapq
from collections import deque

class Pathfinder:
    def __init__(self, graph):
        self.graph = graph

    def bfs(self, start, goal):
        t0 = time.perf_counter() # High precision
        s, g = self.graph.get_node(start), self.graph.get_node(goal)
        if not s or not g: return None, 0, 0, 0
        
        queue = deque([(s, [s.name], 0)])
        visited = {s.name}
        nodes_expanded = 0

        while queue:
            curr, path, cost = queue.popleft()
            nodes_expanded += 1
            if curr == g:
                return path, nodes_expanded, cost, (time.perf_counter()-t0)*1000
            
            for n, w in curr.neighbors.items():
                if n.name not in visited:
                    visited.add(n.name)
                    queue.append((n, path + [n.name], cost + w))
        return None, nodes_expanded, 0, 0

    def dfs(self, start, goal):
        t0 = time.perf_counter()
        s, g = self.graph.get_node(start), self.graph.get_node(goal)
        if not s or not g: return None, 0, 0, 0
        
        stack = [(s, [s.name], 0)]
        visited = set()
        nodes_expanded = 0

        while stack:
            curr, path, cost = stack.pop()
            if curr.name in visited: continue
            visited.add(curr.name)
            nodes_expanded += 1
            
            if curr == g:
                return path, nodes_expanded, cost, (time.perf_counter()-t0)*1000
            
            for n, w in curr.neighbors.items():
                if n.name not in visited:
                    stack.append((n, path + [n.name], cost + w))
        return None, nodes_expanded, 0, 0

    def gbfs(self, start, goal):
        t0 = time.perf_counter()
        s, g = self.graph.get_node(start), self.graph.get_node(goal)
        if not s or not g: return None, 0, 0, 0
        
        # Priority Queue: (Heuristic, NodeName, Path, Cost)
        open_set = [(0, start, [start], 0)]
        visited = {start}
        nodes_expanded = 0

        while open_set:
            _, curr_name, path, cost = heapq.heappop(open_set)
            nodes_expanded += 1
            curr = self.graph.get_node(curr_name)
            
            if curr == g:
                return path, nodes_expanded, cost, (time.perf_counter()-t0)*1000
            
            for n, w in curr.neighbors.items():
                if n.name not in visited:
                    visited.add(n.name)
                    # GBFS uses ONLY heuristic for priority
                    h = self.graph.get_heuristic(n.name, goal)
                    heapq.heappush(open_set, (h, n.name, path+[n.name], cost+w))
        return None, nodes_expanded, 0, 0

    def a_star(self, start, goal):
        t0 = time.perf_counter()
        s, g = self.graph.get_node(start), self.graph.get_node(goal)
        if not s or not g: return None, 0, 0, 0
        
        # Priority Queue: (F-Score, NodeName, Path, G-Score)
        open_set = [(0, start, [start], 0)]
        g_scores = {start: 0}
        nodes_expanded = 0

        while open_set:
            _, curr_name, path, curr_g = heapq.heappop(open_set)
            nodes_expanded += 1
            
            if curr_name == goal:
                return path, nodes_expanded, curr_g, (time.perf_counter()-t0)*1000
            
            curr = self.graph.get_node(curr_name)
            for n, w in curr.neighbors.items():
                tentative_g = curr_g + w
                if n.name not in g_scores or tentative_g < g_scores[n.name]:
                    g_scores[n.name] = tentative_g
                    f = tentative_g + self.graph.get_heuristic(n.name, goal)
                    heapq.heappush(open_set, (f, n.name, path+[n.name], tentative_g))
        return None, nodes_expanded, 0, 0
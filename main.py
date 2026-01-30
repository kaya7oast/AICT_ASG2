import os
import copy
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# IMPORT FROM YOUR SOURCE FOLDER
from src.graph import build_network
from src.algorithms import Pathfinder

# ==========================================
# CONFIGURATION
# ==========================================
# Force output to project folder
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")

# Optimization Parameters
BUS_CAPACITY = 800      # Constraint: Max pax per bus fleet
PEAK_HOUR = True        # Constraint: Affects road travel time

# Commuter Demand (Origin, Destination, Number of Pax)
COMMUTER_DEMAND = [
    ("City Hall", "Changi Airport", 500), 
    ("Orchard", "Changi Airport", 300),
    ("Jurong East", "Changi Airport", 200),
    ("Paya Lebar", "Changi Terminal 5", 150),
    ("Bishan", "Changi Airport", 400)
]

# ==========================================
# PHASE 1: STANDARD EXPERIMENT
# ==========================================
def run_standard_experiments():
    print(f"\n{'='*30}\n PHASE 1: ALGORITHM BENCHMARKING\n{'='*30}")
    
    def run_mode(mode):
        subway = build_network(mode)
        finder = Pathfinder(subway)
        test_pairs = [("Changi Airport", "City Hall"), ("Changi Airport", "Orchard"), 
                      ("Paya Lebar", "Changi Terminal 5"), ("Bishan", "Changi Terminal 5")]
        data = []
        for start, end in test_pairs:
            if not subway.get_node(start) or not subway.get_node(end): continue
            
            for name, func in [("BFS", finder.bfs), ("DFS", finder.dfs), ("GBFS", finder.gbfs), ("A*", finder.a_star)]:
                path, nodes, cost, time_ms = func(start, end)
                data.append({
                    "Mode": mode, "Algorithm": name, "Origin": start, "Dest": end, 
                    "Cost": cost, "Nodes": nodes, "Time (ms)": time_ms
                })
        return pd.DataFrame(data)

    # Run Both Modes
    df = pd.concat([run_mode("TODAY"), run_mode("FUTURE")])
    
    # Save & Plot
    if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)
    
    csv_path = os.path.join(OUTPUT_DIR, "experiment_results.csv")
    df.to_csv(csv_path, index=False)
    print(f"Experimental Data saved to: {csv_path}")

    # Generate Graphs
    print("Generating Benchmark Graphs...")
    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    sns.barplot(data=df, x="Algorithm", y="Nodes", hue="Mode", ax=axes[0], palette="viridis").set_title("Efficiency (Nodes)")
    sns.barplot(data=df, x="Algorithm", y="Cost", hue="Mode", ax=axes[1], palette="magma").set_title("Quality (Mins)")
    sns.barplot(data=df, x="Algorithm", y="Time (ms)", hue="Mode", ax=axes[2], palette="coolwarm").set_title("Speed (ms)")
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "performance_comparison.png"))
    print("Graphs saved.")


# ==========================================
# PHASE 2: OPTIMIZATION (HILL CLIMBING)
# ==========================================
def calculate_objective_score(graph, solution_type="Train"):
    """
    Objective Function: Minimize (Passenger-Minutes + Crowding Penalties)
    """
    finder = Pathfinder(graph)
    total_pax_mins = 0
    stranded_count = 0
    crowding_penalty = 0

    # Constraint Check: Bus Capacity
    total_bus_load = sum([p[2] for p in COMMUTER_DEMAND]) if solution_type == "Bus" else 0
    if solution_type == "Bus" and total_bus_load > BUS_CAPACITY:
        overload = total_bus_load - BUS_CAPACITY
        # Penalty: 0.5 mins delay added for every extra passenger
        crowding_penalty = overload * 0.5 

    for start, end, passengers in COMMUTER_DEMAND:
        if not graph.get_node(start) or not graph.get_node(end): continue

        _, _, time_mins, _ = finder.a_star(start, end)
        
        if time_mins == 0: 
            time_mins = 240 # Penalty: 4 hours if stranded
            stranded_count += 1
            
        # Add constraints to cost
        total_pax_mins += ((time_mins + crowding_penalty) * passengers)

    return total_pax_mins, stranded_count

def run_advanced_optimization():
    print(f"\n{'='*30}\n PHASE 2: DISRUPTION & OPTIMIZATION\n{'='*30}")
    
    # 1. Baseline
    base_graph = build_network("TODAY")
    base_cost, _ = calculate_objective_score(base_graph)
    print(f"[1] Baseline (Normal Ops): {base_cost:,.0f} pax-mins")

    # 2. Simulate Disruption
    print("\n[2] SCENARIO: Segment Suspension (Tanah Merah <-> Expo)")
    disrupted_graph = copy.deepcopy(base_graph)
    disrupted_graph.set_edge_weight("Tanah Merah", "Expo", 9999) # Break the link
    
    fail_cost, stranded = calculate_objective_score(disrupted_graph)
    print(f"    Disrupted Cost:        {fail_cost:,.0f} pax-mins (Stranded: {stranded} routes)")

    # 3. Hill Climbing Search
    print("\n[3] EXECUTING HILL CLIMBING (Bus Bridge Deployment)")
    print(f"    Constraint: Bus Capacity = {BUS_CAPACITY} | Peak Hour = {PEAK_HOUR}")

    traffic_factor = 1.5 if PEAK_HOUR else 1.0
    
    # Candidate Solutions (Neighbors in search space)
    candidates = [
        ("Tanah Merah", "Expo", 15),          # Short Bridge (Slow traffic)
        ("Paya Lebar", "Changi Airport", 40), # Long Express
        ("Tampines", "Changi Airport", 20),   # Northern Divert
    ]

    best_sol = None
    min_cost = fail_cost

    for u, v, base_time in candidates:
        real_time = base_time * traffic_factor
        
        # Test Candidate
        test_graph = copy.deepcopy(disrupted_graph)
        test_graph.add_connection(u, v, real_time)
        
        cost, _ = calculate_objective_score(test_graph, solution_type="Bus")
        print(f"    -> Testing Bridge [{u}<->{v}] ({real_time}m)... Score: {cost:,.0f}")
        
        # Hill Climbing Step
        if cost < min_cost:
            min_cost = cost
            best_sol = (u, v)

    if best_sol:
        print(f"\n✅ OPTIMAL SOLUTION: Deploy Bus [{best_sol[0]} <-> {best_sol[1]}]")
        print(f"   Savings: {fail_cost - min_cost:,.0f} pax-minutes")
    else:
        print("   No improvement found.")

if __name__ == "__main__":
    run_standard_experiments()   
    run_advanced_optimization()  
    print("All tasks complete.")
import os
import copy
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.graph import build_network
from src.algorithms import Pathfinder

# CHASE'S PART (Bayesian)
from src.bayesian_inference import run_bayesian_analysis 

OUTPUT_DIR = "Output"

BUS_CAPACITY = 800      # Constraint: Max pax per bus fleet
PEAK_HOUR = True        # Constraint: Affects road travel time

COMMUTER_DEMAND = [
    ("City Hall", "Changi Airport", 500), 
    ("Orchard", "Changi Airport", 300),
    ("Jurong East", "Changi Airport", 200),
    ("Paya Lebar", "Changi Terminal 5", 150),
    ("Bishan", "Changi Airport", 400)
]

def setup_directories():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created directory: {OUTPUT_DIR}")

def run_experiment(mode):
    print(f"\n{'='*50}")
    print(f" EXPERIMENT MODE: {mode}")
    print(f"{'='*50}")
    
    subway = build_network(mode)
    finder = Pathfinder(subway)
    
    test_pairs = [
        ("Changi Airport", "City Hall"),
        ("Changi Airport", "Orchard"),
        ("Changi Airport", "Gardens by the Bay"),
        ("Paya Lebar", "Changi Terminal 5"),
        ("HarbourFront", "Changi Terminal 5"),
        ("Bishan", "Changi Terminal 5")
    ]
    
    results = []

    for start, end in test_pairs:
        if not subway.get_node(start) or not subway.get_node(end):
            continue

        algos = {
            "BFS": finder.bfs,
            "DFS": finder.dfs,
            "GBFS": finder.gbfs,
            "A*": finder.a_star
        }
        
        for name, func in algos.items():
            path, nodes, cost, time_ms = func(start, end)
            path_str = " -> ".join(path) if path else "No Path"
            
            results.append({
                "Mode": mode,
                "Algorithm": name,
                "Origin": start,
                "Dest": end,
                "Cost (Mins)": cost,
                "Nodes Expanded": nodes,
                "Time (ms)": time_ms,
                "Path": path_str
            })

    df = pd.DataFrame(results)
    if not df.empty:
        csv_path = os.path.join(OUTPUT_DIR, f"experiment_results_{mode}.csv")
        df.to_csv(csv_path, index=False)
        print(f"Saved: {csv_path}")
    
    return df

def plot_results(results_df):
    if results_df.empty: return
    sns.set_theme(style="whitegrid")    
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    sns.barplot(x="Algorithm", y="Nodes Expanded", hue="Mode", data=results_df, ax=axes[0], palette="viridis")
    axes[0].set_title("Efficiency: Nodes Expanded")
    sns.barplot(x="Algorithm", y="Cost (Mins)", hue="Mode", data=results_df, ax=axes[1], palette="magma")
    axes[1].set_title("Quality: Path Cost")
    sns.barplot(x="Algorithm", y="Time (ms)", hue="Mode", data=results_df, ax=axes[2], palette="coolwarm")
    axes[2].set_title("Speed: Execution Time")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'performance_comparison.png'))
    print("Graphs saved to Output/performance_comparison.png")

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
            
        total_pax_mins += ((time_mins + crowding_penalty) * passengers)

    return total_pax_mins, stranded_count

def run_advanced_optimization():
    print(f"\n{'='*50}")
    print(f" PART 2: DISRUPTION OPTIMIZATION (Hill Climbing)")
    print(f"{'='*50}")
    
    base_graph = build_network("TODAY")
    base_cost, _ = calculate_objective_score(base_graph)
    print(f"[1] Baseline (Normal Ops): {base_cost:,.0f} pax-mins")

    print("\n[2] SCENARIO: Segment Suspension (Tanah Merah <-> Expo)")
    disrupted_graph = copy.deepcopy(base_graph)
    disrupted_graph.set_edge_weight("Tanah Merah", "Expo", 9999) 
    
    fail_cost, stranded = calculate_objective_score(disrupted_graph)
    print(f"    Disrupted Cost:        {fail_cost:,.0f} pax-mins (Stranded Routes: {stranded})")

    print("\n[3] EXECUTING HILL CLIMBING (Bus Bridge Deployment)")
    print(f"    Constraint: Bus Capacity = {BUS_CAPACITY} | Peak Hour = {PEAK_HOUR}")

    traffic_factor = 1.5 if PEAK_HOUR else 1.0
    
    candidates = [
        ("Tanah Merah", "Expo", 15),          # Short Bridge (Slow traffic)
        ("Paya Lebar", "Changi Airport", 40), # Long Express
        ("Tampines", "Changi Airport", 20),   # Divert
    ]

    best_sol = None
    min_cost = fail_cost

    for u, v, base_time in candidates:
        real_time = base_time * traffic_factor
        
        # Test 
        test_graph = copy.deepcopy(disrupted_graph)
        test_graph.add_connection(u, v, real_time)
        
        cost, _ = calculate_objective_score(test_graph, solution_type="Bus")
        print(f"    -> Testing Bridge [{u}<->{v}] ({real_time}m)... Score: {cost:,.0f}")
        
        # Hill Climbing Step
        if cost < min_cost:
            min_cost = cost
            best_sol = (u, v)

    if best_sol:
        print(f"\nOPTIMAL SOLUTION: Deploy Bus [{best_sol[0]} <-> {best_sol[1]}]")
        print(f"   Savings: {fail_cost - min_cost:,.0f} pax-minutes")
    else:
        print("   No improvement found.")

def main():
    setup_directories()
    
    print("\n" + "="*80)
    print("PART 1: PATHFINDING ALGORITHMS")
    print("="*80)
    
    df_today = run_experiment("TODAY")
    df_future = run_experiment("FUTURE")
    
    if df_today is not None and df_future is not None:
        all_results = pd.concat([df_today, df_future])
        combined_csv = os.path.join(OUTPUT_DIR, "experiment_results_ALL.csv")
        all_results.to_csv(combined_csv, index=False)
        plot_results(all_results)
    
    run_advanced_optimization()
    run_bayesian_analysis()
    
    print("\n" + "="*80)
    print("ALL EXPERIMENTS COMPLETED")
    print("="*80)
    print(f"Results saved in: {OUTPUT_DIR}/")

if __name__ == "__main__":
    main()
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.graph import build_network
from src.algorithms import Pathfinder

from src.bayesian_inference import run_bayesian_analysis 

OUTPUT_DIR = "Output"

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

def main():
    setup_directories()
    
    print("\n" + "="*80)
    print("PART 1: PATHFINDING ALGORITHMS (Eden's Work)")
    print("="*80)
    
    df_today = run_experiment("TODAY")
    df_future = run_experiment("FUTURE")
    
    if df_today is not None and df_future is not None:
        all_results = pd.concat([df_today, df_future])
        combined_csv = os.path.join(OUTPUT_DIR, "experiment_results_ALL.csv")
        all_results.to_csv(combined_csv, index=False)
        plot_results(all_results)
    
    run_bayesian_analysis()
    
    print("\n" + "="*80)
    print("ALL EXPERIMENTS COMPLETED")
    print("="*80)
    print(f"Results saved in: {OUTPUT_DIR}/")

if __name__ == "__main__":
    main()
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.graph import build_network
from src.algorithms import Pathfinder
from src.logic_inference import run_inference_scenarios

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
        print(df[["Algorithm", "Origin", "Dest", "Cost (Mins)", "Nodes Expanded"]].to_string())
    
    return df

def plot_results(results_df):
    if results_df.empty:
        print("No data to plot!")
        return

    sns.set_theme(style="whitegrid")    
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    # Plot 1: Efficiency
    sns.barplot(x="Algorithm", y="Nodes Expanded", hue="Mode", data=results_df, ax=axes[0], palette="viridis")
    axes[0].set_title("Efficiency: Nodes Expanded")
    
    # Plot 2: Quality
    sns.barplot(x="Algorithm", y="Cost (Mins)", hue="Mode", data=results_df, ax=axes[1], palette="magma")
    axes[1].set_title("Quality: Path Cost")
    
    # Plot 3: Speed
    sns.barplot(x="Algorithm", y="Time (ms)", hue="Mode", data=results_df, ax=axes[2], palette="coolwarm")
    axes[2].set_title("Speed: Execution Time")
    
    plt.tight_layout()
    
    save_path = os.path.join(OUTPUT_DIR, 'performance_comparison.png')
    plt.savefig(save_path)
    plt.show()

def run_logic_inference_experiments(): #Tian Rui
    """Run logical inference experiments for both network modes."""
    print("\n" + "="*80)
    print("LOGICAL INFERENCE EXPERIMENTS")
    print("="*80)
    
    # Run inference scenarios
    today_results = run_inference_scenarios("TODAY")
    future_results = run_inference_scenarios("FUTURE")
    
    # Create DataFrame for results
    all_inference_results = today_results + future_results
    df_inference = pd.DataFrame(all_inference_results)
    
    if not df_inference.empty:
        csv_path = os.path.join(OUTPUT_DIR, "logic_inference_results.csv")
        df_inference.to_csv(csv_path, index=False)
        print(f"\n[SUCCESS] Saved inference results to: {csv_path}")
        
        # Print summary table (cleaner formatting)
        print("\n" + "="*80)
        print("INFERENCE RESULTS SUMMARY")
        print("="*80)
        for idx, row in df_inference.iterrows():
            status = "VALID" if row.get('valid') == True else "INVALID" if row.get('valid') == False else ("CONSISTENT" if row.get('consistent') == True else "INCONSISTENT")
            violations = row.get('violations', [])
            # Handle violations properly - check if it's a list and has items
            violation_text = ""
            if isinstance(violations, list) and len(violations) > 0:
                violation_text = f" - {violations[0]}"
            print(f"{idx+1:2d}. [{row['mode']:6s}] {status:12s} - {row['scenario']}{violation_text}")
        print("="*80)
    
    return df_inference

def main():
    setup_directories()
    
    # Part 1: Pathfinding experiments (existing) - Tian Rui
    print("\n" + "="*80)
    print("PART 1: PATHFINDING ALGORITHMS")
    print("="*80)
    
    df_today = run_experiment("TODAY")
    print("-" * 30)
    df_future = run_experiment("FUTURE")
    
    if df_today is not None and df_future is not None:
        all_results = pd.concat([df_today, df_future])
        
        combined_csv = os.path.join(OUTPUT_DIR, "experiment_results_ALL.csv")
        all_results.to_csv(combined_csv, index=False)
        
        plot_results(all_results)
    
    # Part 2: Logical inference experiments (new) - Tian Rui
    print("\n" + "="*80)
    print("PART 2: LOGICAL INFERENCE & ADVISORY CONSISTENCY")
    print("="*80)
    
    df_inference = run_logic_inference_experiments()
    
    print("\n" + "="*80)
    print("ALL EXPERIMENTS COMPLETED")
    print("="*80)
    print(f"Results saved in: {OUTPUT_DIR}/")

if __name__ == "__main__":
    main()
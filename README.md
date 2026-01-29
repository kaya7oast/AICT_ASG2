# ChangiLink AI - Intelligent MRT Routing and Disruption Support System - Tian Rui

## Overview

ChangiLink AI is an intelligent MRT routing and disruption-support system for Singapore's rail network, developed for AICT Assignment 2. The system supports commuters and operations planning by:

1. **Pathfinding Algorithms**: Finding optimal routes using BFS, DFS, GBFS, and A*
2. **Logical Inference**: Validating routes and checking service advisory consistency using resolution-based inference

## Features

### Two Network Modes

- **TODAY Mode**: Current EWL airport branch operations
- **FUTURE Mode**: Network with TELe/CRL extensions including:
  - Thomson-East Coast Line extension (Sungei Bedok → T5 → Tanah Merah)
  - EWL-to-TEL conversion (Tanah Merah, Expo, Changi Airport)
  - Cross Island Line extension to T5

### Core Components

1. **Graph-based Network Model** (`src/graph.py`)
   - Stations as nodes with coordinates
   - Connections as weighted edges (travel time in minutes)
   - Supports both TODAY and FUTURE network configurations

2. **Pathfinding Algorithms** (`src/algorithms.py`)
   - Breadth-First Search (BFS)
   - Depth-First Search (DFS)
   - Greedy Best-First Search (GBFS)
   - A* Search
   - Performance metrics: path cost, nodes expanded, execution time

3. **Logical Inference System** (`src/logic_inference.py`)
   - 15+ propositional logic rules modeling MRT operations
   - Resolution-based inference engine
   - Route validity checking
   - Service advisory consistency verification
   - Rule violation identification

## Project Structure

```
AICT_ASG2/
├── main.py                              # Main execution script
├── README.md                            # This file
├── LOGIC_INFERENCE_DOCUMENTATION.md    # Detailed logic system docs
├── src/
│   ├── __init__.py
│   ├── graph.py                        # Network graph implementation
│   ├── algorithms.py                   # Pathfinding algorithms
│   └── logic_inference.py              # Logical inference system
└── Output/                             # Generated results
    ├── experiment_results_TODAY.csv
    ├── experiment_results_FUTURE.csv
    ├── experiment_results_ALL.csv
    ├── logic_inference_results.csv
    └── performance_comparison.png
```

## Installation

### Prerequisites

- Python 3.8+
- Required packages: pandas, matplotlib, seaborn

### Setup

```bash
# Install dependencies
pip install pandas matplotlib seaborn

# Run the system
python main.py
```

## Usage

### Running All Experiments

```bash
python main.py
```

This will:
1. Run pathfinding experiments for both TODAY and FUTURE modes
2. Run logical inference scenarios (12 total scenarios)
3. Generate CSV reports and visualization charts in `Output/`

### Running Logic Inference Only

```bash
python src/logic_inference.py
```

This displays:
- All propositional logic rules
- Test scenarios for both modes
- Validation results
- Rule violations (if any)

## Logical Inference System

### Rules Summary (15 Rules)

The system implements rules covering:
- **Station Operational Integrity**: Stations cannot be both operational and under maintenance
- **Line Dependencies**: Line operations require key stations to be functional
- **Transfer Requirements**: Transfers require operational stations
- **Service Adjustments**: Maintenance mandates service adjustments
- **Systems Integration**: EWL-to-TEL conversion impacts (FUTURE mode)
- **New Station Requirements**: T5 operational constraints (FUTURE mode)
- **Line Conversion**: Cannot run both EWL and TEL on same stretch (FUTURE mode)
- **Interchange Requirements**: T5 interchange needs both TEL and CRL (FUTURE mode)

### Test Scenarios (12 Total)

**TODAY Mode (6 scenarios)**:
1. Valid route via operational stations
2. Invalid route through station under maintenance
3. Consistent advisory with proper service adjustments
4. Inconsistent advisory missing service adjustments
5. Valid route using Tanah Merah bypass when Expo is down
6. Invalid route attempting reduced service during peak hours

**FUTURE Mode (6 scenarios)**:
1. Valid T5 operations with extensions complete
2. Invalid T5 operation without TEL extension
3. Consistent systems integration advisory
4. Inconsistent integration without required maintenance
5. Invalid route with both lines operating during conversion
6. Invalid T5 interchange missing CRL service

See `LOGIC_INFERENCE_DOCUMENTATION.md` for complete details.

## Results

Results are saved in the `Output/` directory:

- **Pathfinding Results**: Algorithm performance comparison (CSV + charts)
- **Logic Inference Results**: Route validity and advisory consistency checks
- **Visualizations**: Performance comparison graphs

## Key Findings

### Pathfinding
- A* provides optimal paths with good efficiency
- BFS guarantees shortest path but explores more nodes
- GBFS is fast but may not find optimal paths
- DFS is unpredictable and inefficient for this application

### Logical Inference
- Successfully validates routes against operational rules
- Detects inconsistencies in service advisories
- Identifies specific rule violations
- Supports both current and future network configurations

## Technical Details

### Edge Weight Determination

Travel times (edge weights) are based on:
- Average inter-station travel time (2-5 minutes for adjacent stations)
- Line type (express vs. regular)
- Transfer penalties (implicit in routing)
- Realistic Singapore MRT timings

### Logical Inference Algorithm

Uses **resolution-based inference**:
1. Rules converted to Conjunctive Normal Form (CNF)
2. Resolution principle applied to derive new clauses
3. Empty clause (contradiction) detection
4. Violation attribution through rule checking

## Future Enhancements

1. **Extended Network**: Full Singapore MRT coverage (100+ stations)
2. **Real-time Data**: Integration with LTA DataMall API
3. **First-Order Logic**: More expressive rule modeling
4. **Temporal Reasoning**: Time-dependent constraints
5. **Probabilistic Inference**: Uncertainty handling for delays
6. **Natural Language Explanations**: User-friendly violation reports
7. **Route Optimization**: Multi-criteria optimization (time, cost, crowding)

## References

1. Russell & Norvig (2020). *Artificial Intelligence: A Modern Approach* (4th ed.)
2. LTA Press Release (25 July 2025): TEL-CRL Extensions
3. Singapore MRT Network Map and Operational Data

## License

Academic project for AICT module. For educational purposes only.

## Authors

AICT Assignment Team - January 2026
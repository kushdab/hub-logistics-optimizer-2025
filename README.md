# Hub Logistics Optimizer 2025

## Overview
This project is a micro-warehousing routing engine designed for **boda-boda** (motorcycle taxi) fleets operating in high-density urban environments. It addresses the unique challenges of last-mile delivery in cities where traffic congestion is high and delivery windows are narrow.

## Features
- **Haversine Distance Logic**: Accurate GPS-based distance calculations.
- **Constraint-Aware Routing**: Handles boda-boda load capacity limits.
- **Priority Dispatching**: Balances proximity with order urgency.
- **Multi-Stop Optimization**: Greedy heuristic for sequence planning.

## Installation
```bash
pip install -r requirements.txt
```

## Usage
Run the optimizer script to simulate a routing plan for a set of urban delivery points:
```bash
python optimizer.py
```

## Data Structures
- `Location`: Geographic coordinates.
- `Order`: Payload metadata (weight, priority).
- `BodaOptimizer`: Core engine for route calculation.
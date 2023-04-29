# Trajectory Analysis: Identifying Leader-Follower Relationships and Time to Collision

This repository contains a Python implementation of an algorithm to analyze vehicle trajectories, identify leader-follower relationships, and calculate the Time to Collision (TTC) between vehicles. This information is crucial for traffic management, safety analysis, and the development of autonomous vehicles.

The implementation is provided in two versions: the original functional code (`main.py`) and an Object-Oriented Programming (OOP) version (`main_oop.py`).

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Data](#data)
- [Implementation](#implementation)

## Installation

To use this code, clone the repository and install the required dependencies:

```bash
git clone https://github.com/qwertyz15/trajectory_analysis.git
cd trajectory_analysis
pip install -r requirements.txt
```

## Usage

To run the analysis, execute the `main.py` script for the functional implementation or `main_oop.py` for the OOP implementation:

```bash
python main.py
```

or

```bash
python main_oop.py
```

The scripts will read the CSV files in the `data/` directory, analyze the trajectory pairs, and print the results to the console.

## Data

The input data consists of CSV files containing vehicle trajectory data with columns for Time (s), Latitude, and Longitude. The provided example data includes three trajectory pairs: (T1, T2), (T1, T2_2), and (T3, T4). You can add your own CSV files to the `data/` directory to analyze different trajectory pairs.

## Implementation

The algorithm is implemented using Python and the following main functions:

- `haversine(lat1, lon1, lat2, lon2)`: Calculates the Haversine distance between two points.
- `bearing(lat1, lon1, lat2, lon2)`: Calculates the bearing between two points.
- `analyze_trajectory_pair(trajectory1, trajectory2, Dl)`: Analyzes a pair of trajectories to determine the leader, follower, and minimum TTC.

The OOP version of the code uses two main classes:

- `Trajectory`: Represents a vehicle trajectory with methods for calculating distance and bearing.
- `TrajectoryPair`: Represents a pair of vehicle trajectories with a method for analyzing the leader-follower relationship and calculating the TTC.

## Results

After running the `main.py` script, the following results were obtained:

```
Pair (T1, T2): Leader = T2, Follower = T1, Min TTC = 120.30 seconds
Pair (T1, T2_2): Leader = T2_2, Follower = T1, Min TTC = 87.24 seconds
Pair (T3, T4): Leader = T4, Follower = T3, Min TTC = inf seconds
```

These results indicate the leader and follower vehicles for each trajectory pair, as well as the minimum TTC between them. In the case of (T3, T4), the TTC is infinite, which means the vehicles are not on a collision course.

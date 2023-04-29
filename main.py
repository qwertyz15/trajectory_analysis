import numpy as np
import pandas as pd

def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2.0) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2.0) ** 2
    c = 2 * np.arcsin(np.sqrt(a))
    return 6371 * c * 1000

def bearing(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    x = np.cos(lat2) * np.sin(dlon)
    y = np.cos(lat1) * np.sin(lat2) - np.sin(lat1) * np.cos(lat2) * np.cos(dlon)
    return (np.degrees(np.arctan2(x, y)) + 360) % 360

def analyze_trajectory_pair(trajectory1, trajectory2, Dl = 3.0):
    common_times = sorted(set(trajectory1.index) & set(trajectory2.index))
    
    leader_counts = {trajectory1.name: 0, trajectory2.name: 0}
    follower_counts = {trajectory1.name: 0, trajectory2.name: 0}
    ttc_values = []
    
    for t in common_times:
        if t + 1 in common_times:
            lat1, lon1 = trajectory1.loc[t, ["Latitude", "Longitude"]]
            lat2, lon2 = trajectory2.loc[t, ["Latitude", "Longitude"]]
            
            bearing1 = bearing(lat1, lon1, trajectory1.loc[t + 1, "Latitude"], trajectory1.loc[t + 1, "Longitude"])
            bearing2 = bearing(lat2, lon2, trajectory2.loc[t + 1, "Latitude"], trajectory2.loc[t + 1, "Longitude"])
            bearing12 = bearing(lat1, lon1, lat2, lon2)

            diff1 = abs(bearing1 - bearing12) % 360
            diff2 = abs(bearing2 - bearing12) % 360

            if diff1 < diff2:
                leader_counts[trajectory1.name] += 1
                follower_counts[trajectory2.name] += 1
                leader, follower = trajectory1.name, trajectory2.name
            else:
                leader_counts[trajectory2.name] += 1
                follower_counts[trajectory1.name] += 1
                leader, follower = trajectory2.name, trajectory1.name

            if leader == trajectory1.name:
                leader_trajectory = trajectory1
                follower_trajectory = trajectory2
            else:
                leader_trajectory = trajectory2
                follower_trajectory = trajectory1

            # Calculate the distance between leader and follower at time t
            dist = haversine(*leader_trajectory.loc[t, ["Latitude", "Longitude"]],
                            *follower_trajectory.loc[t, ["Latitude", "Longitude"]])

            # Calculate the speed of the leader and the follower
            vl = (haversine(*leader_trajectory.loc[t, ["Latitude", "Longitude"]],
                            *leader_trajectory.loc[t + 1, ["Latitude", "Longitude"]])) / 1.0
            vf = (haversine(*follower_trajectory.loc[t, ["Latitude", "Longitude"]],
                            *follower_trajectory.loc[t + 1, ["Latitude", "Longitude"]])) / 1.0

            # Calculate the TTC
            # Dl = 3  # Assuming a constant length of 3 meters for the leading vehicle
            ttc = (dist - Dl) / (vf - vl) if vf - vl > 0 else np.inf
            ttc_values.append(ttc)


            # # Calculate TTC
            # ttc = abs((xl - xf) - Dl) / (vf - vl) if vf - vl > 0 else np.inf
            # ttc_values.append(ttc)

    # Determine the most common leader and follower
    leader = max(leader_counts, key=leader_counts.get)
    follower = max(follower_counts, key=follower_counts.get)

    # Calculate the minimum TTC
    min_ttc = min(ttc_values) if ttc_values else np.inf

    return leader, follower, min_ttc



# Read the CSV files
T1 = pd.read_csv('data/T1.csv', index_col='Time (s)')
T1.name = 'T1'
T2 = pd.read_csv('data/T2.csv', index_col='Time (s)')
T2.name = 'T2'
T2_2 = pd.read_csv('data/T2_2.csv', index_col='Time (s)')
T2_2.name = 'T2_2'
T3 = pd.read_csv('data/T3.csv', index_col='Time (s)')
T3.name = 'T3'
T4 = pd.read_csv('data/T4.csv', index_col='Time (s)')
T4.name = 'T4'

# Define the trajectory pairs
pairs = [
    (T1.name, T1, T2.name, T2),
    (T1.name, T1, T2_2.name, T2_2),
    (T3.name, T3, T4.name, T4),
]

# Run the calculations for the trajectory pairs
for name1, trajectory1, name2, trajectory2 in pairs:
    # Dl = 3.0  # Length of the leading vehicle (change this value as needed)
    leader, follower, min_ttc = analyze_trajectory_pair(trajectory1, trajectory2)
    print(f'Pair ({name1}, {name2}): Leader = {leader}, Follower = {follower}, Min TTC = {min_ttc:.2f} seconds')




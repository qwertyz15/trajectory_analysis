import numpy as np
import pandas as pd

class Trajectory:
    def __init__(self, data, name):
        self.data = data
        self.name = name

    def calculate_distance(self, lat1, lon1, lat2, lon2):
        lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = np.sin(dlat / 2.0) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2.0) ** 2
        c = 2 * np.arcsin(np.sqrt(a))
        return 6371 * c * 1000

    def calculate_bearing(self, lat1, lon1, lat2, lon2):
        lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
        dlon = lon2 - lon1
        x = np.cos(lat2) * np.sin(dlon)
        y = np.cos(lat1) * np.sin(lat2) - np.sin(lat1) * np.cos(lat2) * np.cos(dlon)
        return (np.degrees(np.arctan2(x, y)) + 360) % 360


class TrajectoryPair:
    def __init__(self, trajectory1, trajectory2, Dl=3.0):
        self.trajectory1 = trajectory1
        self.trajectory2 = trajectory2
        self.Dl = Dl

    def analyze(self):
        common_times = sorted(set(self.trajectory1.data.index) & set(self.trajectory2.data.index))

        leader_counts = {self.trajectory1.name: 0, self.trajectory2.name: 0}
        follower_counts = {self.trajectory1.name: 0, self.trajectory2.name: 0}
        ttc_values = []

        for t in common_times:
            if t + 1 in common_times:
                lat1, lon1 = self.trajectory1.data.loc[t, ["Latitude", "Longitude"]]
                lat2, lon2 = self.trajectory2.data.loc[t, ["Latitude", "Longitude"]]

                bearing1 = self.trajectory1.calculate_bearing(lat1, lon1, self.trajectory1.data.loc[t + 1, "Latitude"], self.trajectory1.data.loc[t + 1, "Longitude"])
                bearing2 = self.trajectory2.calculate_bearing(lat2, lon2, self.trajectory2.data.loc[t + 1, "Latitude"], self.trajectory2.data.loc[t + 1, "Longitude"])
                bearing12 = self.trajectory1.calculate_bearing(lat1, lon1, lat2, lon2)

                diff1 = abs(bearing1 - bearing12) % 360
                diff2 = abs(bearing2 - bearing12) % 360

                if diff1 < diff2:
                    leader_counts[self.trajectory1.name] += 1
                    follower_counts[self.trajectory2.name] += 1
                    leader, follower = self.trajectory1, self.trajectory2
                else:
                    leader_counts[self.trajectory2.name] += 1
                    follower_counts[self.trajectory1.name] += 1
                    leader, follower = self.trajectory2, self.trajectory1

                # Calculate the distance between leader and follower
                dist = leader.calculate_distance(
                    *leader.data.loc[t, ["Latitude", "Longitude"]],
                    *follower.data.loc[t, ["Latitude", "Longitude"]],
                )

                # Calculate the speed of the leader and the follower
                vl = leader.calculate_distance(
                    *leader.data.loc[t, ["Latitude", "Longitude"]],
                    *leader.data.loc[t + 1, ["Latitude", "Longitude"]],
                ) / 1.0
                vf = follower.calculate_distance(
                    *follower.data.loc[t, ["Latitude", "Longitude"]],
                    *follower.data.loc[t + 1, ["Latitude", "Longitude"]],
                ) / 1.0

                # Calculate the TTC
                ttc = (dist - self.Dl) / (vf - vl) if vf - vl > 0 else np.inf
                ttc_values.append(ttc)

        # Determine the most common leader and follower
        leader = max(leader_counts, key=leader_counts.get)
        follower = max(follower_counts, key=follower_counts.get)

        # Calculate the minimum TTC
        min_ttc = min(ttc_values) if ttc_values else np.inf

        return leader, follower, min_ttc


# Read the CSV files
T1 = Trajectory(pd.read_csv("data/T1.csv", index_col="Time (s)"), "T1")
T2 = Trajectory(pd.read_csv("data/T2.csv", index_col="Time (s)"), "T2")
T2_2 = Trajectory(pd.read_csv("data/T2_2.csv", index_col="Time (s)"), "T2_2")
T3 = Trajectory(pd.read_csv("data/T3.csv", index_col="Time (s)"), "T3")
T4 = Trajectory(pd.read_csv("data/T4.csv", index_col="Time (s)"), "T4")

# Define the trajectory pairs
pairs = [
    (T1, T2),
    (T1, T2_2),
    (T3, T4),
]

# Run the calculations for the trajectory pairs
for trajectory1, trajectory2 in pairs:
    pair = TrajectoryPair(trajectory1, trajectory2)
    leader, follower, min_ttc = pair.analyze()
    print(f"Pair ({trajectory1.name}, {trajectory2.name}): Leader = {leader}, Follower = {follower}, Min TTC = {min_ttc:.2f} seconds")

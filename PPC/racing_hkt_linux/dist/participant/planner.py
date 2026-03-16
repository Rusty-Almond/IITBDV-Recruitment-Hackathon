
'''
PPC Hackathon — Participant Boilerplate
You must implement two functions: plan() and control()
'''

# ─── TYPES (for reference) ────────────────────────────────────────────────────

# Cone: {"x": float, "y": float, "side": "left" | "right", "index": int}
# State: {"x", "y", "yaw", "vx", "vy", "yaw_rate"}  
# CmdFeedback: {"throttle", "steer"}        

# ─── PLANNER ──────────────────────────────────────────────────────────────────
import numpy as np


def densify(path, step=0.4):
    new_path = []
    for i in range(len(path)):
        p1 = path[i]
        p2 = path[(i+1)%len(path)]

        dx = p2["x"] - p1["x"]
        dy = p2["y"] - p1["y"]
        dist = np.hypot(dx, dy)
        n_points = max(int(dist / step), 1)

        for j in range(n_points):
            t = j / n_points
            new_path.append({"x": p1["x"] + t*dx, "y": p1["y"] + t*dy})

    new_path.append(path[-1])
    return new_path


def plan(cones: list[dict]) -> list[dict]:
    """
    Generate a path from the cone layout.
    Called ONCE before the simulation starts.

    Args:
        cones: List of cone dicts with keys x, y, side ("left"/"right"), index

    Returns:
        path: List of waypoints [{"x": float, "y": float}, ...]
              Ordered from start to finish.
    
    Tip: Try midline interpolation between matched left/right cones.
         You can also compute a curvature-optimised racing line.
    """
    path = []
    # TODO: implement your path planning here
    blue = np.array([[cone["x"], cone["y"]] for cone in cones if cone["side"] == "left"])
    yellow = np.array([[cone["x"], cone["y"]] for cone in cones if cone["side"] == "right"])

    # implement a planning algorithm to generate a path from the blue and yellow cones

    blue = sorted(
        [c for c in cones if c["side"]=="left"],
        key=lambda c: c["index"]
    )

    yellow = sorted(
        [c for c in cones if c["side"]=="right"],
        key=lambda c: c["index"]
    )

    path = []

    for b,y in zip(blue,yellow):

        path.append({
            "x": (b["x"] + y["x"]) / 2,
            "y": (b["y"] + y["y"]) / 2
        })

    path = densify(path)
    return path

'''
PPC Hackathon — Participant Boilerplate
You must implement two functions: plan() and control()
'''

# ─── TYPES (for reference) ────────────────────────────────────────────────────

# Path: list of waypoints [{"x": float, "y": float}, ...]
# State: {"x", "y", "yaw", "vx", "vy", "yaw_rate"} 
# CmdFeedback: {"throttle", "steer"}         

# ─── CONTROLLER ───────────────────────────────────────────────────────────────
import numpy as np

prev_error=0
i=0
integral=0
prev_steer=0
prev_yaw=0

def steering(path: list[dict], state: dict,dt):

    length_of_car = 2.6
    # Calculate steering angle based on path and vehicle state
    global prev_steer

    if(prev_steer < -0.30 or prev_steer > 0.30):
        lookahead = 2.0 + np.hypot(state["vx"],state["vy"])*0.61
    elif ( prev_steer <-0.20 or prev_steer >0.20):
        lookahead = 1.3 + np.hypot(state["vx"],state["vy"])*0.69
    else :
        lookahead= 3.0 + np.hypot(state["vx"],state["vy"])*0.65
    pts = np.array([[p["x"], p["y"]] for p in path])
    car = np.array([state["x"], state["y"]])
    dist = np.linalg.norm(pts - car, axis=1)
    closest = np.argmin(dist)

    target=path[-1]
    for i in range(closest,len(path)):
        dx=path[i]["x"] - state["x"]
        dy=path[i]["y"] - state["y"]
        if np.hypot(dx,dy) > lookahead:
            target=path[i]
            break
    dx = target["x"] - state["x"]
    dy = target["y"] - state["y"]
    alpha = np.arctan2(dy, dx) - state["yaw"]
    alpha = np.arctan2(np.sin(alpha),np.cos(alpha))
    Ld = max(np.hypot(dx,dy),2.0)
    steer = np.arctan2(2 * 2.6 * np.sin(alpha), Ld)

    steer= prev_steer*0.78+0.22*steer
    prev_steer=steer

    # 0.5 in the max steering angle in radians (about 28.6 degrees)
    return np.clip(steer, -0.5, 0.5)


def throttle_algorithm(target_speed, current_speed,state, dt):

    global prev_error,integral,prev_yaw

    yaw=0.80*prev_yaw+0.20*state["yaw_rate"]
    #adjust target_speed based on tthe turns being taken
    adjusted_speed=target_speed*(1- 0.85*abs(yaw))

    prev_yaw=yaw
    adjusted_speed=max(adjusted_speed,3.0)

    error=adjusted_speed-current_speed
    integral+=error*dt
    derivative= (error-prev_error)/dt

    prev_error=error

    throttle=0
    brake=0

    if current_speed > adjusted_speed :
        brake = min((current_speed-adjusted_speed)*0.8,1.0)
    elif current_speed - adjusted_speed <=2:
        throttle = 0.50*error+0.1*integral+0.01*derivative
    elif current_speed- adjusted_speed <= 1 :
        throttle =0.10*error +0.1*integral +0.01*derivative
    #elif current_speed-adjusted_speed <= 0.5:
     #   brake =0.20*error
    else:
        throttle= error +0.1*integral +0.01*derivative

   # clip throttle and brake to [0, 1]
    return np.clip(throttle, 0.0, 1.0), np.clip(brake, 0.0, 1.0)

def control(
    path: list[dict],
    state: dict,
    cmd_feedback: dict,
    step: int,
) -> tuple[float, float, float]:
    """
    Generate throttle, steer, brake for the current timestep.
    Called every 50ms during simulation.

    Args:
        path:         Your planned path (waypoints)
        state:        Noisy vehicle state observation
                        x, y        : position (m)
                        yaw         : heading (rad)
                        vx, vy      : velocity in body frame (m/s)
                        yaw_rate    : (rad/s)
        cmd_feedback: Last applied command with noise
                        throttle, steer, brake
        step:         Current simulation timestep index

    Returns:
        throttle  : float in [0.0, 1.0]   — 0=none, 1=full
        steer     : float in [-0.5, 0.5]  — rad, neg=left
        brake     : float in [0.0, 1.0]   — 0=none, 1=full
    
    Note: throttle and brake cannot both be > 0 simultaneously.
    """
    throttle = 0.0
    steer    = 0.0
    brake = 0.0
   
    # TODO: implement your controller here
    steer = steering(path, state,0.05)
    target_speed = 15 # m/s, adjust as needed
    global integral
    speed= np.hypot(state["vx"],state["vy"])
    throttle, brake = throttle_algorithm(target_speed, speed ,state ,0.05)

    return throttle, steer, brake
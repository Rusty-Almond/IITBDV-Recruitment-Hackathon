# PPC Assignment

## Strategies

### Planner

It extracts the coordinates of the blue and yellow cones from the `path` array into the `blue` and `yellow` arrays. Then it sorts the `blue` and `yellow` arrays by their index so that when we match them from closest other color cone later the match is correct. Then the `for` loop calculates the midpoint of the cones which would give the midpoint of the track there. The `densify` function increases the number of points so we have more data to steer the car by placing points at equal distance of `step`. 

### Controller

#### `steer` function

It first calculates the `lookahead` distance from the `prev_steer` because if the car had steered sharply in the last iteration it was probably a turn so it should not look too far ahead as it would cut the corner then.
It then calculates the `dist` the distance between the car's position and the points in `path`and stores the closest one's index in `closest`.
Then it loops over the elements in `path` and checks for points whose distance is greater than the `lookahead` and stores in `target`. Then it calculates `alpha` the angle from the target point required for pure pursuit algorithm.It also factors in the current yaw because the algorithm assumes you are facing at an angle alpha from the target point but we may be some more yaw angle away from our last steer. It then applies the pure pursuit angle formula on the newly calculated correct lookahead distance `Ld` from the target and puts a threshold minimum so that the car keeps on moving forward even if target is too close. It also smooths out the steer by taking in account the previous steer to prevent oscillations.

#### `throttle_algorithm` function

It first calculates the yaw rate in `yaw` using the previous yaw rate and current yaw rate to smoothen it and prevent sudden jitters. Then calculates an `adjusted_speed` based on the `yaw` just calculated because the speed should be adjusted based on yaw rate eg in corners where yaw rate would be higher speed should be lowered. It then applies a PID control on `adjusted_speed`. Then it checks the `current_speed` with the `adjusted_speed` and according to the conditions adjusts the `throttle` or applies `brake`

The speed is also changed to 15 m/s

Name:Aroosh Singh
Roll no:25b2163
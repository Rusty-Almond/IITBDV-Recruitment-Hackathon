# SLAM Assignment

## `data_association.py` changes

The Hungarian Algorithm is used from `scipy` library to get the globally optimal assignment to the cones which is better than our greedy technique which may not be the most optimal globally. It then loops through the `rols` and `cols` got from the algorithm and applies a gating to filter out cones that are too far way from classification

### Judging the effects
The code has changes to accumulate the `total_correct` and `total_measurements` (line 220-235 mainly) and it prints percentage of correct after `N_frames`.

Baseline : 95.76% (changes in every iteration)
Hungarian + gating : 96.28% (changes in every iteration)


## `localization.py` changes

Added use of sensor data using `measurements` to get the average cone heading and moving the car to the centre by a small factor of 0.01 to prevent zig zag paths. It also calculates the offset from the center using the y coordinates and tries to go the center using the constant factor of 0.01. This is done because the model currently does not use the sensor data and only keep its position from previous positions which may drift after some time.

### Possible problems

- The constant factor may not be the best
- Using a moving average or low-pass filter of headings and offsets will help to smooth out the path more

## `mapping.py`

### Problems
- The map adds new elements when distance > 2.0 but it can count the same cone twice if the car was at some angle and saw the same cone twice.
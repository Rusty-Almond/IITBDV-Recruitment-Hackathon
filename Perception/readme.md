# Bounding Boxes

Bounding Boxes were made using openCV using the data from the image which was inferenced by the YOLO output. `cv2.rectangle` makes the bounding  box using the X and Y coordinates from the YOLO output and `cv2.putText` is used for annotating over the bounding box in the image.

# Calculating the distances

The distances are calculated inside the `compute_distance` function. It does this using the given formula d=(H*F)/h. The f should be in pixels but since the given f is 1000mm it has been taken as the focal length in pixels as there is no data to find the focal length in pixels since the sensor size is not given.

# Assumptions

- All cones are upright.
- The focal length pf lens is 1000 pixels
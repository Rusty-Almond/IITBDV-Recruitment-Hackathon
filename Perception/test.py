import cv2
from ultralytics import YOLO

# LOAD THE MODEL

model= YOLO("best.pt")

# run model on image image.png
results = model("image.png")

# function to calculate distances
def compute_distance(pixel_height):
    d= 300/(pixel_height)
    return d

i=0
# Processing the results
for result in results :
    img=result.orig_img
    for box in result.boxes:
        x1,y1,x2,y2=map(int,box.xyxy[0])
        heights=box.xywh[:,3].item()
        distance=compute_distance(heights)
        print(f"Cone {i}:{distance:.1f} m")
        i=i+1
        #draw the box
        cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
        label=f"Dist:{distance:.1f}m"
        cv2.putText(img,label,(x1+5,y1-5),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),1)

cv2.imwrite("annotated.jpg",img)
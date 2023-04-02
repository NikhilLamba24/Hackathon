import cv2
import sys


(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

if __name__ == '__main__' :

    # Set up tracker.
    # Instead of CSRT, you can also use

    tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
    tracker_type = tracker_types[7]

    if int(minor_ver) < 3:
        tracker = cv2.Tracker_create(tracker_type)
    else:
        if tracker_type == 'BOOSTING':
            tracker = cv2.legacy.TrackerBoosting_create()
        elif tracker_type == 'MIL':
            tracker = cv2.TrackerMIL_create()
        elif tracker_type == 'KCF':
            tracker = cv2.legacy.TrackerKCF_create()
        elif tracker_type == 'TLD':
            tracker = cv2.legacy.TrackerTLD_create()
        elif tracker_type == 'MEDIANFLOW':
            tracker = cv2.legacy.TrackerMedianFlow_create()
        elif tracker_type == 'GOTURN':
             tracker = cv2.TrackerGOTURN_create()
        elif tracker_type == 'MOSSE':
            tracker = cv2.legacy.TrackerMOSSE_create()
        elif tracker_type == "CSRT":
            tracker = cv2.TrackerCSRT_create()


video = cv2.VideoCapture("yolorigi.avi")
out = cv2.VideoWriter('CSRT.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 25, (352,288))
#video = cv2.VideoCapture(0) # for using CAM

# Exit if video not opened.
if not video.isOpened():
  print("Could not open video")
  sys.exit()

# Read first frame.
ok, frame = video.read()
if not ok:
  print ('Cannot read video file')
  sys.exit()

bbox = (213,121,21,95)

# Uncomment the line below to select a different bounding box
####bbox = cv2.selectROI(frame, False)

# Initialize tracker with first frame and bounding box
ok = tracker.init(frame, bbox)
list1=[]
list2=[]
bbox_0=[]
bbox_1=[]
bbox_2=[]
bbox_3=[]
while True:
     # Read a new frame
     ok, frame = video.read()
     if not ok:
         break

     # Start timer
     timer = cv2.getTickCount()

     # Update tracker
     ok, bbox = tracker.update(frame)

     # Calculate Frames per second (FPS)
     fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);

     # Draw bounding box
     if ok:
         # Tracking success
         p1 = (int(bbox[0]), int(bbox[1]))
         p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
         print(p1,p2)
         list1.append(p1)
         list2.append(p2)
         bbox_0.append(bbox[0])
         bbox_1.append(bbox[1])
         bbox_2.append(bbox[0]+bbox[2])
         bbox_3.append(bbox[1]+bbox[3])
         cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
     else :
         # Tracking failure
         cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

     # # Display tracker type on frame
     # cv2.putText(frame, tracker_type + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);
     #
     # # Display FPS on frame
     # cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);
     # # Display result
     imS = cv2.resize(frame, (352,288))                    # Resize image
     out.write(frame)
     cv2.imshow("Tracking", imS)

     # Exit if ESC pressed
     if cv2.waitKey(1) & 0xFF == ord('q'): # if press SPACE bar
         break

video.release()
out.release()
cv2.destroyAllWindows()
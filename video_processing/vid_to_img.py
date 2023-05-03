import cv2
import os

def vid_to_img(vid_file, vid_folder):
    cap= cv2.VideoCapture(vid_file)
    i=0
    path=vid_folder
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break
        #cv2.imwrite(os.path.join(path , 'waka.jpg'), img)
        cv2.imwrite(os.path.join(path,'Snap'+str(i)+'.jpg'),frame)
        i+=1
    cap.release()
    cv2.destroyAllWindows()
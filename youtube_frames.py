'''
This program is to extract frames of a video from "folder" location.
to frameloc.
'''
def video_to_frames_auto(folder=None):

    import os
    import cv2
    import youtube_dl
    import glob

    file_list = glob.glob(folder + "*.webm")
    print(len(file_list))
    for file in file_list:
        file_loc = file
        frame_loc = folder+(file.strip(folder)).strip(".webm")
        if not os.path.exists(frame_loc):
            os.makedirs(frame_loc)
        cap = cv2.VideoCapture(file_loc)
        print("capture is done")
        video_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
        print("Number of frames: ", video_length)
        count = 0
        x = 0
        print("Converting video..\n")
        cap.set(1,50)
        while cap.isOpened():
            ret, frame = cap.read()
            
            if not ret:
                break
            
            cv2.imwrite(frame_loc + "/%d.jpg" % (x), frame)
            x+=1
            count+=300 #Skip 300 frames i.e. 10 seconds for 30 fps
            cap.set(1,count)
            if cv2.waitKey(30)&0xFF == ord('q') or count > (video_length - 1):
                print("Done extracting frames.\n%d frames extracted" % count)
                cap.release()
                break


    
folder = '/home/raghu/Lectures/Digital Signal Processing/'
video_to_frames_auto(folder)


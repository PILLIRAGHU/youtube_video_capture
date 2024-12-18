import os
import cv2
import youtube_dl
import numpy as np
import re

# To make a directory for saving video automatically considering all the existing foldernames
video_url='https://www.youtube.com/watch?v=HVGW85eGPQQ&list=PLyqSpQzTE6M_h5UgZWpybzBVDGmHGhQQb' #The Youtube URL
folder = "D:/Lectures/RO2_Humble_Tutorial_Kevin"
reg = re.compile(r'^video_')
lst = sorted(os.listdir(folder))
newlist = filter(reg.match, lst)
numbers = [reg.sub('', x).strip() for x in newlist]
results = map(int, numbers)
results = sorted(results)
#newfile = 2
print(results)
# Make a directory for the video
# If no video's exist as of now, create a folder.
if (results == []):
    os.mkdir(folder + "video_1")
    newfile = 1
else:
    newfile = results[-1] + 1
    os.mkdir(folder + "video_" + str(newfile))

# Create a folder according to the files that are already present.

file_loc = folder + "video_" + str(newfile) + "/video_" + str(newfile) + ".mp4"

ydl_opts={"noplaylist": True}
ydl=youtube_dl.YoutubeDL(ydl_opts)
info_dict=ydl.extract_info(video_url, download=False)

formats = info_dict.get('formats',None)
print("Obtaining frames")
for f in formats:
    if f.get('format_note',None) == '480p':
        url = f.get('url',None)
        cap = cv2.VideoCapture(url)
        video_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
        x=0
        count=0
        cap.set(1,50)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imwrite(folder + "video_" + str(newfile) + "/%d.jpg" % (x), frame)
            x+=1
            count+=300 #Skip 300 frames i.e. 10 seconds for 30 fps
            cap.set(1,count)
            if cv2.waitKey(30)&0xFF == ord('q') or count > (video_length - 1):              
                print("Done extracting frames.\n%d frames extracted" % count)
                cap.release()
                break
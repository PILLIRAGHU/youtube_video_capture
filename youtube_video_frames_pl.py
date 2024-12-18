'''
This program is to download frames of a video of a youtube playlist from
'video_url' and store them in 'folder'.
'''

import os
import cv2
import youtube_dl   
import sys

#url of the playlist / video
video_url='https://www.youtube.com/watch?v=0GvTTThmSq8&list=PLyqSpQzTE6M9py2rcGOLss74ZxBUvaC49&index=81' #The Youtube URL
# Location to save the frames
folder = "/home/raghu/Lectures/"


ydl_opts = {'noplaylist': False, # no playlist
        'yesplaylist': True, # get full playlist
        'playliststart': 5,# starting video number/index of playlist, if not mentioned it takes first index
        'playlistend':5  #ending video number/index of playlist, if not mentioned it takes last index
        } # format of the videos to be downloaded

ydl=youtube_dl.YoutubeDL(ydl_opts)
info_dict=ydl.extract_info(video_url, download=False)
pl_title = info_dict.get('title')
folder = folder + pl_title+'/'
print('Location: \n',folder)
if not os.path.exists(folder):
    os.makedirs(folder)
#sys.exit()
# Get titles and webpage-urls of the individual video links of the playlist.
if 'entries' in info_dict:
    video = info_dict['entries']
    for i,item in enumerate(video):
        v_url = info_dict['entries'][i]['webpage_url']
        print("v_url: \n",v_url)
        v_title = info_dict['entries'][i]['title']
        file_loc = folder+ v_title
        print("Lecture Title: \n",v_title)
        ydl_opts_s = {'noplaylist': False,
        'format': 'bestvideo/best',
        'outtmpl': folder+'%(title)s.%(ext)s'}
        print('extension:\n',info_dict['entries'][i]['ext'])
        v_ext = info_dict['entries'][i]['ext']
        frame_loc = file_loc + '.'+v_ext
        print(frame_loc)
        
        try:
            with youtube_dl.YoutubeDL(ydl_opts_s) as ydl_s:
                info_dict_s = ydl_s.extract_info(v_url, download=False)
                ydl_s.prepare_filename(info_dict_s)
                ydl_s.download([v_url])
                print("no exception")                
        except Exception:
            print("Exception",Exception)
            break
        print("Obtaining frames")
        if not os.path.exists(file_loc):
            os.makedirs(file_loc)
        frame_loc = file_loc + '.'+v_ext
        print(frame_loc)
        cap = cv2.VideoCapture(frame_loc)
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
            
            cv2.imwrite(file_loc + "/%d.jpg" % (x), frame)
            x+=1
            count+=300 #Skip 300 frames i.e. 10 seconds for 30 fps
            cap.set(1,count)
            if cv2.waitKey(30)&0xFF == ord('q') or count > (video_length - 1):
                print("Done extracting frames.\n%d frames extracted" % count)
                cap.release()
                os.remove(frame_loc) # Delete the frames extracted video file.
                #if you want to retain the video file just comment the above line.
                break

                

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
        'playliststart': 1 ,# starting video number/index of playlist, if not mentioned it takes first index
        'playlistend':3  #ending video number/index of playlist, if not mentioned it takes last index
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
        frame_loc = folder+ v_title
        print("Lecture Title: \n",v_title)
        if not os.path.exists(frame_loc):
            os.makedirs(frame_loc)
        #os.mkdir(frame_loc)
#sys.exit()
        ydl_opts_s={"noplaylist": True,'format': 'bestvideo[ext=mp4]'}
        ydl_s=youtube_dl.YoutubeDL(ydl_opts_s)
        info_dict_s=ydl_s.extract_info(v_url, download=False)
        formats = info_dict_s.get('formats',None)
        
        for f in formats:            
            #print(f.get('format_note',None),f.get('height',None))
            if not ( f.get('height',None)==None or f.get('height',None) < 480): # format of the video 114p,360p,480p,720p etc
                print("Obtaining frames")
                v_url = f.get('url',None) #
                cap = cv2.VideoCapture(v_url)
                video_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
                x=0
                count=0
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
                break

                

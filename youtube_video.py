'''
This program is to download playlist in "folder" location. With playlist start and
playlist end.
'''
def video_to_frames_url_auto(url=None, folder='/home/raghu/Desktop'):
    import os
    import cv2
    import youtube_dl

    if (url):
        print("Downloading Youtube Video")
        ydl_opts = {'noplaylist': False,
        'yesplaylist': True,
        'playliststart': 1,
        'playlistend': 2,
        'format': 'bestvideo/best',
        'outtmpl': folder+'%(title)s.%(ext)s'}
        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.cache.remove()
                info_dict = ydl.extract_info(url, download=False)
                ydl.prepare_filename(info_dict)
                ydl.download([url])
                print("no exception")
        except Exception:
            print("Exception",Exception)
            return False 
   
    else:
        print("This is where I should raise an error. --EXCEPTION HANDLING--")
    
    print("Download is done !!!")
    
folder = 'D:/Lectures/RO2_Humble_Tutorial_Kevin'
url = "https://www.youtube.com/watch?v=6dFnpz_AEyA&list=PL9567DFCA3A66F299"
video_to_frames_url_auto(url,folder)


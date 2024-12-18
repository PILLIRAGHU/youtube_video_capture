'''

This program is to download video in "fileloc1" with out playlist,
and it extracts frames from 10th frame to last frame with 300 frames
interval(10s) and saved the images in "fileloc".

'''
def video_to_frames_url_auto(url=None, folder='/home/raghu/Lectures/'):
    """Function to extract frames from input video url or file and save them as separate frames
    in an output directory. Output directory will be named starting from video_1. If a new file is downloaded,
    a video_2 folder will be created and so on.
    Dependencies:
        OpenCV
        youtube-dl (sudo pip install --upgrade youtube_dl)

    Args:
        url: Youtube video URL.
        folder: Directory to download and save each frames.

    Returns:
        None

    Work to be done:
    1. Handle exceptions
    """
    import os
    import re
    import cv2
    import time
    import youtube_dl

    # Log start time
    time_start = time.time()

    # To make a directory for saving video automatically considering all the existing foldernames
    reg = re.compile(r'^video_')
    lst = sorted(os.listdir(folder))
    newlist = filter(reg.match, lst)
    numbers = [reg.sub('', x).strip() for x in newlist]
    results = map(int, numbers)
    results = sorted(results)
    #newfile = 2
    print(results)
    newfile = results[-1] + 1
    # Make a directory for the video
    # If no video's exist as of now, create a folder.
    if (results == []):
        os.mkdir(folder + "video_1")
    # Create a folder according to the files that are already present.
    os.mkdir(folder + "video_" + str(newfile))

    file_loc = folder + "video_" + str(newfile) + "/video_" + str(newfile) + ".mp4"
    # Download from local video file
    file_loc1 = "/home/raghu/.cache/youtube-dl" + "/video_" + str(newfile) + ".mp4"
    if (url):
        print("Downloading Youtube Video")
        ydl_opts = {'noplaylist': True,
        'format': 'mp4',
        'outtmpl': file_loc1}
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
    cap = cv2.VideoCapture(file_loc1                )
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
        
        cv2.imwrite(folder + "video_" + str(newfile) + "/%d.jpg" % (x), frame)
        x+=1
        count+=300 #Skip 300 frames i.e. 10 seconds for 30 fps
        cap.set(1,count)
        if cv2.waitKey(30)&0xFF == ord('q') or count > (video_length - 1):
            time_end = time.time()
            print("Done extracting frames.\n%d frames extracted" % count)
            print("It took %d seconds for conversion." % (time_end - time_start))
            cap.release()
            break

video_to_frames_url_auto("url")


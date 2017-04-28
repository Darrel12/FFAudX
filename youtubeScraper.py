from os import remove
import ffmpy
from pytube import YouTube
from pprint import pprint

import savedData as sd


def stuff():
    # not necessary, just for demo purposes.

    yt = YouTube("http://www.youtube.com/watch?v=Ik-RsDGPI5Y")

    # Once set, you can see all the codec and quality options YouTube has made
    # available for the perticular video by printing videos.

    print(yt.get_videos())

    # [<video: mpeg-4="" visual="" (.3gp)="" -="" 144p="">,
    # <video: mpeg-4="" visual="" (.3gp)="" -="" 240p="">,
    # <video: sorenson="" h.263="" (.flv)="" -="" 240p="">,
    # <video: h.264="" (.flv)="" -="" 360p="">,
    # <video: h.264="" (.flv)="" -="" 480p="">,
    # <video: h.264="" (.mp4)="" -="" 360p="">,
    # <video: h.264="" (.mp4)="" -="" 720p="">,
    # <video: vp8="" (.webm)="" -="" 360p="">,
    # <video: vp8="" (.webm)="" -="" 480p="">]

    # The filename is automatically generated based on the video title. You
    # can override this by manually setting the filename.

    # view the auto generated filename:
    print(yt.filename)

    # Pulp Fiction - Dancing Scene [HD]

    # set the filename:
    yt.set_filename('Dancing Scene from Pulp Fiction')

    # You can also filter the criteria by filetype.
    print(yt.filter('flv'))

    # [<video: sorenson="" h.263="" (.flv)="" -="" 240p="">,
    # <video: h.264="" (.flv)="" -="" 360p="">,
    # <video: h.264="" (.flv)="" -="" 480p="">]

    # Notice that the list is ordered by lowest resolution to highest. If you
    # wanted the highest resolution available for a specific file type, you
    # can simply do:
    print(yt.filter('mp4')[-1])
    # <video: h.264="" (.mp4)="" -="" 720p="">

    # You can also get all videos for a given resolution
    print(yt.filter(resolution='480p'))

    # [<video: h.264="" (.flv)="" -="" 480p="">,
    # <video: vp8="" (.webm)="" -="" 480p="">]

    # To select a video by a specific resolution and filetype you can use the get
    # method.

    # video = yt.get('mp4', '720p') #

    # NOTE: get() can only be used if and only if one object matches your criteria.
    # for example:

    print(yt.get_videos())

    # [<video: mpeg-4="" visual="" (.3gp)="" -="" 144p="">,
    # <video: mpeg-4="" visual="" (.3gp)="" -="" 240p="">,
    # <video: sorenson="" h.263="" (.flv)="" -="" 240p="">,
    # <video: h.264="" (.flv)="" -="" 360p="">,
    # <video: h.264="" (.flv)="" -="" 480p="">,
    # <video: h.264="" (.mp4)="" -="" 360p="">,
    # <video: h.264="" (.mp4)="" -="" 720p="">,
    # <video: vp8="" (.webm)="" -="" 360p="">,
    # <video: vp8="" (.webm)="" -="" 480p="">]

    # Since we have two H.264 (.mp4) available to us... now if we try to call get()
    # on mp4...

    video = yt.get('mp4')
    # MultipleObjectsReturned: 2 videos met criteria.

    # In this case, we'll need to specify both the codec (mp4) and resolution
    # (either 360p or 720p).

    # Okay, let's download it! (a destination directory is required)
    video.download('/tmp/')


def scrape(queue_list, item):
    """
    Download the desired video with the chosen extension.
    If the desired extension doesn't exist, download the highest resolution.
    :param queue_list: the list to be modified after scraping
    :param item: queue object
    """
    try:
        yt = item.yt

        # if the user chose an audio format:
        # Get any video resolution and extract
        # the audio and convert to the desired format
        if item.audio:
            yt_path = getHighestResolution(yt, item)
            convertItem(queue_list, queue_list.row(item), delete_after_download=True, youtube_item_path=yt_path)
            return

        # The user didn't choose an audio format:
        # This means they want video, check if the user
        # chose a video format and download it.
        # Otherwise, download the highest resolution available
        if not item.video:
            getHighestResolution(yt, item)
        else:
            filtered = yt.filter(extension=item.video)
            # If the chosen video format doesn't already exist
            # then download the highest resolution and convert it
            if not filtered:
                yt_path = getHighestResolution(yt, item)
                convertItem(queue_list, queue_list.row(item), delete_after_download=True, youtube_item_path=yt_path)
            else:
                filtered = filtered[-1]  # take the last item (highest resolution)
                video = yt.get(filtered.extension, filtered.resolution)
                video.download(item.fDest, force_overwrite=True)
    except Exception as some_exception:
        print("There was an exception when trying to scrape:")
        pprint(some_exception.args)


def getHighestResolution(yt, item):
    resolutions = ["1080p", "720p", "480p", "360p", "240p", "144p"]
    # if the user didn't choose a format, iterate over resolutions
    # from high to low to get the highest quality video
    try:
        for res in resolutions:
            if yt.filter(resolution=res):
                video = yt.filter(resolution=res)[-1]
                video = yt.get(video.extension, video.resolution)
                video.download(item.fDest, force_overwrite=True)
                return item.fDest + "/" + yt.filename + "." + video.extension
    except Exception as some_exception:
        print("There was an exception when trying to download the highest resolution video:")
        pprint(some_exception.args)


def convertItem(queue_list, item_index, delete_after_download=False, youtube_item_path=None):
    """
    Convert the item at the given index to the format
    specified within the item
    :param queue_list: Custom QListWidget object holding customized QListWidgetItems
    :param item_index: index of the item in the queue_list to be converted
    :param delete_after_download: Delete the file being converted after the conversion (youtube scraping)
    :param youtube_item_path: directory where the youtube video will be saved
    """
    queue_item = queue_list.item(item_index)

    # (re)initialize the dictionaries
    in_file_name = {}
    out_file_name = {}

    if youtube_item_path:
        in_file_name[youtube_item_path] = None
    else:
        in_file_name[queue_item.absFilePath] = None
    # video and audio can be converted to video
    # so if the user has the video format set, make a video
    # otherwise make it audio
    if queue_item.video != "":
        out_file_name[sd.initSaveDir + "/" + queue_item.no_extension + "." + queue_item.video] = None
    else:
        out_file_name[sd.initSaveDir + "/" + queue_item.no_extension + "." + queue_item.audio] = None

    try:
        # -y option forces overwrite of pre-existing output files - more at https://ffmpeg.org/ffmpeg.html
        # TODO: make this optional?
        ff = ffmpy.FFmpeg(inputs=in_file_name, outputs=out_file_name, global_options="-y")
        ff.run()
        print("finished item: ", in_file_name)
        if delete_after_download:
            remove(youtube_item_path)  # removes the video from your hard drive after converting to the preferred format
        queue_list.takeItem(item_index)

    except ffmpy.FFExecutableNotFoundError as ffenf:
        print("---The FFmpeg executable was not found---\n", ffenf)

    except ffmpy.FFRuntimeError as ffre:
        print("---Runtime Error---\n",
              "Command:", ffre.cmd,
              "Exit Code:", ffre.exit_code,
              "Standard Out:", ffre.stdout,
              "Standard Error:", ffre.stderr)


def videoName(link):
    print(link)
    print(type(YouTube(link).filename))
    return YouTube(link).filename

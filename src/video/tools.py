import sys
import os
import subprocess
import json
from ffmpeg_streaming import Formats, Bitrate, Representation, Size
from file.tools import get_file_size
from .models import VideoInfo, VideoDetailedInfo

def get_video_json(path):
  information_command = [
    "ffprobe",
    "-v", "quiet",
    "-print_format", "json",
    "-show_format",
    "-show_streams",
    path
  ]

  with subprocess.Popen(information_command, stdout=PIPE) as command:
    return json.loads(command.stdout.read())

def get_video_info(path: str, detailed: bool):
  result = VideoDetailedInfo() if detailed else VideoInfo()
  video_json = get_video_json(path)
  for stream in video_json["streams"]:

    if stream["codec_type"] is "video":
      result.width = int(stream["width"])
      result.height = int(stream["height"])
      result.ratio = stream["display_aspect_ratio"]
      result.video_codec = stream["codec_name"]
      if detailed:
        result.video_bitrate = int(stream["bit_rate"])
        result.fps = int(stream["avg_frame_rate"].split("/")[0]) / int(stream["avg_frame_rate"].split("/")[1])

    elif stream["codec_type"] is "audio":
      result.audio_codec = stream["codec_name"]
      if detailed:
        result.audio_bitrate = int(stream["bit_rate"])
        result.audio_channels = int(stream["channels"])

  return result

# def get_video_bytes(path, segment_size = None):
#   video_stream = open(path, "rb")
#   video_size = get_file_size(path)
#   if segment_size is not None:
#     sent_bytes = 0
#     while sent_bytes < video_size:
#       print(sent_bytes)
#       video_stream.seek(sent_bytes)

#       if sent_bytes + segment_size < video_size:
#         yield video_stream.read(segment_size)
#       else:
#         yield video_stream.read(video_size - sent_bytes - 1)

#       sent_bytes += segment_size    
#   else:
#     return video_stream.read()

def has_error(path):
  command = ["ffmpeg", "-v", "error", "-i", path, "-f null - >error.log 2>&1"]

def encode_file(path):
  return

def encode_dash(path):
  info = get_video_info(path)

  encoding_command = [
    "ffmpeg",
    "-i", path, #input file
    "-re", #real time
    "-progress", url, #progress of the encoding
    "-ac", 2, #audio channels: 1 mono, 2 stereo
    # "-r", 30, #frames
    "-c:v", "libx264", #video codec: 
    "-c:a", "aac" #audio codec:
  ]

  if info.height >= 360:
    encoding_command = encoding_command + ["-vf:0", "scale=-1:360", "-b:a", "", "-b:v", ""]
  if info.height >= 480:
    encoding_command = encoding_command + ["-vf:1", "scale=-1:480"], "-b:a", "", "-b:v", ""
  if info.height >= 720:
    encoding_command = encoding_command + ["-vf:2", "scale=-1:720", "-b:a", "", "-b:v", ""]
  if info.height >= 1080:
    encoding_command = encoding_command + ["-vf:3", "scale=-1:1080", "-b:a", "", "-b:v", ""]
  if info.height >= 2160:
    encoding_command = encoding_command + ["-vf:4", "scale=-1:2160", "-b:a", "", "-b:v", ""]

  encoding_command = encoding_command + [
    "-vf", "scale:-1:"
    "-dash_segment_type", "mp4", #file extension of the outputs
    "-use_template", 1, #allows for the mpd file to have a segment template instead of a list of them
    "-use_timeline", 1,
    "-init_seg_name", "$RepresentationID$_start.$ext$",
    "-media_seg_name", "$RepresentationID$_$Number%05d$.$ext$",
    "-seg_duration", 8,
    "-adaptation_sets", "\"id=0,streams=v id=1,streams=a\"" #mapping of the streams to adaptation sets
    "-f", "dash", path #file format
  ]

  with subprocess.Popen(encoding_command, stdout=PIPE) as proc:
    log.write(proc.stdout.read())

def encode_hls(path):
  encoding_command = [
    "ffmpeg",
    "-i", path, #input file
    "-re", #real time
    "-progress", url, #progress of the encoding
    "-ac", 2, #audio channels: 1 mono, 2 stereo
    # "-r", 30, #frames
    "-c:v", "libx264", #video codec: 
    "-c:a", "aac" #audio codec:
  ]

  with subprocess.Popen(encoding_command, stdout=PIPE) as proc:
    log.write(proc.stdout.read())

# Libreary Version
_144p  = Representation(Size(256, 144), Bitrate(95 * 1024, 64 * 1024))
_240p  = Representation(Size(426, 240), Bitrate(150 * 1024, 94 * 1024))
_360p  = Representation(Size(640, 360), Bitrate(276 * 1024, 128 * 1024))
_480p  = Representation(Size(854, 480), Bitrate(750 * 1024, 192 * 1024))
_720p  = Representation(Size(1280, 720), Bitrate(2048 * 1024, 320 * 1024))
_1080p = Representation(Size(1920, 1080), Bitrate(4096 * 1024, 320 * 1024))
_2k    = Representation(Size(2560, 1440), Bitrate(6144 * 1024, 320 * 1024))
_4k    = Representation(Size(3840, 2160), Bitrate(17408 * 1024, 320 * 1024))

def encode_dash_with_library(path):
  dash = video.dash(Formats.h264())
  dash.representations(_144p, _240p, _360p, _480p, _720p, _1080p, _2k, _4k)
  dash.output('/var/media/dash.mpd')

def encode_hls_with_library(path):
  #A path you want to save a random key to your local machine
  save_to = '/home/public_html/"PATH TO THE KEY DIRECTORY"/key'

  #A URL (or a path) to access the key on your website
  url = 'https://www.aminyazdanpanah.com/?"PATH TO THE KEY DIRECTORY"/key'
  # or url = '/"PATH TO THE KEY DIRECTORY"/key';

  hls = video.hls(Formats.h264())
  hls.representations(_144p, _240p, _360p, _480p, _720p, _1080p, _2k, _4k)
  hls.encryption(save_to, url)
  hls.auto_generate_representations()
  hls.output('/var/media/hls.m3u8')




# # ficheiros
# ffmpeg -i in.video -c:v libvpx-vp9 -keyint_min 150 \
# -g 150 -tile-columns 4 -frame-parallel 1  -f webm -dash 1 \
# -an -vf scale=160:90 -b:v 250k -dash 1 video_160x90_250k.webm \
# -an -vf scale=320:180 -b:v 500k -dash 1 video_320x180_500k.webm \
# -an -vf scale=640:360 -b:v 750k -dash 1 video_640x360_750k.webm \
# -an -vf scale=640:360 -b:v 1000k -dash 1 video_640x360_1000k.webm \
# -an -vf scale=1280:720 -b:v 1500k -dash 1 video_1280x720_1500k.webm

# # manifesto
# ffmpeg \
#   -f webm_dash_manifest -i video_160x90_250k.webm \
#   -f webm_dash_manifest -i video_320x180_500k.webm \
#   -f webm_dash_manifest -i video_640x360_750k.webm \
#   -f webm_dash_manifest -i video_1280x720_1500k.webm \
#   -f webm_dash_manifest -i my_audio.webm \
#   -c copy \
#   -map 0 -map 1 -map 2 -map 3 -map 4 \
#   -f webm_dash_manifest \
#   -adaptation_sets "id=0,streams=0,1,2,3 id=1,streams=4" \
#   my_video_manifest.mpd

# Kush gauge: pixel count x motion factor x 0.07 ÷ 1000 = bit rate in kbps
# (frame width x height = pixel count) and motion factor is 1,2 or 4

# with subprocess.Popen(["ifconfig"], stdout=PIPE) as proc:
#     log.write(proc.stdout.read())

# -progress url

# 3. Stream(DASH or HLS) To File
# video = ffmpeg_streaming.input('https://www.aminyazdanpanah.com/?PATH/TO/MANIFEST.MPD or M3U8')

# stream = video.stream2file(Formats.h264())
# stream.output('/var/media/new-video.mp4')

# https://github.com/aminyazdanpanah/python-ffmpeg-video-streaming/tree/cd214a1dd60338c427d7aa8fea17bc4bb670f7ad

# ffmpeg -i $VIDEO_IN \
#     -preset $PRESET_P -keyint_min $GOP_SIZE -g $GOP_SIZE -sc_threshold 0 \
#     -r $FPS -c:v libx264 -pix_fmt yuv420p -c:a aac -b:a 128k -ac 1 -ar 44100 \
#     -map v:0 -s:0 $V_SIZE_1 -b:v:0 2M -maxrate:0 2.14M -bufsize:0 3.5M \
#     -map v:0 -s:1 $V_SIZE_2 -b:v:1 145k -maxrate:1 155k -bufsize:1 220k \
#     -map v:0 -s:2 $V_SIZE_3 -b:v:2 365k -maxrate:2 390k -bufsize:2 640k \
#     -map v:0 -s:3 $V_SIZE_4 -b:v:3 730k -maxrate:3 781k -bufsize:3 1278k \
#     -map v:0 -s:4 $V_SIZE_4 -b:v:4 1.1M -maxrate:4 1.17M -bufsize:4 2M \
#     -map v:0 -s:5 $V_SIZE_5 -b:v:5 3M -maxrate:5 3.21M -bufsize:5 5.5M \
#     -map v:0 -s:6 $V_SIZE_5 -b:v:6 4.5M -maxrate:6 4.8M -bufsize:6 8M \
#     -map v:0 -s:7 $V_SIZE_6 -b:v:7 6M -maxrate:7 6.42M -bufsize:7 11M \
#     -map v:0 -s:8 $V_SIZE_6 -b:v:8 7.8M -maxrate:8 8.3M -bufsize:8 14M \
#     -map 0:a \
#     -init_seg_name init\$RepresentationID\$.\$ext\$ 
#     -media_seg_name chunk\$RepresentationID\$-\$Number%05d\$.\$ext\$ \
#     -use_template 1 -use_timeline 1  \
#     -seg_duration 4 -adaptation_sets "id=0,streams=v id=1,streams=a" \
#     -f dash Dash/dash.mpd

# ffmpeg -i $inputFile \
#   -map 0:v:0 -map 0:a\?:0 -map 0:v:0 -map 0:a\?:0 -map 0:v:0 -map 0:a\?:0 -map 0:v:0 -map 0:a\?:0 -map 0:v:0 -map 0:a\?:0 -map 0:v:0 -map 0:a\?:0  \
#   -b:v:0 350k  -c:v:0 libx264 -filter:v:0 "scale=320:-1"  \
#   -b:v:1 1000k -c:v:1 libx264 -filter:v:1 "scale=640:-1"  \
#   -b:v:2 3000k -c:v:2 libx264 -filter:v:2 "scale=1280:-1" \
#   -b:v:3 245k  -c:v:3 libvpx-vp9 -filter:v:3 "scale=320:-1"  \
#   -b:v:4 700k  -c:v:4 libvpx-vp9 -filter:v:4 "scale=640:-1"  \
#   -b:v:5 2100k -c:v:5 libvpx-vp9 -filter:v:5 "scale=1280:-1"  \
#   -use_timeline 1 -use_template 1 -window_size 6 -adaptation_sets "id=0,streams=v  id=1,streams=a" \
#   -hls_playlist true -f dash output/output.mpd

#   ffmpeg -i $INPUT.mp4 \
# -map 0:v:0 -map 0:a:0 -map 0:v:0 -map 0:a:0 \
# -b:v:0 250k -filter:v:0 "scale=-2:240" -profile:v:0 baseline \ 
# -b:v:1 750k -filter:v:1 "scale=-2:480" -profile:v:1 main \    
# -use_timeline 1 -use_template 1 -window_size 5 \
# -adaptation_sets "id=0,streams=v id=1,streams=a" -f dash $OUTPUT.mpd

# ffmpeg -i SampleVideo_1280x720_1mb.mp4 -vcodec copy -acodec copy -encryption_scheme cenc-aes-ctr -encryption_key 76a6c65c5ea762046bd749a2e632ccbb -encryption_kid a7e61c373e219033c21091fa607bf3b8 SampleVideo_1280x720_1mb_encrypted.mp4

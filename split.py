import os
import spleeter
import subprocess


def split(path,name):
    command = f"mkdir songs/{name} & ffmpeg -i {path} -codec copy -an songs/{name}/video.mp4"
    subprocess.call(command, shell=True)
    command = f"ffmpeg -i {path} -ab 160k -ac 2 -ar 44100 -vn audio.wav"
    subprocess.call(command, shell=True)
    command = f"spleeter separate -i audio.wav -p spleeter:2stems -o songs/{name}"
    subprocess.call(command,shell=True)
    command = f"rm -f audio.wav {path}"
    subprocess.call(command,shell=True)

def importAll():
    p = os.listdir("./videos")
    for f in p:
        fnew = f.replace(" ","")
        os.rename(f"videos/{f}",f"videos/{fnew}")
        split(f"./videos/{fnew}",fnew.split(".")[0])

import cv2
import ffmpeg,os

def run(parent, files):
    for file in files:
        new_filename = ".".join(file.split(".")[:-1]+[format])
        cmd = "ffmpeg -i %s -c:v mpeg2video -q:v 5 -c:a mp2 -f vob %s"%(file,new_filename)
        os.system(cmd)

if __name__ == '__main__':
    run(["v5.mp4"],"mpg")


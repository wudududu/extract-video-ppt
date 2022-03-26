import math
import cv2
import os
import shutil
import click

from .compare import compareImg
from .images2pdf import images2pdf

DEFAULT_PATH = './.extract-video-ppt-tmp-data'
DEFAULT_PDFNAME = 'output.pdf'
DEFAULT_MAXDEGREE = 0.6
CV_CAP_PROP_FRAME_WIDTH = 1920
CV_CAP_PROP_FRAME_HEIGHT = 1080

URL = ''
OUTPUTPATH = ''
PDFNAME = DEFAULT_PDFNAME
MAXDEGREE = DEFAULT_MAXDEGREE

@click.command()
@click.option('--similarity', default=DEFAULT_MAXDEGREE, help = 'The similarity between this frame and the previous frame is less than this value and this frame will be saveed, default: 0.6')
@click.option('--pdfname', default=DEFAULT_PDFNAME, help = 'the name of output pdf file, default: output.pdf')
@click.argument('outputpath')
@click.argument('url')
def main(similarity, pdfname, outputpath, url):
    global URL
    global OUTPUTPATH
    global MAXDEGREE
    global PDFNAME

    URL = url
    OUTPUTPATH = outputpath
    MAXDEGREE = similarity
    PDFNAME = pdfname

    prepare()
    start()
    exportPdf()
    clearEnv()

    

def start():
    global CV_CAP_PROP_FRAME_WIDTH
    global CV_CAP_PROP_FRAME_HEIGHT

    vcap = cv2.VideoCapture(URL)
    FPS = int(vcap.get(5))
    TOTAL_FRAME= int(vcap.get(7))

    if TOTAL_FRAME == 0:
        print('Please check if the video url is correct')
        clearEnv()
        exit(1)

    CV_CAP_PROP_FRAME_WIDTH = int(vcap.get(cv2.CAP_PROP_FRAME_WIDTH))
    CV_CAP_PROP_FRAME_HEIGHT = int(vcap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    lastDegree = 0
    lastFrame = []
    readedFrame = 0

    while(True):
            click.clear()
            print('process:' + str(math.floor(readedFrame / TOTAL_FRAME * 100)) + '%')
            ret, frame = vcap.read()
            if ret:
                readedFrame += 1
                if readedFrame % FPS != 0:
                    continue

                isWrite = False

                if len(lastFrame):
                    degree = compareImg(frame, lastFrame)
                    if degree < MAXDEGREE:
                        isWrite = True
                        lastDegree = round(degree, 2)
                else:
                    isWrite = True

                if isWrite:
                    name = DEFAULT_PATH + '/frame'+ second2hms(math.ceil(readedFrame / FPS)) + '-' + str(lastDegree) + '.jpg'
                    if not cv2.imwrite(name, frame):
                        print('write file failed !')
                        exit(1)
                    lastFrame = frame
                    
            else:
                break

    vcap.release()
    cv2.destroyAllWindows()

def prepare():
    global OUTPUTPATH

    try:

        if not os.path.exists(OUTPUTPATH):
            os.makedirs(OUTPUTPATH)

    except OSError as error:
        print (error)
        exit(1)

    try:
        
        if os.path.exists(DEFAULT_PATH):
            shutil.rmtree(DEFAULT_PATH)

        if not os.path.exists(DEFAULT_PATH):
            os.makedirs(DEFAULT_PATH)

    except OSError as error:
        print (error)
        exit(1)

def exportPdf():
    images = os.listdir(DEFAULT_PATH)
    images.sort()
    imagePaths = []

    for image in images:
        basepath = DEFAULT_PATH + '/' + image
        (fileName, mimeType) = os.path.splitext(basepath)
        
        if mimeType != '.jpg':
            continue

        imagePaths.append(basepath)

    pdfPath = DEFAULT_PATH + '/' + PDFNAME
    images2pdf(pdfPath, imagePaths, CV_CAP_PROP_FRAME_WIDTH, CV_CAP_PROP_FRAME_HEIGHT)

    shutil.copy(pdfPath, OUTPUTPATH)

def clearEnv():
    shutil.rmtree(DEFAULT_PATH)

def second2hms(second):
    m, s = divmod(second, 60)
    h, m = divmod(m, 60)
    return ("%02d.%02d.%02d" % (h, m, s))

if __name__ == '__main__':
    main()
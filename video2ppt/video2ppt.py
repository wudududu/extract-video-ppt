from json.encoder import INFINITY
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
INFINITY_SIGN = 'INFINITY'
ZERO_SISG = '00:00:00'

URL = ''
OUTPUTPATH = ''
PDFNAME = DEFAULT_PDFNAME
MAXDEGREE = DEFAULT_MAXDEGREE
START_FRAME = 0
END_FRAME = INFINITY

@click.command()
@click.option('--similarity', default = DEFAULT_MAXDEGREE, help = 'The similarity between this frame and the previous frame is less than this value and this frame will be saveed, default: %02g' % (DEFAULT_MAXDEGREE))
@click.option('--pdfname', default = DEFAULT_PDFNAME, help = 'the name of output pdf file, default: %02s' % (DEFAULT_PDFNAME))
@click.option('--start_frame', default = ZERO_SISG, help = 'start frame time point, default = %02s' % (ZERO_SISG))
@click.option('--end_frame', default = INFINITY_SIGN, help = 'end frame time point, default = %02s' % (INFINITY_SIGN))
@click.argument('outputpath')
@click.argument('url')
def main(
    similarity, pdfname, start_frame, end_frame, 
    outputpath, url):
    global URL
    global OUTPUTPATH
    global MAXDEGREE
    global PDFNAME
    global START_FRAME
    global END_FRAME

    URL = url
    OUTPUTPATH = outputpath
    MAXDEGREE = similarity
    PDFNAME = pdfname
    START_FRAME = hms2second(start_frame)
    END_FRAME = hms2second(end_frame)

    if START_FRAME >= END_FRAME:
        exitByPrint('start >= end can not work')

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
        exitByPrint('Please check if the video url is correct')

    CV_CAP_PROP_FRAME_WIDTH = int(vcap.get(cv2.CAP_PROP_FRAME_WIDTH))
    CV_CAP_PROP_FRAME_HEIGHT = int(vcap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    if START_FRAME > TOTAL_FRAME / FPS:
        exitByPrint('video duration is not support')
    
    # set start frame
    vcap.set(cv2.CAP_PROP_POS_FRAMES, START_FRAME * FPS)
    frameCount = ((int(TOTAL_FRAME / FPS) if END_FRAME == INFINITY else END_FRAME) - START_FRAME) * FPS

    lastDegree = 0
    lastFrame = []
    readedFrame = 0

    while(True):
            click.clear()
            print('process:' + str(math.floor(readedFrame / frameCount * 100)) + '%')
            ret, frame = vcap.read()
            if ret:
                if readedFrame >= frameCount:
                    break

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
                    name = DEFAULT_PATH + '/frame'+ second2hms(math.ceil((readedFrame + START_FRAME * FPS) / FPS)) + '-' + str(lastDegree) + '.jpg'
                    if not cv2.imwrite(name, frame):
                        exitByPrint('write file failed !')

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
        exitByPrint(error)

    try:
        
        clearEnv()
        os.makedirs(DEFAULT_PATH)

    except OSError as error:
        exitByPrint(error)

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

def exitByPrint(str):
    print(str)
    clearEnv()
    exit(1)

def clearEnv():
    if os.path.exists(DEFAULT_PATH):
        shutil.rmtree(DEFAULT_PATH)

def second2hms(second):
    m, s = divmod(second, 60)
    h, m = divmod(m, 60)
    return ("%02d.%02d.%02d" % (h, m, s))

def hms2second(hms):
    if hms == INFINITY_SIGN:
        return INFINITY

    h, m, s = hms.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)

if __name__ == '__main__':
    main()
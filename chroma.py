import cv2
import numpy as np

channels = 0
background = []
foreground = []
result = 0
threshold = 0
channel = 0

def set_thres(thres):
    global threshold
    threshold = thres

def set_channel(ch):
    global channel
    channel = ch

def import_foreground(img):
    global foreground
    global channels
    try:
        foreground = cv2.imread(img)
    except:
        return
    b, g, r = cv2.split(foreground)
    blueness = b.astype(np.float64) - np.maximum(r.astype(np.float64), g.astype(np.float64))
    redness = r.astype(np.float64) - np.maximum(b.astype(np.float64), g.astype(np.float64))
    greenness = g.astype(np.float64) - np.maximum(r.astype(np.float64), b.astype(np.float64))
    channels = [redness, greenness, blueness]

    #cv2.imshow("test", foreground)
    
def import_background(img):
    global background
    global foreground
    try:
        background = cv2.imread(img)
    except:
        return
    #background = cv2.resize(background, (foreground.shape[1], foreground.shape[0]))
    
def cutout_show():
    global result
    global background
    global foreground
    global channel
    global channels
    if len(background) == 0 or len(foreground) == 0:
        return
    result = cv2.resize(background, (foreground.shape[1], foreground.shape[0]))
    
    for x, line in enumerate(foreground):
        for y, pixel in enumerate(line):
            if channels[channel][x][y] < threshold:
                result[x][y] = pixel
                
    #return cv2.imencode('.png', cv2.resize(result,(450,250)))[1].tobytes()
    return cv2.imencode('.png', result)[1].tobytes()
    #cv2.imshow("Base", foreground)
    #cv2.imshow("Back", background)
    
def export(path):
    cv2.imwrite(path, result)
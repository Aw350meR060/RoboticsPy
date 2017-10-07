import math
from PIL import Image, ImageDraw
import numpy as np


def distance(ax, ay, bx, by):
    return math.sqrt((by - ay)**2 + (bx - ax)**2)

def rotation(ax, ay, bx, by, angle):
    radius = distance(ax, ay, bx, by)
    angle += math.atan2(ay-by,ax - bx)
    return(
        round(bx + radius * math.cos(angle)),
        round(by + radius * math.sin(angle)),
    )

image = Image.new('RGB',(400, 400), "white")
draw = ImageDraw.Draw(image)
image.save("output4.png")


img = Image.open("output4.png")
width, height = img.size
white = (255, 255, 255)
lightblue = (128, 194, 255)
pixel = img.load()

delta = 30
whites = []

for x1 in range (2, width - 2):
    for y1 in range (2, height - 2):
        if pixel[x1, y1] == white:
            whites.append([x1, y1])

x = np.asscalar(np.random.randint(0,width,1))
y = np.asscalar(np.random.randint(0,height,1))
dps = []
if [x, y] in whites:
    dps.append([x, y])

i = 0

while i <= 100:
    x1 = np.asscalar(np.random.randint(0,width,1))
    y1 = np.asscalar(np.random.randint(0,height,1))
    t = True
    for j in dps:
        if distance(j[0], j[1], x1, y1) < delta:
            t = False
    if t:
        if [x1, y1] in whites:
            dps.append([x1, y1])
            i += 1

for i in dps:
    for j in range(i[0] - 2, i[0] + 2):
        for k in range(i[1] - 2, i[1] + 2):
            pixel[j, k] = (0, 0, 0)


img.save("output4.png")